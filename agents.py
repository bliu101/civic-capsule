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

def agent_interest_category(message):
    print('IN INTEREST CATEGORY AGENT')    
    query = (
        f'''
        The user provided the following request: ***{message}***.
        Based on this request and the uploaded document, find the closest matching civic engagement interest cateogry.
        The category **must** be explicitly listed in the following based on the civic engagement opportunity
        they chose (local election, petitions, community events, volunteering opportunities):

        If their chosen civic engagement opportunity is "local election":
            Return "".
        
        If their chosen civic engagement opportunity is "volunteering opportunities":
            The categories are:
            "Advocacy & Human Rights",
            "Animals",
            "Arts & Culture",
            "Board Development",
            "Children & Youth",
            "Community",
            "Computers & Technology",
            "Crisis Support",
            "Disaster Relief",
            "Education & Literacy",
            "Emergency & Safety",
            "Employment",
            "Environment",
            "Faith-Based",
            "Health & Medicine",
            "Homeless & Housing",
            "Hunger",
            "Immigrants & Refugees",
            "International",
            "Justice & Legal",
            "LGBTQ+",
            "Media & Broadcasting",
            "People with Disabilities",
            "Politics",
            "Race & Ethnicity",
            "Seniors",
            "Sports & Recreation",
            "Veterans & Military",
            "Families",
            "Women"
            Respond **only** with the exact category name from the above. Do not add any extra text.

        If their chosen civic engagement opportunity is "community events":
            The categories are:
            "Civic Engagement",
            "Environment and Green Living",
            "Learnings and Lectures",
            "Social Good"
            Respond **only** with the exact category name from the above. Do not add any extra text. 

        If their chosen civic engagement opportunity is "petitions":
            The categories are:
            "civil rights", "corporate", "economy", "education",
            "environment", "foreign policy", "government reform", "gun_control", "healthcare", 
            "immigration", "justice", "social services", "womens rights".
            Respond **only** with the exact category name from the above. Do not add any extra text. 
        '''
    )

    system_prompt = """
        You are an assistant that extracts the closest matching category from the query.
        - The category **must** be listed in the query with the user's chosen civic engagement opportunity.
        - Do not infer or create new categories. Paste the exact category name.
        - Respond with only the category name, exactly as it appears in the document.
    """

    response = generate(
        model='4o-mini',
        system=system_prompt,
        query=query,
        temperature=0.0,
        lastk=1,
        session_id="interest_agent",
    )
    
    # Extract the category from the LLM response.
    category = response.get('response', '').strip()
    print("Determined activity category:", category)
    return category

def agent_civic_category(message):
    print('IN CIVIC CATEGORY AGENT')    
    query = (
        f'''
        The user provided the following request: ***{message}***.
        Based on this request and the uploaded document, find the civic enagemnt activity.
        The category **must** be explicitly listed in the following based on the civic engagement activity
        they chose (local election, petitions, community events, volunteering opportunities):

        If their chosen civic engagement activity is "local election":
            Return "election".
        
        If their chosen civic engagement activity is "volunteering opportunities":
            Return "volunteering".

        If their chosen civic engagement activity is "community events":
            Return "events"

        If their chosen civic engagement opportunity is "petitions":
            Return "petitions" 
        '''
    )

    system_prompt = """
        You are an assistant that extracts the activity from the query.
        - Do not infer or create new activities. Paste the exact activity name.
        - Respond with only the specified name, exactly as it appears in the document.
    """

    response = generate(
        model='4o-mini',
        system=system_prompt,
        query=query,
        temperature=0.0,
        lastk=1,
        session_id="civic_agent",
    )
    
    # Extract the activity from the LLM response.
    activity = response.get('response', '').strip()
    print("Determined activity activity:", activity)
    return activity