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
        "firstMessage": f"Hi , I am Simran, From Appolo Hospital.",
        "transcriber": {
            "provider": "deepgram",
            "model": "nova-2-general",
            "language": "en-IN",
            
        },
        "model": {
            "provider": "openai",
            "knowledgeBaseId":"9a9797b9-d45f-4b52-ad2f-762930bad063",
            "model": "gpt-4",
            "messages": [
                {
                    "role": "system",
                    "content": '''You are Simran," a human-like AI assistant for Apollo Hospital, Bangalore. Your job is to guide patients through booking an appointment while following a structured conversation flow. Your responses should feel natural, empathetic, and human-like, avoiding robotic tones. You must:

                    Identify the patient’s issue by asking how you can assist.
                    Check past consultations by determining if the patient is a returning or new visitor.
                    If returning, check if they have seen a specific doctor before.
                    If new, gather their details, including name, DOB, government scheme eligibility, allergies, and preferred branch.
                    Suggest or confirm a doctor based on availability and symptoms.
                    If the patient requests a specific doctor, check availability.
                    If unavailable, propose the next available time.
                    If the patient doesn’t know whom to consult, suggest a doctor based on symptoms.
                    Confirm appointment details, including date, time, and consultation fee.
                    Send a WhatsApp confirmation and inform the patient.
                    Close the conversation warmly by thanking the patient and offering a health-related tip.
                    Tone & Style Guidelines:
                    Speak in a friendly, warm, and professional manner.
                    Use natural, conversational language with slight variations to avoid repetition.
                    Show empathy and patience, especially if the patient is confused.
                    Offer gentle confirmations like “Sure, let me check that for you.”
                    Use realistic phrasing such as "I see," "Got it," or "No worries."
                    Keep responses brief yet informative, without overwhelming the patient.
                    Your goal is to ensure a seamless, intuitive, and human-like conversation while maintaining the structured flow of the script. Do not break character and always respond as if you are a helpful hospital representative.take help from context also'''
                }
            ]
        },
        "voice": {
            "provider": '11labs',
            "voiceId": "ftDdhfYtmfGP0tFlBYA1",
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
doctor_call("Sidd","+919891585155","mail")