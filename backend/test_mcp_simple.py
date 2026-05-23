"""
Simple test script for MCP HTTP endpoint using httpx (already in requirements.txt)
Tests POST /mcp with JSON-RPC 2.0 protocol
"""

import httpx
import json
import sys

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
    
    try:
        response = httpx.post(MCP_URL, json=payload, timeout=10.0)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_mcp_list_tools():
    """Test MCP tools/list method"""
    print("\n=== Testing MCP List Tools ===")
    
    payload = {
        "jsonrpc": "2.0",
        "method": "tools/list",
        "params": {},
        "id": 2
    }
    
    try:
        response = httpx.post(MCP_URL, json=payload, timeout=10.0)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if "result" in data and "tools" in data["result"]:
                tools = data["result"]["tools"]
                print(f"\nFound {len(tools)} tools:")
                for tool in tools:
                    print(f"  - {tool['name']}: {tool.get('description', 'No description')[:80]}...")
                return True
        else:
            print(f"Response: {response.text}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False


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
    
    try:
        response = httpx.post(MCP_URL, json=payload, timeout=10.0)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
            return True
        else:
            print(f"Response: {response.text}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False


def run_all_tests():
    """Run all MCP endpoint tests"""
    print("=" * 60)
    print("MCP HTTP Endpoint Test Suite (using httpx)")
    print("=" * 60)
    
    # Check if backend is running
    try:
        response = httpx.get(f"{BASE_URL}/", timeout=5.0)
        print(f"\nBackend is running at {BASE_URL}")
    except Exception as e:
        print(f"\nERROR: Could not connect to backend at {BASE_URL}")
        print(f"Please ensure the backend is running: python main.py")
        print(f"Error: {e}")
        return False
    
    tests = [
        ("Initialize", test_mcp_initialize),
        ("List Tools", test_mcp_list_tools),
        ("Call Tool", test_mcp_call_tool)
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\nTest '{name}' failed with exception: {e}")
            results.append((name, False))
    
    print("\n" + "=" * 60)
    print("Test Results Summary")
    print("=" * 60)
    
    for name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{status}: {name}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    print(f"\nTotal: {passed}/{total} tests passed")
    
    return passed == total


if __name__ == "__main__":
    try:
        success = run_all_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")
        sys.exit(1)

# Made with Bob
