import base64
from flask import Blueprint, g, json, jsonify, request
import os;
import requests
from app.web.tasks.parse_ticket import parse_ticket

bp = Blueprint('integrated', __name__, url_prefix='/api/integration')

@bp.route("/jira", methods=["POST"])
def create_jira():
    email=os.getenv("EMAIL")
    token=os.getenv("ATLASSIAN_API_TOKEN")
    jira_url= os.getenv("JIRA_URL")
    # Encode credentials
    credentials = f"{email}:{token}"
    encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
    payload = request.get_json()
    # API endpoint
    print(jira_url)
    url = f"{jira_url}/rest/api/3/issue/"

    # Headers
    headers = {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/json"
    }
    # Make the API request
    ticket_payload = parse_ticket(payload["ticket"])
    print(ticket_payload)
    response = requests.post(url, headers=headers, data=json.dumps(ticket_payload))

    # Check the response
    if response.status_code == 201:
        return jsonify({"message": "Story created successfully!", "data": response.json()}), 201
    else:
        return jsonify({"message": "Failed to create story", "error": response.text}), response.status_code
