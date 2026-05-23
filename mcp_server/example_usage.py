"""
Example usage of the MCP Server for Travel Refund Estimation
Demonstrates how to interact with the MCP server programmatically
"""

import asyncio
import json
from datetime import datetime, timedelta


# Example 1: Create a booking and get refund estimate
async def example_create_booking_and_estimate():
    """
    Example: Create a travel booking and generate refund estimate
    """
    print("=" * 60)
    print("Example 1: Create Booking and Generate Refund Estimate")
    print("=" * 60)
    
    # Sample booking data
    booking_data = {
        "customer_name": "John Doe",
        "customer_email": "john.doe@example.com",
        "travel_date": (datetime.now() + timedelta(days=60)).isoformat(),
        "destination": "Paris",
        "origin": "Mumbai",
        "components": [
            {
                "component_type": "flight",
                "provider_name": "Air India",
                "cost": 50000,
                "is_refundable": True,
                "cancellation_fee": 500
            },
            {
                "component_type": "hotel",
                "provider_name": "Marriott Paris",
                "cost": 25000,
                "is_refundable": True,
                "cancellation_fee": 1000
            },
            {
                "component_type": "insurance",
                "provider_name": "Travel Guard",
                "cost": 2000,
                "is_refundable": False,
                "cancellation_fee": 0
            }
        ]
    }
    
    print("\n📝 Booking Data:")
    print(json.dumps(booking_data, indent=2))
    
    print("\n✅ Step 1: Create booking using 'create_booking' tool")
    print("   Tool: create_booking")
    print("   Action: AI agent would call this tool with the booking data")
    
    print("\n✅ Step 2: Generate refund estimate using 'estimate_refund' tool")
    print("   Tool: estimate_refund")
    print("   Parameters: {")
    print('     "booking_id": <returned_booking_id>,')
    print('     "calamity_type": "pandemic",')
    print('     "severity": "high"')
    print("   }")
    
    print("\n📊 Expected Response:")
    print("   - Expected refund: ₹30,000 - ₹45,000 (40-60%)")
    print("   - Confidence interval: 95%")
    print("   - Risk level: High")
    print("   - Best case: ₹55,000 (73%)")
    print("   - Worst case: ₹15,000 (20%)")
    print("   - Most likely: ₹38,000 (50%)")


# Example 2: Check regional risk
async def example_check_regional_risk():
    """
    Example: Check risk level for a specific region
    """
    print("\n" + "=" * 60)
    print("Example 2: Check Regional Risk")
    print("=" * 60)
    
    regions = ["Ukraine", "Paris", "Singapore", "Mumbai"]
    
    for region in regions:
        print(f"\n🌍 Checking risk for: {region}")
        print(f"   Tool: get_regional_risk")
        print(f'   Parameters: {{"region": "{region}"}}')
        print(f"   Expected: Risk level and active events in {region}")


# Example 3: Analyze historical refund trends
async def example_analyze_historical_trends():
    """
    Example: Analyze historical refund data
    """
    print("\n" + "=" * 60)
    print("Example 3: Analyze Historical Refund Trends")
    print("=" * 60)
    
    print("\n📈 Query 1: Flight refunds during pandemics")
    print("   Tool: get_historical_refunds")
    print('   Parameters: {')
    print('     "component_type": "flight",')
    print('     "event_type": "pandemic",')
    print('     "limit": 100')
    print('   }')
    
    print("\n📈 Query 2: Overall refund statistics")
    print("   Tool: get_refund_statistics")
    print("   Parameters: {}")
    print("   Expected: Aggregated statistics by component and event type")


# Example 4: Get provider policies
async def example_get_provider_policies():
    """
    Example: Retrieve provider refund policies
    """
    print("\n" + "=" * 60)
    print("Example 4: Get Provider Refund Policies")
    print("=" * 60)
    
    print("\n🏢 Query 1: All airline policies")
    print("   Tool: get_provider_policies")
    print('   Parameters: {"provider_type": "airline"}')
    
    print("\n🏢 Query 2: Specific provider policy")
    print("   Tool: get_provider_policy")
    print('   Parameters: {"provider_name": "Air India"}')
    print("   Expected: Detailed refund policy including force majeure clause")


# Example 5: Complete AI agent workflow
async def example_complete_workflow():
    """
    Example: Complete workflow for an AI agent helping a customer
    """
    print("\n" + "=" * 60)
    print("Example 5: Complete AI Agent Workflow")
    print("=" * 60)
    
    print("\n💬 User Query:")
    print('   "I want to book a trip to Paris for August 15, 2026.')
    print('    Flight costs ₹50,000, hotel ₹25,000.')
    print('    What refund can I expect if there\'s a war or pandemic?"')
    
    print("\n🤖 AI Agent Actions:")
    
    print("\n   Step 1: Check current risk in Paris")
    print("   └─ Tool: get_regional_risk")
    print('      Parameters: {"region": "Paris"}')
    
    print("\n   Step 2: Create the booking")
    print("   └─ Tool: create_booking")
    print("      Parameters: <booking details>")
    
    print("\n   Step 3: Generate refund estimate for pandemic scenario")
    print("   └─ Tool: estimate_refund")
    print('      Parameters: {')
    print('        "booking_id": <id>,')
    print('        "calamity_type": "pandemic",')
    print('        "severity": "high"')
    print('      }')
    
    print("\n   Step 4: Generate refund estimate for war scenario")
    print("   └─ Tool: estimate_refund")
    print('      Parameters: {')
    print('        "booking_id": <id>,')
    print('        "calamity_type": "war",')
    print('        "severity": "critical"')
    print('      }')
    
    print("\n   Step 5: Get historical data for context")
    print("   └─ Tool: get_historical_refunds")
    print('      Parameters: {"event_type": "pandemic", "limit": 50}')
    
    print("\n   Step 6: Get provider policies")
    print("   └─ Tool: get_provider_policies")
    print('      Parameters: {"provider_type": "airline"}')
    
    print("\n💬 AI Agent Response:")
    print("   'Based on the analysis:")
    print("   - Current risk in Paris: Low")
    print("   - Booking created: REF-ABC123456")
    print("   - Pandemic scenario: Expected refund ₹38,000 (50%)")
    print("   - War scenario: Expected refund ₹15,000 (20%)")
    print("   - Historical average for pandemics: 55% refund")
    print("   - Air India offers 60% refund for force majeure events")
    print("   - Recommendation: Consider travel insurance for better coverage'")


# Example 6: Real-time risk monitoring
async def example_risk_monitoring():
    """
    Example: Monitor global risk events
    """
    print("\n" + "=" * 60)
    print("Example 6: Real-time Risk Monitoring")
    print("=" * 60)
    
    print("\n⚠️ Get all active risk events")
    print("   Tool: get_risk_events")
    print('   Parameters: {"active_only": true}')
    print("   Expected: List of active wars, pandemics, natural disasters")
    
    print("\n📊 Sample Response:")
    print("   [")
    print("     {")
    print('       "event_type": "war",')
    print('       "severity": "critical",')
    print('       "affected_region": "Ukraine",')
    print('       "description": "Ongoing conflict"')
    print("     },")
    print("     {")
    print('       "event_type": "natural_disaster",')
    print('       "severity": "high",')
    print('       "affected_region": "Japan",')
    print('       "description": "Earthquake"')
    print("     }")
    print("   ]")


async def main():
    """Run all examples"""
    print("\n" + "=" * 60)
    print("MCP SERVER USAGE EXAMPLES")
    print("Travel Refund Uncertainty Estimation System")
    print("=" * 60)
    
    await example_create_booking_and_estimate()
    await example_check_regional_risk()
    await example_analyze_historical_trends()
    await example_get_provider_policies()
    await example_complete_workflow()
    await example_risk_monitoring()
    
    print("\n" + "=" * 60)
    print("INTEGRATION NOTES")
    print("=" * 60)
    print("\n1. These examples show the tool calls an AI agent would make")
    print("2. The MCP server handles the communication with FastAPI backend")
    print("3. AI agents (Claude, GPT, etc.) can use these tools naturally")
    print("4. All responses are in JSON format for easy parsing")
    print("5. The server supports async operations for better performance")
    
    print("\n" + "=" * 60)
    print("NEXT STEPS")
    print("=" * 60)
    print("\n1. Install dependencies: pip install -r requirements.txt")
    print("2. Start FastAPI backend: cd backend && python main.py")
    print("3. Start MCP server: python refund_mcp_server.py")
    print("4. Configure your AI agent to use the MCP server")
    print("5. Test with real queries!")
    
    print("\n✅ Examples completed!\n")


if __name__ == "__main__":
    asyncio.run(main())

# Made with Bob
