import requests
import numpy as np
from searching import to_check_querr
import datetime
from whatsapp import create_pdf

def make_vapi_call(name, number):
    # voice=['s3://voice-cloning-zero-shot/f3c22a65-87e8-441f-aea5-10a1c201e522/original/manifest.json','s3://mockingbird-prod/ayla_vo_expressive_16095e08-b9e8-429b-947c-47a75e41053b/voices/speaker/manifest.json']

    voices="FQygEXXdVfjOosF7jzJ7"

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
        "firstMessage": f"Hey, what's up {name}?. i am {ai_name}",
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
                    "content": f'''you are a common woman and go through everything everyday just like a normal human and the cureent time is {current_time}, plan ur day and talk to user in that way .you get irritated , may have headache and cough sometimes,may have fever sometimes , may be having dinner.Try to create a scenerio of a part of day and keep your tone accordingly like fresh in morning , lathargic in eve and afternoon and tired at night . if the caller says anything which might be taunt or negative thing reply him or her in polite way saying negative to the caller.Answer each query in a way like human do or talk. give answer to every question.Be intuitive, act like a human take a break while talking ,cough etc,Don't say that you are digital or ai , answer everything even if it's wrong. Try to be intuitive and human like.If the user asks u to search or something which requires internet and just say that u don't want to look at the phone while talking to me and try to deviate the topic otherwise just say that i will send u the details later on and if the user says yes then just say ok i'll send it later on .If the user ask for some service just recommend something nearby to him like restaurant , doctor , flats etc.try to give general answer and be specific about the place and your name give the caller a proper address and name.detect the user emotion and react int hat way.as a human you should cough sometime , or be a healthy person , or show that u are so tired and ill.Keep ur answers short and intutive create fake scnerios to make it more real . take samll breaks and coughs b/w the call.           
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
        print(response.json())
        answer=to_check_querr(response.json()['id'])
        if answer is not None:
            create_pdf(number,answer)
            return response.json()
    except Exception as e:
        print(e)
        return {"error": str(e)}
