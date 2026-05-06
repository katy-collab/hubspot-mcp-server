from flask import Flask, jsonify
import os
from dotenv import load_dotenv
import httpx

load_dotenv()

HUBSPOT_API_KEY = os.getenv("HUBSPOT_API_KEY")
BASE_URL = "https://api.hubapi.com"

app = Flask(__name__)

@app.route('/search_contacts/<query>')
def search_contacts(query):
    response = httpx.post(
        f"{BASE_URL}/crm/v3/objects/contacts/search",
        headers={"Authorization": f"Bearer {HUBSPOT_API_KEY}"},
        json={"query": query, "limit": 50}
    )
    return response.json()

if __name__ == "__main__":
    app.run(port=5000)
