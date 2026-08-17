# Application Support & Database Monitoring Platform

A beginner-to-intermediate Python project that combines application monitoring, database monitoring, REST API testing, incident management, log analysis, and automated regression testing.

The goal of this project is to simulate an application-support environment where system health can be monitored, incidents can be detected and tracked, and automated tests can verify that the application continues to work correctly.

---

## Project Overview

The platform monitors:

- REST API availability
- REST API response time
- MySQL database availability
- MySQL database response time
- Application health
- Incident conditions
- Application logs

When a problem is detected, the system can:

1. Analyze the health-check results.
2. Determine whether an incident exists.
3. Assign an incident severity.
4. Identify the affected area.
5. Determine the root cause.
6. Recommend an action.
7. Store the incident in MySQL.
8. Use a local JSON fallback if MySQL is unavailable.
9. Resolve recovered incidents.
10. Provide REST APIs for incident management.
11. Analyze application logs for additional evidence.

The project also contains an automated pytest suite covering API behavior, database operations, monitoring logic, incident management, and log analysis.

---

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application and monitoring logic |
| Flask | REST API |
| MySQL | Persistent application and incident data |
| mysql-connector-python | MySQL connectivity |
| Requests | HTTP/API communication |
| pytest | Automated testing |
| python-dotenv | Environment configuration |
| Git | Version control |

---

## Architecture

```text
                    Application Support Platform
                               |
             +-----------------+-----------------+
             |                                   |
             v                                   v
       Flask REST API                      Monitoring Layer
             |                                   |
             v                         +---------+---------+
      API / Database                    |                   |
       Operations                       v                   v
                                  API Monitoring     DB Monitoring
                                        |                   |
                                        +---------+---------+
                                                  |
                                                  v
                                          Health Monitor
                                                  |
                                                  v
                                         Incident Analyzer
                                                  |
                                    +-------------+-------------+
                                    |                           |
                                    v                           v
                              MySQL Incident Store       Local JSON Fallback
                                    |
                                    v
                              Incident Lifecycle
                                    |
                              +-----+------+
                              |            |
                              v            v
                           OPEN        RESOLVED
```

---

## Monitoring Workflow

The monitoring cycle follows this general flow:

```text
Run Monitoring Cycle
        |
        v
Run API Health Checks
        |
        v
Check MySQL Database
        |
        v
Determine Overall Health
        |
        +----------------------+
        |                      |
        v                      v
     HEALTHY              Problem Detected
        |                      |
        v                      v
Resolve Recovered        Analyze Incident
Incidents                     |
                              v
                       Create Incident
                              |
                              v
                         Store in MySQL
                              |
                              v
                       Log Evidence
```

---

## Health Status

The health monitor determines one of three overall states.

### HEALTHY

The API and database are available and operating within the configured response-time thresholds.

### DEGRADED

The monitored systems are available, but one or more components are slower than the configured response-time threshold.

### CRITICAL

The database or one or more monitored API endpoints are unavailable.

---

## Incident Severity

The project currently uses two incident severities:

```text
WARNING
CRITICAL
```

### WARNING

Used for degraded conditions such as slow API responses.

### CRITICAL

Used when a critical component is unavailable, such as a database failure or failed API health check.

---

## Incident Areas

Incidents can be associated with areas such as:

```text
APPLICATION
DATABASE
TEST
APPLICATION/API
```

The REST API validates the supported incident-area values for incident filtering.

---

## Incident Lifecycle

Incidents have two main states:

```text
OPEN
RESOLVED
```

Example lifecycle:

```text
System Failure
      |
      v
Incident Created
      |
      v
OPEN
      |
      |
System Recovers
      |
      v
Incident Resolved
      |
      v
RESOLVED
```

The monitoring workflow can automatically resolve matching open incidents when the system becomes healthy again.

---

## Log Analysis

Application logs are written to:

```text
logs/application.log
```

The log analyzer reads the application log and extracts information such as:

- INFO messages
- WARNING messages
- ERROR messages
- API requests
- API response times
- Slow API requests
- API monitoring results
- Database monitoring results

Log information can also be used as supporting evidence when analyzing incidents.

Runtime logs are intentionally excluded from Git using `.gitignore`.

---

## REST API Endpoints

### Health

```http
GET /health
```

Returns the application health status.

---

### Customers

```http
GET /customers
```

Returns customer information from MySQL.

---

### Orders

```http
GET /orders
```

Supports:

- Status filtering
- Customer filtering
- Pagination
- Page-size validation

Examples:

```http
GET /orders
GET /orders?status=PENDING
GET /orders?customer_id=1
GET /orders?page=2&limit=10
```

---

### Incidents

```http
GET /incidents
```

Returns incidents.

The endpoint supports:

- Status filtering
- Severity filtering
- Area filtering

Examples:

```http
GET /incidents
GET /incidents?status=OPEN
GET /incidents?severity=CRITICAL
GET /incidents?area=DATABASE
GET /incidents?status=OPEN&severity=CRITICAL&area=DATABASE
```

---

### Incident Summary

```http
GET /incidents/summary
```

Returns overall incident counts including:

- Total incidents
- Open incidents
- Resolved incidents
- Critical incidents
- Warning incidents

---

### Incident Summary by Area

```http
GET /incidents/summary/areas
```

Returns incident totals grouped by area.

---

### Incident Statistics

```http
GET /incidents/statistics
```

Returns incident statistics grouped by area and severity.

---

### Incident History

```http
GET /incidents/history
```

Returns the incident history stored in MySQL.

---

### Incident Details

```http
GET /incidents/<incident_id>
```

Returns details for a specific incident.

---

### Create Incident

```http
POST /incidents
```

Creates a new incident.

Example request:

```json
{
    "severity": "CRITICAL",
    "area": "DATABASE",
    "root_cause": "Database health check failed.",
    "recommended_action": "Check MySQL service and database connectivity."
}
```

---

### Resolve Incident

```http
PATCH /incidents/<incident_id>/resolve
```

Resolves an open incident.

---

## Database Layer

Database operations are separated from the Flask routes.

The database configuration is located in:

```text
config/database.py
```

Incident database operations are handled by:

```text
utils/incident_repository.py
```

This separation keeps HTTP/API logic separate from database access logic.

---

## Local Incident Fallback

The monitoring system includes a local JSON fallback mechanism.

If MySQL incident storage fails, incidents can be stored locally using:

```text
logs/incidents.json
```

The fallback is intended to prevent monitoring information from being completely lost when the database is unavailable.

Runtime fallback data is excluded from Git.

---

## Project Structure

```text
Application-Support-Database-Monitoring/
│
├── app/
│   ├── __init__.py
│   └── routes.py
│
├── config/
│   └── database.py
│
├── monitoring/
│   ├── __init__.py
│   ├── api_monitor.py
│   ├── db_monitor.py
│   ├── health_monitor.py
│   ├── incident_analyzer.py
│   ├── incident_store.py
│   ├── log_analyzer.py
│   └── run_monitor.py
│
├── utils/
│   ├── __init__.py
│   ├── incident_repository.py
│   └── logger.py
│
├── tests/
│   ├── test_api_monitor.py
│   ├── test_customers_api.py
│   ├── test_database_connection.py
│   ├── test_db_monitor.py
│   ├── test_health.py
│   ├── test_health_monitor.py
│   ├── test_incident_analyzer.py
│   ├── test_incident_area_filter_api.py
│   ├── test_incident_area_summary_api.py
│   ├── test_incident_create_api.py
│   ├── test_incident_details_api.py
│   ├── test_incident_filter_api.py
│   ├── test_incident_history_api.py
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
│   └── test_orders_api.py
│
├── logs/
│   ├── application.log
│   └── incidents.json
│
├── .env
├── .gitignore
├── requirements.txt
└── run.py
```

> Runtime files under `logs/` and environment files are excluded from version control.

---

## Environment Configuration

Database configuration is provided through environment variables.

Example:

```text
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=application_support
```

Do not commit real database credentials to Git.

The project uses `.env` for local configuration, and `.env` files are excluded through `.gitignore`.

---

## Installation

### 1. Clone the project

```bash
git clone <repository-url>
cd Application-Support-Database-Monitoring
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv venv
```

### 3. Activate the virtual environment

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```powershell
pip install -r requirements.txt
```

### 5. Configure environment variables

Create a local `.env` file containing the required MySQL configuration.

---

## Running the Application

Start the Flask application using:

```powershell
python run.py
```

The application runs locally at:

```text
http://127.0.0.1:5000
```

---

## Running the Monitoring Cycle

Run:

```powershell
python -m monitoring.run_monitor
```

The monitoring cycle:

1. Checks APIs.
2. Checks MySQL.
3. Determines overall health.
4. Analyzes incidents.
5. Creates incidents when necessary.
6. Resolves recovered incidents.
7. Produces an incident report.

---

## Running Tests

Run the complete automated test suite:

```powershell
python -m pytest -v
```

The current project regression suite contains:

```text
60 tests
```

with the latest verified result:

```text
60 passed
```

---

## Testing Strategy

The project uses pytest to validate several layers.

### API Tests

Verify:

- HTTP status codes
- Response structure
- Filtering
- Pagination
- Invalid parameters
- Incident creation
- Incident resolution

### Database Tests

Verify:

- Database connectivity
- Database queries
- Repository operations
- Incident persistence

### Monitoring Tests

Verify:

- API health checks
- Database health checks
- Overall health status
- Slow API detection

### Incident Tests

Verify:

- Incident classification
- Severity
- Area
- Incident creation
- Incident resolution
- Incident lifecycle
- Duplicate handling
- Recovery behavior

### Log Tests

Verify:

- Log file reading
- INFO detection
- WARNING detection
- ERROR detection
- API request extraction
- Slow request detection
- Log evidence used by incident analysis

---

## Example PowerShell Commands

Check application health:

```powershell
Invoke-RestMethod `
    -Uri "http://127.0.0.1:5000/health" `
    -Method GET
```

Get open incidents:

```powershell
Invoke-RestMethod `
    -Uri "http://127.0.0.1:5000/incidents" `
    -Method GET
```

Get critical incidents:

```powershell
Invoke-RestMethod `
    -Uri "http://127.0.0.1:5000/incidents?severity=CRITICAL" `
    -Method GET
```

Get incident summary:

```powershell
Invoke-RestMethod `
    -Uri "http://127.0.0.1:5000/incidents/summary" `
    -Method GET
```

Get incident statistics:

```powershell
Invoke-RestMethod `
    -Uri "http://127.0.0.1:5000/incidents/statistics" `
    -Method GET
```

Run the monitoring cycle:

```powershell
python -m monitoring.run_monitor
```

Run all tests:

```powershell
python -m pytest -v
```

---

## SDET / Automation Concepts Demonstrated

This project demonstrates practical experience with:

- Python automation
- REST API testing
- pytest
- Positive testing
- Negative testing
- API validation
- HTTP status-code validation
- Request parameter validation
- Database validation
- SQL queries
- MySQL integration
- Test isolation
- Mocking
- Monitoring
- Log analysis
- Incident lifecycle testing
- Regression testing
- Git version control

---

## Application Support Concepts Demonstrated

The project also demonstrates application-support workflows including:

- Health monitoring
- API availability monitoring
- Database monitoring
- Response-time monitoring
- Incident detection
- Incident severity classification
- Root-cause identification
- Recommended troubleshooting actions
- Incident creation
- Incident resolution
- Incident history
- Log-based troubleshooting
- Database fallback handling

---

## Future Improvements

Possible future improvements include:

- GitHub Actions CI/CD
- HTML test reports
- Scheduled monitoring
- Email or Slack notifications
- Authentication and authorization
- Dashboard visualization
- More advanced log correlation
- Monitoring metrics and historical trends
- Docker containerization

---

## Project Status

```text
Application Support & Database Monitoring Platform

API Monitoring              ✅
Database Monitoring         ✅
Health Monitoring           ✅
Incident Detection          ✅
Incident Lifecycle          ✅
Incident Filtering          ✅
Incident Statistics         ✅
Log Analysis                ✅
MySQL Persistence           ✅
Local Fallback              ✅
Automated pytest Tests      ✅
Git Repository              ✅

Latest Test Result:
60 passed
```

---

## Author

Built as a hands-on Python, API automation, database monitoring, and application-support project.