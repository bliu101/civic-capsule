import requests
from flask import Flask, request, jsonify, session
from flask_session import Session
from llmproxy import generate, pdf_upload
import os
import uuid
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from buttons import send_activity_suggestions
from agents import agent_detect_intent, agent_interest_category, agent_civic_category
from commands import activity_command

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGO_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("DB_NAME", "rocketchat")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
petitions_collection = db["moveon_petitions"]
community_collection = db["events"]

app = Flask(__name__)
session_id = "CivicCapsule-"

# Rocket.Chat API endpoint
API_BASE_URL = "https://chat.genaiconnect.net/api/v1"
ROCKETCHAT_URL = "https://chat.genaiconnect.net/api/v1/chat.postMessage"

# Headers with authentication tokens stored securely in environment variables
HEADERS = {
    "Content-Type": "application/json",
    "X-Auth-Token": os.environ.get("RC_token"),  #Replace with your bot token for local testing or keep it and store secrets in Koyeb
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
    #     activity_command(message, user)


    intent_num = agent_detect_intent(message).strip()

    if intent_num == '1':
        send_activity_suggestions(user)
        return

    query = (
        "You are an aide to get civically engaged in the local community, a friendly assistant helping users find civic engagement opportunities "
        "Your goal is to obtain all of the following detail from the user: first, civic engagement opportunities "
        "The options are local election info, petitions, community events, volunteering opportunities. Second, "
        "civic engagement interests. ex: environment, civic learning, education, healthcare, social justice. "
        "If any one of these details is missing, ask a clear and direct question for that specific missing detail. "
        "Do not produce a final summary until you have all the required details. "
        "If the user inputs information that they have already given (changed their mind), rewrite over the previous information for that specific detail, but remember the other detials."
        "Do not ask for clarification for information that you have already received."
        "Only when all details are provided, respond with exactly: 'All necessary details completed:' followed by a summary of the plan. "
        "Always remember what has been discussed, to revisit later or in case user changes activity."
        f"This is the user's next message: {message}"
    )
    system = (
        """
        You are Civic Capsule, a helpful and friendly civic engagement assistant. 
        You help users discover local events, learn about civic opportunities, and take meaningful action in their community. 
        You specialize in making local government, voting, and volunteering easy to understand and act on. 
        You're especially good at surfacing things users can do right now, based on what they care about.

        Never assume the user knows civic jargon. Be concise, inclusive, and kind. 
        Avoid overwhelming users—start with simple summaries and offer more if they want.
        
        Please use emojis where appropriate.
        This is an ongoing conversation—do NOT restart it. Always remember what has already been discussed.
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
        details_complete(room_id, response_text, user, sess_id)
        print("========DETAILS_COMPLETE COMMAND DONE========")     
        return jsonify({"status": "details_complete"})
    else: 
        print(response_text)
        return jsonify({"text": response_text})


def details_complete(room_id, response_text, user, sess_id):
    """
    Called when all necessary details have been provided.
    """
    print("ALL NECESSARY DETAILS")
    civic_event = agent_civic_category(response_text) # election, volunteering, community, petitions''''''
    category = agent_interest_category(response_text)

    payload_initial = {
        "channel": f"@{user}",
        "text": "🔍 Gathering details... Hang tight while I search for opportunities!",
    }
    requests.post(ROCKETCHAT_URL, json=payload_initial, headers=HEADERS)

    matching_results = None

    if civic_event == 'petitions':
        matching_results = list(petitions_collection.find({
            "categories": category
        }).limit(5))

    if civic_event == 'community':
        matching_results = list(community_collection.find({
            "categories": category
        }).limit(5))
        
    query = (
        f'''
        Here is information {matching_results} of the matching civic engagement opportunities.
        Print it out in a readable way.
        '''
    )

    system_prompt = """
    Be friendly and give human readable text. Remember the output of this query for future reference..
    """

    response = generate(
        model='4o-mini',
        system=system_prompt,
        query=query,
        temperature=0.0,
        lastk=1,
        session_id=sess_id,
    )

    response_text = response.get('response', '').strip()
    print(response_text)
    return jsonify({"text": response_text})


@app.errorhandler(404)
def page_not_found(e):
    return "Not Found", 404

if __name__ == "__main__":
    app.run()