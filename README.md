# Travel Refund Uncertainty Estimation System

AI-Powered Refund Prediction for Force Majeure Events

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.9+-green.svg)
![React](https://img.shields.io/badge/react-18.2-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
## 🔗 Repository

**GitHub**: `https://github.com/abhijitjoshi140377/Uncertainty_Refund`

Clone this repository:
```bash
git clone https://github.com/abhijitjoshi140377/Uncertainty_Refund.git
cd Uncertainty_Refund
```


## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [System Architecture](#system-architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Testing](#testing)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Usage Guide](#usage-guide)
- [Test Cases](#test-cases)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [MCP Server for IBM ICA Agents](#-mcp-server-for-ibm-ica-agents)
- [ICA-MCP Context Forge Bulk Import](#ica-mcp-context-forge-bulk-import)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

The Travel Refund Uncertainty Estimation System is an innovative AI-powered platform that predicts expected refund amounts for travel bookings cancelled due to force majeure events (wars, natural disasters, pandemics, etc.). The system provides probabilistic refund predictions with confidence intervals, enabling travelers to make informed decisions.

### Key Highlights

- **First-of-its-kind** probabilistic refund prediction system
- **Multi-component analysis** (flights, hotels, visas, insurance)
- **Real-time integration** with global risk indicators
- **Machine learning-based** forecasting with historical data
- **AI Agent Integration** via MCP server for conversational AI access
- **Modern responsive design** for professional UI/UX

## ✨ Features

### Core Features

1. **Refund Estimation Engine**
   - ML-powered refund prediction
   - Confidence interval calculation
   - Scenario analysis (best/worst/expected case)
   - Multi-component aggregation

2. **Risk Monitoring**
   - Real-time global risk event tracking
   - Severity-based classification
   - Regional risk assessment
   - Force majeure event detection

3. **Booking Management**
   - Create and manage travel bookings
   - Multi-component booking support
   - Booking history and tracking
   - Status management

4. **Analytics Dashboard**
   - Historical refund statistics
   - Component-wise analysis
   - Event-type based insights

5. **MCP Server (AI Agent Integration)**
   - Model Context Protocol server for AI agents
   - 11 tools for booking and refund operations
   - Compatible with Claude, GPT, and custom AI systems
   - Real-time API access for conversational agents
   - Visual data representation

## 🛠 Technology Stack

### Backend
- **Framework**: FastAPI 0.109.0
- **Database**: SQLite with SQLAlchemy ORM
- **ML Libraries**: scikit-learn, NumPy, Pandas
- **Python**: 3.9+

### Frontend
- **Framework**: React 18.2
- **UI Library**: Custom React Components
- **Build Tool**: Vite 5.0
- **Charts**: Recharts 2.10
- **Routing**: React Router 6.20
- **HTTP Client**: Axios 1.6

### MCP Server (AI Agent Integration)
- **Protocol**: Model Context Protocol (MCP)
- **Purpose**: Expose API endpoints to ICA agents (Claude, GPT, etc.)
- **Tools**: 11 AI-accessible tools for booking and refund estimation
- **Integration**: Compatible with Claude Desktop, Cline, and custom AI agents

### Development Tools
- **Testing**: pytest, React Testing Library
- **Code Quality**: ESLint
- **Package Management**: pip, npm

## 🏗 System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (React + Carbon)                │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │Dashboard │  │ Bookings │  │   Risk   │  │Analytics │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    API Layer (FastAPI)                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │ Booking  │  │Estimation│  │   Risk   │  │Historical│   │
│  │   API    │  │   API    │  │   API    │  │   API    │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   Business Logic Layer                       │
│  ┌──────────────────┐         ┌──────────────────┐         │
│  │ Refund Estimator │         │  Data Generator  │         │
│  │  (ML Engine)     │         │  (Synthetic Data)│         │
│  └──────────────────┘         └──────────────────┘         │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    Data Layer (SQLite)                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │ Bookings │  │Historical│  │   Risk   │  │ Provider │   │
│  │          │  │ Refunds  │  │  Events  │  │ Policies │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.9 or higher**
  - Download from [python.org](https://www.python.org/downloads/)
  - Verify: `python --version`

- **Node.js 16.0 or higher**
  - Download from [nodejs.org](https://nodejs.org/)
  - Verify: `node --version`

- **npm 8.0 or higher**
  - Comes with Node.js
  - Verify: `npm --version`

- **Git** (optional, for cloning)
  - Download from [git-scm.com](https://git-scm.com/)

## 🚀 Installation

### Step 1: Clone or Download the Repository

```bash
# Clone the repository
git clone https://github.com/abhijitjoshi140377/Uncertainty_Refund.git
cd Uncertainty_Refund

# Or if you downloaded as ZIP, extract and navigate to the directory
cd path/to/Uncertainty_Refund
```

### Step 2: Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Frontend Setup

```bash
# Navigate to frontend directory (from project root)
cd frontend

# Install dependencies
npm install
```

## 🎮 Running the Application

### Option 1: Run Both Services Separately

#### Terminal 1 - Backend Server

```bash
# From project root
cd backend

# Activate virtual environment if not already activated
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# Run the backend server
python main.py
```

The backend API will start at: **http://localhost:8000**
- API Documentation: http://localhost:8000/api/docs
- Alternative Docs: http://localhost:8000/api/redoc

#### Terminal 2 - Frontend Development Server

```bash
# From project root
cd frontend

# Run the frontend development server
npm run dev
```

The frontend application will start at: **http://localhost:3000**

### Option 2: Using PowerShell Script (Windows)

Create a file `start.ps1` in the project root:

```powershell
# Start backend
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; .\venv\Scripts\activate; python main.py"

# Wait a few seconds for backend to start
Start-Sleep -Seconds 5

# Start frontend
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; npm run dev"
```

Run: `.\start.ps1`

### Option 3: Using Batch Script (Windows)

Create a file `start.bat` in the project root:

```batch
@echo off
start cmd /k "cd backend && venv\Scripts\activate && python main.py"
timeout /t 5
start cmd /k "cd frontend && npm run dev"
```

Run: `start.bat`

## 🧪 Testing

### Backend Tests

```bash
cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_api.py

# Run with verbose output
pytest -v
```

### Frontend Tests (if implemented)

```bash
cd frontend

# Run tests
npm test

# Run with coverage
npm test -- --coverage
```

## 📚 API Documentation

### Base URL
```
http://localhost:8000/api
```

### Key Endpoints

#### Bookings

- **GET** `/bookings` - Get all bookings
- **GET** `/bookings/{id}` - Get booking by ID
- **POST** `/bookings` - Create new booking

#### Refund Estimation

- **POST** `/estimate-refund/{booking_id}` - Generate refund estimate
- **GET** `/estimates/{booking_id}` - Get all estimates for booking

#### Risk Events

- **GET** `/risk-events` - Get active risk events
- **GET** `/risk-events/region/{region}` - Get risks by region

#### Historical Data

- **GET** `/historical-refunds` - Get historical refund data
- **GET** `/statistics/refund-rates` - Get refund statistics

#### Provider Policies

- **GET** `/providers` - Get all provider policies
- **GET** `/providers/{provider_name}` - Get specific provider policy

### Interactive API Documentation

Visit http://localhost:8000/api/docs for interactive Swagger UI documentation.

## 📁 Project Structure

```
Uncertainty_Refund/
├── backend/
│   ├── main.py                 # FastAPI application entry point
│   ├── crud.py                 # Database CRUD operations
│   ├── schemas.py              # Pydantic models for validation
│   ├── requirements.txt        # Python dependencies
│   ├── models/
│   │   └── database.py         # SQLAlchemy database models
│   ├── services/
│   │   ├── __init__.py
│   │   ├── refund_estimator.py # ML-based refund estimation
│   │   └── data_generator.py   # Synthetic data generation
│   └── tests/
│       ├── __init__.py
│       └── test_api.py         # API endpoint tests
├── mcp_server/
│   ├── refund_mcp_server.py    # MCP server for AI agents
│   ├── requirements.txt        # MCP dependencies
│   ├── config.json             # MCP configuration
│   ├── example_usage.py        # Usage examples
│   ├── start_mcp_server.bat    # Windows startup script
│   ├── start_mcp_server.sh     # Unix startup script
│   └── README.md               # MCP server documentation
├── frontend/
│   ├── package.json            # Node.js dependencies
│   ├── vite.config.js          # Vite configuration
│   ├── index.html              # HTML entry point
│   ├── src/
│   │   ├── main.jsx            # React entry point
│   │   ├── App.jsx             # Main App component
│   │   ├── index.scss          # Global styles
│   │   ├── components/
│   │   │   └── Header.jsx      # Navigation header
│   │   ├── pages/
│   │   │   ├── Dashboard.jsx   # Dashboard page
│   │   │   ├── BookingList.jsx # Bookings list page
│   │   │   ├── CreateBooking.jsx # Create booking form
│   │   │   ├── BookingDetails.jsx # Booking details page
│   │   │   ├── RiskMonitor.jsx # Risk monitoring page
│   │   │   └── Analytics.jsx   # Analytics page
│   │   └── services/
│   │       └── api.js          # API client
│   └── public/                 # Static assets
├── README.md                   # This file
└── backend/
    └── refund_estimation.db    # SQLite database (auto-generated)
```

## 📖 Usage Guide

### 1. First Time Setup

When you first run the application:

1. **Backend automatically**:
   - Creates the SQLite database
   - Generates 500 historical refund records
   - Creates 50 sample bookings
   - Populates provider policies
   - Trains ML models

2. **Access the application**:
   - Open http://localhost:3000 in your browser
   - You'll see the dashboard with sample data

### 2. Creating a Booking

1. Click **"Create New Booking"** button
2. Fill in the form:
   - Customer name and email
   - Origin and destination cities
   - Travel date
   - Flight and hotel details
3. Click **"Create Booking"**
4. You'll be redirected to the booking details page

### 3. Generating Refund Estimate

1. Navigate to a booking details page
2. Click **"Generate Estimate"** button
3. The system will:
   - Analyze booking components
   - Check current risk levels
   - Apply ML models
   - Calculate confidence intervals
4. View the estimate with:
   - Expected refund amount
   - Confidence interval
   - Risk assessment
   - Scenario analysis

### 4. Monitoring Risks

1. Go to **Risk Monitor** page
2. View active global risk events
3. See severity levels and affected regions
4. Monitor force majeure situations

### 5. Viewing Analytics

1. Go to **Analytics** page
2. View historical refund statistics
3. Analyze trends by:
   - Component type (flight, hotel, visa, insurance)
   - Event type (war, pandemic, natural disaster)
   - Refund percentages

## 🧪 Test Cases

### Test Case 1: Create Booking
**Objective**: Verify booking creation functionality

**Steps**:
1. Navigate to http://localhost:3000/bookings/new
2. Enter customer details:
   - Name: "Test User"
   - Email: "test@example.com"
3. Enter travel details:
   - Origin: "Mumbai"
   - Destination: "Paris"
   - Travel Date: 60 days from today
4. Enter component costs:
   - Flight: ₹50,000
   - Hotel: ₹25,000
5. Click "Create Booking"

**Expected Result**:
- Booking created successfully
- Redirected to booking details page
- Total cost shows ₹75,000
- Booking reference generated

### Test Case 2: Generate Refund Estimate
**Objective**: Verify refund estimation functionality

**Steps**:
1. Open any booking details page
2. Click "Generate Estimate" button
3. Wait for processing

**Expected Result**:
- Estimate generated within 2-3 seconds
- Expected refund amount displayed
- Confidence interval shown (lower and upper bounds)
- Risk level indicated (low/medium/high/critical)
- Scenario analysis displayed (best/worst/most likely)
- All values are reasonable (0-100% refund)

### Test Case 3: View Risk Events
**Objective**: Verify risk monitoring functionality

**Steps**:
1. Navigate to http://localhost:3000/risk-monitor
2. View active risk events

**Expected Result**:
- List of active risk events displayed
- Each event shows:
  - Event type (war, pandemic, etc.)
  - Severity level with color coding
  - Affected region
  - Start date
  - Description

### Test Case 4: View Analytics
**Objective**: Verify analytics functionality

**Steps**:
1. Navigate to http://localhost:3000/analytics
2. View statistics and charts

**Expected Result**:
- Bar chart displays refund percentages
- Statistics cards show:
  - Component type
  - Event type
  - Average refund percentage
  - Total cases
  - Force majeure cases
- All data is properly formatted

### Test Case 5: API Health Check
**Objective**: Verify backend API is operational

**Steps**:
1. Open http://localhost:8000/api/health in browser

**Expected Result**:
```json
{
  "status": "healthy",
  "service": "refund-estimation-api",
  "timestamp": "2026-05-16T08:45:00Z"
}
```

### Test Case 6: ML Model Prediction
**Objective**: Verify ML model produces consistent results

**Steps**:
1. Create a booking with high-risk destination
2. Generate estimate twice
3. Compare results

**Expected Result**:
- Both estimates should be similar (within 10% variance)
- Risk score should be consistent
- Confidence intervals should overlap

## 🎯 Best Practices

### Code Quality

1. **Backend**:
   - Follow PEP 8 style guide
   - Use type hints
   - Write docstrings for functions
   - Keep functions small and focused
   - Use meaningful variable names

2. **Frontend**:
   - Follow React best practices
   - Use functional components with hooks
   - Keep components small and reusable
   - Use modern UI components
   - Implement proper error handling

### Security

1. **Input Validation**:
   - All inputs validated with Pydantic
   - SQL injection prevention via ORM
   - XSS prevention in React

2. **API Security**:
   - CORS configured properly
   - Rate limiting (can be added)
   - Authentication (can be added)

### Performance

1. **Backend**:
   - Database indexing on key fields
   - Efficient query design
   - Caching for ML predictions (can be added)

2. **Frontend**:
   - Code splitting with React Router
   - Lazy loading of components
   - Optimized re-renders

### Testing

1. **Unit Tests**:
   - Test individual functions
   - Mock external dependencies
   - Aim for >80% coverage

2. **Integration Tests**:
   - Test API endpoints
   - Test database operations
   - Test ML model predictions

## 🔧 Troubleshooting

### Backend Issues

**Issue**: `ModuleNotFoundError: No module named 'fastapi'`
**Solution**: 
```bash
cd backend
pip install -r requirements.txt
```

**Issue**: `Database is locked`
**Solution**: 
- Close all connections to the database
- Delete `refund_estimation.db` and restart

**Issue**: Port 8000 already in use
**Solution**:
```bash
# Find process using port 8000
netstat -ano | findstr :8000
# Kill the process
taskkill /PID <process_id> /F
```

### Frontend Issues

**Issue**: `npm ERR! code ENOENT`
**Solution**:
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

**Issue**: Port 3000 already in use
**Solution**: Vite will automatically use next available port (3001, 3002, etc.)

**Issue**: API calls failing with CORS error
**Solution**: Ensure backend is running and CORS is configured in `main.py`

### Common Issues

**Issue**: Synthetic data not generated
**Solution**: Delete `refund_estimation.db` and restart backend

**Issue**: ML models not training
**Solution**: Check if historical data exists in database

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)

## 🤖 MCP Server for IBM ICA Agents

The project includes a **production-ready** MCP (Model Context Protocol) server optimized for IBM ICA (Intelligent Conversational Agents) that exposes the refund estimation API to AI agents like Claude, GPT, and custom conversational systems.

### Production Features

✅ **Comprehensive Error Handling** - Structured error responses with error types
✅ **Request Timeouts** - 30-second timeout with automatic retry (3 attempts)
✅ **Structured JSON Responses** - Consistent success/error format
✅ **Logging & Monitoring** - Full request/response logging
✅ **Input Validation** - Schema-based parameter validation
✅ **Retry Logic** - Automatic retry on transient failures

### Quick Start

```bash
# Navigate to MCP server directory
cd mcp_server

# Install dependencies
pip install -r requirements.txt

# Start the production MCP server (ensure backend is running first)
python refund_mcp_server_production.py
```

### Available Tools for IBM ICA Agents

The MCP server provides **11 production-ready tools** with comprehensive documentation:

1. **create_booking** - Create travel bookings with validation
   - Full input schema with field validation
   - Email format validation
   - Component type enum validation
   - Returns booking reference and total cost

2. **get_bookings** - Retrieve all bookings with pagination
   - Skip/limit parameters (max 1000)
   - Returns total count and pagination metadata

3. **get_booking_details** - Get specific booking information
   - Validates booking ID
   - Returns complete booking with all components
   - 404 error if booking not found

4. **estimate_refund** - Generate AI-powered refund estimates
   - ML model selection (auto/random_forest/gradient_boosting/rule_based)
   - Calamity type and severity parameters
   - Returns confidence intervals and risk scores
   - Best/worst/most likely scenarios

5. **get_refund_estimates** - Get estimate history for a booking
   - Track estimates over time
   - Compare different scenarios

6. **get_risk_events** - Query global risk events
   - Filter by active status
   - Returns severity levels and affected regions

7. **get_regional_risk** - Check regional risk assessment
   - Aggregate risk level calculation
   - List of active events in region

8. **get_historical_refunds** - Access historical refund data
   - Filter by component type and event type
   - Limit parameter (max 1000 records)

9. **get_refund_statistics** - Get aggregated statistics
   - Grouped by component and event type
   - Average refund percentages and amounts

10. **get_provider_policies** - Query provider refund policies
    - Filter by provider type
    - Returns refund percentages and fees

11. **get_provider_policy** - Get specific provider details
    - Complete policy text
    - Force majeure clauses

### Response Format

**Success Response:**
```json
{
  "status": "success",
  "message": "Operation completed successfully",
  "data": { /* response data */ },
  "tool": "tool_name",
  "timestamp": "2026-05-20T10:00:00Z"
}
```

**Error Response:**
```json
{
  "status": "error",
  "error_type": "timeout|api_error|http_error|unexpected_error",
  "message": "Error description",
  "details": { /* additional error info */ },
  "tool": "tool_name",
  "timestamp": "2026-05-20T10:00:00Z"
}
```

### Integration with IBM ICA Systems

**Claude Desktop**: Add to `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "refund-estimation-production": {
      "command": "python",
      "args": ["path/to/mcp_server/refund_mcp_server_production.py"],
      "env": {
        "API_BASE_URL": "http://localhost:8000/api"
      }
    }
  }
}
```

**Cline (VS Code)**: Add to MCP settings:
```json
{
  "mcpServers": {
    "refund-estimation": {
      "command": "python",
      "args": ["C:/Users/AbhijitJoshi/Uncertainty_Refund/mcp_server/refund_mcp_server_production.py"]
    }
  }
}
```

### Configuration

**Environment Variables:**
- `API_BASE_URL` - FastAPI backend URL (default: http://localhost:8000/api)
- `REQUEST_TIMEOUT` - Request timeout in seconds (default: 30)
- `MAX_RETRIES` - Maximum retry attempts (default: 3)

**Logging:**
- All requests and responses are logged
- Error tracking with stack traces
- Performance monitoring

### Error Handling

The production MCP server handles:
- **Timeout errors** - Automatic retry with exponential backoff
- **HTTP 4xx errors** - Client errors (no retry)
- **HTTP 5xx errors** - Server errors (automatic retry)
- **Network errors** - Connection failures (automatic retry)
- **Validation errors** - Input schema validation
- **Unexpected errors** - Graceful error responses

### 🔌 Native MCP SSE Endpoint

The FastAPI backend now includes a **native MCP (Model Context Protocol) SSE endpoint** at `/mcp` that exposes all 11 API tools using the MCP protocol with Server-Sent Events transport.

#### Quick Start

```bash
# Backend already running on http://localhost:8000
# MCP endpoint automatically available at:
http://localhost:8000/mcp
```

#### Key Features

✅ **Native Integration** - Built directly into FastAPI backend
✅ **Real-Time Communication** - SSE transport for instant responses
✅ **11 Production Tools** - All API endpoints exposed as MCP tools
✅ **Structured Responses** - Consistent JSON format
✅ **No External Server** - No separate MCP server process needed
✅ **Ngrok Compatible** - Works with ngrok tunnels

#### MCP Server URLs

- **Local**: `http://localhost:8000/mcp`
- **Ngrok**: `https://famished-vertebrae-basil.ngrok-free.app/mcp`
- **Production**: `https://your-domain.com/mcp`

#### Configure AI Agent

**Claude Desktop** (`claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "refund-estimation-sse": {
      "url": "http://localhost:8000/mcp",
      "transport": "sse"
    }
  }
}
```

**Cline (VS Code)**:
```json
{
  "mcpServers": {
    "refund-estimation-sse": {
      "url": "http://localhost:8000/mcp",
      "transport": "sse"
    }
  }
}
```

#### Available via MCP

All 11 tools are accessible via the MCP protocol:
- create_booking, get_bookings, get_booking_details
- estimate_refund, get_refund_estimates
- get_risk_events, get_regional_risk
- get_historical_refunds, get_refund_statistics
- get_provider_policies, get_provider_policy

#### Comprehensive Guide

📖 **[MCP SSE Endpoint Integration Guide](MCP_SSE_ENDPOINT_GUIDE.md)**

This guide includes:
- Complete tool documentation with input schemas
- Response format examples
- AI agent configuration
- Ngrok setup instructions
- Testing procedures
- Production deployment checklist
- Troubleshooting guide

### ICA-MCP Context Forge Bulk Import

For IBM ICA users, we provide a **ready-to-import bulk configuration file** that allows you to import all 11 API endpoints as MCP tools in a single operation.

**File**: `refund-api-bulk-import.json`

#### Quick Import Steps

1. **Start Backend**: Ensure FastAPI backend is running on `http://localhost:8000`
2. **Access Context Forge**: Navigate to IBM ICA → Context Forge → "Add New Tool from REST API"
3. **Bulk Import**: Select "Bulk Import" and upload `refund-api-bulk-import.json`
4. **Review & Import**: Review the 11 tools and click "Import All"
5. **Test**: Use ICA's test interface to verify each tool

#### What's Included

The bulk import file includes complete configurations for all 11 endpoints:

✅ **create-booking** - Create travel bookings with validation
✅ **get-bookings** - List all bookings with pagination
✅ **get-booking-details** - Get specific booking information
✅ **estimate-refund** - AI-powered refund estimation
✅ **get-refund-estimates** - List refund estimate history
✅ **get-risk-events** - Query global risk events
✅ **get-regional-risk** - Regional risk assessment
✅ **get-historical-refunds** - Historical refund data
✅ **get-refund-statistics** - Aggregated statistics
✅ **get-provider-policies** - List provider policies
✅ **get-provider-policy** - Get specific provider details

#### Features

- **Complete Input Schemas** - Full validation with types, enums, and constraints
- **Detailed Descriptions** - AI-optimized tool descriptions with use cases
- **Response Filtering** - JSONPath filters for clean data extraction
- **Path Parameters** - Automatic substitution for URLs like `/bookings/{booking_id}`
- **Pagination Support** - Skip/limit parameters for large datasets
- **Error Handling** - Proper HTTP status codes and validation errors
- **Tags** - Organized by category (booking, refund, risk, analytics, provider)

#### Example AI Agent Prompts

Once imported, AI agents can use natural language:

```
User: "Create a booking for John Doe traveling to France from June 1-15, 2026"
Agent: [Uses create-booking tool with provided details]

User: "What's the refund estimate if there's a natural disaster?"
Agent: [Uses estimate-refund tool with high severity]

User: "Show me the risk level for Ukraine"
Agent: [Uses get-regional-risk tool]

User: "What's Air India's cancellation policy?"
Agent: [Uses get-provider-policy tool]
```

#### Production Deployment

For production, update the base URL in the bulk import file:

```bash
# Find and replace in refund-api-bulk-import.json
From: http://localhost:8000
To: https://api.yourcompany.com
```

#### Comprehensive Guide

For detailed instructions, configuration options, and troubleshooting:

📖 **[ICA-MCP Context Forge Integration Guide](ICA_MCP_CONTEXT_FORGE_GUIDE.md)**

This guide includes:
- Step-by-step import instructions
- Tool descriptions and use cases
- Input schema details
- Authentication configuration
- Response filtering with JSONPath
- Pagination examples
- Error handling
- Production deployment checklist
- Troubleshooting common issues

### For Detailed Documentation

- **MCP SSE Endpoint Guide**: [MCP_SSE_ENDPOINT_GUIDE.md](MCP_SSE_ENDPOINT_GUIDE.md) ⭐ **NEW**
- **ICA Context Forge Guide**: [ICA_MCP_CONTEXT_FORGE_GUIDE.md](ICA_MCP_CONTEXT_FORGE_GUIDE.md)
- **Bulk Import File**: [refund-api-bulk-import.json](refund-api-bulk-import.json)
- **MCP Server Guide**: [mcp_server/README.md](mcp_server/README.md)
- **API Enhancement Guide**: [backend/API_ENHANCEMENT_GUIDE.md](backend/API_ENHANCEMENT_GUIDE.md)
- **Context Schema**: [context_schema.yaml](context_schema.yaml)
- **MCP Endpoint Code**: [backend/mcp_endpoint.py](backend/mcp_endpoint.py) ⭐ **NEW**

5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 👥 Authors

- **IBM Development Team**
- **Project Lead**: Abhijit Joshi

## 🙏 Acknowledgments

- FastAPI Framework
- React Community
- scikit-learn Contributors
- Open Source Community

## 📞 Support

For support, please contact:
- Email: support@example.com
- Documentation: http://localhost:8000/api/docs

---

**Made with ❤️ using React and FastAPI**

**Version**: 1.0.0
**Last Updated**: May 18, 2026