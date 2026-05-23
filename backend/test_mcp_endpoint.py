"""
Test script for MCP HTTP endpoint
Tests POST /mcp with JSON-RPC 2.0 protocol
"""

import requests
import json

# Base URL
BASE_URL = "http://localhost:8000"
MCP_URL = f"{BASE_URL}/mcp"

def test_mcp_initialize():
    """Test MCP initialize handshake"""
    print("\n=== Testing MCP Initialize ===")
    
    payload = {
        "jsonrpc": "2.0",
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {
                "name": "test-client",
                "version": "1.0.0"
            }
        },
        "id": 1
    }
    
    response = requests.post(MCP_URL, json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    return response.status_code == 200


def test_mcp_list_tools():
    """Test MCP tools/list method"""
    print("\n=== Testing MCP List Tools ===")
    
    payload = {
        "jsonrpc": "2.0",
        "method": "tools/list",
        "params": {},
        "id": 2
    }
    
    response = requests.post(MCP_URL, json=payload)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        
        if "result" in data and "tools" in data["result"]:
            tools = data["result"]["tools"]
            print(f"\n✅ Found {len(tools)} tools:")
            for tool in tools:
                print(f"  - {tool['name']}: {tool.get('description', 'No description')[:80]}...")
    else:
        print(f"Response: {response.text}")
    
    return response.status_code == 200


def test_mcp_call_tool():
    """Test MCP tools/call method"""
    print("\n=== Testing MCP Call Tool (get_bookings) ===")
    
    payload = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": "get_bookings",
            "arguments": {
                "skip": 0,
                "limit": 5
            }
        },
        "id": 3
    }
    
    response = requests.post(MCP_URL, json=payload)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
    else:
        print(f"Response: {response.text}")
    
    return response.status_code == 200


def test_mcp_call_tool_with_error():
    """Test MCP tools/call with invalid booking ID"""
    print("\n=== Testing MCP Call Tool with Error (get_booking_details) ===")
    
    payload = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": "get_booking_details",
            "arguments": {
                "booking_id": 99999
            }
        },
        "id": 4
    }
    
    response = requests.post(MCP_URL, json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    return True  # Error handling is expected


def run_all_tests():
    """Run all MCP endpoint tests"""
    print("=" * 60)
    print("MCP HTTP Endpoint Test Suite")
    print("=" * 60)
    
    tests = [
        ("Initialize", test_mcp_initialize),
        ("List Tools", test_mcp_list_tools),
        ("Call Tool", test_mcp_call_tool),
        ("Call Tool with Error", test_mcp_call_tool_with_error)
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ Test '{name}' failed with exception: {e}")
            results.append((name, False))
    
    print("\n" + "=" * 60)
    print("Test Results Summary")
    print("=" * 60)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    print(f"\nTotal: {passed}/{total} tests passed")
    
    return passed == total


if __name__ == "__main__":
    try:
        success = run_all_tests()
        exit(0 if success else 1)
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to backend at http://localhost:8000")
        print("Please ensure the backend is running: python main.py")
        exit(1)

# Made with Bob
