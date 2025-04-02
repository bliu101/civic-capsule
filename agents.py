from llmproxy import generate

def agent_detect_intent(query):
    '''
    Uses LLM to detect intent.
    "1": Introduction message
    "2": all other messages
    '''
    query = (f"""
                You are determining whether the user is starting a chat by greeting or asking what can be done. 
                Analyze the following message: {query}.
                Respond with a single number and just a single number. Respond with '1'
                if the user is greeting or asking 'what do you do?'.
                
                Otherwise, return '2'.
            """)
    intent_response = generate(
        model='4o-mini',
        system=(
            "You are an intent detection assistant. "
            "Analyze the following user message and return a single number: "
            "return '1' if the user is greeting or questioning your purpose, and '2' otherwise." 
            "Be very sparing in returning '1', in most instances you will return '2'"       
        ),
        query=query,
        temperature=0.0,
        lastk=1,
        session_id="intent_detector"
    )

    if isinstance(intent_response, dict):
        intent = intent_response.get('response', '').strip()
    else:
        intent = intent_response.strip()
    print(f"Detected intent: {intent}")
    return intent
