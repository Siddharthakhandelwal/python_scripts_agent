import requests

api_key = '277f9672-6826-41e2-8774-c193991b06fd'
file_id = '75592415-b855-4c43-89fa-e35de31b5227'

url = 'https://api.vapi.ai/knowledge-base'
headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
}
data = {
    'name': 'Doctor genral',
    'provider': 'trieve',
    'searchPlan': {
        'searchType': 'semantic',
        'topK': 3,
        'removeStopWords': True,
        'scoreThreshold': 0.7
    },
    'createPlan': {
        'type': 'create',
        'chunkPlans': [
            {
                'fileIds': [file_id],
                'targetSplitsPerChunk': 50,
                'splitDelimiters': ['.!?\n'],
                'rebalanceChunks': True
            }
        ]
    }
}

response = requests.post(url, headers=headers, json=data)

if response.status_code == 201:
    kb_id = response.json().get('id')
    print(f'Knowledge Base created successfully. KB ID: {kb_id}')
else:
    print(f'Failed to create Knowledge Base. Status code: {response.status_code}')
    print(response.text)
