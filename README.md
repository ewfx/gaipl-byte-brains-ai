# 🚀 Project Name
Integrated Platform Environment (IPE) - Agentic AI Solution
## 📌 Table of Contents
- [Introduction](#introduction)
- [Demo](#demo)
- [Inspiration](#inspiration)
- [What It Does](#what-it-does)
- [How We Built It](#how-we-built-it)
- [Challenges We Faced](#challenges-we-faced)
- [How to Run](#how-to-run)
- [Tech Stack](#tech-stack)
- [Documentation](#documentation)
- [Team](#team)
---

## Introduction

### Overview
The Integrated Platform Environment (IPE) is a Gen-AI enabled platform designed to enhance support operations within technology organizations. It combines intelligent task automation, log analysis, and knowledge management into a unified solution powered by OpenAI's capabilities.

## Demo 
📹 [Video Demo](artifacts/demo/ByteBrains_AI_IPE_Demo.mp4)  
🖼️ [Screenshots](artifacts/demo/ByteBrains_AI_IPE_Screenshots.pdf)

## Inspiration
Platform support teams face challenges due to the context switch between multiple tools for troubleshooting, running Ansible scripts, and reviewing telemetry and CI data. This random workflow increases resolution time and complexity. The project aims to create an integrated platform that consolidates these tasks, providing a unified interface for faster issue resolution, better visibility into system health, and improved operational efficiency.

## What It Does
### Core Components
- **AI-Powered Chat Interface**: Contextual support assistance using OpenAI
- **Real-time Telemetry Dashboard**: System metrics monitoring and visualization
- **Knowledge Base Management**: Vector-based search for documentation and articles
- **Automation Engine**: Automated response and remediation capabilities
- **Role-Based Access Control**: Secure access management with multiple user roles
- **AI-Powered Task Automation**: Intelligent task planning and execution using OpenAI
- **Task Management System**: Create, execute, and track automated tasks
- **Task History**: Comprehensive tracking of completed tasks and their results
- **Log Analysis**: AI-powered analysis of system logs and performance metrics
- **Anomaly Detection**: Automated detection of system anomalies and issues

### Salient Features of Key Components
#### Chat Interface
- AI-powered responses using OpenAI
- Context-aware assistance
- History tracking
- Knowledge base integration
- Real-time conversation management
- Multi-turn dialogue support

#### Telemetry Dashboard
- Real-time metrics visualization
- System health monitoring
- Configurable alerts
- Historical data analysis
- Performance trend tracking
- Resource utilization monitoring

#### Knowledge Base
- Vector-based similarity search
- Document management
- Category organization
- Tag-based filtering
- Content versioning
- Search history tracking

#### Automation Engine
- Automated incident response
- Health check automation
- Alert management
- Task scheduling
- Workflow automation
- Event-driven actions

#### Task Automation
- AI-powered task planning
- Step-by-step execution
- Status tracking and updates
- Result collection and storage

#### Log Analysis
- System log analysis
- Performance metrics tracking
- Anomaly detection
- Insight generation
- Pattern recognition
- Root cause analysis

#### Data Storage
- JSON-based task storage
- Persistent task history
- Active task management
- Execution results tracking
- Data versioning
- Backup and recovery


### Technical Features
- Vector similarity search using ChromaDB
- JWT-based authentication
- Real-time data processing
- Configurable alerting system
- Automated health checks
- Comprehensive logging system
- OpenAI integration for intelligent task planning and execution
- JSON-based task storage and history
- Real-time task status tracking
- Automated task archiving
- Step-by-step task execution with status tracking
- Secure API integration

### Task Management
1. **Creating Tasks**
   - Go to the "Agent Tasks" tab
   - Fill in task description and context
   - Click "Create Task"

2. **Executing Tasks**
   - View active tasks
   - Click "Execute Task" for the desired task
   - Monitor task progress and results

3. **Viewing History**
   - Access completed tasks in the "Task History" tab
   - View detailed execution results and timestamps



## How We Built It
Briefly outline the technologies, frameworks, and tools used in development.

### Technologies Used
Python, Open AI Turbo 3.5 LLM, Streamlit, Git, Chroma DB

### Tools Used
PyCharm CE

#### 🏗️ Project Structure
```
code/   
├── src/
│   └── app.py             # Application entry point
│   ├── components/        # UI components
│   │   ├── automation_panel.py
│   │   └── chat_interface.py
│   │   └── cmdb_viewer.py
│   │   └── incident_manager.py
│   │   └── knowledge_base.py
│   │   └── log_analyzer.py
│   │   └── recommendation_dashboard.py
│   │   └── sidebar.py
│   │   └── telemetry_dashboard.py
│   │   └── ticket_analyzer.py
│   ├── config/            # Configuration files
│   │   └── config.py
│   │   └── ipe_config.py
│   ├── scripts/           # To initialize and Load Datsets
│   │   ├── initialize_vectordb.py
│   │   └── load_datasets.py
│   │   └── test_datasets.py    
│   ├── services/          # Service implementations
│   │   ├── agent_service.py
│   │   └── data_service.py
│   │   └── dataset_loader.py
│   │   └── ipe_service.py
│   │   └── log_service.py
│   │   └── openai_service.py
│   │   └── recommendation_service.py
│   │   └── ticket_analysis_service.py
│   │   └── vector_store.py
│   ├── utils/             # Utility functions
│   │   ├── alerts_service.py
│   │   ├── ansible_service.py
│   │   ├── auth.py
│   │   ├── context_engine.py
│   │   ├── health_check_service.py
│   │   ├── jwt_auth.py
│   │   ├── kb_service.py
│   │   ├── log_service.py
│   │   ├── openai_service.py
│   │   ├── sample_data_generator.py
│   │   ├── session_state.py
│   │   └── telemetry_service.py
├── logs/                  # Application logs
└── test/                  # Test cases folder
│   └── test_cases.md      # Test cases and scenarios
├── task_history.json      # Task history storage
├── requirements.txt       # Requirements file to install python dependencies
artifcats/                 # Documentation Artifacts
└── docs/                  # Documentation
│   └── markdown.md        # System integration documentation
├── arch/
│   └── system_architecture.md  # Detailed system architecture
├── demo/    
│   └── ByteBrain_AI_IPE.pptx                 # PPT of the project
│   └── ByteBrain_AI_IPE.pdf                  # PDF version of PPT
│   └── ByteBrains_AI_IPE_Demo.mp4            # Demo Video of the Application
│   └── ByteBrains_AI_IPE_Screenshots.pdf     # Demo Video of the Application
├── LICENSE                # License file(Generated)
└── README.md              # Readme file for the Application
```

### 🔒 Security Features
- JWT-based authentication
- Role-based access control (ADMIN, SUPPORT, VIEWER)
- Secure token refresh mechanism
- API rate limiting
- Input validation and sanitization

## Challenges We Faced
### Dataset preparation
One of the main challenge was generating the dataset for the scenarios handled by platform support and integrating various data sources, such as telemetry, CI data, and knowledge base articles, into one platform while keeping the data consistent and up to date. 
### Using the LLM to solve the problem
One challenge we faced while using Open API Turbo 3.5 LLM model to solve this problem was ensuring the accuracy and relevance of the responses generated. Since the platform support environment involves complex and dynamic data from telemetry, CI relationships, and knowledge bases, the LLM sometimes produced incomplete or contextually incorrect suggestions. Fine-tuning the model with domain-specific data and improving prompt engineering were necessary to enhance the model’s performance.

## How to Run

### 🛠️ Installation

#### Manual Installation
```bash
# Clone the repository
git clone https://github.com/your-repo/ipe.git
cd ipe

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Start the application
python src/main.py
```

### ⚙️ Configuration

#### Environment Variables
```env
# API Keys
OPENAI_API_KEY=your-api-key-here

# Logging
LOG_LEVEL=INFO
LOG_FILE_PATH=./logs/ipe.log

# Server
PORT=8501
HOST=0.0.0.0

# Security
JWT_SECRET_KEY=your-jwt-secret
JWT_EXPIRATION_HOURS=24
```

### Starting the Application
```bash
streamlit run src/app.py
```

### Accessing the Interface
- Main application: http://localhost:8501

### Default Credentials
```
Admin User:
- Username: admin
- Password: admin123

Support User:
- Username: support
- Password: support123

Viewer:
- Username: viewer
- Password: viewer123
```

### 🧪 Testing
```bash
# Run all tests
pytest

# Run specific test category
pytest tests/test_task_creation.py
pytest tests/test_task_execution.py
pytest tests/test_task_history.py
pytest tests/test_log_analysis.py
pytest tests/test_data_persistence.py
```

### 📊 Sample Data
The application includes sample data for testing:
- Task templates and examples
- Log analysis datasets
- System performance metrics
- Task execution results
- Historical task data

### 🔧 Troubleshooting

#### Common Issues
1. **Vector DB Connection Issues**
   - Verify ChromaDB is running
   - Check connection settings
   - Validate database credentials
   - Ensure proper network access
   - Check database health status

2. **OpenAI API Errors**
   - Validate API key
   - Check rate limits
   - Verify network connectivity
   - Ensure proper API permissions
   - Monitor API usage quotas

3. **Authentication Issues**
   - Clear browser cache
   - Verify JWT settings
   - Check user permissions
   - Validate token expiration
   - Ensure proper role assignments

4. **Task Execution Issues**
   - Check task status
   - Review execution logs
   - Verify task parameters
   - Monitor resource usage
   - Check task dependencies

5. **Data Storage Issues**
   - Verify file permissions
   - Check disk space
   - Validate JSON format
   - Monitor file system health
   - Ensure backup integrity

### 📝 Contributing
1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to the branch
5. Create a Pull Request
   ```

## Tech Stack
- 🔹 Frontend: Streamlit Python Library
- 🔹 Backend: Python
- 🔹 Database: Chroma DB
- 🔹 LLM Model: OpenAI API Turbo 3.5

## Documentation

### System Integration Documentation - [artifacts/docs/markdown.md](artifacts/docs/markdown.md)
- Integration points and data flow
- API configurations and endpoints
- Data schemas and formats
- Error handling strategies
- Performance considerations
- Security implementations

### System Architecture - [artifacts/arch/system_architecture.md](artifacts/arch/system_architecture.md)
- Core components and services
- Data flow architecture
- Service layer implementation
- Data loading and initialization
- Sample data generation
- Error handling
- Performance optimization
- OpenAI integration details

### Test Cases - [code/test/test_cases.md](code/test/test_cases.md)
- Authentication tests
- Chat interface tests
- Telemetry dashboard tests
- Knowledge base tests
- Integration tests
- Performance tests
- Error handling tests
- Task management tests
- Log analysis tests
- Data persistence tests

## Team
- **Teammate 1** - Udayaramu Peethani
- **Teammate 2** - Rajiv Kumar
- **Teammate 3** - Venkata Aditya Vajapeyajula
- **Teammate 4** - Veerendranadh Valeti
- **Teammate 5** - Satyanarayana Pampana
