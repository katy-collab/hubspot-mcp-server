#!/usr/bin/env python3
"""HubSpot MCP Server"""
import json
import os
import sys
import asyncio
from dotenv import load_dotenv
import httpx
from mcp.server import Server
from mcp.types import Tool, TextContent

load_dotenv()

HUBSPOT_API_KEY = os.getenv("HUBSPOT_API_KEY")
HUBSPOT_BASE_URL = "https://api.hubapi.com"

if not HUBSPOT_API_KEY:
    print("Error: HUBSPOT_API_KEY not set", file=sys.stderr)
    sys.exit(1)

server = Server("hubspot-mcp")

@server.list_tools()
async def list_tools():
    return [
        Tool(name="search_contacts", description="Search contacts by name or email", inputSchema={"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}),
        Tool(name="search_deals", description="Search deals by stage", inputSchema={"type": "object", "properties": {"dealstage": {"type": "string"}}, "required": ["dealstage"]}),
        Tool(name="update_deal", description="Update a deal", inputSchema={"type": "object", "properties": {"deal_id": {"type": "string"}, "dealstage": {"type": "string"}}, "required": ["deal_id", "dealstage"]}),
    ]

@server.call_tool()
async def call_tool(name, arguments):
    try:
        if name == "search_contacts":
            result = await search_contacts(arguments["query"])
        elif name == "search_deals":
            result = await search_deals(arguments["dealstage"])
        elif name == "update_deal":
            result = await update_deal(arguments["deal_id"], arguments["dealstage"])
        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]

async def search_contacts(query):
    async with httpx.AsyncClient() as client:
        r = await client.post(f"{HUBSPOT_BASE_URL}/crm/v3/objects/contacts/search", headers={"Authorization": f"Bearer {HUBSPOT_API_KEY}"}, json={"query": query, "limit": 50})
        return r.json()

async def search_deals(dealstage):
    async with httpx.AsyncClient() as client:
        r = await client.post(f"{HUBSPOT_BASE_URL}/crm/v3/objects/deals/search", headers={"Authorization": f"Bearer {HUBSPOT_API_KEY}"}, json={"filterGroups": [{"filters": [{"propertyName": "dealstage", "operator": "EQ", "value": dealstage}]}], "limit": 50})
        return r.json()

async def update_deal(deal_id, dealstage):
    async with httpx.AsyncClient() as client:
        r = await client.patch(f"{HUBSPOT_BASE_URL}/crm/v3/objects/deals/{deal_id}", headers={"Authorization": f"Bearer {HUBSPOT_API_KEY}"}, json={"properties": [{"name": "dealstage", "value": dealstage}]})
        return r.json()

async def amain():
    from mcp.server.stdio import stdio_server
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(amain())
