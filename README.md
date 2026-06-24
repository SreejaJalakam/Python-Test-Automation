# Python Test Automation & Log Analyzer

A Python-based automation tool that validates software test runs by comparing expected vs actual outputs, parses execution logs, flags anomalies, and generates structured reports to speed up debugging and verification.

---

## 📖 About This Project

This project automates the verification of test results for embedded systems and automotive software testing. It helps engineers quickly identify failures, analyze logs, and generate actionable reports without manual inspection.

**What it does:**
- Compares actual test outputs against expected baselines with tolerance checks
- Parses execution logs to extract warnings, errors, and test events
- Detects anomalies and assigns severity levels
- Generates reports in multiple formats (console, CSV, JSON)

**Why it matters:**
- Saves time by automating manual verification
- Reduces human error in test analysis
- Provides clear, structured reports for debugging
- Mirrors real-world verification workflows used in industry

---

## 📁 Project Structure

```
Python Test Automation/
│
├── data/                        # Input data files
│   ├── expected_results.json    # Baseline test expectations
│   ├── actual_results.json      # Actual test run outputs
│   └── sample_logs.txt          # Simulated execution logs
│
├── src/                         # Source code modules
│   ├── validator.py             # Output validation logic
│   ├── log_parser.py            # Log parsing and analysis
│   ├── anomaly_checker.py       # Anomaly detection rules
│   ├── report_generator.py      # Report generation
│   └── main.py                  # Main orchestrator
│
├── reports/                     # Generated reports (auto-created)
│   ├── test_summary.csv         # CSV report
│   └── test_summary.json        # JSON report
│
├── README.md                    # This file
└── requirements.txt             # Dependencies (none - uses stdlib)
```

---

## 📄 What Each File Does

### Data Files (`data/`)

**`expected_results.json`**
- Contains baseline test expectations
- Format: test_id, expected_output, tolerance, description
- Example: `{"test_id": "TC_001", "expected_output": 75, "tolerance": 2}`

**`actual_results.json`**
- Contains actual test run outputs
- Format: test_id, actual_output, timestamp
- Example: `{"test_id": "TC_001", "actual_output": 77, "timestamp": "2026-01-31T10:15:23"}`

**`sample_logs.txt`**
- Simulated system execution logs
- Format: `[timestamp] [LEVEL] message`
- Levels: INFO, DEBUG, WARN, ERROR

### Source Code (`src/`)

**`validator.py`**
- Compares expected vs actual test outputs
- Applies tolerance-based validation
- Returns status: PASS, FAIL, or BORDERLINE
- Calculates deviation and pass rates

**`log_parser.py`**
- Parses log files using regex patterns
- Extracts timestamps, log levels, and messages
- Associates logs with specific test cases
- Counts warnings and errors per test

**`anomaly_checker.py`**
- Implements anomaly detection rules
- Flags outputs outside tolerance
- Detects ERROR logs and excessive warnings
- Assigns severity: CRITICAL, HIGH, MEDIUM, LOW, NONE

**`report_generator.py`**
- Generates console reports with formatted tables
- Creates CSV reports for Excel analysis
- Creates JSON reports for programmatic access
- Calculates summary statistics

**`main.py`**
- Main entry point that orchestrates the workflow
- Loads data, validates outputs, parses logs
- Detects anomalies and generates reports
- Handles errors gracefully

---

## ⚙️ How It Works

### Workflow

1. **Load Data**
   - Reads expected results from `data/expected_results.json`
   - Reads actual results from `data/actual_results.json`
   - Reads execution logs from `data/sample_logs.txt`

2. **Validate Outputs**
   - Compares each actual output against expected baseline
   - Checks if deviation is within tolerance
   - Classifies as PASS, FAIL, or BORDERLINE

3. **Parse Logs**
   - Extracts log entries using regex
   - Identifies log levels (INFO, DEBUG, WARN, ERROR)
   - Associates logs with test cases
   - Counts warnings and errors

4. **Detect Anomalies**
   - Flags tests with outputs outside tolerance
   - Detects ERROR logs
   - Identifies excessive warnings (threshold: 2+)
   - Assigns severity based on multiple factors

5. **Generate Reports**
   - Creates console summary with formatted tables
   - Generates CSV file in `reports/test_summary.csv`
   - Generates JSON file in `reports/test_summary.json`
   - Displays summary statistics and anomalies

### Validation Logic

```python
# Tolerance-based classification
if abs(actual - expected) <= tolerance:
    status = 'PASS'
elif abs(actual - expected) <= tolerance * 1.5:
    status = 'BORDERLINE'  # Within 150% of tolerance
else:
    status = 'FAIL'
```

### Severity Classification

- **CRITICAL**: Failed validation + ERROR logs
- **HIGH**: Failed validation OR ERROR logs
- **MEDIUM**: Borderline results or missing completion
- **LOW**: Only warnings or minor issues
- **NONE**: No anomalies detected

---

## 🚀 How to Run

### Prerequisites

- Python 3.7 or higher
- No external dependencies (uses only standard library)

### Installation

```bash
# Navigate to project directory
cd "C:\Users\Sreeja\Downloads\Python Test Automation"

# Verify Python installation
python --version
```

### Run the Complete Analysis

```bash
python src/main.py
```

**This will:**
1. Validate all test outputs
2. Parse execution logs
3. Detect anomalies
4. Generate console, CSV, and JSON reports

### Run Individual Components

```bash
# Test validation logic
python src/validator.py

# Test log parsing
python src/log_parser.py

# Test anomaly detection
python src/anomaly_checker.py

# Test report generation
python src/report_generator.py
```

### View Generated Reports

**Console Output:**
- Displays formatted table with test results
- Shows summary statistics
- Lists detected anomalies

**CSV Report:**
```bash
# Open in Excel or text editor
reports/test_summary.csv
```

**JSON Report:**
```bash
# View in text editor or parse programmatically
reports/test_summary.json
```

---

## 📊 Sample Output

### Console Report

```
====================================================================================================
                                   TEST EXECUTION REPORT
====================================================================================================

TEST RESULTS:
----------------------------------------------------------------------------------------------------
Test ID      Status       Expected     Actual       Warnings   Errors     Severity    
----------------------------------------------------------------------------------------------------
TC_001       PASS         75           77           0          0          NONE        
TC_002       PASS         120          118          0          0          NONE        
TC_003       BORDERLINE   3500         3650         0          0          MEDIUM      
TC_004       FAIL         98.5         95.2         0          0          HIGH        
TC_005       PASS         45           48           0          0          NONE        
----------------------------------------------------------------------------------------------------

SUMMARY STATISTICS:
Total Tests:        5
Passed:             3 (60.0%)
Failed:             1
Borderline:         1
Overall Health:     GOOD
```

### CSV Report

| Test ID | Status | Expected | Actual | Tolerance | Deviation | Severity |
|---------|--------|----------|--------|-----------|-----------|----------|
| TC_001 | PASS | 75 | 77 | 2 | 2 | NONE |
| TC_003 | BORDERLINE | 3500 | 3650 | 100 | 150 | MEDIUM |
| TC_004 | FAIL | 98.5 | 95.2 | 1.5 | 3.3 | HIGH |

---

## 🎯 Key Features

- ✅ **Tolerance-based validation** - Nuanced PASS/BORDERLINE/FAIL classification
- ✅ **Regex log parsing** - Flexible pattern matching for log analysis
- ✅ **Severity classification** - Multi-factor anomaly detection
- ✅ **Multi-format reports** - Console, CSV, and JSON outputs
- ✅ **Modular architecture** - 5 independent, testable components
- ✅ **No dependencies** - Uses only Python standard library
- ✅ **Error handling** - Graceful handling of edge cases

---

## 🔧 Customization

### Modify Test Data

Edit `data/expected_results.json` and `data/actual_results.json` to add your own test cases.

### Adjust Tolerance Thresholds

Edit the tolerance values in `expected_results.json` for each test case.

### Change Warning Threshold

In `src/anomaly_checker.py`, modify:
```python
WARN_THRESHOLD = 2  # Change this value
```

### Customize Report Format

Edit `src/report_generator.py` to change table formatting or add new report types.

---

## 📝 Technical Details

**Language:** Python 3.7+

**Libraries Used (Standard Library Only):**
- `json` - Data parsing
- `csv` - Report generation
- `re` - Log parsing with regex
- `os` - File operations
- `datetime` - Timestamps

**Architecture:** Modular design with separation of concerns

**Testing:** Each component can be tested independently

---

## 🎓 Use Cases

- **Embedded Systems Testing** - Validate sensor outputs and controller behavior
- **Automotive Software** - Verify engine control and safety systems
- **Hardware-in-the-Loop** - Analyze test bench results
- **Regression Testing** - Compare current vs baseline test runs
- **CI/CD Integration** - Automate test verification in pipelines

---

## 📄 License

This project is open source and available under the MIT License.

---

## 👤 Author

**Sreeja Jalakam**
