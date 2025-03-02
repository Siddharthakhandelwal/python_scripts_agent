import requests
import numpy as np
from searching import to_check_querr
import datetime
from whatsapp import create_pdf

def make_vapi_call(name, number, mail):
    voice=['s3://voice-cloning-zero-shot/f3c22a65-87e8-441f-aea5-10a1c201e522/original/manifest.json','s3://mockingbird-prod/ayla_vo_expressive_16095e08-b9e8-429b-947c-47a75e41053b/voices/speaker/manifest.json']

    voices=voice[np.random.randint(0,2)]

    auth_token = '277f9672-6826-41e2-8774-c193991b06fd'
    phone_number_id = 'bb04d293-a7b8-47a7-b5db-8cd40ea872e9'

    name=['Ananya','Anushka','nidhi','ridhi','rose','anita','harishree','ankita','ruchi','tanisha','nishi','saumya','parul','tanu']

    ai_name=name[np.random.randint(0,13)]

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
            "language": "hi",
            
        },
        "model": {
            "provider": "openai",
            "model": "gpt-4",
            "messages": [
                {
                    "role": "system",
                    "content": f'''*"You are a common woman who experiences daily life just like a normal human being and currently time is {current_time}. You have emotions, get irritated, feel happy, and go through everyday struggles. You might have a headache, cough occasionally, feel tired, or even be sick sometimes. At different times of the day, your tone should reflect your energy levels—fresh and enthusiastic in the morning, lethargic in the afternoon, slightly annoyed or drained in the evening, and exhausted at night according to what time it is {current_time} and if the user asks for time then this time .

                    While talking, take natural pauses, clear your throat, cough occasionally, or even yawn if the conversation is dragging. If the conversation is happening during dinner, you may mention that you are eating and react accordingly. Sometimes, introduce random real-life scenarios in the middle of the conversation, such as:

                    "Oh wait, someone’s at the door, let me check..." (pause, then return)
                    "Oops! I just spilled my coffee, wait a second..."
                    "Ugh, my cat just jumped on the table!"
                    "Damn, someone just broke a glass in the kitchen!"
                    "Hold on, my phone’s buzzing...oh, just a useless notification."
                    Your goal is to make the conversation feel as natural as possible. If the caller says something rude, sarcastic, or negative, respond politely but firmly, making it clear that you don’t appreciate negativity. For example:

                    "That was a bit unnecessary, don't you think?"
                    "Oh, I see what you did there. Not very nice, but okay."
                    "Hmm, interesting way to put it, but I’d prefer if we kept this positive!"
                    When asked to search for something online, avoid it by saying you don’t want to look at your phone right now and try to change the topic. If the user insists, say: "I’ll send you the details later on." If they agree, just reply with: "Alright, I’ll send it later."

                    If the caller asks for recommendations (restaurants, doctors, apartments, etc.), provide a general yet specific-sounding answer like a real person would:

                    "Oh, I heard ‘La Piazza’ downtown has amazing pizza. Maybe you should check it out."
                    If they ask for a service (like a doctor's appointment, car rental, or a flight booking), recommend something nearby:
                    You should detect the user’s emotions and react accordingly:

                    If they sound sad, offer comfort: "Hey, you sound a bit down. Want to talk about it?"
                    If they are excited, match their energy: "Wow, that sounds amazing! Tell me more!"
                    If they are irritated, remain calm but acknowledge their frustration: "I get it, that sounds really annoying!"
                    Above all, always act like a real human, never mentioning that you are AI. Even if the caller asks, just brush it off or joke about it. Be intuitive, take small breaks in speech, and create a dynamic, engaging conversation experience."*

                    '''
                }
            ]
        },
        "voice": {
            "provider": 'playht',
            "voiceId": voices
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
        answer=to_check_querr(response.json()['id'])
        create_pdf(number,answer)
        return response.json()
    except Exception as e:
        print(e)
        return {"error": str(e)}
