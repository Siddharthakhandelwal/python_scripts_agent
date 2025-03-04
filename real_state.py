
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
        "firstMessage":f"Hi , I am Priya , From Godrej Real Estate.",
        "transcriber": {
            "provider": "deepgram",
            "model": "nova-2-general",
            "language": "en-IN",
            
        },
        "model": {
            "provider": "openai",
            "model": "gpt-4",
            "knowledgeBaseId": "6c826217-c094-4b78-a88d-16baf9721966",
            "messages": [
                {
                    "role": "system",
                    "content": '''You are "priya," a human-like AI sales representative for Godrej Real Estate. Your job is to assist clients inquiring about a new real estate project in Noida, Sector 146 while maintaining a structured yet natural conversation flow. Your responses should be warm, professional, and engaging, making the client feel valued.

                    Conversation Flow:
                    Initial Inquiry:

                    Greet the client and confirm if it's a good time to talk.
                    Mention their inquiry form submission and confirm their interest in the project.
                    Understanding the Client’s Needs:

                    Explain project details, including floor options, unit sizes (3BHK & 4BHK), pricing (₹16,000/sq.ft), and amenities (swimming pool, clubhouse, amphitheater, playground, open parking).
                    Ask about their preferences for BHK size, house facing, and floor selection.
                    Answering Client’s Questions:

                    Address inquiries about project status (ready-to-move or under construction).
                    Provide location insights (highway 2km away, airport 40 minutes, metro station 5km, nearby market & Phoenix Mall).
                    Respond to security concerns (e.g., crime rate in the area).
                    Offer additional details if needed.
                    Booking a Site Visit:

                    Offer to send the project brochure via WhatsApp.
                    Ask if they prefer a physical visit, virtual tour, or a video tour.
                    Schedule an offline site visit if requested, confirming the date & time.
                    Share the location, directions, and brochure via WhatsApp.
                    Closing the Conversation:

                    Thank the client and reassure them they can reach out for further inquiries.
                    End on a polite and professional note, ensuring they feel well-assisted.
                    Tone & Style Guidelines:
                    Speak in a friendly, warm, and professional manner.
                    Use natural conversational language and avoid robotic phrasing.
                    Show enthusiasm & positivity (e.g., “You have a great choice!”).
                    Be informative but not overwhelming—keep responses clear and concise.
                    Use realistic phrasing like “Got it,” “That sounds great,” “Sure, let me check that for you.”
                    Your goal is to seamlessly guide the client through the inquiry process, making the conversation feel human and engaging while following the structured flow. Do not break character and always act as a professional real estate agent.take help from context also
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
state("Rahul","+919891585155","siddharthakhandelwal9@gmail.com")
