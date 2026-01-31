"""
validator.py - Output Validation Module

This module compares expected vs actual test outputs with tolerance checks.
Returns validation status: PASS, FAIL, or BORDERLINE.
"""

import json
from typing import Dict, List, Tuple


class OutputValidator:
    """Validates test outputs against expected baselines with tolerance."""
    
    def __init__(self, expected_file: str, actual_file: str):
        """
        Initialize validator with expected and actual result files.
        
        Args:
            expected_file: Path to JSON file with expected results
            actual_file: Path to JSON file with actual results
        """
        self.expected_data = self._load_json(expected_file)
        self.actual_data = self._load_json(actual_file)
        self.expected_dict = {item['test_id']: item for item in self.expected_data}
        self.actual_dict = {item['test_id']: item for item in self.actual_data}
    
    def _load_json(self, filepath: str) -> List[Dict]:
        """Load JSON data from file."""
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: File not found - {filepath}")
            return []
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in file - {filepath}")
            return []
    
    def validate_single_test(self, test_id: str) -> Tuple[str, Dict]:
        """
        Validate a single test case.
        
        Args:
            test_id: Test case identifier
            
        Returns:
            Tuple of (status, details_dict)
            status: 'PASS', 'FAIL', 'BORDERLINE', or 'MISSING'
        """
        if test_id not in self.expected_dict:
            return 'MISSING', {'error': 'Expected data not found'}
        
        if test_id not in self.actual_dict:
            return 'MISSING', {'error': 'Actual data not found'}
        
        expected = self.expected_dict[test_id]
        actual = self.actual_dict[test_id]
        
        expected_output = expected['expected_output']
        actual_output = actual['actual_output']
        tolerance = expected['tolerance']
        
        # Calculate deviation
        deviation = abs(actual_output - expected_output)
        
        # Determine status
        if deviation <= tolerance:
            status = 'PASS'
        elif deviation <= tolerance * 1.5:
            # Borderline: within 150% of tolerance
            status = 'BORDERLINE'
        else:
            status = 'FAIL'
        
        details = {
            'expected': expected_output,
            'actual': actual_output,
            'tolerance': tolerance,
            'deviation': deviation,
            'description': expected.get('description', 'N/A'),
            'timestamp': actual.get('timestamp', 'N/A')
        }
        
        return status, details
    
    def validate_all_tests(self) -> Dict[str, Tuple[str, Dict]]:
        """
        Validate all test cases.
        
        Returns:
            Dictionary mapping test_id to (status, details) tuples
        """
        results = {}
        
        # Get all unique test IDs from both expected and actual
        all_test_ids = set(self.expected_dict.keys()) | set(self.actual_dict.keys())
        
        for test_id in sorted(all_test_ids):
            status, details = self.validate_single_test(test_id)
            results[test_id] = (status, details)
        
        return results
    
    def get_summary_stats(self, results: Dict[str, Tuple[str, Dict]]) -> Dict:
        """
        Calculate summary statistics from validation results.
        
        Args:
            results: Dictionary of validation results
            
        Returns:
            Dictionary with summary statistics
        """
        total = len(results)
        passed = sum(1 for status, _ in results.values() if status == 'PASS')
        failed = sum(1 for status, _ in results.values() if status == 'FAIL')
        borderline = sum(1 for status, _ in results.values() if status == 'BORDERLINE')
        missing = sum(1 for status, _ in results.values() if status == 'MISSING')
        
        return {
            'total': total,
            'passed': passed,
            'failed': failed,
            'borderline': borderline,
            'missing': missing,
            'pass_rate': (passed / total * 100) if total > 0 else 0
        }


if __name__ == '__main__':
    # Standalone test
    import os
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    expected_file = os.path.join(base_dir, 'data', 'expected_results.json')
    actual_file = os.path.join(base_dir, 'data', 'actual_results.json')
    
    validator = OutputValidator(expected_file, actual_file)
    results = validator.validate_all_tests()
    
    print("Validation Results:")
    print("-" * 80)
    for test_id, (status, details) in results.items():
        print(f"{test_id}: {status}")
        if 'error' not in details:
            print(f"  Expected: {details['expected']}, Actual: {details['actual']}, "
                  f"Deviation: {details['deviation']:.2f}")
    
    stats = validator.get_summary_stats(results)
    print("\nSummary:")
    print(f"Total: {stats['total']}, Passed: {stats['passed']}, "
          f"Failed: {stats['failed']}, Borderline: {stats['borderline']}")
