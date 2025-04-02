import requests
import os

ROCKETCHAT_URL = "https://chat.genaiconnect.net/api/v1/chat.postMessage"
HEADERS = {
    "Content-Type": "application/json",
    "X-Auth-Token": os.environ.get("RC_token"),
    "X-User-Id": os.environ.get("RC_userId")
}

def send_activity_suggestions(user):
    # Pair each suggestion with an emoji for a more visual presentation
    suggestions = [
        ("Local Elections", "🗳️"),
        ("Petitions", "📝"),
        ("Community Events", "🎤"),
        ("Volunteering Opportunities", "🤝"),
    ]
    
    # Build the actions array with improved formatting and optional styling
    actions = []
    for idx, (suggestion, emoji) in enumerate(suggestions):
        actions.append({
            "type": "button",
            "text": f"{emoji} {suggestion.capitalize()}",
            "msg": f"The activity category chosen is: {suggestion}",
            "msg_in_chat_window": True,
            "style": "primary"  # Optional: use "primary", "danger", etc. if supported
        })
    
    payload = {
        "channel": f"@{user}",
        "text": "Here are some civic engagement category suggestions for you:",
        "attachments": [
            {
                "text": "Please choose one of the following categories:",
                "actions": actions
            }
        ]
    }
    
    try:
        print("Token:", os.environ.get("RC_token"))
        print("User ID:", os.environ.get("RC_userId"))
        response = requests.post(ROCKETCHAT_URL, json=payload, headers=HEADERS)
        response.raise_for_status()
        print(f"Sent activity suggestion buttons to {user}.")
        return response.json()
    except Exception as e:
        print(f"Error sending activity suggestions: {e}")
        return {"error": f"Unexpected error: {e}"}
