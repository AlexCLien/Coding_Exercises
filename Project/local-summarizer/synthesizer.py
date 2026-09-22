import requests

class Synthesizer:
    def __init__(self, responses, user_prompt):
        self.responses = responses
        self.user_prompt = user_prompt

    def format_response(self):
        formatted_responses = []
        for idx, response in enumerate(self.responses, start=1):
            formating = "Response from section " + str(idx) + ": \n" + response
            formatted_responses.append(formating)
        str_formatted_responses = "\n\n".join(formatted_responses)
    
        return str_formatted_responses
    def build_request(self):
        request = {}
        str_formatted_response = self.format_response()
        system_message = {
        "role": "system",
        "content": "You have all the analysis from all the sections."
        "Synthesize them into one answer to the user's request"
        }
        user_message = {
            "role": "user",
            "content": 
            "User message: \n" + self.user_prompt + "\n\nSection Analysis:\n" +
            str_formatted_response
                    
        }
        value = [system_message , user_message]
        request["messages"] = value
        request["max_tokens"] = 500
        request["chat_template_kwargs"] = {"enable_thinking": False}
        return request
    def send_request(self, request):
        response = requests.post("http://192.168.10.175:8080/v1/chat/completions", json=request)
        return response

    def synthesize(self):
    
        request = self.build_request()
        response = self.send_request(request)
        data = response.json()
        #print(response.json(scp summarizer.py t14:~/services/local-summarizer/))
        synthesized_data = data["choices"][0]["message"]["content"]

        return synthesized_data