# IBM ICA Context Forge: Add New Tool from REST API

## Congratulations! 🎉
Your bulk import was successful! All 11 tools are now available in ICA Context Forge.

---

## How to Add Additional Tools Manually

If you need to add more REST API endpoints as MCP tools in the future, follow this guide.

---

## Method 1: Add New Tool from REST API (Recommended)

### Step 1: Click "Add New Tool"
1. In ICA Context Forge, go to **Tools** section
2. Click **"Add New Tool"** or **"Create Tool"** button
3. Select **"From REST API"** option

### Step 2: Enter Basic Information

**Tool Name** (required):
```
delete-booking
```
- Use lowercase with hyphens
- Must be unique
- No spaces or special characters

**Display Name** (required):
```
Delete Travel Booking
```
- User-friendly name
- Can include spaces and capitals

**Description** (required):
```
Delete a travel booking by ID. This will permanently remove the booking and all associated components from the system.
```
- Clear explanation of what the tool does
- Include any important warnings

**Tags** (optional):
```
booking, delete, management, refund-estimation
```
- Comma-separated
- Helps with organization and search

### Step 3: Configure REST API Details

**Integration Type**:
```
REST
```

**Request Type** (HTTP Method):
```
DELETE
```
- Options: GET, POST, PUT, DELETE, PATCH

**API URL** (required):
```
http://localhost:8000/api/bookings/{booking_id}
```
- Full endpoint URL
- Use `{parameter_name}` for path parameters
- Example: `/api/bookings/{booking_id}`

**Authentication Type**:
```
none
```
- Options: none, basic, bearer, api_key, oauth2
- Our API doesn't require auth

**Headers** (optional):
```json
{
  "Accept": "application/json",
  "Content-Type": "application/json"
}
```
- Click "Add Header" for each
- Key: `Accept`, Value: `application/json`
- Key: `Content-Type`, Value: `application/json`

### Step 4: Define Input Schema

Click **"Add Input Schema"** or **"Define Parameters"**

**For Path Parameters** (in URL):
```json
{
  "type": "object",
  "properties": {
    "booking_id": {
      "type": "integer",
      "description": "Unique booking identifier to delete",
      "minimum": 1
    }
  },
  "required": ["booking_id"]
}
```

**For Query Parameters** (GET requests):
```json
{
  "type": "object",
  "properties": {
    "skip": {
      "type": "integer",
      "description": "Number of records to skip",
      "default": 0,
      "minimum": 0
    },
    "limit": {
      "type": "integer",
      "description": "Maximum records to return",
      "default": 100,
      "minimum": 1,
      "maximum": 1000
    }
  }
}
```

**For Request Body** (POST/PUT requests):
```json
{
  "type": "object",
  "properties": {
    "customer_name": {
      "type": "string",
      "description": "Customer full name",
      "minLength": 2,
      "maxLength": 100
    },
    "customer_email": {
      "type": "string",
      "format": "email",
      "description": "Customer email address"
    },
    "amount": {
      "type": "number",
      "description": "Transaction amount",
      "minimum": 0
    },
    "status": {
      "type": "string",
      "enum": ["pending", "approved", "rejected"],
      "description": "Status of the request"
    }
  },
  "required": ["customer_name", "customer_email"]
}
```

### Step 5: Configure Response Handling

**JSONPath Filter** (optional):
```
$
```
- Use `$` for entire response
- Use `$.data` if response is wrapped: `{"data": {...}}`
- Use `$.items[*]` for array of items
- Use `$.result.bookings` for nested data

**Response Schema** (optional):
```json
{
  "type": "object",
  "properties": {
    "message": {
      "type": "string"
    },
    "deleted_id": {
      "type": "integer"
    }
  }
}
```

### Step 6: Test the Tool

1. Click **"Test"** or **"Try It"** button
2. Enter sample values:
   ```json
   {
     "booking_id": 1
   }
   ```
3. Click **"Execute"** or **"Run"**
4. Verify response is correct
5. Check for any errors

### Step 7: Save the Tool

1. Click **"Save"** or **"Create Tool"**
2. Tool will appear in your tools list
3. Status should show "Active" or "Ready"

---

## Method 2: Convert Existing REST API to MCP Tool

If you have an existing REST API and want to convert it to an MCP tool:

### Step 1: Document Your API

Create a specification for your endpoint:

**Example: Update Booking Status**

```yaml
Endpoint: PUT /api/bookings/{booking_id}/status
Description: Update the status of a travel booking
Path Parameters:
  - booking_id (integer, required): Booking ID to update
Request Body:
  - status (string, required): New status (pending/confirmed/cancelled)
  - notes (string, optional): Additional notes
Response:
  - Updated booking object with new status
```

### Step 2: Follow "Add New Tool" Steps

Use the information from Step 1 to fill in the ICA form:

**Tool Name**: `update-booking-status`

**Display Name**: `Update Booking Status`

**Description**: `Update the status of a travel booking to pending, confirmed, or cancelled`

**Request Type**: `PUT`

**URL**: `http://localhost:8000/api/bookings/{booking_id}/status`

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "booking_id": {
      "type": "integer",
      "description": "Booking ID to update",
      "minimum": 1
    },
    "status": {
      "type": "string",
      "enum": ["pending", "confirmed", "cancelled"],
      "description": "New booking status"
    },
    "notes": {
      "type": "string",
      "description": "Optional notes about status change"
    }
  },
  "required": ["booking_id", "status"]
}
```

### Step 3: Test and Save

Same as Method 1, Step 6 and 7.

---

## Common Input Schema Patterns

### Pattern 1: Simple GET with Query Parameters
```json
{
  "type": "object",
  "properties": {
    "search": {
      "type": "string",
      "description": "Search term"
    },
    "page": {
      "type": "integer",
      "default": 1,
      "minimum": 1
    },
    "per_page": {
      "type": "integer",
      "default": 20,
      "minimum": 1,
      "maximum": 100
    }
  }
}
```

### Pattern 2: POST with Complex Object
```json
{
  "type": "object",
  "properties": {
    "user": {
      "type": "object",
      "properties": {
        "name": {"type": "string"},
        "email": {"type": "string", "format": "email"}
      },
      "required": ["name", "email"]
    },
    "preferences": {
      "type": "object",
      "properties": {
        "notifications": {"type": "boolean"},
        "theme": {"type": "string", "enum": ["light", "dark"]}
      }
    }
  },
  "required": ["user"]
}
```

### Pattern 3: POST with Array
```json
{
  "type": "object",
  "properties": {
    "items": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "id": {"type": "integer"},
          "quantity": {"type": "integer", "minimum": 1}
        },
        "required": ["id", "quantity"]
      },
      "minItems": 1
    }
  },
  "required": ["items"]
}
```

### Pattern 4: File Upload
```json
{
  "type": "object",
  "properties": {
    "file": {
      "type": "string",
      "format": "binary",
      "description": "File to upload"
    },
    "description": {
      "type": "string",
      "description": "File description"
    }
  },
  "required": ["file"]
}
```

---

## Data Types Reference

### String Types
```json
{
  "type": "string",
  "minLength": 2,
  "maxLength": 100,
  "pattern": "^[A-Za-z]+$",
  "format": "email"  // or "date-time", "uri", "uuid"
}
```

### Number Types
```json
{
  "type": "number",  // or "integer"
  "minimum": 0,
  "maximum": 100,
  "multipleOf": 0.01
}
```

### Boolean Type
```json
{
  "type": "boolean",
  "default": false
}
```

### Enum (Fixed Values)
```json
{
  "type": "string",
  "enum": ["option1", "option2", "option3"],
  "default": "option1"
}
```

### Array Type
```json
{
  "type": "array",
  "items": {
    "type": "string"
  },
  "minItems": 1,
  "maxItems": 10,
  "uniqueItems": true
}
```

### Object Type
```json
{
  "type": "object",
  "properties": {
    "key1": {"type": "string"},
    "key2": {"type": "integer"}
  },
  "required": ["key1"],
  "additionalProperties": false
}
```

---

## Example: Adding a New Endpoint

Let's add a new endpoint to your Refund Estimation API:

### New Endpoint: Get Booking Statistics

**Backend Code** (add to `backend/main.py`):
```python
@app.get("/api/statistics/bookings")
async def get_booking_statistics(db: Session = Depends(get_db)):
    """Get booking statistics"""
    total = db.query(Booking).count()
    by_status = db.query(
        Booking.status, 
        func.count(Booking.id)
    ).group_by(Booking.status).all()
    
    return {
        "total_bookings": total,
        "by_status": {status: count for status, count in by_status},
        "timestamp": datetime.utcnow().isoformat()
    }
```

### Add to ICA Context Forge:

**Tool Name**: `get-booking-statistics`

**Display Name**: `Get Booking Statistics`

**Description**: `Retrieve aggregated statistics about all bookings including total count and breakdown by status`

**Request Type**: `GET`

**URL**: `http://localhost:8000/api/statistics/bookings`

**Input Schema**:
```json
{
  "type": "object",
  "properties": {}
}
```
(No parameters needed)

**JSONPath Filter**: `$`

**Tags**: `statistics, analytics, bookings, refund-estimation`

**Test**:
- Click Test
- Click Execute (no parameters needed)
- Should return statistics object

**Save**: Click Save

---

## Troubleshooting

### Issue 1: Tool Test Fails with "Connection Refused"
**Cause**: Backend API not running  
**Solution**:
```bash
cd backend
python main.py
```

### Issue 2: Tool Test Returns 404
**Cause**: URL is incorrect  
**Solution**: Verify URL matches backend route exactly

### Issue 3: Tool Test Returns 422 Validation Error
**Cause**: Input schema doesn't match API requirements  
**Solution**: Check backend schemas.py and update input schema

### Issue 4: Tool Test Returns Empty Response
**Cause**: JSONPath filter is incorrect  
**Solution**: 
- Try `$` for entire response
- Try `$.data` if response is wrapped
- Check actual API response format

### Issue 5: Tool Saves But Doesn't Appear in List
**Cause**: Browser cache or sync issue  
**Solution**: Refresh page, clear cache, or wait a moment

---

## Best Practices

### 1. Naming Conventions
- **Tool Name**: lowercase-with-hyphens
- **Display Name**: Title Case With Spaces
- **Consistent Prefixes**: Use prefixes for related tools (e.g., `booking-create`, `booking-update`, `booking-delete`)

### 2. Descriptions
- Start with action verb (Get, Create, Update, Delete)
- Explain what the tool does
- Mention any side effects
- Include example use cases

### 3. Input Validation
- Always specify `type`
- Use `required` array for mandatory fields
- Set `minimum`/`maximum` for numbers
- Use `enum` for fixed options
- Add helpful `description` for each field

### 4. Error Handling
- Test with invalid inputs
- Verify error messages are clear
- Check edge cases (empty arrays, null values)

### 5. Documentation
- Keep a list of all tools and their purposes
- Document any special requirements
- Note dependencies between tools
- Track version changes

---

## Next Steps

Now that your 11 tools are imported and you know how to add more:

1. ✅ **Test All Tools**: Verify each tool works correctly
2. ✅ **Start Backend**: Ensure API is running
3. ✅ **Deploy MCP Server**: Make tools available to AI agents
4. ✅ **Connect AI Agent**: Configure agent to use your tools
5. ✅ **Add More Tools**: Use this guide to add new endpoints

---

## Quick Reference Card

### Add New Tool Checklist
- [ ] Tool name (lowercase-with-hyphens)
- [ ] Display name (User Friendly)
- [ ] Description (clear and concise)
- [ ] Request type (GET/POST/PUT/DELETE)
- [ ] URL (with {parameters})
- [ ] Authentication (usually "none")
- [ ] Headers (Content-Type, Accept)
- [ ] Input schema (JSON Schema format)
- [ ] JSONPath filter (usually "$")
- [ ] Tags (for organization)
- [ ] Test with sample data
- [ ] Save and verify

### Common URLs for Your API
```
http://localhost:8000/api/bookings
http://localhost:8000/api/bookings/{booking_id}
http://localhost:8000/api/estimate-refund/{booking_id}
http://localhost:8000/api/estimates/{booking_id}
http://localhost:8000/api/risk-events
http://localhost:8000/api/risk-events/region/{region}
http://localhost:8000/api/historical-refunds
http://localhost:8000/api/statistics/refund-rates
http://localhost:8000/api/providers
http://localhost:8000/api/providers/{provider_name}
```

---

**Last Updated**: 2026-05-20  
**Status**: Bulk import successful - 11 tools active  
**Next**: Add more tools as needed using this guide