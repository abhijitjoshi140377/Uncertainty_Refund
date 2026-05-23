# 10 Demo Prompts for Hackathon Video

## 🎬 Demo Video Script (8-10 minutes)

### Introduction (30 seconds)
"This is the Travel Refund Uncertainty Estimation System - an AI-powered assistant that helps customers understand refund options during force majeure events using ML predictions with 95% confidence intervals."

---

## 📝 10 Demo Prompts (In Order)

### Prompt 1: List All Bookings (Basic Functionality)
```
Show me all my travel bookings
```

**What to Highlight:**
- Agent calls get_bookings tool
- Displays 53 active bookings
- Shows booking IDs, destinations, dates, costs
- Demonstrates basic data retrieval

**Expected Response:** List of bookings with IDs, destinations, travel dates, and costs

---

### Prompt 2: Get Specific Booking Details
```
Show me the details for booking 51
```

**What to Highlight:**
- Agent calls get_booking_details tool
- Shows complete booking breakdown
- Lists all components (flight, hotel, visa, insurance)
- Displays individual costs

**Expected Response:** Detailed breakdown of Bangalore → Frankfurt booking with all components

---

### Prompt 3: Refund Estimation - High Severity (⭐ Main Feature)
```
I need to cancel booking 51 due to a natural disaster. Can you estimate my refund with high severity?
```

**What to Highlight:**
- ⭐ Agent calls estimate_refund tool
- ⭐ Shows ML-powered prediction
- ⭐ Displays 95% confidence interval (lower and upper bounds)
- ⭐ Presents three scenarios: best case, worst case, most likely
- ⭐ Shows risk score
- ⭐ Component-wise breakdown

**Expected Response:** 
- Expected refund: ~$76,500
- 95% CI: $68,850 to $84,150
- Best case: $85,000
- Most likely: $76,500
- Worst case: $68,000
- Risk score and explanation

---

### Prompt 4: Compare Different Severity Levels
```
What would be the difference if I cancel the same booking with medium severity instead of high severity?
```

**What to Highlight:**
- Agent makes another estimate_refund call
- Shows how severity affects refund amounts
- Demonstrates scenario analysis
- Helps customer make informed decisions

**Expected Response:** Lower refund estimate with medium severity, comparison with high severity

---

### Prompt 5: Global Risk Assessment
```
What are the current global risk events affecting travel?
```

**What to Highlight:**
- Agent calls get_risk_events tool
- Lists active force majeure events worldwide
- Shows event types (war, pandemic, natural disaster, etc.)
- Displays severity levels and affected regions

**Expected Response:** List of current global risk events with severity and locations

---

### Prompt 6: Regional Risk Check
```
I'm planning to travel to Ukraine. What's the current risk level there?
```

**What to Highlight:**
- Agent calls get_regional_risk tool
- Provides region-specific risk assessment
- Shows aggregate risk level
- Lists specific events affecting the region
- Gives travel recommendations

**Expected Response:** High/Critical risk level for Ukraine with specific events and warnings

---

### Prompt 7: Historical Statistics
```
Show me historical refund statistics for flight cancellations during pandemics
```

**What to Highlight:**
- Agent calls get_refund_statistics tool
- Displays historical data and trends
- Shows average refund rates
- Indicates success rates for force majeure claims
- Provides data-driven insights

**Expected Response:** Statistics showing average refund rates for flights during pandemics

---

### Prompt 8: Provider Policies Comparison
```
What are the refund policies for different travel providers?
```

**What to Highlight:**
- Agent calls get_provider_policies tool
- Lists multiple providers
- Compares standard vs. force majeure refund percentages
- Shows cancellation fees
- Helps customers choose better providers

**Expected Response:** Comparison table of provider policies with refund percentages

---

### Prompt 9: Complex Multi-Component Analysis
```
For booking 53 (Mumbai to Barcelona), if I cancel due to political unrest with medium severity, what would be my expected refund for each component?
```

**What to Highlight:**
- Agent analyzes multiple components
- Provides component-specific estimates
- Shows how different components have different refund rates
- Demonstrates sophisticated analysis
- Total refund calculation

**Expected Response:** Breakdown by flight, hotel, visa, insurance with individual refund estimates

---

### Prompt 10: Confidence Interval Explanation (AI Transparency)
```
Can you explain what the 95% confidence interval means in my refund estimate?
```

**What to Highlight:**
- ⭐ AI explainability and transparency
- ⭐ Agent explains uncertainty quantification
- ⭐ Clarifies what confidence intervals mean
- ⭐ Helps customers understand predictions
- ⭐ Shows responsible AI practices

**Expected Response:** Clear explanation of confidence intervals in customer-friendly language

---

## 🎯 Key Points to Emphasize During Demo

### Technical Excellence:
1. **ML-Powered Predictions** - Not just rules, but trained models
2. **Uncertainty Quantification** - 95% confidence intervals show sophistication
3. **Multi-Model Ensemble** - Random Forest + Gradient Boosting
4. **Real-time Integration** - Live API calls visible in terminal
5. **MCP Protocol** - Enterprise-grade tool integration with IBM ICA

### Business Value:
1. **Reduces Customer Service Load** - Instant estimates vs. manual processing
2. **Improves Customer Satisfaction** - Transparent, data-driven answers
3. **Risk Management** - Real-time global and regional risk monitoring
4. **Data-Driven Decisions** - Historical statistics inform estimates
5. **Scalable Architecture** - API-first design, ready for production

### Innovation:
1. **Uncertainty Estimation** - Not just point predictions
2. **Force Majeure Handling** - Specialized for exceptional events
3. **Component-Level Analysis** - Granular refund breakdown
4. **AI Transparency** - Explainable predictions with confidence intervals
5. **Enterprise Integration** - IBM ICA agent orchestration

---

## 🎬 Demo Flow Timeline (10 minutes)

**0:00-0:30** - Introduction and overview
**0:30-1:30** - Prompts 1-2: Basic functionality (bookings)
**1:30-4:00** - Prompts 3-4: ⭐ Core feature (refund estimation with CI)
**4:00-5:30** - Prompts 5-6: Risk assessment
**5:30-7:00** - Prompts 7-8: Statistics and policies
**7:00-8:30** - Prompt 9: Complex analysis
**8:30-9:30** - Prompt 10: AI explainability
**9:30-10:00** - Wrap-up and business value

---

## 📊 What Makes This Demo Stand Out

### Compared to Other Hackathon Projects:

✅ **Working End-to-End** - Not just a prototype
✅ **ML Sophistication** - Confidence intervals, not just predictions
✅ **Enterprise Integration** - IBM ICA, not just a chatbot
✅ **Real Data** - Actual API calls, not mocked responses
✅ **Production Quality** - Professional UI, error handling, documentation
✅ **Business Focus** - Solves real problem in travel industry
✅ **AI Transparency** - Explainable AI with uncertainty quantification

---

## 🎥 Recording Tips

1. **Show Terminal** - Split screen to show MCP tool calls
2. **Highlight Numbers** - Point out confidence intervals and amounts
3. **Explain Briefly** - Don't just read responses, explain significance
4. **Show Enthusiasm** - This is impressive work!
5. **Mention Challenges** - "Integrating MCP with ICA was complex but worth it"
6. **Business Value** - Always tie back to real-world impact
7. **Time Management** - Practice to stay within 10 minutes

---

## 🏆 Closing Statement

"This Travel Refund Uncertainty Estimation System demonstrates how AI can provide transparent, data-driven solutions for complex business problems. By combining ML predictions with confidence intervals, real-time risk assessment, and enterprise integration through IBM ICA, we've created a production-ready system that can transform how travel companies handle refunds during force majeure events. Thank you!"

---

## 📝 Backup Prompts (If Time Permits)

```
Compare refund rates for Air India vs Lufthansa
```

```
What factors affect refund amounts the most?
```

```
Show me bookings to high-risk destinations
```

---

**Good luck with your demo! You've built something truly impressive! 🚀🏆**