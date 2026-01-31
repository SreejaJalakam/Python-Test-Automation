"""
main.py - Main Orchestrator

This is the main entry point for the Python Test Automation & Log Analyzer.
It orchestrates the entire workflow: validation, log parsing, anomaly detection, and reporting.
"""

import os
import sys
from validator import OutputValidator
from log_parser import LogParser
from anomaly_checker import AnomalyChecker
from report_generator import ReportGenerator


def main():
    """Main execution function."""
    
    print("\n" + "=" * 100)
    print(" " * 30 + "Python Test Automation & Log Analyzer")
    print("=" * 100)
    print("Initializing test analysis...")
    
    # Get base directory (parent of src)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Define file paths
    expected_file = os.path.join(base_dir, 'data', 'expected_results.json')
    actual_file = os.path.join(base_dir, 'data', 'actual_results.json')
    log_file = os.path.join(base_dir, 'data', 'sample_logs.txt')
    reports_dir = os.path.join(base_dir, 'reports')
    
    # Verify files exist
    for filepath in [expected_file, actual_file, log_file]:
        if not os.path.exists(filepath):
            print(f"Error: Required file not found - {filepath}")
            sys.exit(1)
    
    print(f"✓ Data files located")
    
    # Step 1: Initialize components
    print("\n[1/5] Initializing components...")
    validator = OutputValidator(expected_file, actual_file)
    log_parser = LogParser(log_file)
    anomaly_checker = AnomalyChecker()
    report_generator = ReportGenerator(reports_dir)
    print("✓ Components initialized")
    
    # Step 2: Validate outputs
    print("\n[2/5] Validating test outputs...")
    validation_results = validator.validate_all_tests()
    print(f"✓ Validated {len(validation_results)} test cases")
    
    # Step 3: Parse logs
    print("\n[3/5] Parsing execution logs...")
    log_summaries = log_parser.get_all_test_summaries()
    print(f"✓ Parsed logs for {len(log_summaries)} test cases")
    
    # Step 4: Check for anomalies
    print("\n[4/5] Analyzing anomalies...")
    test_results = {}
    
    for test_id in validation_results.keys():
        validation_status, validation_details = validation_results[test_id]
        log_summary = log_parser.get_test_log_summary(test_id)
        test_completed = log_parser.check_test_completion(test_id)
        
        # Analyze for anomalies
        severity, anomalies = anomaly_checker.analyze_test(
            test_id,
            validation_status,
            validation_details,
            log_summary,
            test_completed
        )
        
        # Store complete results
        test_results[test_id] = {
            'validation_status': validation_status,
            'validation_details': validation_details,
            'log_summary': log_summary,
            'test_completed': test_completed,
            'anomaly_severity': severity,
            'anomalies': anomalies
        }
    
    print(f"✓ Anomaly analysis completed")
    
    # Step 5: Generate reports
    print("\n[5/5] Generating reports...")
    
    # Console report
    report_generator.generate_console_report(test_results)
    
    # CSV report
    csv_path = report_generator.generate_csv_report(test_results)
    print(f"\n✓ CSV report saved: {csv_path}")
    
    # JSON report
    json_path = report_generator.generate_json_report(test_results)
    print(f"✓ JSON report saved: {json_path}")
    
    print("\n" + "=" * 100)
    print("Analysis complete! Check the reports directory for detailed output.")
    print("=" * 100 + "\n")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExecution interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nError during execution: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
