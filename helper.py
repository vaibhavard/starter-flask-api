import json
import requests
nline = False
ans={}
model = {
    "data": [
        {
            "id": "gpt-3.5-turbo",
            "object": "model",
            "owned_by": "reversed",
            "tokens": 8192,
            "fallbacks": [
                "gpt-3.5-turbo-16k"
            ],
            "endpoints": [
                "/api/v1/chat/completions"
            ],
            "limits": [
                "2/minute",
                "300/day"
            ],
            "public": True,
            "permission": []
        },

    ],
    "object": "list"
}
python_boolean_to_json = {
  "true": True,
}
data = {
    'jailbreakConversationId':json.dumps(python_boolean_to_json['true']),
    # "clientOptions.promptPrefix":"You are a cute assistant.",
    # "systemMessage":"You are a cute assistant."
}
api_endpoint = "http://7040-182-69-179-37.ngrok-free.app/conversation"
