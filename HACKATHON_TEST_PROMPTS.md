# Travel Refund Estimation Assistant - Test Prompts & Scenarios

## Hackathon Demo Guide
**Agent Name:** TravelRefundAdvisor  
**Purpose:** AI-powered travel refund estimation during force majeure events  
**Date:** May 23, 2026

---

## 10 Test Prompts & Scenarios

### Scenario 1: Basic Booking Query
**Prompt:**
```
Show me all my travel bookings
```

**Expected Response:**
- Agent retrieves list of bookings
- Displays booking references, destinations, dates
- Shows total costs

**Demo Value:** Shows basic data retrieval capability

---

### Scenario 2: Specific Booking Details
**Prompt:**
```
Can you show me the details for booking ID 1?
```

**Expected Response:**
- Retrieves specific booking information
- Shows customer details
- Lists all components (flights, hotels, visas, insurance)
- Displays individual costs

**Demo Value:** Demonstrates detailed data access

---

### Scenario 3: Refund Estimation - High Severity
**Prompt:**
```
I need to cancel my booking to Paris (booking ID 1) due to a natural disaster. Can you estimate my refund with high severity?
```

**Expected Response:**
- Calls estimate_refund API
- Shows expected refund amount and percentage
- Displays 95% confidence interval (lower and upper bounds)
- Provides best case, worst case, and most likely scenarios
- Shows risk score
- Explains force majeure considerations

**Demo Value:** Core ML-powered refund estimation feature

---

### Scenario 4: Global Risk Assessment
**Prompt:**
```
What are the current global risk events affecting travel?
```

**Expected Response:**
- Lists active force majeure events worldwide
- Shows event types (war, pandemic, natural disaster, etc.)
- Displays severity levels
- Indicates affected regions

**Demo Value:** Real-time risk monitoring capability

---

### Scenario 5: Regional Risk Check
**Prompt:**
```
I'm planning to travel to Ukraine. What's the current risk level there?
```

**Expected Response:**
- Retrieves regional risk assessment
- Shows aggregate risk level (low/medium/high/critical)
- Lists specific events affecting the region
- Provides travel safety recommendations

**Demo Value:** Location-specific risk analysis

---

### Scenario 6: Refund Statistics Analysis
**Prompt:**
```
Show me historical refund statistics by component type and event type
```

**Expected Response:**
- Displays aggregated refund statistics
- Shows average refund percentages by:
  - Component type (flight, hotel, visa, insurance)
  - Event type (war, pandemic, natural disaster)
- Indicates force majeure success rates
- Provides insights on refund patterns

**Demo Value:** Data-driven insights and trends

---

### Scenario 7: Provider Policy Inquiry
**Prompt:**
```
What are the refund policies for different travel providers?
```

**Expected Response:**
- Lists provider refund policies
- Shows standard vs. force majeure refund percentages
- Displays cancellation fees
- Compares different providers

**Demo Value:** Policy comparison and transparency

---

### Scenario 8: Complex Multi-Component Booking
**Prompt:**
```
I have a booking with flights, hotel, and visa. If I cancel due to political unrest with medium severity, what would be my expected refund for each component?
```

**Expected Response:**
- Analyzes each component separately
- Provides component-specific refund estimates
- Shows total expected refund
- Explains differences in refund rates by component type
- Considers provider-specific policies

**Demo Value:** Sophisticated multi-component analysis

---

### Scenario 9: Confidence Interval Explanation
**Prompt:**
```
Can you explain what the confidence intervals mean in my refund estimate?
```

**Expected Response:**
- Explains 95% confidence interval concept
- Clarifies lower and upper bounds
- Describes uncertainty in predictions
- Relates to historical data patterns
- Helps customer understand risk

**Demo Value:** AI transparency and explainability

---

### Scenario 10: Comparative Scenario Analysis
**Prompt:**
```
Compare the refund estimates for booking ID 1 under low, medium, and high severity scenarios
```

**Expected Response:**
- Generates multiple estimates with different severity levels
- Shows side-by-side comparison
- Highlights differences in expected refunds
- Explains impact of severity on refund amounts
- Helps customer make informed decisions

**Demo Value:** Decision support and scenario planning

---

## Additional Quick Test Prompts

### Quick Test 1: Health Check
```
Are you connected to the refund estimation system?
```

### Quick Test 2: Capabilities
```
What can you help me with?
```

### Quick Test 3: Specific Provider
```
What's the refund policy for Air India?
```

### Quick Test 4: Historical Data
```
Show me historical refund data for flight cancellations during pandemics
```

### Quick Test 5: Risk Events Filter
```
Show me only active risk events
```

---

## Demo Flow Recommendation

### 5-Minute Hackathon Demo:

**Minute 1: Introduction (30 seconds)**
- "This is an AI-powered travel refund estimation assistant"
- "Uses ML models to predict refunds during force majeure events"

**Minute 2: Basic Functionality (1 minute)**
- Test Prompt: "Show me all my travel bookings"
- Test Prompt: "Show me details for booking ID 1"

**Minute 3: Core Feature - Refund Estimation (1.5 minutes)**
- Test Prompt: "Estimate refund for booking 1 with high severity"
- Highlight: Confidence intervals, scenarios, ML predictions

**Minute 4: Risk Assessment (1 minute)**
- Test Prompt: "What are current global risk events?"
- Test Prompt: "What's the risk level for Ukraine?"

**Minute 5: Advanced Features (1 minute)**
- Test Prompt: "Show me refund statistics"
- Test Prompt: "Compare low vs high severity scenarios"
- Wrap up with business value

---

## Key Points to Emphasize

### Technical Excellence:
✅ Full-stack application (React + FastAPI)
✅ ML-powered predictions (Random Forest, Gradient Boosting)
✅ Real-time API integration
✅ IBM ICA agent integration
✅ Confidence intervals and uncertainty quantification

### Business Value:
✅ Reduces customer service workload
✅ Provides instant refund estimates
✅ Improves customer satisfaction
✅ Data-driven decision making
✅ Transparent AI explanations

### Innovation:
✅ AI agent for travel industry
✅ Force majeure event handling
✅ Uncertainty estimation (not just point predictions)
✅ Multi-component booking analysis
✅ Real-time risk monitoring

---

## Troubleshooting Tips

### If Agent Doesn't Respond:
1. Check backend is running: `python main.py`
2. Check ngrok is active
3. Verify API health: `https://famished-vertebrae-basil.ngrok-free.dev/api/health`

### If Data Seems Wrong:
1. Database has synthetic data for demo
2. Refund estimates are ML predictions (not actual)
3. Risk events are sample data

### If Agent Says "Can't Access":
1. Ensure OpenAPI tools are configured
2. Check ngrok URL hasn't changed
3. Verify API endpoints are accessible

---

## Success Metrics for Demo

### What Judges Will Look For:
✅ **Working Demo** - Agent responds correctly
✅ **Technical Depth** - ML models, confidence intervals
✅ **Business Value** - Solves real problem
✅ **User Experience** - Natural conversation
✅ **Innovation** - Unique approach to refund estimation

### What Makes This Stand Out:
✅ **Uncertainty Quantification** - Not just predictions, but confidence
✅ **Multi-Model Approach** - Ensemble of ML models
✅ **Real-Time Integration** - Live API calls
✅ **IBM Technology** - ICA agent integration
✅ **Complete Solution** - End-to-end working system

---

## Backup Prompts (If Time Permits)

```
1. "Create a new booking for a trip to London"
2. "What factors affect refund amounts?"
3. "Show me the most common reasons for refunds"
4. "Compare refund rates for flights vs hotels"
5. "What's the average processing time for refunds?"
```

---

## Final Checklist Before Demo

- [ ] Backend running (`python main.py`)
- [ ] Ngrok active and URL noted
- [ ] Agent responding in ICA
- [ ] Tested at least 3 prompts
- [ ] Prepared to explain ML models
- [ ] Ready to discuss business value
- [ ] Backup slides/screenshots ready
- [ ] Confident and enthusiastic!

---

**Good luck with your hackathon! 🚀**

**Your agent is working perfectly - just follow these prompts and you'll have an impressive demo!**

---

*Generated for Bob ICA Catalysts May 2026 Hackathon*  
*Travel Refund Uncertainty Estimation System*  
*Date: May 23, 2026*