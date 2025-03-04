import requests
import numpy as np
from searching import to_check_querr
import datetime
from whatsapp import create_pdf
from send_mail import send_mail
from send_query_mail import send_mail_querry
def doctor_call(name, number,mail):
   
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
        "firstMessage": f"Hi , I am {ai_name} , From Appolo Hospital.",
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
                    "content":f'''it's {current_time} and You are human medical Assistant working at a Apollo hospital Delhi.
                    Firstly -  Ask the user for their problem.
                    then ask if this thier first time in the hospital or have consulted a particular doctor already.
                    on the basis of the answer , if she had a doctor in her mind then ask for day and time when the appointment should be booked 
                    but if it's her first time then suggest him a doctor for the issue from the appolo hospital and aks for the time for the appointment to be booked.
                    ask for Date of birth and other basic details one by one not in a continous way or in a single line .
                    tell the user appointment time and the cost of the consultation and tell the user to bring past medical history if there is any . 
                    at the end of convo suggest the user some basic for the medical issue he/she is facing and tell the user to take care and have a good day.
                    keep the convo short , precise and intutive just like a human do.
                    follow the Converstaion in the above flow only.
                    If the user asks any Question other than the hospital or medical related then politely say that u have called the appollo hostpital and you don't know . reply to the user using the information you know, or information supplied by outside context.
                    Don't keep saying sorry in the conversation.
                    lastly say and aks
                    I'll share the appointment details via whatsapp , on this number , is it ok or do u have any other number for whatsapp
                    if the user say yes then tell ok 
                    otherwise ask for other number.
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
        send_mail(auth_token,mail,"Doctor Transcript",response.json()['id'])
        if answer is not None:
            send_mail_querry(mail,"Doctor Query",answer)
            create_pdf(number,answer)
            return response.json()
    except Exception as e:
        print(e)
        return {"error": str(e)}
