import json
import sys

if len(sys.argv) < 2:
    print("Usage: python update_urls_for_ngrok.py <ngrok-url>")
    print("Example: python update_urls_for_ngrok.py https://abc123-xyz.ngrok-free.app")
    sys.exit(1)

ngrok_url = sys.argv[1].rstrip('/')

# Read the v2 bulk import file
with open('refund-api-bulk-import-v2.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Update all URLs
for tool in data:
    tool['url'] = tool['url'].replace('http://localhost:8000', ngrok_url)

# Write to new file
with open('refund-api-bulk-import-ngrok.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)

print(f"SUCCESS: Created refund-api-bulk-import-ngrok.json")
print(f"All URLs updated to use: {ngrok_url}")
print(f"\nUpdated {len(data)} tools:")
for tool in data:
    print(f"  - {tool['name']}: {tool['url']}")

print(f"\nNext steps:")
print(f"1. Import refund-api-bulk-import-ngrok.json into ICA Context Forge")
print(f"2. Keep backend running: cd backend && python main.py")
print(f"3. Keep ngrok running: ngrok http 8000")
print(f"4. Test tools in ICA - they should work now!")

# Made with Bob
