
from flask import Flask, request, jsonify
import requests
import datetime

app = Flask(__name__)

# Set these before running
NOTION_API_KEY = "your_integration_token_here"
DATABASE_ID = "your_metrics_tracker_database_id_here"

headers = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

def create_notion_entry(data):
    notion_url = "https://api.notion.com/v1/pages"
    
    payload = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "Date": {"date": {"start": data.get("Date")}},
            "HRV": {"number": float(data.get("HRV", 0))},
            "RHR": {"number": float(data.get("RHR", 0))},
            "Steps": {"number": int(data.get("Steps", 0))},
            "Weight": {"number": float(data.get("Weight", 0))},
            "Sleep": {"number": float(data.get("Sleep", 0))},
            "VO2Max": {"number": float(data.get("VO2Max", 0))}
        }
    }
    response = requests.post(notion_url, headers=headers, json=payload)
    return response.status_code, response.json()

@app.route('/health-sync', methods=['POST'])
def receive_data():
    if not request.is_json:
        return jsonify({"error": "Invalid request format"}), 400
    
    data = request.get_json()
    
    # Ensure 'Date' is ISO format
    if "Date" not in data:
        data["Date"] = datetime.datetime.now().date().isoformat()
    
    status, resp = create_notion_entry(data)
    return jsonify({"status": status, "notion_response": resp})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
