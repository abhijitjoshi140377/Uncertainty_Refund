import json

# Read original bulk import file
with open('refund-api-bulk-import.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Update each tool with v2- prefix
for tool in data:
    tool['name'] = f"v2-{tool['name']}"
    tool['displayName'] = f"{tool['displayName']} (v2)"

# Write to new file
with open('refund-api-bulk-import-v2.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)

print("SUCCESS: Created refund-api-bulk-import-v2.json")
print(f"SUCCESS: Updated {len(data)} tools with v2- prefix")
print("\nNew tool names:")
for tool in data:
    print(f"  - {tool['name']}")

# Made with Bob
