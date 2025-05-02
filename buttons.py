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
        #("Local Elections", "🗳️"),
        ("Petitions", "📝"),
        ("Community Events", "🎤")
        # ("Volunteering Opportunities", "🤝"),
    ]
    
    # Build the actions array with improved formatting and optional styling
    actions = []
    for idx, (suggestion, emoji) in enumerate(suggestions):
        actions.append({
            "type": "button",
            "text": f"{emoji} {suggestion.capitalize()}",
            "msg": f"The activity category chosen is: {suggestion}",
            "msg_in_chat_window": True,
            "style": "primary"  # Optional: use "primary", "danger", etc. if supported
        })
    
    payload = {
        "channel": f"@{user}",
        "text": "Hi there I am Civic Capsule! 😊 I'm here to help you find ways to get involved in your community. To get started, could you tell me what civic engagement opportunities you're interested in?",
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

def use_skills(user):
    # Pair each suggestion with an emoji for a more visual presentation
    suggestions = [
        ("Yes", "✅"),
        ("No", "❌"),
    ]
    
    # Build the actions array with improved formatting and optional styling
    actions = []
    for idx, (suggestion, emoji) in enumerate(suggestions):
        actions.append({
            "type": "button",
            "text": f"{emoji} {suggestion.capitalize()}",
            "msg": f"!skills {suggestion}",
            "msg_in_chat_window": True,
            "style": "primary"  # Optional: use "primary", "danger", etc. if supported
        })
    
    payload = {
        "channel": f"@{user}",
        "text": "Would you like to use any relevant job/hobby skills in your volunteering",
        "attachments": [
            {
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

def send_place_options(num, username, options, event_type, text):
    min_num = 4
    if num < 4:
        min_num = num

    print("IN SEND PLACE OPTIONS")
    print("TEXT: ,", text)
    """Send a message with the place options as buttons."""
    payload = {
        "channel": f"@{username}",
        "text": "Gathering places",
    }

    actions = []
    for n in range(1, min_num + 1):
        id = ""
        print('IN THE FOR LOOPS FOR OPTIONS')
        actions.append({
            "type": "button",
            "text": f"{n}",
            "msg": f"!place {event_type} {n} {id}",
            "msg_in_chat_window": True,
            "style": "primary"
        })

    # if  num > 4:
    #     actions.append({
    #         "type": "button",
    #         "text": "🔽 See more options",
    #         "msg": f"!more options",
    #         "msg_in_chat_window": True,
    #         "style": "primary"
    #     })

    payload = {
        "channel": f"@{username}",
        "text": text,
        "attachments": [
            {
                "text": "Which option do you like?",
                "actions": actions
            }
        ]
    }

    try:
        response = requests.post(ROCKETCHAT_URL, json=payload, headers=HEADERS)
        response.raise_for_status()
        print(f"Message with buttons sent to {username}.")
        return response.json()
    except Exception as e:
        print(f"An unexpected error occurred while sending message to {username}: {e}")
        return {"error": f"Unexpected error: {e}"}