
import requests

class Chat:
    def __init__(self, chat_history):
        self.chat_history = chat_history

    def build_request(self):
        request = {}
    
        system_message = {
        "role": "system",
        "content": "You are continuing a conversation about a document. Use the conversation history to answer the user's latest message." 
        }
    
        value = [system_message] + self.chat_history
        request["messages"] = value
        request["max_tokens"] = 500
        request["chat_template_kwargs"] = {"enable_thinking": False}
        return request

    
    def send_request(self, request):
        response = requests.post("http://192.168.10.175:8080/v1/chat/completions", json=request)
        return response

    def chat_with_llm(self):
    
        request = self.build_request()
        response = self.send_request(request)
        data = response.json()
        #print(response.json(scp summarizer.py t14:~/services/local-summarizer/))
        chat_data = data["choices"][0]["message"]["content"]
        response.raise_for_status()

        return chat_data