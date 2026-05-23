# Bob ICA Catalysts Hackathon Journey
## Travel Refund Uncertainty Estimation System

**Team:** Abhijit Joshi  
**Event:** Bob ICA Catalysts May 2026 Hackathon  
**Date:** May 21-23, 2026  
**Project:** AI-Powered Travel Refund Estimation with IBM ICA Integration

---

## Executive Summary

We built a complete Travel Refund Uncertainty Estimation System that uses Machine Learning to predict refund amounts with 95% confidence intervals during force majeure events. The system integrates with IBM Consulting Advantage (ICA) through MCP (Model Context Protocol) to provide an AI agent that customers can interact with naturally.

**Key Achievement:** Successfully integrated a full-stack ML application with IBM ICA's Agent Orchestration framework using MCP protocol.

---

## Step 1: Project Ideation and Planning with Bob

### What We Did:
Asked Bob (AI coding assistant) to help us create a comprehensive project report for our idea: "Travel Refund Uncertainty Estimation during Force Majeure Events"

### Process:
1. **Described the Problem:**
   - Travel companies struggle to estimate refunds during force majeure events (wars, pandemics, natural disasters)
   - Customers need transparent, data-driven refund estimates
   - Current process is manual and inconsistent

2. **Defined Requirements:**
   - ML-powered refund predictions
   - Uncertainty quantification (confidence intervals)
   - Real-time risk assessment
   - Historical data analysis
   - Multi-component booking support (flights, hotels, visas, insurance)

3. **Bob Generated Project Report:**
   - **Frontend:** React with Vite, SCSS styling, React Router
   - **Backend:** FastAPI (Python), RESTful API design
   - **Database:** SQLite for development, PostgreSQL-ready for production
   - **ML Models:** Random Forest and Gradient Boosting ensemble
   - **UI/UX:** Professional dashboard with charts and analytics
   - **Integration:** MCP server for IBM ICA connectivity

### Output:
- Complete project architecture document
- Technology stack definition
- API endpoint specifications
- Database schema design
- ML model requirements

**Time Taken:** 30 minutes

---

## Step 2: Building the Complete Project in Bob IDE

### What We Did:
Used Bob IDE (VS Code with AI assistance) to build the entire full-stack application from scratch.

### Process:

#### 2.1 Backend Development
1. **Created FastAPI Application:**
   - Set up project structure: `backend/` directory
   - Installed dependencies: FastAPI, SQLAlchemy, scikit-learn, pandas, numpy
   - Created `main.py` with 11 API endpoints

2. **Implemented Database Layer:**
   - Created SQLAlchemy models in `models/database.py`
   - Defined tables: Bookings, BookingComponents, RiskEvents, HistoricalRefunds, ProviderPolicies
   - Set up database initialization and session management

3. **Built ML Models:**
   - Created `services/refund_estimator.py`
   - Implemented Random Forest and Gradient Boosting models
   - Added confidence interval calculation using ensemble predictions
   - Trained models on synthetic historical data

4. **Created API Endpoints:**
   ```
   GET  /api/health - Health check
   GET  /api/bookings - List all bookings
   GET  /api/bookings/{id} - Get booking details
   POST /api/estimate-refund/{id} - Estimate refund with ML
   GET  /api/risk-events - Get global risk events
   GET  /api/risk-events/regional/{region} - Regional risk assessment
   GET  /api/statistics/refund-rates - Historical statistics
   GET  /api/provider-policies - Provider refund policies
   GET  /openapi.json - API documentation
   ```

5. **Generated Synthetic Data:**
   - Created `services/data_generator.py`
   - Generated 100+ bookings with realistic data
   - Created 50+ risk events across different regions
   - Generated 500+ historical refund records for ML training

#### 2.2 Frontend Development
1. **Set Up React Application:**
   - Created `frontend/` directory with Vite
   - Installed dependencies: React, React Router, Axios, Recharts
   - Set up SCSS for styling

2. **Built UI Components:**
   - **Dashboard:** Overview with key metrics and charts
   - **Booking List:** Searchable, filterable table of all bookings
   - **Booking Details:** Detailed view with component breakdown
   - **Refund Estimator:** Interactive form with ML predictions
   - **Risk Monitor:** Global and regional risk visualization
   - **Analytics:** Historical trends and statistics
   - **Refund Comparator:** Side-by-side scenario comparison

3. **Implemented Features:**
   - Real-time API integration
   - Interactive charts using Recharts
   - Responsive design
   - Professional color scheme
   - Loading states and error handling

#### 2.3 Testing and Refinement
1. Started backend: `python backend/main.py`
2. Started frontend: `npm run dev` in frontend directory
3. Tested all features end-to-end
4. Fixed bugs and improved UX

### Output:
- ✅ Fully functional backend API (11 endpoints)
- ✅ Beautiful React frontend (7 pages)
- ✅ Trained ML models with confidence intervals
- ✅ SQLite database with synthetic data
- ✅ Complete API documentation

**Time Taken:** 4-5 hours

---

## Step 3: Creating Context Graph in IBM ICA

### What We Did:
Created a comprehensive knowledge graph in IBM ICA's Context Studio with detailed schema documentation (812 lines) and API tool definitions (465 lines).

### Process:

#### Step 3.1: Create Context Schema (context_schema.yaml - 812 lines)
Built a complete YAML schema documenting the entire system:

**Key Sections:**
1. **System Architecture** (lines 10-18): Full-stack components
2. **Backend API** (lines 21-231): 11 endpoints with complete specs
3. **Database Schema** (lines 28-76): 6 tables with relationships
4. **Data Models** (lines 234-482): Request/response schemas with validation
5. **ML Models** (lines 523-573): Random Forest + Gradient Boosting with 95% CI
6. **Frontend** (lines 576-610): React pages and routing
7. **MCP Server** (lines 613-666): 11 tools with parameter schemas
8. **Business Rules** (lines 669-703): Refund calculation logic and risk assessment

#### Step 3.2: Create Bulk Import File (refund-api-bulk-import-v2.json - 465 lines)
Created JSON file with 11 REST API tool definitions for Context Forge:

**Tools Defined:**
1. **v2-create-booking**: POST /api/bookings - Create travel bookings
2. **v2-get-bookings**: GET /api/bookings - List all bookings with pagination
3. **v2-get-booking-details**: GET /api/bookings/{id} - Detailed booking info
4. **v2-estimate-refund**: POST /api/estimate-refund/{id} - ML-powered estimation
5. **v2-get-refund-estimates**: GET /api/estimates/{id} - Historical estimates
6. **v2-get-risk-events**: GET /api/risk-events - Global risk monitoring
7. **v2-get-regional-risk**: GET /api/risk-events/region/{region} - Regional assessment
8. **v2-get-historical-refunds**: GET /api/historical-refunds - Analytics data
9. **v2-get-refund-statistics**: GET /api/statistics/refund-rates - Aggregated metrics
10. **v2-get-provider-policies**: GET /api/providers - Provider policies
11. **v2-get-provider-policy**: GET /api/providers/{name} - Specific provider details

Each tool includes complete JSON Schema validation, headers, and descriptions.

#### Step 3.3: Access Context Studio
1. Logged into IBM Consulting Advantage platform
2. Navigated to **Context Studio** in left sidebar
3. Clicked **"Create New Context"**

#### Step 3.4: Upload Schema Files
1. Uploaded **context_schema.yaml** (812 lines)
   - Complete system architecture documentation
   - All data models and business rules
   - ML model specifications
   
2. Uploaded **refund-api-bulk-import-v2.json** (465 lines)
   - 11 REST API tool definitions
   - Complete input/output schemas
   - Ready for Context Forge integration

3. Context Studio parsed and validated both files

#### Step 3.5: Generate Knowledge Graph
Context Studio automatically generated knowledge graph:

**Nodes (80+):**
- Bookings: 53 sample travel bookings
- Components: 200+ (flights, hotels, visa, insurance)
- Risk Events: 50+ global force majeure events
- Customers: Names, emails, destinations
- Providers: 20+ airlines, hotels, insurance companies
- Policies: Provider-specific refund rules

**Relationships (179+):**
- Booking → Components (one-to-many)
- Booking → Customer (one-to-one)
- Component → Provider (many-to-one)
- Risk Event → Region (many-to-one)
- Historical Refund → Event Type (many-to-one)

**Entity Types:**
- Travel bookings with references
- Individual booking components
- Global and regional risk events
- Service providers and policies
- Historical refund data

### Output:
- ✅ **context_schema.yaml** - 812 lines of complete system documentation
- ✅ **refund-api-bulk-import-v2.json** - 465 lines with 11 API tool definitions
- ✅ Knowledge graph with 80+ nodes and 179+ relationships
- ✅ Context available for agent queries
- ✅ Structured data about refunds, ML models, and business rules
- ✅ Ready for Context Forge and Agent Orchestration

**Key Achievement:** Created comprehensive context enabling AI agents to understand complete API structure, data models, ML capabilities, business logic, and force majeure handling.

**Time Taken:** 2 hours (including schema creation and validation)

---

## Step 4: Creating MCP Server

### What We Did:
Implemented a Model Context Protocol (MCP) server to expose our API as tools that AI agents can use.

### Process:

#### Step 4.1: Understand MCP Protocol
- MCP is a protocol for connecting AI agents to external tools
- Uses JSON-RPC 2.0 for communication
- Supports tool discovery, calling, and result handling

#### Step 4.2: Create MCP Endpoint
1. Created `backend/mcp_endpoint_simple.py`
2. Defined 7 tools matching our API endpoints:
   ```python
   TOOLS = [
       {
           "name": "get_bookings",
           "description": "Retrieve all travel bookings",
           "inputSchema": {...}
       },
       {
           "name": "get_booking_details",
           "description": "Get detailed booking information",
           "inputSchema": {
               "properties": {
                   "booking_id": {"type": "integer", "required": true}
               }
           }
       },
       {
           "name": "estimate_refund",
           "description": "Estimate refund with ML predictions",
           "inputSchema": {
               "properties": {
                   "booking_id": {"type": "integer"},
                   "severity": {"type": "string", "enum": ["low", "medium", "high"]},
                   "event_type": {"type": "string", "enum": ["war", "pandemic", ...]}
               }
           }
       },
       // ... 4 more tools
   ]
   ```

3. Implemented MCP request handlers:
   - `initialize` - Handshake with client
   - `tools/list` - Return available tools
   - `tools/call` - Execute tool and return results
   - `notifications/initialized` - Acknowledge initialization
   - `ping` - Health check

4. Added JSON-RPC 2.0 response formatting:
   ```python
   {
       "jsonrpc": "2.0",
       "id": request_id,
       "result": {...}
   }
   ```

#### Step 4.3: Integrate with FastAPI
1. Imported MCP router in `main.py`:
   ```python
   from mcp_endpoint_simple import router as mcp_router
   app.include_router(mcp_router)
   ```

2. MCP endpoint available at: `/mcp`

#### Step 4.4: Set Up Ngrok Tunnel
1. Installed ngrok: `choco install ngrok`
2. Started tunnel: `ngrok http 8000`
3. Got public URL: `https://famished-vertebrae-basil.ngrok-free.dev`
4. MCP endpoint accessible at: `https://famished-vertebrae-basil.ngrok-free.dev/mcp`

#### Step 4.5: Test MCP Server
1. Verified initialization request/response
2. Tested tools/list endpoint
3. Confirmed tool calling works
4. Checked JSON-RPC 2.0 compliance

### Output:
- ✅ MCP server with 7 tools
- ✅ JSON-RPC 2.0 compliant
- ✅ Public endpoint via ngrok
- ✅ All tools tested and working

**Time Taken:** 2 hours (including troubleshooting)

---

## Step 5: Creating Agent App in IBM ICA

### What We Did:
Created a simple AI assistant in IBM ICA that can interact with users about travel refunds.

### Process:

#### Step 5.1: Navigate to Agent Studio
1. Went to **Agent & Assistant Studio** in ICA
2. Clicked **"Create"** button
3. Selected **"Assistant"** type

#### Step 5.2: Configure Agent
1. **Name:** TravelRefundAdvisor

2. **Description:**
   ```
   AI-powered travel refund estimation assistant that helps customers 
   understand refund options during force majeure events using ML 
   predictions with 95% confidence intervals
   ```

3. **Instructions:**
   ```
   You are a professional travel refund estimation assistant.
   Help customers understand refund options during force majeure events.
   Be empathetic, clear, and data-driven in your responses.
   ```

4. **Welcome Message:**
   ```
   Hello! I'm your Travel Refund Estimation Assistant. I can help you 
   understand your refund options for travel bookings affected by force 
   majeure events. How can I assist you today?
   ```

#### Step 5.3: Initial Testing
1. Published the agent
2. Tested basic conversation
3. Found that agent couldn't access external tools yet
4. Realized we needed Agent Orchestration for tool integration

### Output:
- ✅ Basic agent created
- ✅ Conversational interface working
- ❌ No tool access yet (needed orchestration)

**Time Taken:** 30 minutes

---

## Step 6: Creating Orchestration Agent

### What We Did:
Created an Agent Orchestration using LangGraph and ReAct pattern to enable tool calling.

### Process:

#### Step 6.1: Access Agent Orchestration
1. Navigated to **Agent Orchestration** in ICA
2. Clicked **"Create Agent Orchestration"**
3. Selected configuration:
   - **Platform:** IBM Consulting Advantage
   - **Framework:** LangGraph
   - **Model:** gpt-5.2
   - **Pattern:** ReAct (Reasoning + Action)

#### Step 6.2: Configure Orchestration
1. **Used Chat Interface** to describe requirements:
   ```
   Create a travel refund estimation agent that uses MCP tools from 
   RefundEstimationAPI server to:
   1. Retrieve travel bookings
   2. Estimate refunds with ML predictions and 95% confidence intervals
   3. Assess global and regional risk events
   4. Provide historical refund statistics
   5. Explain provider refund policies
   ```

2. **Filled Configuration Fields:**
   - **What would you like to create?**
     ```
     A professional travel refund estimation assistant that helps 
     customers understand refund options during force majeure events 
     using ML predictions with 95% confidence intervals
     ```

   - **Name:** RefundEstimator

   - **Summary:**
     ```
     A professional assistant that estimates travel refunds during 
     force majeure events using machine learning with 95% confidence 
     intervals
     ```

   - **Instructions:**
     ```
     Provide users with clear, data-driven refund estimations by 
     analyzing trip details, force majeure conditions, and ML-based 
     predictions while presenting results with 95% confidence intervals 
     and transparent explanations
     ```

   - **Welcome Message:**
     ```
     Hello, I'm here to help you estimate potential travel refunds 
     during force majeure events using predictive modeling. How can 
     I assist you today?
     ```

#### Step 6.3: Add Tools
1. Scrolled to **"Tools (Optional)"** section
2. Clicked **"Add tools"** button
3. Selected all 7 tools from RefundEstimationAPI:
   - ✅ Get Bookings
   - ✅ Get Booking Details
   - ✅ Estimate Refund
   - ✅ Get Risk Events
   - ✅ Get Regional Risk
   - ✅ Get Refund Statistics
   - ✅ Get Provider Policies

4. All tools showed green checkmarks (active status)

#### Step 6.4: Publish Agent
1. Reviewed all configuration
2. Clicked **"Publish"** button
3. Waited for deployment (30 seconds)
4. Agent became available for testing

### Output:
- ✅ LangGraph ReAct agent created
- ✅ All 7 MCP tools integrated
- ✅ Agent deployed and ready
- ✅ Tool calling enabled

**Time Taken:** 1 hour

---

## Step 7: Linking Agent to MCP Server

### What We Did:
Connected the Agent Orchestration to our MCP server so the agent could actually call our API tools.

### Process:

#### Step 7.1: Register External MCP Server
1. Went to **Tools** section in ICA
2. Clicked **"Add New"** → **"Add External MCP Server"**
3. Filled in server details:
   - **Name:** RefundEstimationAPI
   - **URL:** `https://famished-vertebrae-basil.ngrok-free.dev/mcp`
   - **Tile Summary:** AI-powered travel refund estimation with confidence intervals
   - **Description:** Complete set of tools for travel refund estimation
   - **Transport Type:** STREAMABLE HTTP
   - **Authentication:** None
   - **Visibility:** Team (with Partners checked)

4. Clicked **"Add"** button
5. ICA connected to MCP server and discovered 7 tools

#### Step 7.2: Verify Tool Discovery
1. Checked terminal logs:
   ```
   [MCP] Received request: {"method": "initialize", ...}
   [MCP] Sending response: {...}
   [MCP] Received request: {"method": "tools/list", ...}
   [MCP] Sending tools list
   ```

2. Confirmed all 7 tools were discovered
3. Verified tools showed in "Available Tools" list

#### Step 7.3: Associate Tools with Agent
1. Went back to Agent Orchestration
2. In the agent creation form, tools were now available
3. Selected all 7 tools from RefundEstimationAPI
4. Tools appeared with green checkmarks
5. Published the agent with tools

#### Step 7.4: Test Integration
1. Opened agent chat interface
2. Sent test message: "Show me all my travel bookings"
3. Watched terminal for MCP calls:
   ```
   [MCP] Received request: {
     "method": "tools/call",
     "params": {
       "name": "get_bookings",
       "arguments": {}
     }
   }
   [MCP] Calling tool: get_bookings with args: {}
   INFO: GET /api/bookings HTTP/1.1 200 OK
   ```

4. Agent successfully retrieved and displayed bookings!

### Output:
- ✅ MCP server registered in ICA
- ✅ 7 tools discovered and available
- ✅ Tools linked to agent
- ✅ End-to-end integration working
- ✅ Agent calling tools successfully

**Time Taken:** 2 hours (including troubleshooting visibility and registry issues)

---

## Step 8: Demo Preparation and Testing

### What We Did:
Prepared comprehensive demo scenarios and tested all functionality.

### Process:

#### Step 8.1: Create Test Scenarios
1. Developed 10 demo prompts covering all features:
   - Basic booking queries
   - Detailed booking information
   - Refund estimation with confidence intervals
   - Severity comparison
   - Global risk assessment
   - Regional risk checks
   - Historical statistics
   - Provider policy comparison
   - Multi-component analysis
   - AI explainability

2. Created `DEMO_VIDEO_PROMPTS.md` with:
   - Exact prompts to use
   - Expected responses
   - What to highlight
   - 10-minute timeline
   - Recording tips

#### Step 8.2: Test All Prompts
1. **Prompt 1:** "Show me all my travel bookings"
   - ✅ Agent called get_bookings tool
   - ✅ Displayed 53 active bookings
   - ✅ Showed IDs, destinations, dates, costs

2. **Prompt 2:** "Show me details for booking 51"
   - ✅ Agent called get_booking_details
   - ✅ Displayed complete breakdown
   - ✅ Listed all components

3. **Prompt 3:** "Estimate refund for booking 51 with high severity due to natural disaster"
   - ✅ Agent called estimate_refund tool
   - ✅ Showed ML prediction: ~$76,500
   - ✅ Displayed 95% CI: $68,850 to $84,150
   - ✅ Presented three scenarios
   - ✅ Showed risk score

4. **Prompts 4-10:** All tested successfully
   - ✅ Risk assessment working
   - ✅ Statistics retrieval working
   - ✅ Policy comparison working
   - ✅ AI explanations clear

#### Step 8.3: Verify Terminal Logs
Confirmed MCP tool calls in terminal:
```
[MCP] Calling tool: get_bookings
[MCP] Calling tool: get_booking_details
[MCP] Calling tool: estimate_refund
[MCP] Calling tool: get_risk_events
[MCP] Calling tool: get_regional_risk
[MCP] Calling tool: get_refund_statistics
[MCP] Calling tool: get_provider_policies
```

All returning 200 OK responses!

#### Step 8.4: Create Documentation
1. **HACKATHON_TEST_PROMPTS.docx** - 10 test scenarios with expected results
2. **DEMO_VIDEO_PROMPTS.md** - Complete demo script with timeline
3. **PROJECT_SUMMARY.md** - Technical overview
4. **CURRENT_STATUS.md** - System status and capabilities

### Output:
- ✅ 10 tested demo prompts
- ✅ All features working
- ✅ Complete documentation
- ✅ Demo script ready
- ✅ Recording plan prepared

**Time Taken:** 1.5 hours

---

## Technical Architecture

### System Components:

```
┌─────────────────────────────────────────────────────────────┐
│                     IBM ICA Platform                         │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Agent Orchestration (LangGraph + ReAct)               │ │
│  │  - gpt-5.2 model                                       │ │
│  │  - 7 MCP tools integrated                              │ │
│  └────────────────────────────────────────────────────────┘ │
│                           │                                  │
│                           │ JSON-RPC 2.0                     │
│                           ▼                                  │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  MCP Server (External)                                 │ │
│  │  - Tool discovery                                      │ │
│  │  - Tool calling                                        │ │
│  │  - Result formatting                                   │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                           │
                           │ HTTPS (ngrok)
                           ▼
┌─────────────────────────────────────────────────────────────┐
│              Local Development Environment                   │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  FastAPI Backend (Python)                              │ │
│  │  - 11 REST API endpoints                               │ │
│  │  - MCP endpoint at /mcp                                │ │
│  │  - ML models (Random Forest + Gradient Boosting)      │ │
│  │  - SQLite database                                     │ │
│  └────────────────────────────────────────────────────────┘ │
│                           │                                  │
│                           │ HTTP                             │
│                           ▼                                  │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  React Frontend (Vite)                                 │ │
│  │  - 7 pages (Dashboard, Bookings, Analytics, etc.)     │ │
│  │  - Interactive charts                                  │ │
│  │  - Real-time API integration                           │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### Technology Stack:

**Frontend:**
- React 18
- Vite
- React Router
- Axios
- Recharts
- SCSS

**Backend:**
- Python 3.11
- FastAPI
- SQLAlchemy
- scikit-learn
- pandas, numpy

**ML Models:**
- Random Forest Regressor
- Gradient Boosting Regressor
- Ensemble predictions
- Confidence interval calculation

**Database:**
- SQLite (development)
- PostgreSQL-ready schema

**Integration:**
- MCP (Model Context Protocol)
- JSON-RPC 2.0
- ngrok for public access
- IBM ICA Agent Orchestration

---

## Key Achievements

### Technical Excellence:
1. ✅ **Full-Stack Application** - Complete React + FastAPI system
2. ✅ **ML Sophistication** - Ensemble models with confidence intervals
3. ✅ **MCP Integration** - Successfully implemented MCP protocol
4. ✅ **IBM ICA Integration** - Agent Orchestration with LangGraph
5. ✅ **Production Quality** - Error handling, logging, documentation

### Innovation:
1. ✅ **Uncertainty Quantification** - 95% confidence intervals, not just predictions
2. ✅ **Force Majeure Handling** - Specialized for exceptional events
3. ✅ **Multi-Component Analysis** - Granular refund breakdown
4. ✅ **AI Transparency** - Explainable predictions
5. ✅ **Enterprise Integration** - IBM ICA agent orchestration

### Business Value:
1. ✅ **Reduces Customer Service Load** - Instant automated estimates
2. ✅ **Improves Customer Satisfaction** - Transparent, data-driven answers
3. ✅ **Risk Management** - Real-time global and regional monitoring
4. ✅ **Data-Driven Decisions** - Historical statistics inform estimates
5. ✅ **Scalable Architecture** - API-first design, production-ready

---

## Challenges Overcome

### Challenge 1: MCP Protocol Implementation
**Problem:** MCP protocol documentation was limited, FastMCP library had compatibility issues with FastAPI.

**Solution:** 
- Implemented custom MCP endpoint using native FastAPI
- Used JSON-RPC 2.0 specification directly
- Added comprehensive logging for debugging
- Tested with ICA's MCP client to ensure compatibility

### Challenge 2: ICA Tool Registry
**Problem:** External MCP Server wasn't appearing in Agent Orchestration's tool registry.

**Solution:**
- Discovered separate registries for External MCP Servers vs. Agent Orchestration
- Registered MCP server specifically for Agent Orchestration
- Set proper visibility (Team vs. Private)
- Linked tools to agent during creation

### Challenge 3: Confidence Interval Calculation
**Problem:** Single model predictions don't provide uncertainty estimates.

**Solution:**
- Implemented ensemble of Random Forest and Gradient Boosting
- Used prediction variance across models
- Calculated 95% confidence intervals
- Provided best/worst/likely scenarios

### Challenge 4: Unicode Encoding in Windows
**Problem:** Emoji characters in print statements caused crashes on Windows.

**Solution:**
- Replaced Unicode emojis with ASCII text markers
- Set UTF-8 encoding for console output
- Used platform-agnostic logging

---

## Demo Script

### Introduction (30 seconds)
"Welcome to the Travel Refund Uncertainty Estimation System. This AI-powered assistant helps customers understand refund options during force majeure events using Machine Learning predictions with 95% confidence intervals. The system is fully integrated with IBM Consulting Advantage through the Model Context Protocol."

### Demo Flow (9 minutes)

**1. Basic Functionality (1 minute)**
- Prompt: "Show me all my travel bookings"
- Highlight: Agent calls MCP tool, retrieves 53 bookings
- Show: Terminal logs with MCP tool calls

**2. Core Feature - ML Predictions (2.5 minutes)**
- Prompt: "Estimate refund for booking 51 with high severity due to natural disaster"
- Highlight: 
  - ML prediction: $76,500
  - 95% confidence interval: $68,850 to $84,150
  - Three scenarios: best ($85,000), likely ($76,500), worst ($68,000)
  - Risk score and component breakdown
- Emphasize: This is not just a prediction, but uncertainty quantification

**3. Scenario Analysis (1 minute)**
- Prompt: "What if I cancel with medium severity instead?"
- Highlight: Different estimates based on severity
- Show: How ML adapts to different scenarios

**4. Risk Assessment (1.5 minutes)**
- Prompt: "What are current global risk events?"
- Prompt: "What's the risk level for Ukraine?"
- Highlight: Real-time risk monitoring, regional assessment

**5. Data Insights (1.5 minutes)**
- Prompt: "Show historical refund statistics for flights during pandemics"
- Prompt: "What are refund policies for different providers?"
- Highlight: Data-driven insights, policy comparison

**6. AI Transparency (1.5 minutes)**
- Prompt: "Explain what the 95% confidence interval means"
- Highlight: AI explainability, responsible AI practices
- Emphasize: Customer-friendly explanations

### Closing (30 seconds)
"This system demonstrates how AI can provide transparent, data-driven solutions for complex business problems. By combining ML predictions with confidence intervals, real-time risk assessment, and enterprise integration through IBM ICA, we've created a production-ready system that can transform how travel companies handle refunds during force majeure events."

---

## Results and Impact

### Quantitative Results:
- **11 API endpoints** - All functional
- **7 MCP tools** - Successfully integrated
- **95% confidence intervals** - Uncertainty quantification
- **53 sample bookings** - Realistic test data
- **500+ historical records** - ML training data
- **100% success rate** - All demo prompts working

### Qualitative Impact:
- **Customer Experience:** Instant, transparent refund estimates
- **Business Efficiency:** Automated process vs. manual review
- **Risk Management:** Real-time global and regional monitoring
- **AI Transparency:** Explainable predictions build trust
- **Enterprise Ready:** IBM ICA integration for production deployment

---

## Future Enhancements

### Short Term:
1. Add more ML models (XGBoost, Neural Networks)
2. Implement real-time data feeds for risk events
3. Add multi-language support
4. Create mobile app interface

### Long Term:
1. Integrate with actual travel booking systems
2. Add payment processing for refunds
3. Implement blockchain for transparent audit trail
4. Scale to handle millions of bookings
5. Add predictive analytics for future risk events

---

## Conclusion

We successfully built a complete Travel Refund Uncertainty Estimation System from ideation to deployment in 48 hours. The system demonstrates:

1. **Technical Excellence:** Full-stack development with ML and enterprise integration
2. **Innovation:** Uncertainty quantification and AI transparency
3. **Business Value:** Solves real problem in travel industry
4. **Production Quality:** Professional code, documentation, and testing

The integration with IBM ICA through MCP protocol showcases how modern AI agents can be connected to specialized business applications, creating powerful, transparent, and user-friendly solutions.

**This project represents the future of AI-powered business applications: intelligent, explainable, and seamlessly integrated.**

---

## Appendix: Key Files and Documentation

### Code Files:
- `backend/main.py` - FastAPI application
- `backend/mcp_endpoint_simple.py` - MCP server implementation
- `backend/services/refund_estimator.py` - ML models
- `frontend/src/` - React application

### Documentation:
- `HACKATHON_TEST_PROMPTS.docx` - Test scenarios
- `DEMO_VIDEO_PROMPTS.md` - Demo script
- `PROJECT_SUMMARY.md` - Technical overview
- `COMPLETE_ICA_ORCHESTRATION_SETUP.md` - Integration guide

### Configuration:
- `backend/requirements.txt` - Python dependencies
- `frontend/package.json` - Node dependencies
- `context_schema.yaml` - Context graph schema

---

**Project Completed:** May 23, 2026  
**Total Development Time:** ~12 hours  
**Status:** ✅ Fully Functional and Demo-Ready

**Team:** Abhijit Joshi  
**Event:** Bob ICA Catalysts May 2026 Hackathon  
**Achievement:** Complete AI-powered system with IBM ICA integration