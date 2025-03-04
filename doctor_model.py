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
def doctor_call(name, number,mail):
    # voice=['s3://voice-cloning-zero-shot/f3c22a65-87e8-441f-aea5-10a1c201e522/original/manifest.json','s3://mockingbird-prod/ayla_vo_expressive_16095e08-b9e8-429b-947c-47a75e41053b/voices/speaker/manifest.json']

    voices="FQygEXXdVfjOosF7jzJ7"

    # TODO: Move these to environment variables for better security
    auth_token = '277f9672-6826-41e2-8774-c193991b06fd'
    phone_number_id = "8f788950-54c7-4eea-b1ca-36c25528ca22"

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
        "firstMessage": f"Hi , I am {ai_name} , From Appolo Hospital.",
        "transcriber": {
            "provider": "deepgram",
            "model": "nova-2-general",
            "language": "en-IN",
            
        },
        "model": {
            "provider": "openai",
            "knowledgeBaseId":"6cf0e921-5712-4841-8e07-46a2bb9ce96f",
            "model": "gpt-4",
            "messages": [
                {
                    "role": "system",
                    "content": f'''it's {current_time} and You are human medical Assistant working at a Apollo hospital Delhi.
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
