from llmproxy import generate, pdf_upload
from buttons import use_skills

def activity_command(message, user, sess_id):
    parts = message.split()
    place = parts[1:]
    response = generate(
        model = '4o-mini',
        system = 'Give human readable text and be friendly',
        query = (
            f"""There is a previously generated API list of petitions.
            The user selected the #{place} place from that list.
            Please provide a detailed, human-readable summary of this event."""                    
        ),
        # Please provide a detailed, human-readable summary of this activity or place, including key details such as location, features, and highlights.
        #     Make sure to retain this summary in our session context for future reference.
        temperature=0.3,
        lastk=20,
        session_id=sess_id
    )
    response_text = response['response']

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
