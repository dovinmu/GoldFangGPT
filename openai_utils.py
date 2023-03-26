import requests
import json
import os
from pathlib import Path
import random

with open('openai-keys.json') as f:
    openai = json.loads(f.read())
    OPENAI_API_KEY=openai['key']
    
models = {
    'paragraph-tag':  'gpt-4',
    'paragraph-summary': 'gpt-4'
}
MODEL = "gpt-3.5-turbo"
def query_openai(prompt: str, prompt_system: str = '', model = "default", max_tokens=500, debug=False, debug_system=False, temp=0.8):
    # March 17, 2023 version
    if model == "default":
        model = MODEL
    if model in set('gpt-4, gpt-4-0314, gpt-4-32k, gpt-4-32k-0314, gpt-3.5-turbo, gpt-3.5-turbo-0301'.split(', ')):
        endpoint = 'v1/chat/completions'
        prompt =  { "messages": [ { "role": "system", "content": prompt_system }, { "role": "user", "content": prompt } ]}
    else:
        raise Error("only chat completions supported")
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {OPENAI_API_KEY}'
    }
    data = {"model": model, **prompt,
            "temperature": temp, 
            "max_tokens": max_tokens
    }
    if debug:
        if debug_system:
            print("~ system prompt:", prompt['messages'][0]['content'])
        print("~ prompt:", prompt['messages'][1]['content'])
    r = requests.post(f'https://api.openai.com/{endpoint}', headers=headers, json=data)
    j = r.json()
    try:
        if 'chat' in endpoint:
            a = j['choices'][0]['message']['content']
        else:
            a = j['choices'][0]['text'].strip()
    except Exception as e:
        print(j)
        raise(e)
    if debug:
        print("~ response:", a, "\n~")
    return a
