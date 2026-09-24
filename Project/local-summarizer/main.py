from flask import Flask, request, render_template
from read_document import ReadDocument
from text_chunker import TextChunker
from chunk_analyzer import ChunkAnalyzer
from synthesizer import Synthesizer
from markdown_interpreter import MarkDownToHTML
from conversation_history import ConversationHistory 
from chat import Chat

app = Flask(__name__)

conversation = ConversationHistory()

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
    conversation.add_user_message(user_prompt)


    responses = []
    for chunk in chunks:
        chunk_analysis = ChunkAnalyzer(chunk, user_prompt)
        response = chunk_analysis.analyze()
        responses.append(response)


    synthesizer = Synthesizer(responses, user_prompt)
    final_response = synthesizer.synthesize()


    html_render = MarkDownToHTML(final_response)
    html_of_results = html_render.build_html()

    conversation.add_assistant_message(final_response)
  

    return render_template(
    "index.html",
    result=html_of_results
    )

@app.route("/chat", methods=["POST"])
def chat():
    
    user_prompt = request.form.get("chat_prompt")
    print("CHAT PROMPT:", user_prompt)
    conversation.add_user_message(user_prompt)
    
    conversation_history = conversation.messages
    chat_llm = Chat(conversation_history)
    assistant_response = chat_llm.chat_with_llm()
    conversation.add_assistant_message(assistant_response)

    print(conversation.messages)
    return render_template(
        "index.html",
        our_chat=conversation_history
        )

    

if __name__ == "__main__":


    app.run(debug=True)
    #main()