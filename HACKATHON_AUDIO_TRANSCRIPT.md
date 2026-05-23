# Bob-a-thon Hackathon Audio Transcript
## Travel Refund Uncertainty Estimation System
**Duration: 4-5 minutes**

---

## [0:00 - 0:30] Introduction

Hello! I'm Abhijit Joshi, and I'm excited to present my Bob-a-thon hackathon project: the Travel Refund Uncertainty Estimation System. This is an AI-powered solution that helps travel companies and customers estimate refunds during force majeure events like wars, pandemics, and natural disasters, using machine learning with 95% confidence intervals.

---

## [0:30 - 1:15] The Problem and Solution

The travel industry faces a major challenge: estimating refunds during unexpected events is manual, inconsistent, and time-consuming. Customers are left uncertain about their refund amounts, and companies struggle with the complexity.

My solution combines machine learning, real-time risk assessment, and IBM Consulting Advantage integration to provide instant, transparent refund estimates. The system uses Random Forest and Gradient Boosting models to predict not just a single number, but a range with 95% confidence intervals, giving both best-case and worst-case scenarios.

---

## [1:15 - 2:00] The 8-Step Journey

I built this complete system in 48 hours through 8 key steps:

**Step 1:** I worked with Bob, the AI coding assistant, to create a comprehensive project plan defining the full technology stack.

**Step 2:** Built the entire full-stack application - a React frontend with 7 pages, FastAPI backend with 11 endpoints, SQLite database, and trained ML models on 500 historical records.

**Step 3:** Created detailed context for IBM ICA. This included an 812-line schema file documenting the complete system architecture, and a 465-line bulk import file with 11 REST API tool definitions. The context graph generated 80 nodes and 179 relationships.

**Step 4:** Implemented a Model Context Protocol server using JSON-RPC 2.0, exposing 7 tools that AI agents can call.

---

## [2:00 - 2:45] IBM ICA Integration

**Steps 5 through 7** focused on IBM ICA integration:

I created a basic agent in Agent Studio, then built an Agent Orchestration using LangGraph and the ReAct pattern with GPT-5.2. I registered the MCP server as an external tool in ICA, and successfully linked all 7 tools to the agent.

The integration works end-to-end. When users ask questions, the agent calls the MCP tools, which hit my API endpoints, and returns real data with ML predictions.

---

## [2:45 - 3:30] Demo and Testing

**Step 8** was comprehensive testing. I created 10 demo prompts covering all features:

Users can ask "Show me all my travel bookings" and get 53 bookings instantly. They can request "Estimate refund for booking 51 with high severity" and receive ML predictions with confidence intervals - for example, a likely refund of 76,500 dollars with a range from 68,850 to 84,150.

The system also provides global risk monitoring, regional assessments, historical statistics, and provider policy comparisons. Every feature includes AI explainability, so customers understand how estimates are calculated.

---

## [3:30 - 4:15] Technical Excellence and Innovation

The technical architecture is impressive: IBM ICA's Agent Orchestration communicates via JSON-RPC 2.0 with my MCP server, which is publicly accessible through ngrok. The backend runs FastAPI with ML models, and the React frontend provides beautiful visualizations.

What makes this innovative? First, uncertainty quantification - not just predictions, but confidence intervals. Second, specialized force majeure handling with real-time risk assessment. Third, complete AI transparency with explainable predictions. And fourth, enterprise-ready integration with IBM ICA.

---

## [4:15 - 4:45] Business Value and Impact

The business value is clear: this reduces customer service load with instant automated estimates, improves customer satisfaction through transparent answers, enables real-time risk management, and provides a scalable, production-ready architecture.

We achieved 100% success rate on all demo prompts, with 11 functional API endpoints, 7 integrated MCP tools, and complete documentation.

---

## [4:45 - 5:00] Conclusion

This project demonstrates the future of AI-powered business applications: intelligent, explainable, and seamlessly integrated. By combining machine learning with IBM ICA's Agent Orchestration through the Model Context Protocol, we've created a system that can transform how travel companies handle refunds during force majeure events.

Thank you for your time, and I'm happy to answer any questions!

---

**Total Duration: 5 minutes**
**Word Count: ~650 words**
**Speaking Rate: ~130 words per minute**