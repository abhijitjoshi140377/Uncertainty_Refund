# API Enhancement Guide

## Overview

This guide documents the enhancements made to the FastAPI backend to ensure clean REST standards, consistent response structure, comprehensive error handling, and detailed OpenAPI documentation.

## What Was Enhanced

### 1. **Consistent Response Structure**

All API responses now follow a standard format:

```json
{
  "status": "success",
  "message": "Human-readable message",
  "data": { /* actual response data */ }
}
```

**Error responses:**
```json
{
  "status": "error",
  "message": "Error description",
  "errors": [
    {
      "field": "email",
      "message": "Invalid email format",
      "type": "value_error"
    }
  ]
}
```

### 2. **Enhanced Pydantic Schemas** (`schemas_enhanced.py`)

#### New Features:
- **Enums for validation**: ComponentType, EventType, SeverityLevel, MLModel, BookingStatus
- **Generic response wrappers**: APIResponse[T], ErrorResponse, PaginatedResponse[T]
- **Comprehensive field descriptions**: Every field has detailed description
- **JSON schema examples**: All schemas include example data
- **Proper validation**: Min/max lengths, value ranges, required fields

#### Key Schemas:

**APIResponse[T]** - Generic wrapper for all successful responses
```python
class APIResponse(BaseModel, Generic[T]):
    status: str = "success"
    message: str
    data: Optional[T] = None
```

**ErrorResponse** - Standard error format
```python
class ErrorResponse(BaseModel):
    status: str = "error"
    message: str
    errors: Optional[List[ErrorDetail]] = None
```

**PaginatedResponse[T]** - For paginated list endpoints
```python
class PaginatedResponse(BaseModel, Generic[T]):
    status: str = "success"
    message: str
    data: List[T]
    total: int
    skip: int
    limit: int
```

### 3. **Enhanced Main Application** (`main_enhanced.py`)

#### Global Exception Handlers:

**Validation Error Handler** (422):
```python
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    # Returns structured error with field-level details
```

**HTTP Exception Handler** (4xx, 5xx):
```python
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    # Returns consistent error format
```

**General Exception Handler** (500):
```python
@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    # Catches unexpected errors
```

#### Enhanced Endpoint Documentation:

Every endpoint now includes:
- **Comprehensive docstrings** with usage examples
- **Parameter descriptions** with validation rules
- **Response examples** for success and error cases
- **Use case descriptions**
- **Error code documentation**

### 4. **Improved OpenAPI Documentation**

#### Enhanced API Metadata:
```python
app = FastAPI(
    title="Travel Refund Uncertainty Estimation API",
    description="Detailed markdown description with features",
    version="1.0.0",
    contact={...},
    license_info={...}
)
```

#### Response Models:
- All endpoints have explicit `response_model`
- Error responses documented with `responses` parameter
- Status codes properly defined

## Migration Guide

### Option 1: Replace Existing Files

1. **Backup current files:**
   ```bash
   cd backend
   cp main.py main_backup.py
   cp schemas.py schemas_backup.py
   ```

2. **Replace with enhanced versions:**
   ```bash
   mv main_enhanced.py main.py
   mv schemas_enhanced.py schemas.py
   ```

3. **Restart the server:**
   ```bash
   python main.py
   ```

### Option 2: Gradual Migration

1. **Keep both versions:**
   - Run enhanced version on different port for testing
   - Gradually migrate endpoints
   - Update frontend to use new response structure

2. **Test enhanced version:**
   ```bash
   # Run on port 8001
   uvicorn main_enhanced:app --host 0.0.0.0 --port 8001 --reload
   ```

3. **Update frontend API client:**
   ```javascript
   // Old format
   const data = response.data;
   
   // New format
   const data = response.data.data;
   const message = response.data.message;
   const status = response.data.status;
   ```

## API Response Examples

### Success Response (Single Item)

**Endpoint:** `GET /api/bookings/1`

```json
{
  "status": "success",
  "message": "Booking retrieved successfully",
  "data": {
    "id": 1,
    "booking_reference": "BK12345678",
    "customer_name": "John Doe",
    "customer_email": "john@example.com",
    "total_cost": 75000,
    "status": "active",
    "components": [...]
  }
}
```

### Success Response (List with Pagination)

**Endpoint:** `GET /api/bookings?skip=0&limit=10`

```json
{
  "status": "success",
  "message": "Retrieved 10 bookings",
  "data": [
    { /* booking 1 */ },
    { /* booking 2 */ }
  ],
  "total": 50,
  "skip": 0,
  "limit": 10
}
```

### Error Response (404)

**Endpoint:** `GET /api/bookings/999`

```json
{
  "status": "error",
  "message": "Booking with ID 999 not found"
}
```

### Error Response (422 Validation)

**Endpoint:** `POST /api/bookings` (invalid data)

```json
{
  "status": "error",
  "message": "Validation failed",
  "errors": [
    {
      "field": "customer_email",
      "message": "value is not a valid email address",
      "type": "value_error.email"
    },
    {
      "field": "components",
      "message": "ensure this value has at least 1 items",
      "type": "value_error.list.min_items"
    }
  ]
}
```

## Endpoint Documentation Examples

### Before Enhancement:

```python
@app.get("/api/bookings/{booking_id}")
async def get_booking(booking_id: int, db: Session = Depends(get_db)):
    """Get a specific booking by ID"""
    booking = crud.get_booking(db, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking
```

### After Enhancement:

```python
@app.get(
    "/api/bookings/{booking_id}",
    response_model=APIResponse[BookingResponse],
    tags=["Bookings"],
    summary="Get Booking Details",
    description="Retrieve detailed information about a specific booking",
    responses={
        200: {"description": "Booking details retrieved successfully"},
        404: {
            "description": "Booking not found",
            "model": ErrorResponse,
            "content": {
                "application/json": {
                    "example": {
                        "status": "error",
                        "message": "Booking with ID 999 not found"
                    }
                }
            }
        }
    }
)
async def get_booking(
    booking_id: int = Path(..., gt=0, description="Unique booking ID"),
    db: Session = Depends(get_db)
):
    """
    Get detailed information about a specific booking.
    
    **Path Parameters:**
    - **booking_id**: Unique booking ID (must be positive integer)
    
    **Returns:**
    - Complete booking details including:
      - Customer information
      - Travel dates and destinations
      - All booking components
      - Total cost and status
      - Booking reference
    
    **Errors:**
    - **404**: Booking not found
    """
    booking = crud.get_booking(db, booking_id)
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Booking with ID {booking_id} not found"
        )
    
    return APIResponse(
        status="success",
        message="Booking retrieved successfully",
        data=booking
    )
```

## Benefits of Enhanced API

### 1. **Consistency**
- All responses follow the same structure
- Predictable error handling
- Easier frontend integration

### 2. **Better Documentation**
- Comprehensive OpenAPI/Swagger docs
- Clear parameter descriptions
- Example requests and responses
- Use case documentation

### 3. **Improved Error Handling**
- Field-level validation errors
- Consistent error format
- Helpful error messages
- Proper HTTP status codes

### 4. **Type Safety**
- Enum validation for fixed values
- Proper type hints
- Pydantic validation
- JSON schema generation

### 5. **Developer Experience**
- Auto-generated API clients
- Interactive API documentation
- Clear endpoint organization with tags
- Searchable documentation

## Testing the Enhanced API

### 1. **Access Interactive Documentation**

```
http://localhost:8000/api/docs
```

Features:
- Try out endpoints directly
- See request/response schemas
- View example data
- Test error scenarios

### 2. **Test with cURL**

**Create Booking:**
```bash
curl -X POST "http://localhost:8000/api/bookings" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "John Doe",
    "customer_email": "john@example.com",
    "travel_date": "2026-08-15T10:00:00",
    "destination": "Paris",
    "origin": "Mumbai",
    "components": [{
      "component_type": "flight",
      "provider_name": "Air India",
      "cost": 50000,
      "is_refundable": true,
      "cancellation_fee": 500
    }]
  }'
```

**Get Booking:**
```bash
curl "http://localhost:8000/api/bookings/1"
```

**Generate Estimate:**
```bash
curl -X POST "http://localhost:8000/api/estimate-refund/1" \
  -H "Content-Type: application/json" \
  -d '{
    "selected_model": "auto",
    "calamity_type": "pandemic",
    "severity": "high"
  }'
```

### 3. **Test Error Handling**

**404 Error:**
```bash
curl "http://localhost:8000/api/bookings/999"
```

**422 Validation Error:**
```bash
curl -X POST "http://localhost:8000/api/bookings" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "J",
    "customer_email": "invalid-email",
    "components": []
  }'
```

## Frontend Integration

### Update API Client

**Before:**
```javascript
// frontend/src/services/api.js
export const getBooking = async (id) => {
  const response = await axios.get(`${API_BASE_URL}/bookings/${id}`);
  return response.data; // Direct data
};
```

**After:**
```javascript
// frontend/src/services/api.js
export const getBooking = async (id) => {
  const response = await axios.get(`${API_BASE_URL}/bookings/${id}`);
  
  // Check status
  if (response.data.status === 'error') {
    throw new Error(response.data.message);
  }
  
  return response.data.data; // Nested data
};

// Or create a wrapper
const handleResponse = (response) => {
  if (response.data.status === 'error') {
    throw new Error(response.data.message);
  }
  return response.data.data;
};

export const getBooking = async (id) => {
  const response = await axios.get(`${API_BASE_URL}/bookings/${id}`);
  return handleResponse(response);
};
```

### Handle Errors

```javascript
try {
  const booking = await getBooking(id);
  // Use booking data
} catch (error) {
  if (error.response?.data?.errors) {
    // Handle validation errors
    error.response.data.errors.forEach(err => {
      console.error(`${err.field}: ${err.message}`);
    });
  } else {
    // Handle general error
    console.error(error.message);
  }
}
```

## Best Practices

### 1. **Always Use Response Models**
```python
@app.get("/api/endpoint", response_model=APIResponse[YourSchema])
```

### 2. **Document All Parameters**
```python
param: int = Path(..., gt=0, description="Clear description")
```

### 3. **Provide Response Examples**
```python
responses={
    200: {
        "content": {
            "application/json": {
                "example": { /* example data */ }
            }
        }
    }
}
```

### 4. **Use Enums for Fixed Values**
```python
class ComponentType(str, Enum):
    FLIGHT = "flight"
    HOTEL = "hotel"
```

### 5. **Write Comprehensive Docstrings**
```python
"""
Brief description.

**Parameters:**
- param1: Description

**Returns:**
- Description of return value

**Errors:**
- 404: When not found
"""
```

## Troubleshooting

### Issue: Import errors after migration

**Solution:**
```bash
# Ensure all dependencies are installed
pip install -r requirements.txt
```

### Issue: Frontend getting nested data

**Solution:** Update API client to access `response.data.data`

### Issue: Validation errors not showing

**Solution:** Check that `RequestValidationError` handler is registered

### Issue: OpenAPI docs not showing examples

**Solution:** Ensure `json_schema_extra` is defined in schema Config

## Next Steps

1. **Test all endpoints** with the enhanced version
2. **Update frontend** to handle new response structure
3. **Add authentication** if needed
4. **Implement rate limiting** for production
5. **Add logging** for better debugging
6. **Set up monitoring** for API health

## Support

For questions or issues:
- Check OpenAPI docs: http://localhost:8000/api/docs
- Review this guide
- Check FastAPI documentation: https://fastapi.tiangolo.com/

---

**Enhanced API Version**: 1.0.0  
**Last Updated**: May 20, 2026  
**Author**: Abhijit Joshi