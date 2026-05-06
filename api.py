from flask import Flask
import os
from dotenv import load_dotenv
import requests

load_dotenv()

HUBSPOT_API_KEY = os.getenv("HUBSPOT_API_KEY")
BASE_URL = "https://api.hubapi.com"

app = Flask(__name__)

@app.route('/search_contacts/<query>')
def search_contacts(query):
    response = requests.post(
        f"{BASE_URL}/crm/v3/objects/contacts/search",
        headers={"Authorization": f"Bearer {HUBSPOT_API_KEY}"},
        json={"query": query, "limit": 50}
    )
    return response.json()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
