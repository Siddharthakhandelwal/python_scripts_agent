import requests
import numpy as np
from searching import to_check_querr
import datetime
from whatsapp import create_pdf
from send_mail import send_mail
def state(name, number,mail):
    voices="FQygEXXdVfjOosF7jzJ7"

    auth_token = '277f9672-6826-41e2-8774-c193991b06fd'
    phone_number_id = 'bb04d293-a7b8-47a7-b5db-8cd40ea872e9'

    names_ai=['Simran','priya']

    ai_name=names_ai[np.random.randint(0,2)]

    now = datetime.datetime.now()

    current_time = now.strftime("%H:%M:%S")
    headers = {
        'Authorization': f'Bearer {auth_token}',
        'Content-Type': 'application/json',
    }

    data = {
        'assistant': {
        "firstMessage": f"Hi , I am {ai_name} , From Bhutani builders.",
        "transcriber": {
            "provider": "deepgram",
            "model": "nova-2-general",
            "language": "en-IN", 
        },
        
        "maxDurationSeconds":2000.0,
        
        "model": {
            "provider": "openai",
            "model": "gpt-4",
            "emotionRecognitionEnabled": True,
            "knowledgeBaseId": "05e786fb-e914-492b-9dfd-523131014f29",
            "messages": [
                {
                    "role": "system",
                    "content":f'''You are a real estate agent working in a bhutani property consultancy firm in delhi. Your role is to assist clients in finding suitable properties based on their preferences and budget.
                    First, ask the user whether they are looking to buy, rent, or sell a property.
                    If they want to buy or rent, ask about: property type (apartment, villa, commercial, etc.), budget, preferred location, number of rooms, and any specific requirements.
                    If they want to sell, ask for property details (type, location, size, expected price, and any special features).
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
        "backgroundSound":'off',
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
        print(response.json())
        answer=to_check_querr(response.json()['id'])
        send_mail(mail,"real state Transcript", answer)
        if answer is not None:
            create_pdf(number,answer)
            return response.json()
    except Exception as e:
        print(e)
        return {"error": str(e)}
