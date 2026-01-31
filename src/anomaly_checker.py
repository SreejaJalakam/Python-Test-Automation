"""
anomaly_checker.py - Anomaly Detection Module

This module implements rules to detect anomalies in test results and logs.
"""

from typing import Dict, List, Tuple


class AnomalyChecker:
    """Detects anomalies in test validation results and logs."""
    
    # Thresholds for anomaly detection
    WARN_THRESHOLD = 2  # Flag if warnings >= this value
    
    def __init__(self):
        """Initialize anomaly checker."""
        self.anomalies = []
    
    def check_validation_anomaly(self, test_id: str, status: str, details: Dict) -> List[str]:
        """
        Check for anomalies in validation results.
        
        Args:
            test_id: Test case identifier
            status: Validation status (PASS, FAIL, BORDERLINE, MISSING)
            details: Validation details
            
        Returns:
            List of anomaly descriptions
        """
        anomalies = []
        
        if status == 'FAIL':
            if 'deviation' in details:
                anomalies.append(
                    f"Output outside tolerance: deviation={details['deviation']:.2f}, "
                    f"tolerance={details['tolerance']}"
                )
            else:
                anomalies.append("Test failed validation")
        
        elif status == 'BORDERLINE':
            anomalies.append(
                f"Borderline result: deviation={details['deviation']:.2f} "
                f"exceeds tolerance={details['tolerance']} but within 150%"
            )
        
        elif status == 'MISSING':
            anomalies.append(f"Missing data: {details.get('error', 'Unknown error')}")
        
        return anomalies
    
    def check_log_anomaly(self, test_id: str, log_summary: Dict) -> List[str]:
        """
        Check for anomalies in log data.
        
        Args:
            test_id: Test case identifier
            log_summary: Log summary from LogParser
            
        Returns:
            List of anomaly descriptions
        """
        anomalies = []
        
        if not log_summary['found']:
            anomalies.append("No log entries found for this test")
            return anomalies
        
        # Check for errors
        if log_summary['error_count'] > 0:
            anomalies.append(
                f"ERROR logs detected: {log_summary['error_count']} error(s)"
            )
            if log_summary['errors']:
                # Include first error message
                anomalies.append(f"  └─ {log_summary['errors'][0]}")
        
        # Check for excessive warnings
        if log_summary['warn_count'] >= self.WARN_THRESHOLD:
            anomalies.append(
                f"Excessive warnings: {log_summary['warn_count']} warning(s) "
                f"(threshold: {self.WARN_THRESHOLD})"
            )
        
        return anomalies
    
    def check_test_completion(self, test_id: str, completed: bool) -> List[str]:
        """
        Check if test completion was logged.
        
        Args:
            test_id: Test case identifier
            completed: Whether test completion was found in logs
            
        Returns:
            List of anomaly descriptions
        """
        anomalies = []
        
        if not completed:
            anomalies.append("Missing test completion log")
        
        return anomalies
    
    def analyze_test(
        self,
        test_id: str,
        validation_status: str,
        validation_details: Dict,
        log_summary: Dict,
        test_completed: bool
    ) -> Tuple[str, List[str]]:
        """
        Perform comprehensive anomaly analysis for a test.
        
        Args:
            test_id: Test case identifier
            validation_status: Validation status
            validation_details: Validation details
            log_summary: Log summary
            test_completed: Whether test completion was logged
            
        Returns:
            Tuple of (severity, anomaly_list)
            severity: 'CRITICAL', 'HIGH', 'MEDIUM', 'LOW', or 'NONE'
        """
        all_anomalies = []
        
        # Check validation anomalies
        val_anomalies = self.check_validation_anomaly(test_id, validation_status, validation_details)
        all_anomalies.extend(val_anomalies)
        
        # Check log anomalies
        log_anomalies = self.check_log_anomaly(test_id, log_summary)
        all_anomalies.extend(log_anomalies)
        
        # Check completion
        completion_anomalies = self.check_test_completion(test_id, test_completed)
        all_anomalies.extend(completion_anomalies)
        
        # Determine severity
        severity = self._calculate_severity(
            validation_status,
            log_summary,
            test_completed,
            len(all_anomalies)
        )
        
        return severity, all_anomalies
    
    def _calculate_severity(
        self,
        validation_status: str,
        log_summary: Dict,
        test_completed: bool,
        anomaly_count: int
    ) -> str:
        """
        Calculate anomaly severity based on multiple factors.
        
        Returns:
            Severity level: 'CRITICAL', 'HIGH', 'MEDIUM', 'LOW', or 'NONE'
        """
        if anomaly_count == 0:
            return 'NONE'
        
        # Critical: Failed validation + errors in logs
        if validation_status == 'FAIL' and log_summary.get('error_count', 0) > 0:
            return 'CRITICAL'
        
        # High: Failed validation or errors in logs
        if validation_status == 'FAIL' or log_summary.get('error_count', 0) > 0:
            return 'HIGH'
        
        # Medium: Borderline or missing completion
        if validation_status == 'BORDERLINE' or not test_completed:
            return 'MEDIUM'
        
        # Low: Only warnings or minor issues
        return 'LOW'
    
    def get_overall_health(self, all_severities: List[str]) -> str:
        """
        Calculate overall test suite health.
        
        Args:
            all_severities: List of severity levels from all tests
            
        Returns:
            Overall health: 'CRITICAL', 'POOR', 'FAIR', 'GOOD', or 'EXCELLENT'
        """
        if not all_severities:
            return 'UNKNOWN'
        
        critical_count = all_severities.count('CRITICAL')
        high_count = all_severities.count('HIGH')
        medium_count = all_severities.count('MEDIUM')
        
        if critical_count > 0:
            return 'CRITICAL'
        elif high_count > 0:
            return 'POOR'
        elif medium_count > 1:
            return 'FAIR'
        elif medium_count == 1:
            return 'GOOD'
        else:
            return 'EXCELLENT'


if __name__ == '__main__':
    # Standalone test
    checker = AnomalyChecker()
    
    # Test case 1: Failed validation with errors
    test_id = "TC_001"
    status = "FAIL"
    details = {'deviation': 10.5, 'tolerance': 2.0}
    log_summary = {'found': True, 'error_count': 1, 'warn_count': 0, 
                   'errors': ['Calibration error'], 'warnings': []}
    completed = True
    
    severity, anomalies = checker.analyze_test(test_id, status, details, log_summary, completed)
    
    print(f"Test: {test_id}")
    print(f"Severity: {severity}")
    print("Anomalies:")
    for anomaly in anomalies:
        print(f"  - {anomaly}")
