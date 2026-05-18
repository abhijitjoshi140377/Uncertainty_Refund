# Refund Intelligence Platform - Demo Presentation

## Slide 1 - Title Slide
**Title:** Refund Intelligence Platform  
**Subtitle:** AI-assisted refund estimation, risk monitoring, and model comparison  
**Presented by:** Abhijit Joshi  
**Duration target:** 3-5 minutes  

**Speaker notes:**
- Introduce the project as a platform for estimating refund outcomes under uncertainty.
- Mention that the solution combines booking data, risk events, historical refunds, and multiple estimation approaches.
- State that the platform helps evaluate refund impact under calamities such as war, pandemics, disasters, and disruptions.

---

## Slide 2 - Problem Statement
**Title:** The Problem We Are Solving

**Content:**
- Travel and refund decisions are uncertain during force majeure situations
- Customers and operators need visibility into possible refund outcomes
- Manual refund estimation is inconsistent and slow
- Different calamity types affect refund likelihood differently
- Historical outcomes are difficult to compare without a unified interface

**Speaker notes:**
- Explain that the system addresses uncertainty rather than just simple booking storage.
- Highlight the lack of structured decision support during disruptive events.
- Position the project as a decision intelligence tool rather than only a travel app.

---

## Slide 3 - Solution Overview
**Title:** Proposed Solution

**Content:**
- Centralized booking management
- Risk event monitoring dashboard
- Refund estimation engine
- Historical refund analytics
- Model comparison workflow
- Notification support for new events and bookings

**Speaker notes:**
- Explain that the platform combines operational visibility with estimation capability.
- Mention that users can create bookings, monitor global events, and estimate refund scenarios from multiple models.

---

## Slide 4 - High-Level Architecture
**Title:** System Architecture

**Content:**
- **Frontend:** React + Vite + SCSS
- **Backend:** FastAPI
- **Database:** SQLite (`backend/refund_estimation.db`)
- **ML / Estimation Layer:** Random Forest, Gradient Boosting, Rule-based logic
- **Data Sources:** Synthetic historical refunds, provider policies, bookings, risk events

**Speaker notes:**
- Mention that the backend exposes APIs for bookings, risk events, historical analytics, and refund estimation.
- Highlight that synthetic data is used to bootstrap model behavior and testing.

---

## Slide 5 - Dashboard Screen
**Title:** Dashboard Overview

**On-screen focus:**
- Statistics cards
- Recent bookings
- Quick actions
- System summary

**What this screen does:**
- Shows total bookings
- Displays active risk events
- Shows average refund rate
- Provides navigation into key workflows

**Speaker notes:**
- Describe the dashboard as the system overview screen.
- Emphasize that it gives a quick operational snapshot for decision-makers.

---

## Slide 6 - Booking Management Screen
**Title:** Bookings List

**On-screen focus:**
- Existing bookings table
- Status badges
- Create booking action
- View details action

**What this screen does:**
- Lists all customer bookings
- Helps review routes, customers, travel dates, and total cost
- Provides entry point to booking-level refund estimation

**Speaker notes:**
- Explain that bookings are the primary entities on which refund estimation is performed.
- Mention that users can drill into each booking for deeper analysis.

---

## Slide 7 - Create Booking Screen
**Title:** Create New Booking

**On-screen focus:**
- Customer information
- Travel details
- Flight and hotel cost inputs
- Calamity simulation section

**What this screen does:**
- Creates a new booking for an existing customer scenario
- Captures booking components and total value
- Lets the user define travel details used later for refund estimation

**Speaker notes:**
- Explain that this is where the evaluation journey begins.
- Mention that once created, the booking can be used in detail view or comparator workflows.
- Point out that new booking creation now triggers a bell notification.

---

## Slide 8 - Booking Details + Refund Estimate
**Title:** Booking Details and Estimate View

**On-screen focus:**
- Booking information
- Booking components
- Refund estimate tile
- Risk level and scenario analysis

**What this screen does:**
- Displays a full booking breakdown
- Generates refund estimates for the selected booking
- Shows:
  - expected refund amount
  - refund percentage
  - confidence interval
  - risk score
  - best / likely / worst case scenarios

**Speaker notes:**
- Describe this as the detailed estimation screen for one booking.
- Explain that users can generate or refresh an estimate based on current logic.

---

## Slide 9 - New Comparator Screen
**Title:** Refund Model Comparator

**On-screen focus:**
- Existing booking selector
- Model selector
- Calamity selector
- Severity selector
- Result panel

**What this screen does:**
- Selects an existing customer booking
- Allows comparing different estimation approaches:
  - Auto Ensemble
  - Random Forest
  - Gradient Boosting
  - Rule Based
- Allows choosing calamity type and severity
- Returns a comparative refund estimate for the selected scenario

**Speaker notes:**
- Explain that this is one of the strongest capabilities of the platform.
- Mention that users can compare model outputs under different calamity assumptions.
- Position this as useful for analysis, experimentation, and decision support.

---

## Slide 10 - Risk Monitor Screen
**Title:** Risk Monitoring and Event Entry

**On-screen focus:**
- Active and historical risk cards
- Add Risk Event modal
- Severity and region data
- Event start/end dates

**What this screen does:**
- Displays current global force majeure risk events
- Allows adding new risk events
- Tracks severity, region, description, and active status
- Supports operational awareness around disruptions

**Speaker notes:**
- Explain that this screen connects real-world disruptions to refund uncertainty.
- Mention that adding a new risk event now updates the bell notification system.

---

## Slide 11 - Notification Experience
**Title:** Bell Notifications

**Content:**
- Notification badge on the bell icon
- Triggered when:
  - a new booking is created
  - a new risk event is created
- Dropdown displays recent notifications
- Clear action resets current session notifications

**Speaker notes:**
- Explain that the notification system improves operational awareness.
- Mention that notifications are currently session-based in memory.
- If needed, note that this can later be persisted to local storage or database.

---

## Slide 12 - Analytics Screen
**Title:** Historical Refund Analytics

**On-screen focus:**
- Refund charts
- Component filter buttons
- Event type metrics
- Summary statistics

**What this screen does:**
- Visualizes historical refund outcomes
- Shows average refund by event type and component
- Helps understand trends from past cases
- Supports interpretation of refund behavior under different disruptions

**Speaker notes:**
- Explain that analytics gives evidence behind the estimation logic.
- Mention that the platform is not just predictive; it is also explanatory.

---

## Slide 13 - Estimation Logic
**Title:** How Refund Estimation Works

**Content:**
- Booking components are analyzed individually
- Risk score is resolved using:
  - active regional risk events, or
  - selected calamity type and severity
- Estimation methods:
  - Auto ensemble
  - Random Forest
  - Gradient Boosting
  - Rule-based fallback
- Final result aggregates component-level estimates

**Speaker notes:**
- Explain that the system combines booking attributes, risk context, and historical patterns.
- Mention that if ML is not applicable, fallback rule-based estimation still provides usable output.

---

## Slide 14 - Example Demo Flow
**Title:** Suggested 3-5 Minute Demo Walkthrough

**Content:**
1. Start on Dashboard  
2. Open Bookings List  
3. Create a new booking  
4. Show bell notification update  
5. Open Booking Details and generate estimate  
6. Open Comparator and compare models  
7. Open Risk Monitor and add a new event  
8. Show bell notification update again  
9. Open Analytics for historical explanation  

**Speaker notes:**
- Use this as the actual flow for your live demo or recorded walkthrough.
- Keep transitions smooth and explain only the user value, not every implementation detail.

---

## Slide 15 - Business Value
**Title:** Why This Platform Matters

**Content:**
- Faster refund decision support
- Better visibility into uncertainty
- Model-based comparison for analysis
- Centralized monitoring of disruptions
- Improved communication with customers and operators

**Speaker notes:**
- Emphasize the operational and analytical benefits.
- Mention that the platform reduces ambiguity during disruptive travel events.

---

## Slide 16 - Future Enhancements
**Title:** Possible Next Steps

**Content:**
- Persistent notifications
- Real external risk feeds
- Provider-specific refund policy intelligence
- Advanced model evaluation metrics
- User authentication and role-based access
- Exportable reports and downloadable comparisons

**Speaker notes:**
- Show that the platform is extensible.
- Mention that the current system already demonstrates the core workflow successfully.

---

## Slide 17 - Closing Slide
**Title:** Thank You

**Content:**
- Questions?
- Demo complete
- Refund Intelligence Platform

**Speaker notes:**
- Close by summarizing that the platform integrates booking workflows, risk intelligence, historical analytics, and refund estimation into one interface.

---

# Suggested Screenshot Plan
Use these screenshots in the presentation:
1. Dashboard
2. Bookings List
3. Create Booking form
4. Booking Details
5. Refund Comparator
6. Risk Monitor
7. Add Risk Event modal
8. Bell notification dropdown
9. Analytics page

---

# Optional Video Demo Script
If you later record a video, use this short script:
- “This is the Refund Intelligence Platform, designed to estimate refunds under uncertainty.”
- “The dashboard provides a snapshot of bookings, active risks, and refund trends.”
- “Here I create a new booking, which also triggers a notification.”
- “In booking details, I generate a refund estimate with risk-aware scenario analysis.”
- “In the comparator, I can choose a customer booking, select a model, choose a calamity, and compare refund outcomes.”
- “In the risk monitor, I can add a new event and track operational disruptions.”
- “Analytics helps explain historical refund behavior.”
- “Overall, the platform supports smarter refund decision-making under force majeure scenarios.”