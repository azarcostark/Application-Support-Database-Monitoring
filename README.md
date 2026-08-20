# Application Support & Database Monitoring Platform

A Python/Flask application-support and monitoring platform designed to simulate real-world production support workflows across application/API health, database health, incident management, alerting, logging, and automated testing.

The project combines **application support concepts** with **SDET/QA automation practices**, including REST API validation, SQL/database validation, monitoring, incident lifecycle testing, regression testing, mocking, and CI execution.

---

## Project Overview

The platform continuously evaluates application and database health and provides structured information that can be used by an application-support or engineering team to investigate issues.

### Core workflow

```text
Application / API
       |
       v
API Health Monitoring
       |
       +------------------+
       |                  |
       v                  v
Database Monitoring   Response-Time Monitoring
       |                  |
       +--------+---------+
                |
                v
          Health Report
                |
                v
        Incident Analyzer
                |
        +-------+-------+
        |               |
     Healthy        Incident
                        |
                        v
                 Incident Store
                        |
                        v
                  Alert Manager
                        |
                        v
               Notification Service
                        |
                        v
                Dashboard / APIs
```

---

## Key Features

### 1. API Health Monitoring

The application monitors configured API endpoints and evaluates:

- Endpoint availability
- HTTP/API health
- Response-time thresholds
- Failed endpoints
- Slow endpoints
- Overall API status

API failures can result in incidents classified as critical, while slow endpoints can be classified as warnings.

---

### 2. Database Monitoring

The platform monitors MySQL database availability and connectivity.

Database monitoring includes:

- MySQL connectivity checks
- Database health status
- Database response-time validation
- SQL-based validation
- Database failure detection

Database operations are kept separate from Flask route handling.

---

### 3. Full Health Monitoring

The health-monitoring layer combines API and database checks into a single health report.

Example overall states:

```text
HEALTHY
DEGRADED
CRITICAL
```

This provides a single view of the application's current operational state.

---

### 4. Incident Detection and Analysis

The incident analyzer evaluates monitoring results and determines whether an incident exists.

Incident information can include:

- Incident status
- Severity
- Area
- Root cause
- Recommended action
- Failed API endpoints
- Slow API endpoints

Example areas include:

```text
APPLICATION/API
DATABASE
```

Severity is determined from the detected condition, allowing the platform to distinguish between critical failures and performance warnings.

---

### 5. Incident Lifecycle Management

The platform supports incident-management workflows including:

- Incident creation
- Incident retrieval
- Incident details
- Incident filtering
- Incident summaries
- Incident statistics
- Incident resolution
- Incident history
- Open-incident detection
- Recovery handling

This models the type of lifecycle commonly used in application-support environments.

---

### 6. Alert Management

Alerts are generated from detected incidents.

The alert layer supports:

- Alert creation
- Alert retrieval
- Alert history
- Alert formatting
- Severity information
- Incident association
- Failed endpoint information
- Slow endpoint information

Alerts are linked to their corresponding incidents through the database relationship.

---

### 7. Notification Service

The monitoring workflow can pass generated alerts to the notification service.

The behavior is intentionally controlled so that:

```text
Healthy system
     |
     v
No incident
     |
     v
No alert
     |
     v
No notification
```

When an incident is detected:

```text
Incident
   |
   v
Alert
   |
   v
Notification
```

This behavior is covered by automated tests.

---

### 8. Scheduled Monitoring

The project includes a scheduler for repeated monitoring cycles.

The scheduler supports:

- Repeated monitoring cycles
- Configurable intervals
- Multiple-cycle execution
- Maximum-cycle control
- Invalid interval validation

This allows the monitoring process to behave more like a continuously running support-monitoring service.

---

### 9. Log Analysis

The platform includes application logging and log-analysis functionality.

Logs can be used as supporting evidence during incident analysis.

The incident workflow can correlate monitoring failures with relevant log information to help identify potential causes.

Example log evidence includes:

```text
INCIDENT CREATED
INCIDENT DETECTED
OPEN INCIDENT ALREADY EXISTS
INCIDENT SAVED TO LOCAL FALLBACK
```

---

### 10. Local Incident Fallback

The platform includes a local JSON fallback mechanism.

If MySQL incident persistence is unavailable, incident information can be stored locally:

```text
logs/incidents.json
```

The purpose of this fallback is to prevent monitoring information from being completely lost when database persistence is unavailable.

Runtime fallback data is excluded from version control.

---

### 11. Monitoring Dashboard

The project includes a Flask/Jinja-based web dashboard.

The dashboard provides visibility into:

- Overall system status
- API status
- Database status
- Open incidents
- Total alerts
- API monitoring metrics
- Database monitoring metrics
- Incident information
- Recent incidents

The dashboard also provides navigation into incident and alert history/detail views.

---

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application and monitoring logic |
| Flask | Web application and REST API |
| MySQL | Persistent database storage |
| SQL | Database validation and data operations |
| Pytest | Automated testing |
| Mocking / Monkeypatch | Isolated unit testing |
| HTML / Jinja | Monitoring dashboard |
| Git | Version control |
| GitHub | Repository hosting |
| GitHub Actions | CI test execution |

---

## Project Structure

```text
Application-Support-Database-Monitoring/
│
├── .github/
│   └── workflows/
│       └── tests.yml
│
├── app/
│   ├── __init__.py
│   ├── dashboard_service.py
│   ├── routes.py
│   └── templates/
│       ├── alert_history.html
│       ├── dashboard.html
│       ├── incident_details.html
│       └── incident_history.html
│
├── config/
│   ├── __init__.py
│   ├── database.py
│   └── settings.py
│
├── database/
│   └── ...
│
├── logs/
│   ├── application.log
│   └── incidents.json
│
├── monitoring/
│   ├── __init__.py
│   ├── alert_manager.py
│   ├── alert_repository.py
│   ├── api_monitor.py
│   ├── db_monitor.py
│   ├── health_monitor.py
│   ├── incident_analyzer.py
│   ├── incident_store.py
│   ├── log_analyzer.py
│   ├── notification_service.py
│   ├── run_monitor.py
│   └── scheduler.py
│
├── tests/
│   ├── conftest.py
│   ├── test_alert_manager.py
│   ├── test_alert_repository.py
│   ├── test_alerts_api.py
│   ├── test_alert_history_view.py
│   ├── test_api_monitor.py
│   ├── test_customers_api.py
│   ├── test_dashboard_api.py
│   ├── test_database_connection.py
│   ├── test_db_monitor.py
│   ├── test_health.py
│   ├── test_health_monitor.py
│   ├── test_incident_analyzer.py
│   ├── test_incident_area_filter_api.py
│   ├── test_incident_area_summary_api.py
│   ├── test_incident_create_api.py
│   ├── test_incident_details_api.py
│   ├── test_incident_details_view.py
│   ├── test_incident_filter_api.py
│   ├── test_incident_history_api.py
│   ├── test_incident_history_view.py
│   ├── test_incident_lifecycle_api.py
│   ├── test_incident_repository.py
│   ├── test_incident_resolve_api.py
│   ├── test_incident_statistics_api.py
│   ├── test_incident_store.py
│   ├── test_incident_summary_api.py
│   ├── test_incidents_api.py
│   ├── test_log_analyzer.py
│   ├── test_logger.py
│   ├── test_monitor_runner.py
│   ├── test_notification_service.py
│   ├── test_orders_api.py
│   └── test_scheduler.py
│
├── .env
├── .gitignore
├── requirements.txt
└── run.py
```

---

## Environment Configuration

Database configuration is provided through environment variables.

Example:

```text
DB_HOST=localhost
DB_PORT=3306
DB_USER=<your_database_user>
DB_PASSWORD=<your_database_password>
DB_NAME=application_db
```

Do not commit real credentials to Git.

The project's `.gitignore` excludes environment-specific and runtime files where appropriate.

---

## Running the Application

### 1. Activate the virtual environment

On Windows PowerShell:

```powershell
.env\Scripts\Activate.ps1
```

### 2. Start the Flask application

```powershell
python run.py
```

The application runs locally and exposes the monitoring APIs and web dashboard.

---

## Running the Monitoring Cycle

A single monitoring cycle can be executed with:

```powershell
python -m monitoring.run_monitor
```

The monitoring cycle performs the following high-level operations:

```text
Run health checks
      ↓
Analyze health report
      ↓
Detect incident
      ↓
Persist incident
      ↓
Create alert
      ↓
Send notification when required
      ↓
Print/report monitoring result
```

---

## Running the Scheduler

The scheduler is responsible for executing monitoring cycles repeatedly according to the configured interval and execution limits.

The scheduler is covered by automated tests for:

- Normal execution
- Multiple cycles
- Waiting between cycles
- Invalid intervals
- Maximum-cycle handling

---

## API Examples

The platform exposes REST endpoints for application, incident, alert, monitoring, and dashboard functionality.

### Health Check

```http
GET /health
```

### Incident Summary

```http
GET /incidents/summary
```

PowerShell:

```powershell
Invoke-RestMethod `
    -Uri "http://127.0.0.1:5000/incidents/summary" `
    -Method GET
```

### Incident Statistics

```http
GET /incidents/statistics
```

PowerShell:

```powershell
Invoke-RestMethod `
    -Uri "http://127.0.0.1:5000/incidents/statistics" `
    -Method GET
```

### Resolve Incident

```http
PATCH /incidents/<incident_id>/resolve
```

### Incident History View

```http
GET /incidents/history/view
```

The application also provides endpoints for incident filtering, incident details, incident creation, alert management, customer/order data, and dashboard information.

---

## Automated Testing

Testing is a major part of this project.

The test suite covers:

### API Testing

- HTTP response validation
- Endpoint behavior
- Positive scenarios
- Negative scenarios
- Request parameter validation
- Customer APIs
- Order APIs
- Incident APIs
- Alert APIs
- Dashboard APIs

### Database Testing

- Database connectivity
- SQL queries
- Database health
- Data consistency
- Repository operations

### Monitoring Testing

- API health monitoring
- Response-time thresholds
- Database monitoring
- Full health checks
- Incident analysis
- Log analysis
- Monitoring runner
- Scheduler behavior

### Incident and Alert Testing

- Incident creation
- Incident retrieval
- Filtering
- Statistics
- Summary
- Resolution
- Lifecycle behavior
- Alert creation
- Alert retrieval
- Alert formatting
- Alert history
- Notification behavior

### Test Isolation

The project uses Pytest fixtures, monkeypatching, and test configuration to isolate individual components and avoid unnecessary dependency on live behavior during unit tests.

---

## Test Execution

Run the complete test suite:

```powershell
python -m pytest -v
```

Example verified project result:

```text
117 passed
```

The latest recorded full-suite run completed successfully with all 117 tests passing.

---

## Code Quality Checks

Check for whitespace and formatting issues with:

```powershell
git diff --check
```

Python syntax can be validated with:

```powershell
.env\Scripts\python.exe -m py_compile appoutes.py
```

---

## CI / GitHub Actions

The project includes a GitHub Actions workflow:

```text
.github/workflows/tests.yml
```

The CI workflow is used to automate project validation and test execution.

This helps ensure that changes pushed to the repository are validated consistently rather than relying only on local test execution.

---

## Application Support Concepts Demonstrated

This project demonstrates practical application-support workflows including:

- Application health monitoring
- API availability monitoring
- API response-time monitoring
- Database monitoring
- SQL troubleshooting
- Incident detection
- Incident severity classification
- Root-cause identification
- Recommended troubleshooting actions
- Incident creation
- Incident resolution
- Incident history
- Incident filtering
- Alert management
- Notification handling
- Log-based troubleshooting
- Database fallback handling
- Monitoring scheduling

---

## SDET / QA Automation Concepts Demonstrated

The project also demonstrates:

- Python automation
- REST API testing
- Pytest
- Positive testing
- Negative testing
- HTTP status-code validation
- Request validation
- Response validation
- Database validation
- SQL queries
- MySQL integration
- Test isolation
- Mocking
- Monkeypatching
- Regression testing
- Monitoring automation
- Incident lifecycle testing
- Git version control
- CI automation

---

## Architecture and Separation of Responsibilities

The project separates major responsibilities into different layers.

### Flask Application Layer

```text
app/
```

Responsible for:

- HTTP routes
- API responses
- Dashboard rendering
- Web views

### Monitoring Layer

```text
monitoring/
```

Responsible for:

- API monitoring
- Database monitoring
- Health checks
- Incident analysis
- Alert management
- Notifications
- Scheduling
- Log analysis

### Configuration Layer

```text
config/
```

Responsible for:

- Database configuration
- Application settings
- Environment-based configuration

### Test Layer

```text
tests/
```

Responsible for:

- Unit tests
- API tests
- Integration-style validation
- Monitoring tests
- Database tests
- Regression coverage

This separation keeps HTTP/API logic, monitoring logic, persistence, configuration, and testing responsibilities organized independently.

---

## Persistence and Reliability

The platform uses MySQL for persistent incident and alert storage.

The project also includes a local incident fallback:

```text
MySQL
  |
  | available
  v
Persistent incident storage

MySQL
  |
  | unavailable
  v
logs/incidents.json
```

This provides an additional layer of resilience for monitoring information.

---

## Git Workflow

The project is maintained using Git and GitHub.

Typical workflow:

```powershell
git status
git diff
git diff --check
git add .
git commit -m "Describe change"
git push origin main
```

The repository contains the project's development history and CI configuration.

---

## Project Status

```text
Application Support & Database Monitoring Platform

API Monitoring              ✅
Database Monitoring         ✅
Health Monitoring           ✅
Response-Time Monitoring    ✅
Incident Detection          ✅
Incident Analysis           ✅
Incident Lifecycle          ✅
Incident Filtering          ✅
Incident Statistics         ✅
Incident History            ✅
Alert Management            ✅
Notifications               ✅
Log Analysis                ✅
Monitoring Scheduler        ✅
Web Dashboard               ✅
MySQL Persistence           ✅
Local Incident Fallback     ✅
Automated Pytest Tests      ✅
Git Version Control         ✅
GitHub Actions CI           ✅
```

### Latest Recorded Test Result

```text
117 passed
```

---

## Why This Project Is Relevant to SDET

Although the application is designed around application-support and monitoring scenarios, it provides a strong practical foundation for SDET and QA automation work.

The project demonstrates how to:

1. Identify application/API behavior that needs validation.
2. Build reusable automated checks.
3. Validate HTTP responses and API behavior.
4. Validate backend data using SQL.
5. Test positive and negative scenarios.
6. Isolate dependencies through fixtures and mocking.
7. Detect failures automatically.
8. Classify failures into actionable incidents.
9. Run regression tests repeatedly.
10. Integrate automated testing into CI.

This makes the project particularly relevant for roles involving **SDET, QA Automation, API Testing, Software Testing, and Application Support**.

---

## Resume Project Summary

**Application Support & Database Monitoring Platform**  
*Python, Flask, MySQL, SQL, Pytest, GitHub Actions*

Built a Python/Flask application-support and monitoring platform covering API health, response-time monitoring, MySQL database monitoring, automated incident analysis, alert management, scheduled monitoring, notifications, logging, and a web dashboard. Developed comprehensive Pytest coverage across API, database, monitoring, incident, alert, dashboard, and scheduler components, with CI validation through GitHub Actions.

---

## Author

Built as a hands-on project to develop practical skills in:

- Python
- REST API testing
- SDET/QA automation
- SQL and MySQL
- Application support
- Monitoring
- Incident management
- Test automation
- CI/CD
- Git/GitHub
