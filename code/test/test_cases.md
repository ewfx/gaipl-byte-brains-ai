# Integrated Platform Environment (IPE) - Agentic AI Test Cases
________________________________________

## 1. Task Creation Tests

### 1.1 Basic Task Creation
| Test ID | Description | Test Data | Expected Result |
|---------|-------------|-----------|-----------------|
| TASK-001 | Create task with description | Description: "Analyze system logs", Context: {} | Task created with pending status |
| TASK-002 | Create task with context | Description: "Check CPU usage", Context: {"time_range": "24h"} | Task created with context |
| TASK-003 | Create task with invalid JSON | Description: "Test", Context: "{invalid json}" | Error message displayed |
| TASK-004 | Create task with empty description | Description: "", Context: {} | Validation error shown |

### 1.2 Task Planning
```python
# Sample task planning test data
test_tasks = [
    {
        "description": "Analyze system logs for the last 24 hours",
        "context": {
            "time_range": "24h",
            "severity": ["ERROR", "CRITICAL"],
            "include_performance": true
        },
        "expected_steps": [
            {
                "id": "step_1",
                "description": "Access system log files",
                "type": "action",
                "parameters": {
                    "location": "system log directory",
                    "access_rights": "administrator privileges"
                }
            },
            {
                "id": "step_2",
                "description": "Filter logs for last 24 hours",
                "type": "analysis",
                "parameters": {
                    "time_range": "24 hours"
                }
            }
        ]
    }
]
```

## 2. Task Execution Tests

### 2.1 Task Execution Flow
| Test ID | Description | Test Data | Expected Result |
|---------|-------------|-----------|-----------------|
| EXEC-001 | Execute pending task | Task ID: "task_1" | Task status updates to running |
| EXEC-002 | Execute completed task | Task ID: "task_2" | Error message displayed |
| EXEC-003 | Execute non-existent task | Task ID: "invalid_id" | Error message displayed |
| EXEC-004 | Step execution | Step ID: "step_1" | Step status updates to completed |

### 2.2 Sample Execution Data
```python
test_execution = {
    "task_id": "task_1",
    "status": "running",
    "steps": [
        {
            "id": "step_1",
            "status": "completed",
            "result": "Successfully accessed log files",
            "completed_at": "2024-03-23T19:30:00"
        },
        {
            "id": "step_2",
            "status": "running",
            "result": None,
            "started_at": "2024-03-23T19:30:05"
        }
    ]
}
```

## 3. Task History Tests

### 3.1 History Management
| Test ID | Description | Test Data | Expected Result |
|---------|-------------|-----------|-----------------|
| HIST-001 | Archive completed task | Task ID: "task_1" | Task moves to history |
| HIST-002 | View task history | None | List of completed tasks |
| HIST-003 | Filter history by date | Date range: "Last 7 days" | Filtered history list |
| HIST-004 | Search history | Query: "CPU analysis" | Matching tasks |

### 3.2 Sample History Data
```python
test_history = {
    "completed_tasks": [
        {
            "task_id": "task_1",
            "description": "CPU Usage Analysis",
            "status": "completed",
            "created_at": "2024-03-23T19:00:00",
            "completed_at": "2024-03-23T19:15:00",
            "steps": [
                {
                    "id": "step_1",
                    "status": "completed",
                    "result": "CPU usage within normal range"
                }
            ]
        }
    ]
}
```

## 4. Log Analysis Tests

### 4.1 Log Processing
| Test ID | Description | Test Data | Expected Result |
|---------|-------------|-----------|-----------------|
| LOG-001 | Analyze error logs | Log type: "error" | Error patterns identified |
| LOG-002 | Analyze performance logs | Log type: "performance" | Performance metrics extracted |
| LOG-003 | Invalid log format | Log: "invalid format" | Error handled |
| LOG-004 | Empty log file | Log: "" | Warning message |

### 4.2 Sample Log Data
```python
test_logs = {
    "error_logs": [
        {
            "timestamp": "2024-03-23T19:00:00",
            "level": "ERROR",
            "message": "CPU usage exceeded threshold",
            "source": "system_monitor"
        }
    ],
    "performance_logs": [
        {
            "timestamp": "2024-03-23T19:00:00",
            "metric": "cpu_usage",
            "value": 95.5,
            "threshold": 90.0
        }
    ]
}
```

## 5. Data Persistence Tests

### 5.1 File Operations
| Test ID | Description | Test Data | Expected Result |
|---------|-------------|-----------|-----------------|
| DATA-001 | Save active tasks | Tasks: [task_1, task_2] | Tasks saved to file |
| DATA-002 | Load active tasks | File: "active_tasks.json" | Tasks loaded correctly |
| DATA-003 | Save task history | History: [task_1, task_2] | History saved to file |
| DATA-004 | Load task history | File: "task_history.json" | History loaded correctly |

### 5.2 Sample File Data
```python
test_files = {
    "active_tasks.json": [
        {
            "task_id": "task_1",
            "status": "pending",
            "created_at": "2024-03-23T19:00:00"
        }
    ],
    "task_history.json": [
        {
            "task_id": "task_2",
            "status": "completed",
            "completed_at": "2024-03-23T18:00:00"
        }
    ]
}
```

## 6. Log Analysis and Insights Tests

### 6.1 Log Filtering and Time Range
| Test ID | Description | Test Data | Expected Result |
|---------|-------------|-----------|-----------------|
| LOG-005 | Filter logs by custom date range | Start: "2024-03-20", End: "2024-03-23" | Logs within date range |
| LOG-006 | Filter logs by application | App: "web_server" | Logs for web_server only |
| LOG-007 | Filter logs by server | Server: "server-01" | Logs for server-01 only |
| LOG-008 | Filter logs by log level | Level: "ERROR" | Error logs only |
| LOG-009 | Filter logs by multiple criteria | App: "web_server", Level: "ERROR", Time: "24h" | Combined filtered logs |

### 6.2 Log Visualization
| Test ID | Description | Test Data | Expected Result |
|---------|-------------|-----------|-----------------|
| LOG-010 | Generate log level distribution | Logs: [100 INFO, 20 WARNING, 10 ERROR] | Pie chart with correct proportions |
| LOG-011 | Generate component distribution | Components: ["api", "auth", "database"] | Bar chart with correct counts |
| LOG-012 | Generate timeline visualization | Time series data | Scatter plot with correct timestamps |
| LOG-013 | Update visualizations on filter change | New filter criteria | Updated charts |

### 6.3 Log Statistics
| Test ID | Description | Test Data | Expected Result |
|---------|-------------|-----------|-----------------|
| LOG-014 | Calculate total log count | Logs: [100 entries] | Count: 100 |
| LOG-015 | Calculate error rate | Total: 100, Errors: 10 | Rate: 10% |
| LOG-016 | Count unique components | Components: ["api", "auth", "api", "db"] | Count: 3 |
| LOG-017 | Calculate time range | Start: "2024-03-20", End: "2024-03-23" | Range: "2024-03-20 to 2024-03-23" |

### 6.4 AI Analysis
| Test ID | Description | Test Data | Expected Result |
|---------|-------------|-----------|-----------------|
| LOG-018 | Generate AI insights | Custom prompt | Structured analysis with summary |
| LOG-019 | Identify key events | Log sequence | Chronological event list |
| LOG-020 | Detect potential issues | Error patterns | Issue list with severity |
| LOG-021 | Generate recommendations | Analysis results | Actionable recommendations |

### 6.5 Sample Test Data
```python
test_log_analysis = {
    "logs": [
        {
            "timestamp": "2024-03-23T19:00:00",
            "level": "INFO",
            "message": "User authentication successful",
            "server": "server-01",
            "application": "web_server",
            "component": "auth",
            "trace_id": "trace-1234",
            "user_id": "user-1",
            "duration_ms": 150,
            "status_code": 200
        },
        {
            "timestamp": "2024-03-23T19:01:00",
            "level": "ERROR",
            "message": "Database connection failed",
            "server": "server-02",
            "application": "database",
            "component": "database",
            "trace_id": "trace-1235",
            "user_id": "user-2",
            "duration_ms": 500,
            "status_code": 500
        }
    ],
    "filters": {
        "time_range": {
            "start": "2024-03-23T00:00:00",
            "end": "2024-03-23T23:59:59"
        },
        "application": "web_server",
        "server": "server-01",
        "log_level": "INFO"
    },
    "expected_statistics": {
        "total_logs": 100,
        "error_rate": 10.5,
        "unique_components": 5,
        "time_range": "2024-03-23 to 2024-03-23"
    }
}
```

### 6.6 Sample Test Script
```python
import pytest
from datetime import datetime, timedelta
from components.log_analyzer import LogAnalyzer
from services.log_service import LogService

def test_log_filtering():
    analyzer = LogAnalyzer()
    service = LogService()
    
    # Test custom date range
    start_time = datetime(2024, 3, 20)
    end_time = datetime(2024, 3, 23)
    logs = service.get_logs(
        application="all",
        server="all",
        start_time=start_time,
        end_time=end_time
    )
    assert all(start_time <= log['timestamp'] <= end_time for log in logs)
    
    # Test application filter
    logs = service.get_logs(application="web_server")
    assert all(log['application'] == "web_server" for log in logs)
    
    # Test log level filter
    logs = service.get_logs(log_level="ERROR")
    assert all(log['level'] == "ERROR" for log in logs)

def test_log_visualization():
    analyzer = LogAnalyzer()
    service = LogService()
    
    # Get sample logs
    logs = service.get_logs()
    df = pd.DataFrame(logs)
    
    # Test log level distribution
    level_counts = df['level'].value_counts()
    assert len(level_counts) > 0
    assert all(level in ['INFO', 'WARNING', 'ERROR', 'DEBUG'] for level in level_counts.index)
    
    # Test component distribution
    component_counts = df['component'].value_counts()
    assert len(component_counts) > 0
    assert all(component in ['api', 'auth', 'database', 'cache', 'network'] for component in component_counts.index)

def test_log_statistics():
    analyzer = LogAnalyzer()
    service = LogService()
    
    # Get sample logs
    logs = service.get_logs()
    df = pd.DataFrame(logs)
    
    # Test total log count
    assert len(df) > 0
    
    # Test error rate calculation
    error_rate = (len(df[df['level'] == 'ERROR']) / len(df)) * 100
    assert 0 <= error_rate <= 100
    
    # Test unique components
    unique_components = df['component'].nunique()
    assert unique_components > 0

def test_ai_analysis():
    analyzer = LogAnalyzer()
    service = LogService()
    
    # Get sample logs
    logs = service.get_logs()
    
    # Test AI analysis generation
    analysis = asyncio.run(
        analyzer.agent_service.analyze_logs(
            "Analyze these logs and provide insights",
            logs
        )
    )
    
    assert 'summary' in analysis
    assert 'key_events' in analysis
    assert 'issues' in analysis
    assert 'recommendations' in analysis
```

## 7. Authentication and User Management Tests

### 7.1 User Authentication
| Test ID | Description | Test Data | Expected Result |
|---------|-------------|-----------|-----------------|
| AUTH-001 | Valid user login | Username: "admin", Password: "valid_password" | Login successful, session created |
| AUTH-002 | Invalid credentials | Username: "admin", Password: "wrong_password" | Login failed, error message |
| AUTH-003 | Empty credentials | Username: "", Password: "" | Validation error |
| AUTH-004 | Session timeout | Session duration: 30 minutes | Session expired, redirect to login |
| AUTH-005 | Remember me functionality | Remember me: true | Extended session duration |

### 7.2 User Management
| Test ID | Description | Test Data | Expected Result |
|---------|-------------|-----------|-----------------|
| AUTH-006 | Create new user | User details: {username, email, role} | User created successfully |
| AUTH-007 | Update user profile | Updated details: {name, email} | Profile updated |
| AUTH-008 | Change password | Old: "current", New: "new_password" | Password updated |
| AUTH-009 | Reset password | Email: "user@example.com" | Reset link sent |
| AUTH-010 | Delete user account | User ID: "user_123" | Account deleted |

### 7.3 Role-Based Access Control
| Test ID | Description | Test Data | Expected Result |
|---------|-------------|-----------|-----------------|
| AUTH-011 | Admin access | Role: "admin" | Full system access |
| AUTH-012 | User access | Role: "user" | Limited access |
| AUTH-013 | Guest access | Role: "guest" | Read-only access |
| AUTH-014 | Role modification | New role: "analyst" | Access updated |
| AUTH-015 | Permission check | Resource: "logs", Action: "delete" | Access denied |

### 7.4 Sample Authentication Data
```python
test_auth_data = {
    "users": [
        {
            "id": "user_1",
            "username": "admin",
            "email": "admin@example.com",
            "password_hash": "hashed_password_1",
            "role": "admin",
            "created_at": "2024-03-23T00:00:00",
            "last_login": "2024-03-23T19:00:00",
            "is_active": True,
            "permissions": ["read", "write", "delete", "manage_users"]
        },
        {
            "id": "user_2",
            "username": "analyst",
            "email": "analyst@example.com",
            "password_hash": "hashed_password_2",
            "role": "analyst",
            "created_at": "2024-03-23T01:00:00",
            "last_login": "2024-03-23T18:00:00",
            "is_active": True,
            "permissions": ["read", "write"]
        }
    ],
    "sessions": [
        {
            "session_id": "session_1",
            "user_id": "user_1",
            "created_at": "2024-03-23T19:00:00",
            "expires_at": "2024-03-23T19:30:00",
            "ip_address": "192.168.1.1",
            "user_agent": "Mozilla/5.0..."
        }
    ],
    "login_attempts": [
        {
            "id": "attempt_1",
            "username": "admin",
            "timestamp": "2024-03-23T19:00:00",
            "success": True,
            "ip_address": "192.168.1.1"
        }
    ]
}
```

### 7.5 Sample Test Script
```python
import pytest
from datetime import datetime, timedelta
from services.auth_service import AuthService
from models.user import User

def test_user_login():
    auth_service = AuthService()
    
    # Test successful login
    result = auth_service.login("admin", "valid_password")
    assert result["success"] == True
    assert "session_id" in result
    assert "user" in result
    
    # Test invalid credentials
    result = auth_service.login("admin", "wrong_password")
    assert result["success"] == False
    assert "error" in result

def test_session_management():
    auth_service = AuthService()
    
    # Create session
    session = auth_service.create_session("user_1")
    assert session["user_id"] == "user_1"
    assert session["expires_at"] > datetime.now()
    
    # Test session validation
    assert auth_service.validate_session(session["session_id"]) == True
    
    # Test session expiration
    expired_session = auth_service.create_session("user_1", duration=timedelta(seconds=1))
    time.sleep(2)
    assert auth_service.validate_session(expired_session["session_id"]) == False

def test_user_management():
    auth_service = AuthService()
    
    # Create new user
    user_data = {
        "username": "new_user",
        "email": "new@example.com",
        "role": "user"
    }
    user = auth_service.create_user(user_data)
    assert user["username"] == "new_user"
    assert user["role"] == "user"
    
    # Update user
    updated_data = {"email": "updated@example.com"}
    updated_user = auth_service.update_user(user["id"], updated_data)
    assert updated_user["email"] == "updated@example.com"
    
    # Delete user
    auth_service.delete_user(user["id"])
    assert auth_service.get_user(user["id"]) is None

def test_permission_check():
    auth_service = AuthService()
    
    # Test admin permissions
    admin = auth_service.get_user("user_1")
    assert auth_service.check_permission(admin["id"], "manage_users") == True
    
    # Test user permissions
    user = auth_service.get_user("user_2")
    assert auth_service.check_permission(user["id"], "manage_users") == False
    assert auth_service.check_permission(user["id"], "read") == True
```

## Test Execution Instructions

1. Setup Test Environment:
```bash
# Install requirements
pip install -r requirements.txt

# Set up test configuration
cp .env.example .env.test
```

2. Run Tests:
```bash
# Run all tests
python -m pytest tests/

# Run specific test category
python -m pytest tests/test_task_creation.py
python -m pytest tests/test_task_execution.py
```

3. Generate Test Report:
```bash
python -m pytest tests/ --html=report.html
```

## Sample Test Script

```python:tests/test_task_creation.py
import pytest
from services.agent_service import AgentService

def test_create_task():
    service = AgentService()
    task = service.create_task(
        "Analyze system logs",
        {"time_range": "24h"}
    )
    assert task is not None
    assert task["status"] == "pending"
    assert len(task["steps"]) > 0

def test_task_execution():
    service = AgentService()
    task = service.create_task(
        "Check CPU usage",
        {"threshold": 90}
    )
    result = service.execute_task(task["task_id"])
    assert result["status"] == "completed"
    assert all(step["status"] == "completed" for step in result["steps"])

def test_task_archiving():
    service = AgentService()
    task = service.create_task(
        "Test task",
        {}
    )
    service.archive_task(task["task_id"])
    history = service.get_task_history()
    assert any(t["task_id"] == task["task_id"] for t in history)
```

## Test Data Management

### Test Data Cleanup
```python
def cleanup_test_data():
    """Clean up test data files"""
    import os
    import json
    
    # Clean up active tasks
    if os.path.exists("active_tasks.json"):
        with open("active_tasks.json", "w") as f:
            json.dump([], f)
    
    # Clean up task history
    if os.path.exists("task_history.json"):
        with open("task_history.json", "w") as f:
            json.dump([], f)
```