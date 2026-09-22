import requests

class ChunkAnalyzer:
    def __init__(self, text, user_prompt):
        self.text = text
        self.user_prompt = user_prompt
    def build_request(self):
        request = {}
        system_message = {
        "role": "system",
        "content": "You are performing the preprocessing stage of document analysis."
        "You are receiving one section of a larger document."

        "Extract information from this section that is relevant to the user's request."
        "Do not attempt to answer as though this section represents the entire document."
        "Preserve important facts, findings, arguments, and details that may be useful"
        "when the results from all sections are later synthesized."
        "Do not introduce information not present in this section."
        }
        user_message = {
            "role": "user",
            "content": 
            "User message: \n" + self.user_prompt + "\n\nDocument:\n" +
            self.text
                    
        }
        value = [system_message , user_message]
        request["messages"] = value
        request["max_tokens"] = 500
        request["chat_template_kwargs"] = {"enable_thinking": False}
        return request

    def send_request(self, request):
        response = requests.post("http://192.168.10.175:8080/v1/chat/completions", json=request)
        return response

    def analyze(self):

        request = self.build_request()
        response = self.send_request(request)
        data = response.json()
        #print(response.json(scp summarizer.py t14:~/services/local-summarizer/))
        analisis = data["choices"][0]["message"]["content"]

        return analisis