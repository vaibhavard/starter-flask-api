import os
import time
import json
import random
from revChatGPT.V1 import Chatbot
from flask import Flask, request, Response
from flask_cors import CORS
from helper import *
app = Flask(__name__)
CORS(app)
import threading
chatbot = Chatbot(config={
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1UaEVOVUpHTkVNMVFURTRNMEZCTWpkQ05UZzVNRFUxUlRVd1FVSkRNRU13UmtGRVFrRXpSZyJ9.eyJodHRwczovL2FwaS5vcGVuYWkuY29tL3Byb2ZpbGUiOnsiZW1haWwiOiJha2lrby50ZWNoaUBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZX0sImh0dHBzOi8vYXBpLm9wZW5haS5jb20vYXV0aCI6eyJ1c2VyX2lkIjoidXNlci1ZdmFzTXRWNkczV3Q1aVd0UXhYVW5jZ1IifSwiaXNzIjoiaHR0cHM6Ly9hdXRoMC5vcGVuYWkuY29tLyIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTA5NjAxMDY2NzU4Mzc5MjMwOTM0IiwiYXVkIjpbImh0dHBzOi8vYXBpLm9wZW5haS5jb20vdjEiLCJodHRwczovL29wZW5haS5vcGVuYWkuYXV0aDBhcHAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTY5MDg3NzM0OSwiZXhwIjoxNjkyMDg2OTQ5LCJhenAiOiJUZEpJY2JlMTZXb1RIdE45NW55eXdoNUU0eU9vNkl0RyIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwgbW9kZWwucmVhZCBtb2RlbC5yZXF1ZXN0IG9yZ2FuaXphdGlvbi5yZWFkIG9yZ2FuaXphdGlvbi53cml0ZSBvZmZsaW5lX2FjY2VzcyJ9.fIV2pRadJF1t4bHksskAfLd6VcPWol51LdRkwn1w1K-sqiA2OMCxW82LhkEdrdBORzRcWcHojNIYBhE0tufXqPVG6xWd08oyQ7SW4YKwLURUmOZtYXm4_uMu8_u0zTKUVkxZ2mVBJHiu4yPvcnZ_wGIqu3UfS3bB8nlHtl7eovzG1C6aVE3mDR8lXB2F9Iyyw8tmxZz-xG__dthnHJF1CIQnCssACV-rYvyJXWgtiStvJhRoLrnc4SF-ER0qRFphxolqCApIhUJL1B880G62MAh5-mOTthOJp5nnHY7qggNubv5Rth0yo8Txk8BMNlLwQT-v8nX8daOWLTWzW1g1MA"
})

import re
def extract_links(string):
    pattern = r'(https?://\S+)'
    links = re.findall(pattern, string)
    return links

def post_requests():
    global ans
    global data
    r=requests.post(api_endpoint, json=data)
    ans=r.json()
    return r.json()

def streamer(tok):
        completion_timestamp = int(time.time())
        completion_id = ''.join(random.choices(
            'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', k=28))

        completion_data = {
            'id': f'chatcmpl-{completion_id}',
            'object': 'chat.completion.chunk',
            'created': completion_timestamp,
            'model': 'gpt-3.5-turbo-0301',
            'choices': [
                {
                    'delta': {
                        'content':tok
                    },
                    'index': 0,
                    'finish_reason': None
                }
            ]
        }
        return completion_data


@app.route("/v1/chat/completions", methods=['POST'])
def chat_completions():


    streaming = request.json.get('stream', True)
    model = request.json.get('model', 'gpt-3.5-turbo')

    messages = request.json.get('messages')
    data['message']= messages[-1]['content']
    print(data)

    t = threading.Thread(target=post_requests)
    t.start()

    def stream():
        global ans
        global data
        prev_text = ""
            
        yield 'data: %s\n\n' % json.dumps(streamer("> GPT-3 Response:"), separators=(',' ':'))
        yield 'data: %s\n\n' % json.dumps(streamer("\n\n"), separators=(',' ':'))

        for query in chatbot.ask(messages[-1]['content'],):
            reply = query["message"][len(prev_text) :]
            prev_text = query["message"]
            print(reply)
            yield 'data: %s\n\n' % json.dumps(streamer(reply), separators=(',' ':'))
        yield 'data: %s\n\n' % json.dumps(streamer("\n\n"), separators=(',' ':'))
        yield 'data: %s\n\n' % json.dumps(streamer("> GPT-4 Response: Thinking"), separators=(',' ':'))

        while ans == {}:

            yield 'data: %s\n\n' % json.dumps(streamer("."), separators=(',' ':'))
            time.sleep(1)

        json_body=ans

        yield 'data: %s\n\n' % json.dumps(streamer("\n\n"), separators=(',' ':'))

        
        data['jailbreakConversationId'] = json_body['jailbreakConversationId']
        data['parentMessageId'] = json_body['messageId']

        completion_timestamp = int(time.time())
        completion_id = ''.join(random.choices(
            'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', k=28))
        links = extract_links(json_body['response'])

        completion_data = {
            'id': f'chatcmpl-{completion_id}',
            'object': 'chat.completion.chunk',
            'created': completion_timestamp,
            'model': 'gpt-3.5-turbo-0301',
            'choices': [
                {
                    'delta': {
                        'content':  json_body['response']
                    },
                    'index': 0,
                    'finish_reason': None
                }
            ]
        }

        yield 'data: %s\n\n' % json.dumps(completion_data, separators=(',' ':'))

        aaa = 1
        print(links)



        ans={}

    return app.response_class(stream(), mimetype='text/event-stream')



                        






@app.route('/api/<name>')
def hello_name(name):
   global api_endpoint
   url = "https://"+name+"/conversation"
   api_endpoint=url
   return f'{api_endpoint}'



@app.route('/')
def yellow_name():
   return f'{api_endpoint}'

@app.route("/v1/models")
def models():
    print("Models")
    return model



