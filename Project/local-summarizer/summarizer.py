import requests

def main():
    document = ReadDocument(input("File path: "))
    document_text = document.read_document()
    summarizer = Summarizer(document_text)
    summary = summarizer.summarize()
    print(summary)

class ReadDocument:
    def __init__(self, user_input):
        self.user_input = user_input


    def read_document(self):
        text = open(self.user_input)
        read_text = text.read()
        return read_text
    
class Summarizer:
    def __init__(self, text):
        self.text = text
        
    def build_request(self):
        request = {}
        system_message = {
        "role": "system",
        "content": "You are a document summarizer. "
        "Produce a concise and accurate summary of the provided document. "
        "Prioritize the document's central argument, main ideas, important findings, "
        "and conclusions. Omit minor details, unnecessary examples, and repeated information. "
        "Do not introduce information that is not present in the document. "
        "Organize the summary clearly and use bullet points only when they improve readability. "
        "Prioritize completing the summary cleanly within the available output limit rather "
        "than including every detail."
        }
        user_message = {
            "role": "user",
            "content": "Summarize this document:\n\n" + self.text
        }
        value = [system_message , user_message]
        request["messages"] = value
        request["max_tokens"] = 500
        request["chat_template_kwargs"] = {"enable_thinking": False}
        return request

    def send_request(self, request):
        response = requests.post("http://127.0.0.1:8080/v1/chat/completions", json=request)
        return response

    def summarize(self):

        request = self.build_request()
        response = self.send_request(request)
        data = response.json()
        #print(response.json(scp summarizer.py t14:~/services/local-summarizer/))
        summary = data["choices"][0]["message"]["content"]

        return summary


if __name__ == "__main__":
    main()