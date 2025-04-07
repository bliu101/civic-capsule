from llmproxy import generate, pdf_upload
from buttons import use_skills

def activity_command(message, user):
    content = message[len('!activity'):].strip().lower()
            
    if content == 'local elections':
        print("Local Elections")
    if content == 'petitions':
        print("Petitions")
        
    if content == 'community events':
        print("Community Events")

    if content == 'volunteering opportunities':
        print("Volunteering Opportunities")
        use_skills(user)
