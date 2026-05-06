"""HubSpot API Helper for Claude"""
import os
import httpx
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("HUBSPOT_API_KEY")
BASE_URL = "https://api.hubapi.com"

def search_contacts(query, limit=10):
    """Search contacts"""
    response = httpx.post(
        f"{BASE_URL}/crm/v3/objects/contacts/search",
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={"query": query, "limit": limit}
    )
    return response.json()

def search_deals(stage, limit=10):
    """Search deals by stage"""
    response = httpx.post(
        f"{BASE_URL}/crm/v3/objects/deals/search",
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={"filterGroups": [{"filters": [{"propertyName": "dealstage", "operator": "EQ", "value": stage}]}], "limit": limit}
    )
    return response.json()

def update_deal(deal_id, properties):
    """Update a deal"""
    props = [{"name": k, "value": v} for k, v in properties.items()]
    response = httpx.patch(
        f"{BASE_URL}/crm/v3/objects/deals/{deal_id}",
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={"properties": props}
    )
    return response.json()

def create_contact(email, firstname=None, lastname=None):
    """Create a contact"""
    props = [{"name": "email", "value": email}]
    if firstname:
        props.append({"name": "firstname", "value": firstname})
    if lastname:
        props.append({"name": "lastname", "value": lastname})
    response = httpx.post(
        f"{BASE_URL}/crm/v3/objects/contacts",
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={"properties": props}
    )
    return response.json()

if __name__ == "__main__":
    # Test it
    print("Testing HubSpot API...")
    result = search_contacts("test")
    print(f"Found {result.get('total', 0)} contacts")
