# Complete Guide: Connect AI Agent to Your MCP Tools

## Overview

Your 11 MCP tools are now in IBM ICA Context Forge. To use them, you need to connect an AI agent. This guide shows you how to connect different AI agents to use your refund estimation tools.

---

## Option 1: Use IBM watsonx Assistant (Recommended for ICA)

Since you're using IBM ICA Context Forge, IBM watsonx Assistant is the most integrated option.

### Step 1: Access watsonx Assistant

**1.1 From IBM Cloud Dashboard:**
1. Go to: https://cloud.ibm.com
2. Click **Catalog**
3. Search for **"watsonx Assistant"**
4. Click on it

**1.2 Or from ICA Context Forge:**
1. Look for **"Assistant"**, **"Chat"**, or **"AI Agent"** section
2. May be integrated directly in ICA interface

### Step 2: Create or Open Assistant

**2.1 Create New Assistant:**
1. Click **"Create Assistant"** or **"New Assistant"**
2. Name: `Refund Estimation Assistant`
3. Description: `AI assistant for travel refund estimation`
4. Click **"Create"**

**2.2 Or Open Existing:**
1. Select your existing assistant
2. Go to **Settings** or **Configuration**

### Step 3: Connect to ICA Context Forge Tools

**3.1 Find Integration Settings:**
1. In watsonx Assistant, look for:
   - **"Integrations"** tab
   - **"Extensions"** section
   - **"Custom Extensions"** option
   - **"MCP Tools"** or **"Context Forge"** option

**3.2 Add ICA Context Forge Integration:**
1. Click **"Add Integration"** or **"Connect"**
2. Select **"Context Forge"** or **"MCP Tools"**
3. Enter your ICA workspace details:
   - Workspace URL: Your ICA Context Forge URL
   - Authentication: Use your IBM Cloud credentials
4. Click **"Connect"** or **"Authorize"**

**3.3 Select Tools:**
1. You should see your 11 tools listed:
   - v2-create-booking
   - v2-get-bookings
   - v2-get-booking-details
   - v2-estimate-refund
   - v2-get-refund-estimates
   - v2-get-risk-events
   - v2-get-regional-risk
   - v2-get-historical-refunds
   - v2-get-refund-statistics
   - v2-get-provider-policies
   - v2-get-provider-policy
2. Select all 11 tools (or specific ones you want)
3. Click **"Enable"** or **"Activate"**

### Step 4: Test the Assistant

**4.1 Open Chat Interface:**
1. Click **"Preview"** or **"Try It"** button
2. Chat window should open

**4.2 Test Tool Discovery:**
Ask the assistant:
```
What tools do you have available?
```

Expected response:
```
I have access to 11 refund estimation tools:
- Create booking
- Get bookings
- Get booking details
- Estimate refund
- Get refund estimates
- Get risk events
- Get regional risk
- Get historical refunds
- Get refund statistics
- Get provider policies
- Get provider policy
```

**4.3 Test Tool Usage:**

**Test 1: List Bookings**
```
Show me all bookings
```
or
```
List all travel bookings
```

**Test 2: Create Booking**
```
Create a booking for Jane Smith (jane@example.com) traveling to Paris from New York on June 15, 2026. Include a flight with Air France costing 50000 INR.
```

**Test 3: Estimate Refund**
```
Estimate the refund for booking ID 1 with high severity
```

**Test 4: Check Risk Events**
```
What are the current global risk events?
```

**Test 5: Get Statistics**
```
Show me refund statistics
```

### Step 5: Deploy Assistant (Optional)

**5.1 Deploy to Web:**
1. Click **"Deploy"** or **"Publish"**
2. Select **"Web Chat"**
3. Get embed code
4. Add to your website

**5.2 Deploy to Slack/Teams:**
1. Click **"Deploy"**
2. Select **"Slack"** or **"Microsoft Teams"**
3. Follow integration steps

---

## Option 2: Use Claude Desktop (For Local Testing)

Claude Desktop is great for testing your MCP tools locally.

### Step 1: Download Claude Desktop

1. Go to: https://claude.ai/download
2. Download for Windows
3. Install Claude Desktop
4. Sign in with your Anthropic account

### Step 2: Configure MCP Server

**2.1 Find Configuration File:**

Claude Desktop config location:
```
C:\Users\AbhijitJoshi\AppData\Roaming\Claude\claude_desktop_config.json
```

**2.2 Edit Configuration:**

Open the file in notepad and add:

```json
{
  "mcpServers": {
    "refund-estimation": {
      "command": "python",
      "args": [
        "C:\\Users\\AbhijitJoshi\\Uncertainty_Refund\\backend\\mcp_server_http.py"
      ],
      "env": {
        "PYTHONPATH": "C:\\Users\\AbhijitJoshi\\Uncertainty_Refund\\backend"
      }
    }
  }
}
```

**Important:** This uses the native MCP server, not ICA. For ICA integration, you'd need the ICA MCP endpoint URL (if available).

### Step 3: Start Required Services

**Terminal 1: Backend**
```powershell
cd C:\Users\AbhijitJoshi\Uncertainty_Refund\backend
python main.py
```

**Terminal 2: MCP Server** (if using native)
```powershell
cd C:\Users\AbhijitJoshi\Uncertainty_Refund\backend
python mcp_server_http.py
```

### Step 4: Restart Claude Desktop

1. Close Claude Desktop completely
2. Reopen Claude Desktop
3. Wait for it to connect to MCP server

### Step 5: Test with Claude

**Test 1: Check Tools**
```
What tools do you have available?
```

**Test 2: Use Tools**
```
List all bookings
```

```
Create a test booking for a trip to Paris
```

```
Estimate refund for booking 1
```

---

## Option 3: Use OpenAI GPT with Custom Actions

If you have ChatGPT Plus or Enterprise, you can create custom GPTs with your tools.

### Step 1: Create Custom GPT

1. Go to: https://chat.openai.com
2. Click your profile → **"My GPTs"**
3. Click **"Create a GPT"**
4. Name: `Refund Estimation Assistant`

### Step 2: Configure Actions

**2.1 Add Actions:**
1. Go to **"Configure"** tab
2. Scroll to **"Actions"** section
3. Click **"Create new action"**

**2.2 Import OpenAPI Schema:**

You need to create an OpenAPI schema for your endpoints. Here's a template:

```yaml
openapi: 3.0.0
info:
  title: Refund Estimation API
  version: 1.0.0
servers:
  - url: https://famished-vertebrae-basil.ngrok-free.dev
paths:
  /api/bookings:
    get:
      operationId: getBookings
      summary: Get all bookings
      parameters:
        - name: skip
          in: query
          schema:
            type: integer
            default: 0
        - name: limit
          in: query
          schema:
            type: integer
            default: 100
      responses:
        '200':
          description: List of bookings
    post:
      operationId: createBooking
      summary: Create a new booking
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                customer_name:
                  type: string
                customer_email:
                  type: string
                travel_date:
                  type: string
                destination:
                  type: string
                origin:
                  type: string
                components:
                  type: array
                  items:
                    type: object
      responses:
        '201':
          description: Booking created
  /api/bookings/{booking_id}:
    get:
      operationId: getBookingDetails
      summary: Get booking details
      parameters:
        - name: booking_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: Booking details
  /api/estimate-refund/{booking_id}:
    post:
      operationId: estimateRefund
      summary: Estimate refund for booking
      parameters:
        - name: booking_id
          in: path
          required: true
          schema:
            type: integer
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                selected_model:
                  type: string
                severity:
                  type: string
      responses:
        '200':
          description: Refund estimate
```

**2.3 Save and Test:**
1. Paste the schema
2. Click **"Test"**
3. Try calling an endpoint
4. Click **"Save"**

### Step 3: Use Custom GPT

1. Start a conversation with your custom GPT
2. Ask it to use the tools:
   - "List all bookings"
   - "Create a booking for Paris"
   - "Estimate refund for booking 1"

---

## Option 4: Build Custom Python Agent

Create your own AI agent that uses your MCP tools.

### Step 1: Install Dependencies

```powershell
pip install openai requests
```

### Step 2: Create Agent Script

**File: `ai_agent.py`**

```python
import openai
import requests
import json

# Configure OpenAI
openai.api_key = "your-openai-api-key"

# Your backend URL
BASE_URL = "https://famished-vertebrae-basil.ngrok-free.dev"

# Define tools for OpenAI function calling
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_bookings",
            "description": "Get list of all travel bookings",
            "parameters": {
                "type": "object",
                "properties": {
                    "skip": {"type": "integer", "description": "Records to skip"},
                    "limit": {"type": "integer", "description": "Max records"}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_booking",
            "description": "Create a new travel booking",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_name": {"type": "string"},
                    "customer_email": {"type": "string"},
                    "travel_date": {"type": "string"},
                    "destination": {"type": "string"},
                    "origin": {"type": "string"},
                    "components": {"type": "array"}
                },
                "required": ["customer_name", "customer_email", "travel_date", "destination", "origin", "components"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "estimate_refund",
            "description": "Estimate refund amount for a booking",
            "parameters": {
                "type": "object",
                "properties": {
                    "booking_id": {"type": "integer"},
                    "severity": {"type": "string", "enum": ["low", "medium", "high", "critical"]}
                },
                "required": ["booking_id"]
            }
        }
    }
]

# Tool execution functions
def execute_tool(tool_name, arguments):
    if tool_name == "get_bookings":
        response = requests.get(f"{BASE_URL}/api/bookings", params=arguments)
        return response.json()
    
    elif tool_name == "create_booking":
        response = requests.post(f"{BASE_URL}/api/bookings", json=arguments)
        return response.json()
    
    elif tool_name == "estimate_refund":
        booking_id = arguments.pop("booking_id")
        response = requests.post(f"{BASE_URL}/api/estimate-refund/{booking_id}", json=arguments)
        return response.json()
    
    return {"error": "Unknown tool"}

# Chat function
def chat(user_message, conversation_history=[]):
    # Add user message
    conversation_history.append({"role": "user", "content": user_message})
    
    # Call OpenAI
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=conversation_history,
        tools=tools,
        tool_choice="auto"
    )
    
    message = response.choices[0].message
    
    # Check if tool call is needed
    if message.tool_calls:
        # Execute tool
        tool_call = message.tool_calls[0]
        tool_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)
        
        print(f"🔧 Calling tool: {tool_name}")
        print(f"📝 Arguments: {arguments}")
        
        # Execute the tool
        tool_result = execute_tool(tool_name, arguments)
        
        print(f"✅ Result: {tool_result}")
        
        # Add tool result to conversation
        conversation_history.append(message)
        conversation_history.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps(tool_result)
        })
        
        # Get final response
        final_response = openai.chat.completions.create(
            model="gpt-4",
            messages=conversation_history
        )
        
        assistant_message = final_response.choices[0].message.content
    else:
        assistant_message = message.content
    
    # Add assistant response
    conversation_history.append({"role": "assistant", "content": assistant_message})
    
    return assistant_message, conversation_history

# Main loop
if __name__ == "__main__":
    print("🤖 Refund Estimation AI Agent")
    print("=" * 50)
    
    conversation = []
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Goodbye!")
            break
        
        response, conversation = chat(user_input, conversation)
        print(f"\nAssistant: {response}")
```

### Step 3: Run the Agent

```powershell
python ai_agent.py
```

### Step 4: Test

```
You: List all bookings
Assistant: [Shows bookings]

You: Create a booking for Jane traveling to Paris
Assistant: [Creates booking]

You: Estimate refund for booking 1
Assistant: [Shows refund estimate]
```

---

## Comparison of Options

| Option | Pros | Cons | Best For |
|--------|------|------|----------|
| **watsonx Assistant** | - Integrated with IBM<br>- Easy setup<br>- Enterprise features | - Requires IBM account<br>- May have costs | Production use with ICA |
| **Claude Desktop** | - Easy to use<br>- Great UI<br>- Free tier | - Local only<br>- Requires config | Testing and development |
| **Custom GPT** | - ChatGPT interface<br>- Easy to share | - Requires Plus/Enterprise<br>- Limited customization | Quick demos |
| **Custom Python Agent** | - Full control<br>- Customizable<br>- Free | - Requires coding<br>- More setup | Advanced users |

---

## Recommended Approach

### For Your Use Case (IBM ICA Context Forge):

**Best Option: watsonx Assistant**

1. ✅ Already integrated with IBM ecosystem
2. ✅ Works seamlessly with ICA Context Forge
3. ✅ Enterprise-ready
4. ✅ Can deploy to web, Slack, Teams
5. ✅ Supports your 11 MCP tools natively

**Steps:**
1. Access watsonx Assistant from IBM Cloud
2. Create new assistant
3. Connect to ICA Context Forge
4. Enable your 11 tools
5. Test in preview
6. Deploy to desired channel

---

## Summary

**To connect AI agent to your MCP tools:**

1. **Choose an option** (watsonx Assistant recommended)
2. **Configure the agent** to connect to ICA or your backend
3. **Enable your 11 tools** in the agent
4. **Test tool discovery** ("What tools do you have?")
5. **Test tool usage** ("List bookings", "Estimate refund")
6. **Deploy** (optional) to web, Slack, Teams, etc.

**Your MCP tools are ready - just connect an AI agent to start using them!** 🚀

---

**Last Updated**: 2026-05-20  
**Recommended**: watsonx Assistant for IBM ICA Context Forge  
**Alternative**: Claude Desktop for local testing