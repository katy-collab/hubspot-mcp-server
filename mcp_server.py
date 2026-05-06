#!/usr/bin/env python3
import json
import os
import sys
from dotenv import load_dotenv
import requests

load_dotenv()

HUBSPOT_API_KEY = os.getenv("HUBSPOT_API_KEY")
BASE_URL = "https://api.hubapi.com"

def search_contacts(query):
    response = requests.post(
        f"{BASE_URL}/crm/v3/objects/contacts/search",
        headers={"Authorization": f"Bearer {HUBSPOT_API_KEY}"},
        json={"query": query, "limit": 50}
    )
    return response.json()

def search_deals(dealstage):
    response = requests.post(
        f"{BASE_URL}/crm/v3/objects/deals/search",
        headers={"Authorization": f"Bearer {HUBSPOT_API_KEY}"},
        json={"filterGroups": [{"filters": [{"propertyName": "dealstage", "operator": "EQ", "value": dealstage}]}], "limit": 50}
    )
    return response.json()

def process_request(request):
    method = request.get("method")
    
    if method == "tools/list":
        return {
            "tools": [
                {
                    "name": "search_contacts",
                    "description": "Search HubSpot contacts",
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
        }
    
    elif method == "tools/call":
        tool_name = request.get("params", {}).get("name")
        arguments = request.get("params", {}).get("arguments", {})
        
        if tool_name == "search_contacts":
            result = search_contacts(arguments.get("query"))
        elif tool_name == "search_deals":
            result = search_deals(arguments.get("dealstage"))
        else:
            result = {"error": f"Unknown tool: {tool_name}"}
        
        return {"result": result}
    
    return {"error": "Unknown method"}

if __name__ == "__main__":
    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break
            
            request = json.loads(line)
            response = process_request(request)
            print(json.dumps(response))
            sys.stdout.flush()
        except Exception as e:
            print(json.dumps({"error": str(e)}))
            sys.stdout.flush()
