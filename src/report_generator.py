"""
report_generator.py - Report Generation Module

This module generates test reports in multiple formats (console, CSV, JSON).
"""

import csv
import json
import os
from typing import Dict, List
from datetime import datetime


class ReportGenerator:
    """Generates test reports in various formats."""
    
    def __init__(self, output_dir: str = 'reports'):
        """
        Initialize report generator.
        
        Args:
            output_dir: Directory to save reports
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def generate_console_report(self, test_results: Dict) -> None:
        """
        Generate formatted console report.
        
        Args:
            test_results: Dictionary containing all test analysis results
        """
        print("\n" + "=" * 100)
        print(" " * 35 + "TEST EXECUTION REPORT")
        print("=" * 100)
        print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 100)
        
        # Test Results Table
        print("\nTEST RESULTS:")
        print("-" * 100)
        header = f"{'Test ID':<12} {'Status':<12} {'Expected':<12} {'Actual':<12} {'Warnings':<10} {'Errors':<10} {'Severity':<12}"
        print(header)
        print("-" * 100)
        
        for test_id in sorted(test_results.keys()):
            result = test_results[test_id]
            
            status = result['validation_status']
            expected = result['validation_details'].get('expected', 'N/A')
            actual = result['validation_details'].get('actual', 'N/A')
            warn_count = result['log_summary'].get('warn_count', 0)
            error_count = result['log_summary'].get('error_count', 0)
            severity = result['anomaly_severity']
            
            # Format expected and actual
            if isinstance(expected, (int, float)):
                expected_str = f"{expected:.2f}" if isinstance(expected, float) else str(expected)
            else:
                expected_str = str(expected)
            
            if isinstance(actual, (int, float)):
                actual_str = f"{actual:.2f}" if isinstance(actual, float) else str(actual)
            else:
                actual_str = str(actual)
            
            row = f"{test_id:<12} {status:<12} {expected_str:<12} {actual_str:<12} {warn_count:<10} {error_count:<10} {severity:<12}"
            print(row)
        
        print("-" * 100)
        
        # Summary Statistics
        print("\nSUMMARY STATISTICS:")
        print("-" * 100)
        stats = self._calculate_statistics(test_results)
        
        print(f"Total Tests:        {stats['total']}")
        print(f"Passed:             {stats['passed']} ({stats['pass_rate']:.1f}%)")
        print(f"Failed:             {stats['failed']}")
        print(f"Borderline:         {stats['borderline']}")
        print(f"Missing:            {stats['missing']}")
        print(f"\nTotal Warnings:     {stats['total_warnings']}")
        print(f"Total Errors:       {stats['total_errors']}")
        print(f"\nOverall Health:     {stats['overall_health']}")
        
        # Anomalies
        print("\nANOMALIES DETECTED:")
        print("-" * 100)
        
        anomaly_found = False
        for test_id in sorted(test_results.keys()):
            result = test_results[test_id]
            if result['anomalies']:
                anomaly_found = True
                print(f"\n{test_id} [{result['anomaly_severity']}]:")
                for anomaly in result['anomalies']:
                    print(f"  • {anomaly}")
        
        if not anomaly_found:
            print("No anomalies detected.")
        
        print("\n" + "=" * 100)
    
    def generate_csv_report(self, test_results: Dict, filename: str = 'test_summary.csv') -> str:
        """
        Generate CSV report.
        
        Args:
            test_results: Dictionary containing all test analysis results
            filename: Output filename
            
        Returns:
            Path to generated CSV file
        """
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', newline='') as csvfile:
            fieldnames = [
                'Test ID', 'Status', 'Expected', 'Actual', 'Tolerance', 'Deviation',
                'Warnings', 'Errors', 'Severity', 'Anomalies', 'Description'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            
            for test_id in sorted(test_results.keys()):
                result = test_results[test_id]
                
                row = {
                    'Test ID': test_id,
                    'Status': result['validation_status'],
                    'Expected': result['validation_details'].get('expected', 'N/A'),
                    'Actual': result['validation_details'].get('actual', 'N/A'),
                    'Tolerance': result['validation_details'].get('tolerance', 'N/A'),
                    'Deviation': result['validation_details'].get('deviation', 'N/A'),
                    'Warnings': result['log_summary'].get('warn_count', 0),
                    'Errors': result['log_summary'].get('error_count', 0),
                    'Severity': result['anomaly_severity'],
                    'Anomalies': len(result['anomalies']),
                    'Description': result['validation_details'].get('description', 'N/A')
                }
                
                writer.writerow(row)
        
        return filepath
    
    def generate_json_report(self, test_results: Dict, filename: str = 'test_summary.json') -> str:
        """
        Generate JSON report.
        
        Args:
            test_results: Dictionary containing all test analysis results
            filename: Output filename
            
        Returns:
            Path to generated JSON file
        """
        filepath = os.path.join(self.output_dir, filename)
        
        # Add statistics to the report
        report_data = {
            'generated_at': datetime.now().isoformat(),
            'statistics': self._calculate_statistics(test_results),
            'test_results': test_results
        }
        
        with open(filepath, 'w') as jsonfile:
            json.dump(report_data, jsonfile, indent=2)
        
        return filepath
    
    def _calculate_statistics(self, test_results: Dict) -> Dict:
        """Calculate summary statistics from test results."""
        total = len(test_results)
        passed = sum(1 for r in test_results.values() if r['validation_status'] == 'PASS')
        failed = sum(1 for r in test_results.values() if r['validation_status'] == 'FAIL')
        borderline = sum(1 for r in test_results.values() if r['validation_status'] == 'BORDERLINE')
        missing = sum(1 for r in test_results.values() if r['validation_status'] == 'MISSING')
        
        total_warnings = sum(r['log_summary'].get('warn_count', 0) for r in test_results.values())
        total_errors = sum(r['log_summary'].get('error_count', 0) for r in test_results.values())
        
        severities = [r['anomaly_severity'] for r in test_results.values()]
        
        # Calculate overall health
        critical_count = severities.count('CRITICAL')
        high_count = severities.count('HIGH')
        medium_count = severities.count('MEDIUM')
        
        if critical_count > 0:
            overall_health = 'CRITICAL'
        elif high_count > 0:
            overall_health = 'POOR'
        elif medium_count > 1:
            overall_health = 'FAIR'
        elif medium_count == 1:
            overall_health = 'GOOD'
        else:
            overall_health = 'EXCELLENT'
        
        return {
            'total': total,
            'passed': passed,
            'failed': failed,
            'borderline': borderline,
            'missing': missing,
            'pass_rate': (passed / total * 100) if total > 0 else 0,
            'total_warnings': total_warnings,
            'total_errors': total_errors,
            'overall_health': overall_health
        }


if __name__ == '__main__':
    # Standalone test
    sample_results = {
        'TC_001': {
            'validation_status': 'PASS',
            'validation_details': {'expected': 75, 'actual': 77, 'tolerance': 2, 'deviation': 2, 'description': 'Test 1'},
            'log_summary': {'warn_count': 0, 'error_count': 0},
            'anomaly_severity': 'NONE',
            'anomalies': []
        },
        'TC_002': {
            'validation_status': 'FAIL',
            'validation_details': {'expected': 100, 'actual': 120, 'tolerance': 5, 'deviation': 20, 'description': 'Test 2'},
            'log_summary': {'warn_count': 1, 'error_count': 1},
            'anomaly_severity': 'CRITICAL',
            'anomalies': ['Output outside tolerance', 'ERROR logs detected']
        }
    }
    
    generator = ReportGenerator()
    generator.generate_console_report(sample_results)
