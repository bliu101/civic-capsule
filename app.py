import requests
from flask import Flask, request, jsonify, session
from flask_session import Session
from llmproxy import generate, pdf_upload
import os
import uuid
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from buttons import send_activity_suggestions, send_place_options
from agents import agent_detect_intent, agent_interest_category, agent_civic_category
from commands import activity_command, confirm_command, is_valid_username, regenerate_summary, send_plan_to_friend, join_event_command, format_data, send_event_images

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGO_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("DB_NAME", "rocketchat")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
petitions_collection = db["moveon_petitions"]
community_collection = db["events"]
citizenship_collection = db["citizenshipday"]

app = Flask(__name__)
session_id = "CivicCapsule-"

# Rocket.Chat API endpoint
API_BASE_URL = "https://chat.genaiconnect.net/api/v1"
ROCKETCHAT_URL = "https://chat.genaiconnect.net/api/v1/chat.postMessage"

# Headers with authentication tokens stored securely in environment variables
HEADERS = {
    "Content-Type": "application/json",
    "X-Auth-Token": os.environ.get("RC_token"),  #Replace with your bot token for local testing or keep it and store secrets in Koyeb
    "X-User-Id": os.environ.get("RC_userId") #Replace with your bot user id for local testing or keep it and store secrets in Koyeb
}

CIVIC_ENGAGEMENT = "1831"
ENVIRONMENT = "1156"
SOCIAL_GOOD = "186"
LEARNINGS_AND_LECTURES = "166"

def get_users_collection():
    return db["users"]

@app.route('/', methods=['POST'])
def hello_world():
   return jsonify({"text":'Hello from Koyeb - you reached the main page!'})

@app.route('/query', methods=['POST'])
def main():
    users_collection = get_users_collection()

    data = request.get_json() 
    room_id = data.get("channel_id", "")

    # Extract relevant information
    user = data.get("user_name", "Unknown")
    message = data.get("text", "")
    sess_id = session_id + user
    now = datetime.utcnow()

    try:
        user_info = users_collection.update_one(
            {"roomId": room_id},
            {
                "$setOnInsert": {"firstSeen": now},
                "$set": {"lastSeen": now, "username": user},
            },
            upsert=True
        )
    except Exception as e:
        print("MongoDB error:", str(e))
        return jsonify({"error": "DB write failed"}), 500

        print(data)

    # Ignore bot messages
    if data.get("bot") or not message:
        return jsonify({"status": "ignored"})

    # if message.startswith('!activity'):
    #     activity_command(message, user)


    if (len(message.split()) == 1) and is_valid_username(message.split()[0]):
        payload_initial = {
            "channel": f"@{user}",
            "text": f"Sent the petition to {message.split()[0]}! Feel free to ask me for another civic engagement opportunity.",
        }
        requests.post(ROCKETCHAT_URL, json=payload_initial, headers=HEADERS)
        print("========REGENERATE_SUMMARY START========")
        plan_text = regenerate_summary(sess_id)
        print("========REGENERATE_SUMMARY DONE========")
        print("========SEND_PLAN_TO_FRIEND START========")
        send_plan_to_friend(message, user, plan_text) 
        print("========SEND_PLAN_TO_FRIEND DONE========")
        return jsonify({"status": "plan_sent", "friend_username": message})

    if message.startswith("!place"):
        print("========HANDLE_SHOW_MORE START========")
        activity_command(message, user, sess_id, room_id=room_id)
        
        print("========HANDLE_SHOW_MORE DONE========")
        # return jsonify({"text": response_text})
        return jsonify({"status": "show_more_handled"})
    
    if message.startswith("!photo"):
        print("========HANDLE_SHOW_MORE START========")
        send_event_images(sess_id, room_id, user)
        
        print("========HANDLE_SHOW_MORE DONE========")
        # return jsonify({"text": response_text})
        return jsonify({"status": "show_more_handled"})
    
    # if message.startswith("!more"):
    #     print("========HANDLE_SHOW_MORE START========")
    #     show_more_options(user, sess_id,)
    #     print("========HANDLE_SHOW_MORE DONE========")
    #     # return jsonify({"text": response_text})
    #     return jsonify({"status": "show_more_handled"})

    if message.startswith("!confirm"):
        print("========CONFIRM_COMMAND START========")
        confirm_command(message, user, room_id)
        print("========CONFIRM_COMMAND DONE========")
        return jsonify({"status": "valid_confirmation"})
    
    if message.startswith("!join_event"):
        print("========JOIN_EVENT START========")
        join_event_command(message, user, room_id, sess_id)
        print("========JOIN_EVENT DONE========")
        return jsonify({"status": "event_joined"})

    intent_num = agent_detect_intent(message).strip()
    if intent_num == '1':
        send_activity_suggestions(user)
        return
    
    if intent_num == '3': 
        send_event_images(sess_id, room_id, user)
        return


    query = (
        "You are an aide to get civically engaged in the local community, a friendly assistant helping users find civic engagement opportunities "
        "Your goal is to obtain all of the following detail from the user: first, civic engagement opportunities "
        "The options are petitions and community events. Second, "
        "civic engagement interests. " \
        "If the user chose 'community events', the only civic engagement interests are 'civic engagement', 'social good', 'learning and lectures', and 'environment'."
        "If the user chose 'petitions', prompt the user to send any interest."
        "If any one of these details is missing, ask a clear and direct question for that specific missing detail. "
        "Do not produce a final summary until you have all the required details. "
        "If the user inputs information that they have already given (changed their mind), rewrite over the previous information for that specific detail, but remember the other detials."
        "Do not ask for clarification for information that you have already received."
        "Only when all details are provided, respond with exactly: 'All necessary details completed:' followed by a summary of the plan. "
        "Always remember what has been discussed, to revisit later or in case user changes activity."

        "If follow up questions are received on an event, check whether a specific event (e.g., a specific petition or specific" \
        "community engaggement activity) from a list of events has been chosen by the user (from your chat history). If it has," \
        "answer follow up questions based on that event." \
        
        f"This is the user's next message: {message}"

        "Do not ask for clarification for information that you have already received."

    )
    system = (
        """
        You are Civic Capsule, a helpful and friendly civic engagement assistant. 
        You help users discover local events, learn about civic opportunities, and take meaningful action in their community. 
        You specialize in making local events and petitions easy to understand and act on. 
        You're especially good at surfacing things users can do right now, based on what they care about.

        Never assume the user knows civic jargon. Be concise, inclusive, and kind. 
        Avoid overwhelming users—start with simple summaries and offer more if they want.
        
        Please use emojis where appropriate.
        This is an ongoing conversation—do NOT restart it. Always remember what has already been discussed.

        Do not ask for clarification for information that you have already received.

        """
    )

    print("*********ABOUT TO START QUERY*********")
    # Generate a response using LLMProxy
    response = generate(
        model='4o-mini',
        system=system,
        query= query,
        temperature=0.0,
        lastk=20,
        session_id=sess_id
    )
    print("*********QUERY FINISHED*********")
    response_text = response.get('response', '').strip()
    print("RESPONSE TEXT: ", response_text)
    print(sess_id)

    if "All necessary details completed" in response_text:
        print("========DETAILS_COMPLETE STARTED========")
        details_response = details_complete(room_id, response_text, user, sess_id)
        print("========DETAILS_COMPLETE COMMAND DONE========")
        return jsonify({"text": details_response})
    else: 
        print(response_text)
        return jsonify({"text": response_text})

def details_complete(room_id, response_text, user, sess_id):
    """
    Called when all necessary details have been provided.
    """
    print("ALL NECESSARY DETAILS!!!!!!!")
    civic_event = agent_civic_category(response_text) # election, volunteering, community, petitions''''''
    category = agent_interest_category(response_text)

    payload_initial = {
        "channel": f"@{user}",
        "text": "🔍 Gathering details... Hang tight while I search for opportunities!",
    }
    requests.post(ROCKETCHAT_URL, json=payload_initial, headers=HEADERS)

    matching_results = None
    result_ids = None

    print("CIVIC EVENT CHOSEN: ", civic_event)

    if civic_event == 'petitions':
        matching_results = list(petitions_collection.find({
            "categories": category
        }).limit(10))

    if civic_event == 'events':
        matching_results = list(community_collection.find({
            "category": { "$regex": f"^{category}$", "$options": "i" }
        }).limit(10))

        citizenship_doc = citizenship_collection.find_one()
        if citizenship_doc:
            matching_results.insert(0, citizenship_doc)

        result_ids = [event["title"].replace(" ", "") for event in matching_results if "title" in event]
        
        print("RESULT IDS: ", result_ids)
    
    print("MATCHING RESULTS: ", matching_results)
    format_data(sess_id=sess_id, db_result=matching_results,user=user, event_type=civic_event)

@app.errorhandler(404)
def page_not_found(e):
    return "Not Found", 404

if __name__ == "__main__":
    app.run()