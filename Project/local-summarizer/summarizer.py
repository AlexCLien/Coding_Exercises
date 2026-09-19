import requests
from flask import Flask, request, render_template

app = Flask(__name__)
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/inputs", methods=["POST"])
def inputs():
    file_input = request.files.get("fname")
    document = ReadDocument(file_input)
    document_text = document.read_document()
    #print(file_input)
    text_chunk = TextChunker(document_text,1500)
    chunks = text_chunk.chunk_text()
 
    user_prompt = request.form.get("uprompt")
    responses = []
    for chunk in chunks:
        chunk_analysis = ChunkAnalyzer(chunk, user_prompt)
        response = chunk_analysis.analyze()
        responses.append(response)


    synthesizer = Synthesizer(responses, user_prompt)
    final_response = synthesizer.synthesize()
 
    return render_template(
    "index.html",
    result=final_response
    )

class ReadDocument:
    def __init__(self, file_input):
        self.file_input = file_input

    def read_document(self):
        document_bytes = self.file_input.read()
        document_decoded = document_bytes.decode("utf-8")
        return document_decoded
    
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
        response = requests.post("http://127.0.0.1:8080/v1/chat/completions", json=request)
        return response

    def analyze(self):

        request = self.build_request()
        response = self.send_request(request)
        data = response.json()
        #print(response.json(scp summarizer.py t14:~/services/local-summarizer/))
        analisis = data["choices"][0]["message"]["content"]

        return analisis

class TextChunker:
    def __init__(self, text, chunk_size):
        self.text = text
        self.chunk_size = chunk_size

    def chunk_text(self):
        chunks = []
        words = self.text.split()
        for start in range(0, len(words), self.chunk_size):
            stop = start + self.chunk_size
            chunk = words[start:stop]
            chunk_string = " ".join(chunk)
            chunks.append(chunk_string)
        return chunks

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
        response = requests.post("http://127.0.0.1:8080/v1/chat/completions", json=request)
        return response

    def synthesize(self):
    
        request = self.build_request()
        response = self.send_request(request)
        data = response.json()
        #print(response.json(scp summarizer.py t14:~/services/local-summarizer/))
        synthesized_data = data["choices"][0]["message"]["content"]

        return synthesized_data

if __name__ == "__main__":
    app.run(debug=True)