#!/usr/bin/env python3
from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
import requests

load_dotenv()

HUBSPOT_API_KEY = os.getenv("HUBSPOT_API_KEY")
BASE_URL = "https://api.hubapi.com"

app = Flask(__name__)

@app.route('/tools/list', methods=['POST'])
def list_tools():
    return jsonify({
        "tools": [
            {
                "name": "search_contacts",
                "description": "Search HubSpot contacts by name or email",
                "inputSchema": {
                    "type": "object",
                    "properties": {"query": {"type": "string"}},
                    "required": ["query"]
                }
            },
            {
                "name": "search_deals",
                "description": "Search HubSpot deals by stage",
                "inputSchema": {
                    "type": "object",
                    "properties": {"dealstage": {"type": "string"}},
                    "required": ["dealstage"]
                }
            }
        ]
    })

@app.route('/tools/call', methods=['POST'])
def call_tool():
    data = request.json
    tool_name = data.get("name")
    arguments = data.get("arguments", {})
    
    try:
        if tool_name == "search_contacts":
            response = requests.post(
                f"{BASE_URL}/crm/v3/objects/contacts/search",
                headers={"Authorization": f"Bearer {HUBSPOT_API_KEY}"},
                json={"query": arguments.get("query"), "limit": 50}
            )
            return jsonify(response.json())
        
        elif tool_name == "search_deals":
            response = requests.post(
                f"{BASE_URL}/crm/v3/objects/deals/search",
                headers={"Authorization": f"Bearer {HUBSPOT_API_KEY}"},
                json={"filterGroups": [{"filters": [{"propertyName": "dealstage", "operator": "EQ", "value": arguments.get("dealstage")}]}], "limit": 50}
            )
            return jsonify(response.json())
        
        return jsonify({"error": f"Unknown tool: {tool_name}"})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
