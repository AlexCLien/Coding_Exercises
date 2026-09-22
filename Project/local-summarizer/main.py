from flask import Flask, request, render_template
from read_document import ReadDocument
from text_chunker import TextChunker
from chunk_analyzer import ChunkAnalyzer
from synthesizer import Synthesizer

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

    

if __name__ == "__main__":
    app.run(debug=True)
    #main()