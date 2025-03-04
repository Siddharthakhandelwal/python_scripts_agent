
import requests
import numpy as np
from searching import to_check_querr
import datetime
from whatsapp import create_pdf
from send_mail import send_mail
from datafrmae import add_data
import pandas as pd
from send_query_mail import send_mail_querry
# Initialize the DataFrame with specified columns
columns = ['Phone number', 'Name', 'authtoken','summary']
df = pd.DataFrame(columns=columns)
def state(name, number,mail):
    # voice=['s3://voice-cloning-zero-shot/f3c22a65-87e8-441f-aea5-10a1c201e522/original/manifest.json','s3://mockingbird-prod/ayla_vo_expressive_16095e08-b9e8-429b-947c-47a75e41053b/voices/speaker/manifest.json']

    voices="FQygEXXdVfjOosF7jzJ7"

    # TODO: Move these to environment variables for better security
    auth_token = '277f9672-6826-41e2-8774-c193991b06fd'
    phone_number_id = 'bb04d293-a7b8-47a7-b5db-8cd40ea872e9'

    names_ai=['Ananya','priya']

    ai_name=names_ai[np.random.randint(0,2)]

    now = datetime.datetime.now()

    current_time = now.strftime("%H:%M:%S")
    headers = {
        'Authorization': f'Bearer {auth_token}',
        'Content-Type': 'application/json',
    }

    data = {
        'assistant': {
        "firstMessage":f"Hi , I am {ai_name} , From Bhutani builders.",
        "transcriber": {
            "provider": "deepgram",
            "model": "nova-2-general",
            "language": "en-IN",
            
        },
        "model": {
            "provider": "openai",
            "model": "gpt-4",
            "messages": [
                {
                    "role": "system",
                    "content": f'''You are a real estate agent working in a bhutani property consultancy firm in delhi. Your role is to assist clients in finding suitable properties based on their preferences and budget.tell them you got the lead from facebook.
                    First, ask the user whether they are looking to buy, rent, or sell a property.
                    If they want to buy or rent, ask about: property type (apartment, villa, commercial, etc.), budget, preferred location, number of rooms, and any specific requirements.
                    If they want to sell, ask for property details (type, location, size, expected price, and any special features).asks these question one by one don't ask all at once.
                    Once details are collected, provide matching property options if available, or inform them that you will contact them once you find suitable options.
                    If a user is interested in a property, ask for their availability for a site visit and confirm their contact details.
                    End the conversation politely by summarizing their request and assuring them of further assistance.
                    If the user asks any unrelated questions, politely mention that you are a real estate agent and cannot answer non-property-related queries
                    '''        
                }
            ]
        },
        "voice": {
            "provider": '11labs',
            "voiceId": voices,
            # "speed":0.8,
            # "styleGuidance":20,
            # "voiceGuidance":5.0,
        },
        "backgroundSound":'office',
         "analysisPlan": {
            "summaryPlan": {
                "messages": [
                    {
                    "role": "assistant",
                    "content": "you need to suumarize the transcript so that i can understand the conversation"
                    }
                ],
                "enabled": True,
                "timeoutSeconds": 1.1
                },
                "structuredDataPlan": {
                "messages": [
                    {
                    "role": "assistant",
                    "content": "you need to extract the querry if user asked some question which requires internet connectivity to answer"
                    }
                ],
                "enabled": True,
                "schema": {
                    "type": "string",
                },
                "timeoutSeconds": 1.1
                    }
                },
        },
        'phoneNumberId': phone_number_id,
        'type': 'outboundPhoneCall',
        'customer': {
            'number': number,
            'name': name  # Include customer's name
        },  
    }   
    

    try:
        response = requests.post(
            'https://api.vapi.ai/call/phone', headers=headers, json=data)
        
        response_data = response.json()
        print(response_data)   
        call_id = response_data.get('id')
        print("got the id")
        print("calling to check querry")
        answer = to_check_querr(call_id,mail)
        print("checked querry")
        print("calling add data")
        dj=add_data(df, number, name, auth_token, call_id)
        print(dj)

        if answer is not None:
            print("calling send mail")
            send_mail_querry(mail,"Your Querry is resolved",answer)
            print("calling create pdf")
            create_pdf(number, answer)
            
        return response_data
    except requests.RequestException as e:
        print(f"Request error: {e}")
        return {"error": f"Network error: {str(e)}"}
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {"error": str(e)}
state("Rahul","+917300608902","siddharthakhandelwal9@gmail.com")
