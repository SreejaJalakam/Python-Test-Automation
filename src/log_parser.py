"""
log_parser.py - Log Analysis Module

This module parses execution logs to extract test information, warnings, and errors.
"""

import re
from typing import Dict, List, Tuple
from collections import defaultdict


class LogParser:
    """Parses test execution logs to extract relevant information."""
    
    # Regex pattern to match log lines
    # Format: [timestamp] [LEVEL] message
    LOG_PATTERN = re.compile(
        r'\[(?P<timestamp>[^\]]+)\]\s+\[(?P<level>INFO|DEBUG|WARN|ERROR)\]\s+(?P<message>.*)'
    )
    
    # Pattern to extract test ID from messages
    TEST_ID_PATTERN = re.compile(r'Test\s+(TC_\d+)')
    
    def __init__(self, log_file: str):
        """
        Initialize log parser with log file.
        
        Args:
            log_file: Path to log file
        """
        self.log_file = log_file
        self.log_entries = []
        self.test_logs = defaultdict(list)
        self._parse_logs()
    
    def _parse_logs(self):
        """Parse the log file and extract structured data."""
        try:
            with open(self.log_file, 'r') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if not line:
                        continue
                    
                    match = self.LOG_PATTERN.match(line)
                    if match:
                        entry = {
                            'line_num': line_num,
                            'timestamp': match.group('timestamp'),
                            'level': match.group('level'),
                            'message': match.group('message')
                        }
                        
                        # Extract test ID if present
                        test_id_match = self.TEST_ID_PATTERN.search(entry['message'])
                        if test_id_match:
                            entry['test_id'] = test_id_match.group(1)
                            self.test_logs[entry['test_id']].append(entry)
                        
                        self.log_entries.append(entry)
        except FileNotFoundError:
            print(f"Error: Log file not found - {self.log_file}")
    
    def get_log_counts_by_level(self) -> Dict[str, int]:
        """
        Count log entries by level.
        
        Returns:
            Dictionary mapping log level to count
        """
        counts = defaultdict(int)
        for entry in self.log_entries:
            counts[entry['level']] += 1
        return dict(counts)
    
    def get_test_log_summary(self, test_id: str) -> Dict:
        """
        Get log summary for a specific test.
        
        Args:
            test_id: Test case identifier
            
        Returns:
            Dictionary with log counts and messages
        """
        if test_id not in self.test_logs:
            return {
                'found': False,
                'info_count': 0,
                'debug_count': 0,
                'warn_count': 0,
                'error_count': 0,
                'warnings': [],
                'errors': []
            }
        
        test_entries = self.test_logs[test_id]
        
        info_count = sum(1 for e in test_entries if e['level'] == 'INFO')
        debug_count = sum(1 for e in test_entries if e['level'] == 'DEBUG')
        warn_count = sum(1 for e in test_entries if e['level'] == 'WARN')
        error_count = sum(1 for e in test_entries if e['level'] == 'ERROR')
        
        warnings = [e['message'] for e in test_entries if e['level'] == 'WARN']
        errors = [e['message'] for e in test_entries if e['level'] == 'ERROR']
        
        return {
            'found': True,
            'info_count': info_count,
            'debug_count': debug_count,
            'warn_count': warn_count,
            'error_count': error_count,
            'warnings': warnings,
            'errors': errors
        }
    
    def get_all_test_summaries(self) -> Dict[str, Dict]:
        """
        Get log summaries for all tests.
        
        Returns:
            Dictionary mapping test_id to log summary
        """
        summaries = {}
        for test_id in self.test_logs.keys():
            summaries[test_id] = self.get_test_log_summary(test_id)
        return summaries
    
    def find_errors(self) -> List[Dict]:
        """
        Find all ERROR level log entries.
        
        Returns:
            List of error log entries
        """
        return [e for e in self.log_entries if e['level'] == 'ERROR']
    
    def find_warnings(self) -> List[Dict]:
        """
        Find all WARN level log entries.
        
        Returns:
            List of warning log entries
        """
        return [e for e in self.log_entries if e['level'] == 'WARN']
    
    def check_test_completion(self, test_id: str) -> bool:
        """
        Check if a test has a completion log entry.
        
        Args:
            test_id: Test case identifier
            
        Returns:
            True if test completion was logged, False otherwise
        """
        if test_id not in self.test_logs:
            return False
        
        for entry in self.test_logs[test_id]:
            if 'completed' in entry['message'].lower():
                return True
        
        return False


if __name__ == '__main__':
    # Standalone test
    import os
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    log_file = os.path.join(base_dir, 'data', 'sample_logs.txt')
    
    parser = LogParser(log_file)
    
    print("Overall Log Counts:")
    print("-" * 80)
    counts = parser.get_log_counts_by_level()
    for level, count in sorted(counts.items()):
        print(f"{level}: {count}")
    
    print("\nTest-Specific Summaries:")
    print("-" * 80)
    summaries = parser.get_all_test_summaries()
    for test_id, summary in sorted(summaries.items()):
        print(f"\n{test_id}:")
        print(f"  Warnings: {summary['warn_count']}, Errors: {summary['error_count']}")
        if summary['errors']:
            print(f"  Error messages: {summary['errors']}")
        if summary['warnings']:
            print(f"  Warning messages: {summary['warnings']}")
