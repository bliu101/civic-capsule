from llmproxy import generate, pdf_upload
from buttons import use_skills
import requests
import os
from flask import Flask, request, jsonify, session
from bson import ObjectId

from buttons import send_place_options

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGO_URI = os.environ.get("MONGODB_URI")
DB_NAME = os.environ.get("DB_NAME", "rocketchat")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
event_signups_collection = db["event_signups"]

client_timeout = MongoClient(MONGO_URI, serverSelectionTimeoutMS=15000, socketTimeoutMS=15000)
db_timeout = client_timeout[DB_NAME]

# Rocket.Chat API endpoint
API_BASE_URL = "https://chat.genaiconnect.net/api/v1"
ROCKETCHAT_URL = "https://chat.genaiconnect.net/api/v1/chat.postMessage"

# Headers with authentication tokens stored securely in environment variables
HEADERS = {
    "Content-Type": "application/json",
    "X-Auth-Token": os.environ.get("RC_token"),  #Replace with your bot token for local testing or keep it and store secrets in Koyeb
    "X-User-Id": os.environ.get("RC_userId") #Replace with your bot user id for local testing or keep it and store secrets in Koyeb
}

upload_headers = {
    "X-Auth-Token": os.environ.get("RC_token"),  #Replace with your bot token for local testing or keep it and store secrets in Koyeb
    "X-User-Id": os.environ.get("RC_userId") #Replace with your bot user id for local testing or keep it and store secrets in Koyeb
}

def get_event_signups_collection():
    return db["event_signups"]

def activity_command(message, user, sess_id, room_id):
    parts = message.split()
    place = parts[1]
    number = parts[2]
    event_title = parts[3] if len(parts) > 3 else None

    response = generate(
        model = '4o-mini',
        system = 'Give human readable text and be friendly',
        query = (
            f"""There is a previously generated API list of petitions or events (discern which it is from the messages).
            The user selected the #{number} place from that list.
            Please provide a detailed, human-readable summary of this event."""                    
        ),
        # Please provide a detailed, human-readable summary of this activity or place, including key details such as location, features, and highlights.
        #     Make sure to retain this summary in our session context for future reference.
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
            response.raise_for_status()  # Raise an exception for HTTP errors (4xx, 5xx)
            return response.json()  # Return the JSON response if successful
        except Exception as e:
            # Handle any other unexpected errors
            return {"error": f"Unexpected error: {e}"}
    
    if place == "events":
        
        print("User selected 'events'")

        print("attempting to get event signups collection")
        try:
            print("looking for existing results")
            existing_event = event_signups_collection.find_one({"event_title": event_title})
            if not existing_event:
                print("no one registered")
                attendees = []
            else:
                print("found attendees")
                attendees = existing_event.get("attendees", [])

            # Compose attendee list message
            attendee_usernames = [att["username"] for att in attendees]
            if attendee_usernames:
                attendee_text = "People going to this event so far:\n" + "\n".join(f"• @{name}" for name in attendee_usernames)
            else:
                attendee_text = "No one has signed up yet."

        except Exception as e:
            print(f"❌ MongoDB lookup failed: {e}")
            attendee_text = "Unable to load signups right now."


        payload = {
            "channel": f"@{user}",
            "text": f"{response_text}\n\n{attendee_text}",
            "attachments": [
                {
                    "text": "Would you like to join this event?",
                    "actions": [
                        {
                            "type": "button", 
                            "text": "✅ Yes, I'm going!",
                            "msg": f"!join_event {event_title}",
                            "msg_in_chat_window": True
                        },
                        {
                            "type": "button",
                            "text": "❌ No thanks",
                            "msg": f"!decline_event {event_title}",
                            "msg_in_chat_window": True
                        }
                    ]
                }
            ]
        }
        try:
            response = requests.post(ROCKETCHAT_URL, json=payload, headers=HEADERS)
            response.raise_for_status()
            print("✅ Event prompt sent to user.")
        except Exception as e:
            print(f"❌ Failed to send event message: {e}")



def join_event_command(message, user, room_id, sess_id):
    print("JOIN_EVENT_COMMAND")
    print("Message:", message)
    parts = message.split(maxsplit=1)
    if len(parts) < 2:
        return {"error": "Event title missing"}

    event_title = parts[1]
    if event_title == "None" or not event_title:
        event_title = "Boston Citizenship Day 2025"

    try:
        event_doc = event_signups_collection.find_one({"event_title": event_title})
        if not event_doc:
            # First person to join
            event_signups_collection.insert_one({
                "event_title": event_title,
                "attendees": [{"username": user, "room_id": room_id}]
            })
            attendees_to_notify = []
        else:
            # Get current attendees
            attendees = event_doc.get("attendees", [])
            existing_usernames = [a["username"] for a in attendees]

            if user not in existing_usernames:
                event_signups_collection.update_one(
                    {"event_title": event_title},
                    {"$addToSet": {"attendees": {"username": user, "room_id": room_id}}}
                )
                attendees_to_notify = [a for a in attendees if a["username"] != user]
            else:
                print(f"User {user} already registered.")
                attendees_to_notify = []

        # Confirmation to the user
        payload = {
            "channel": f"@{user}",
            "text": f"🎉 You’ve been added to '{event_title}'! We’ll keep you in the loop with others going! Add the event to your calendar:"
        }
        requests.post(ROCKETCHAT_URL, json=payload, headers=HEADERS)

        # Send them an ICS file
        create_calendar_event(sess_id, room_id, user)

        # Notify existing attendees
        for attendee in attendees_to_notify:
            notify_payload = {
                "channel": f"@{attendee['username']}",
                "text": f"👋 @{user} just joined the event **'{event_title}'**! 🎉"
            }
            try:
                requests.post(ROCKETCHAT_URL, json=notify_payload, headers=HEADERS)
                print(f"Notified {attendee['username']} that {user} joined.")
            except Exception as e:
                print(f"Failed to notify {attendee['username']}: {e}")

    except Exception as e:
        print(f"Error joining event: {e}")

def create_calendar_event(sess_id, room_id, user):
    print("Creating calendar event...")
    system_message = (
        "You are an assistant that generates iCalendar (ICS) documents based on previous conversation context. " 
        "Your output must be a valid ICS file conforming to RFC 5545, " 
        "and include only the ICS content without any additional commentary or explanation. " 
        "Ensure you include mandatory fields such as BEGIN:VCALENDAR, VERSION, PRODID, BEGIN:VEVENT, UID, DTSTAMP, " 
        "DTSTART, DTEND, and SUMMARY."
        "Note that no line length should exceed 75 characters."
    )
    query = (f"""
            Using the previously generated event summary from our conversation context, generate a complete and valid iCalendar (ICS) document
            that reflects the event details.
            Name the calendar event based on the activity/place found in the summary.
            Set the location of the calendar event to the address of the location in the summary.
            Set the time of the calendar event to the time of the hangout, using the current date as reference.
            Keep the description brief (less than 60 characters) to comply with ICS file format.
            Output only the ICS content with no extra text.
            Follow valid ICS file format.
            """)
    response = generate(
        model='4o-mini',
        system= system_message,
        query= query,
        temperature=0.0,
        lastk=20,
        session_id=sess_id
    )
    ical_content = response.get('response').strip()
    if ical_content.startswith("```") and ical_content.endswith("```"):
        ical_content = ical_content[3:-3].strip()
    print("Generated ICS content:")
    print(ical_content)

    # Define the upload URL (same for all uploads)
    print("Room ID for file upload:", room_id)
    upload_url = f"{API_BASE_URL}/rooms.upload/{room_id}"
    print("Constructed upload URL:", upload_url)

    # Write the ICS content to a file
    ics_filename = "event.ics"
    print(f"Writing ICS content to file: {ics_filename}")
    ics_content = ical_content.replace("\n", "\r\n")
    ics_content = ics_content.strip()

    lines = ics_content.split("\n")
    cleaned_lines = [line.rstrip() for line in lines]  # Remove trailing whitespace from each line
    ics_content = "\r\n".join(cleaned_lines)

    try:
        with open(ics_filename, "w") as f:
            f.write(ics_content)
        print("ICS file written successfully.")
    except Exception as e:
        print(f"Error writing ICS file: {e}")

    # Read and print the ICS file contents
    try:
        with open(ics_filename, "r") as f:
            file_contents = f.read()
        print("ICS file contents:")
        print(file_contents)
    except Exception as e:
        print(f"Error reading ICS file: {e}")


    # Prepare the file for upload
    try:
        files = {'file': (os.path.basename(ics_filename), open(ics_filename, "rb"), "text/calendar")}
        data = {'description': 'Here is a calendar invitation with your plan!'}
        print("About to send file upload POST request with data:", data)
        print("Headers being used:", HEADERS)
        response_upload = requests.post(upload_url, headers=upload_headers, data=data, files=files)
        print("File upload response status code:", response_upload.status_code)
        print("File upload response text:", response_upload.text)
        if response_upload.status_code == 200:
            print(f"File {ics_filename} has been sent to {user}.")
        else:
            print(f"Failed to send file to {user}. Error: {response_upload.text}")
    except Exception as e:
        print(f"An exception occurred during file upload: {e}")


def send_event_images(sess_id, room_id, user):
    print("Sending images")
    image_filename = "citizenship_day.jpg"
    
    # Define the upload URL (same for all uploads)
    print("Room ID for file upload:", room_id)
    upload_url = f"{API_BASE_URL}/rooms.upload/{room_id}"
    print("Constructed upload URL:", upload_url)

    # Prepare the file for upload
    try:
        files = {'file': (os.path.basename(image_filename), open(image_filename, "rb"), "image/jpeg")}
        data = {'description': '📷 Here are some pictures from the 2025 event!'}
        print("About to send file upload POST request with data:", data)
        print("Headers being used:", HEADERS)
        response_upload = requests.post(upload_url, headers=upload_headers, data=data, files=files)
        print("File upload response status code:", response_upload.status_code)
        print("File upload response text:", response_upload.text)
        if response_upload.status_code == 200:
            print(f"File {image_filename} has been sent to {user}.")
        else:
            print(f"Failed to send file to {user}. Error: {response_upload.text}")
    except Exception as e:
        print(f"An exception occurred during file upload: {e}")

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
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx, 5xx)
        print(f"Message with buttons sent successfully to {username}.")
        return response.json()  # Return the JSON response if successful
    except Exception as e:
        # Handle any other unexpected errors
        print(f"An unexpected error occurred while sending message to {username}: {e}")
        return {"error": f"Unexpected error: {e}"}

def format_data(sess_id, db_result, user, event_type):
    system_message = (
        """You are a friendly assistant that formats database responses as a catalog of choices.
        Given a list of activities, output:
        1. On the first line, list the number of results the API returned.
        2. On the following lines, list each option on its own line and the details.
        3. Make any links clickable hyperlinks.
        4. Take out any excess brackets or asteriks.
        Do not include any extra commentary or headings.
        Make sure to delimit each line with a single (one) newline. Do not add additional unnecessary newline characters.
        Format everything nicely"""
    )
    response = generate(
        model = '4o-mini',
        system = system_message,
        query = (
            f'''The following list of activities was generated from a database call: {db_result}.
            Only print the first 4 to start (if there are 4).
            Please format the output so that:
                - The first line is only the count of items in the list in total (the amount of item that resulted from the API call). No other information or text on this line. Just the number.
                - Immediately after a newline, starting on the second line, list the options with all relevant details and a description.
            Only include the options provided and nothing else.
            Make sure to delimit each line with a single (one) newline. Do not add additional unnecessary newline characters.
            In subsequent requests, refer to these items for any follow-up actions.
            Right now, just show the first 4. Only show more when requested to.'''
        ),
        temperature=0.3,
        lastk=20,
        session_id=sess_id
    )
    response_text = response['response']

    print('nonstripped list')
    print(response_text)

    lines = response_text.splitlines()
    clean_lines = [line.strip() for line in response_text.splitlines() if line.strip()]
    print('LINES:', lines)
    responses_no = int(lines[0].strip())
    options = []
    # Reassemble the output without the first line (the number and its newline)
    if len(lines) > 1:
        print('IN LINES IF STATEMENT')
        options = [opt.strip() for opt in clean_lines[1].split(',')]
        print(options)
        response_text = "\n".join(lines[2:])
    else:
        response_text = ""
    print('LIST OF PLACES GENERATED')
    print(response_text)

    rocketchat_response = send_place_options(responses_no, user, options, event_type, response_text)
    return jsonify({"status": "redo_search"})