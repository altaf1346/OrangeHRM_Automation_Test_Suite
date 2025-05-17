# OrangeHRM Automation Test Suite

This project provides a comprehensive automation framework for testing OrangeHRM using Selenium WebDriver with Python and Pytest. The implementation follows the Page Object Model design pattern for better maintainability and code reusability.

## Features

- ✅ Selenium WebDriver with Python and Pytest
- 🚀 CI/CD integration using GitHub Actions
- 📊 Allure Reporting for detailed test results
- 🐳 Docker support for containerized test execution
- 📁 Modular architecture following Page Object Model (POM)
- 🔄 Cross-browser testing support
- 📝 Detailed logging and reporting

## Project Structure

```
OrangeHRM-Automation-Suite/
│
├── tests/                      # All test cases
│   ├── test_login.py
│
├── pages/                      # Page Object Model (POM)
│   ├── base_page.py
│   ├── login_page.py
│
├── utils/                      # Helpers and reusable utilities
│   ├── config.py
│   ├── logger.py
│   └── data_reader.py
│
├── data/                       # Test data files
│   ├── users.json
│   └── login_credentials.csv
│
├── reports/                    # Allure results and HTML reports (in .gitignore)
│
├── .github/                    # GitHub Actions CI
│   └── workflows/
│       └── python-tests.yml
│
├── conftest.py                 # Pytest fixtures and hooks
├── requirements.txt            # All dependencies
├── pytest.ini                  # Pytest configuration
├── .gitignore                  # Ignore cache, IDE, reports, etc.
├── Dockerfile                  # Container for test runs
├── docker-compose.yml          # Docker compose configuration
├── run_tests.bat               # Windows script to run tests
└── run_tests.sh                # Linux/Mac script to run tests
```

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- Chrome or Firefox browser
- Java (for Allure report generation)

### Installation

1. Clone the repository
   ```
   git clone <your-repo-url>
   cd OrangeHRM-Automation-Suite
   ```

2. Setup using script (recommended)
   - Windows: `run_tests.bat`
   - Linux/Mac: `./run_tests.sh` (make sure it's executable: `chmod +x run_tests.sh`)

3. Manual setup
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

### Running Tests

1. Using script:
   - Windows: `run_tests.bat`
   - Linux/Mac: `./run_tests.sh`

2. Manually:
   ```
   pytest
   ```

3. Generate Allure report:
   ```
   allure serve reports/allure-results
   ```

## Docker Execution

```bash
docker-compose up
```

## CI/CD Workflow

Tests are automatically triggered on pull requests and pushes to the main branch using GitHub Actions.

## Troubleshooting

### WebDriver Issues on Windows

If you encounter errors like `[WinError 193] %1 is not a valid Win32 application`, try these solutions:

1. Make sure you have Chrome or Firefox browser installed
2. Download WebDriver manually:
   - ChromeDriver: https://chromedriver.chromium.org/downloads
   - GeckoDriver: https://github.com/mozilla/geckodriver/releases
3. Add the WebDriver to your PATH or place it in your project directory
4. Try using a specific version of WebDriver that matches your browser version

### Other Common Issues

- **NoSuchElementException**: The element locator might have changed. Update the locators in page objects.
- **TimeoutException**: The application is taking too long to load. Consider increasing timeouts in config.py.
- **Browser crashes during test**: Try running in non-headless mode for debugging: `pytest --headless=false`

For more troubleshooting help, check the logs in the reports/logs directory.