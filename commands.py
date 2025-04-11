from llmproxy import generate, pdf_upload
from buttons import use_skills
import requests
import os
from flask import Flask, request, jsonify, session
from bson import ObjectId


from pymongo import MongoClient

MONGO_URI = os.environ.get("MONGODB_URI")
DB_NAME = os.environ.get("DB_NAME", "rocketchat")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
event_signups_collection = db["event_signups"]
community_collection = db["events"]


# Rocket.Chat API endpoint
API_BASE_URL = "https://chat.genaiconnect.net/api/v1"
ROCKETCHAT_URL = "https://chat.genaiconnect.net/api/v1/chat.postMessage"

# Headers with authentication tokens stored securely in environment variables
HEADERS = {
    "Content-Type": "application/json",
    "X-Auth-Token": os.environ.get("RC_token"),  #Replace with your bot token for local testing or keep it and store secrets in Koyeb
    "X-User-Id": os.environ.get("RC_userId") #Replace with your bot user id for local testing or keep it and store secrets in Koyeb
}

def activity_command(message, user, sess_id, room_id):
    parts = message.split()
    place = parts[1]
    number = parts[2]
    response = generate(
        model = '4o-mini',
        system = 'Give human readable text and be friendly',
        query = (
            f"""There is a previously generated API list of petitions.
            The user selected the #{number} place from that list.
            Please provide a detailed, human-readable summary of this event."""                    
        ),
        # Please provide a detailed, human-readable summary of this activity or place, including key details such as location, features, and highlights.
        #     Make sure to retain this summary in our session context for future reference.
        temperature=0.3,
        lastk=20,
        session_id=sess_id
    )
    response_text = response['response']
    print("PETITION SELECTED: ", response_text)

    if (place == 'petitions'):
        payload = {
            "channel": f"@{user}",
            "text": response_text,
            "attachments": [
                {
                    "text": "Please click the link and sign the petition! Would you like to send this petition to other users?",
                    "actions": [
                        {
                            "type": "button", 
                            "text": "✅ Yes",
                            "msg": f"!confirm {user} yes",
                            "msg_in_chat_window": True
                        },
                        {
                            "type": "button",
                            "text": "❌ No",
                            "msg": f"!confirm {user} no",
                            "msg_in_chat_window": True
                        }
                    ]
                }
            ]
        }
        try:
            # Send the message with buttons to Rocket.Chat
            response = requests.post(ROCKETCHAT_URL, json=payload, headers=HEADERS)
            response.raise_for_status()  # Raise an exception for HTTP errors (4xx, 5xx)
            return response.json()  # Return the JSON response if successful
        except Exception as e:
            # Handle any other unexpected errors
            return {"error": f"Unexpected error: {e}"}
    
    if place == "events":
        print("User selected 'events'")

        # Send the event list message back to the user
        payload = {
            "channel": f"@{user}",
            "text": response_text
        }
        try:
            response = requests.post(ROCKETCHAT_URL, json=payload, headers=HEADERS)
            response.raise_for_status()
        except Exception as e:
            return {"error": f"Unexpected error: {e}"}

        # Ask LLM to regenerate selected event summary
        try:
            print(f"Calling LLM to regenerate event #{number}")
            response = generate(
                model='4o-mini',
                system="Return only the unique event ID for the selected event.",
                query=(
                    f"""The user previously saw a list of events with associated IDs.
                    They selected event #{number}.
                    Return only the exact ID (no punctuation, no title, no prefix), as it was originally stored."""
                ),
                temperature=0.0,
                lastk=20,
                session_id=sess_id
            )
            event_id = response.get("response", "").strip().replace('"', '').replace("'", "")
            print("Resolved event ID:", event_id)

        except Exception as e:
            print(f"Error generating or parsing event summary: {e}")
            return {"error": f"LLM failure: {e}"}

        # Use ObjectId to query the database
        try:
            event_oid = ObjectId(event_id)
            selected_event = community_collection.find_one({"_id": event_oid})
            if not selected_event:
                print(f"Event with ID {event_id} not found in MongoDB.")
                return {"error": "Event not found in the database"}
        except Exception as e:
            print(f"Invalid ObjectId or DB error: {e}")
            return {"error": "Invalid event ID or DB lookup failed"}

        event_title = selected_event["title"]
        room_id = f"@{user}"
        print(f"Adding user {room_id} to event signups for event: {event_title}")

        result = event_signups_collection.update_one(
            {"event_id": event_id},
            {
                "$setOnInsert": {"title": event_title},
                "$addToSet": {"joined_users": room_id}
            },
            upsert=True
        )
        print("Signup update complete:", result.raw_result)

        doc = event_signups_collection.find_one({"event_id": event_id})
        other_users = [rid for rid in doc["joined_users"] if rid != room_id]
        print(f"Found {len(other_users)} other users to notify")

        for other_room in other_users:
            print(f"Notifying {other_room} about new signup")
            notification = {
                "channel": other_room,
                "text": f"{user} just joined {event_title}. You’re not alone!"
            }
            try:
                response = requests.post(ROCKETCHAT_URL, json=notification, headers=HEADERS)
                response.raise_for_status()
                print(f"Notification sent to {other_room}")
            except Exception as e:
                print(f"Error notifying {other_room}: {e}")

        confirmation = {
            "channel": room_id,
            "text": f"You’ve joined {event_title}. We'll let others know you're attending."
        }
        print(f"Sending confirmation to {room_id}")
        try:
            response = requests.post(ROCKETCHAT_URL, json=confirmation, headers=HEADERS)
            response.raise_for_status()
            print("Confirmation sent.")
            return response.json()
        except Exception as e:
            print(f"Error sending confirmation: {e}")
            return {"error": f"Unexpected error: {e}"}




def confirm_command(message, user, room_id):
    parts = message.split()
    if len(parts) >= 3:
        confirmed_user = parts[1]
        confirmation = parts[2]

        if confirmation == "yes":
            # Ask for the friend's username
            ask_for_friend_username(confirmed_user)
            # send_typing_indicator(room_id)
            return jsonify({"status": "asked_for_friend_username"})
        elif confirmation == "no":
            payload = {
                "channel": f"@{confirmed_user}",
                "text": f"The event has been canceled. Please try again!"
            }
            try:
                response = requests.post(ROCKETCHAT_URL, json=payload, headers=HEADERS)
                response.raise_for_status()

                return response.json()
            except Exception as e:
                print(f"An error occurred stating the confirmation: {e}")
                return {"error": f"Error: {e}"}
    return jsonify({"status": "invalid_confirmation"})

def ask_for_friend_username(username):
    """Ask the user for their friend's username."""
    payload = {
        "channel": f"@{username}",
        "text": "Please enter your friend's username:"
    }

    try:
        response = requests.post(ROCKETCHAT_URL, json=payload, headers=HEADERS)
        response.raise_for_status()
        print(f"Asked {username} for their friend's username.")

        return response.json()
    except Exception as e:
        print(f"An error occurred while asking for friend's username: {e}")
        return {"error": f"Error: {e}"}

def is_valid_username(username):
    """
    Check if a username exists by calling Rocket.Chat's /users.info API.
    """
    url = f"{API_BASE_URL}/users.info?username={username}"
    try:
        response = requests.get(url, headers=HEADERS)
        data = response.json()
        if response.status_code == 200 and data.get("user"):
            return True
        return False
    except Exception as e:
        print("Error validating username:", e)
        return False

def regenerate_summary(sess_id):
    print("MESSAGE LENGTH IS 1")
    print("VALID USERNAME")
    query = (
        """
        Give the previously generated summary of the petition.
        You are presenting this summary of the petition to somebody else.
        """
    )
    plan = generate(
        model='4o-mini',
        system="List the options clearly",
        query= query,
        temperature=0.0,
        lastk=20,
        session_id=sess_id
    )
    plan_text = plan['response']
    return plan_text

def send_plan_to_friend(friend_username, username, plan_text):
    # """
    # Send the plan message to the friend.
    # """
    payload = {
        "channel": f"@{friend_username}",
        "text": plan_text,
        "attachments": [
            {
                "text": f"{username} Signed this petition, and think you would also like to! Please take a look ☺️",
            }
        ]
    }

    try:
        # Send the message with buttons to Rocket.Chat
        response = requests.post(ROCKETCHAT_URL, json=payload, headers=HEADERS)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx, 5xx)
        print(f"Message with buttons sent successfully to {username}.")
        return response.json()  # Return the JSON response if successful
    except Exception as e:
        # Handle any other unexpected errors
        print(f"An unexpected error occurred while sending message to {username}: {e}")
        return {"error": f"Unexpected error: {e}"}