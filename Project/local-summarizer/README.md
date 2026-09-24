DOCUMENTATION:

Architecture:

Front end 
    Interface is provided by HTML
    Javascript handles client side behavior to prevent duplicate submissions 

Web/Application Layer
    Flask connects the browser to the Python backend
    Receives file_input and user_prompt through the /inputs POST endpoint.
    Passes them into the processing pipeline.
    Passes final_response to render_template() and inserts it into a <p> element    

Back end 
    Coded in python

Backend Pipeline:
    Inputs file_input and user_prompt are recieved through Flask
    the file_input is then processed through ReadDocument to decode the input document with UTF-8 decoding.

    The string document is then sent through TextChunker to dicide the work into smaller sections. These chunks are taken into ChunkAnalyzer where we build a request to the llm to preproccess the chunks and extract relevant information for the user_prompt. The request is sent to the model server through requests.post(). The response is returned and appended into a list.

    The synthesizer takes all the processed chunks in the responses list and builds another request to the llm to create an analysis of all the sections and synthesize the answer to the user's prompt. It returns the response where we use the synthesize method to return the synthesized data. 

LLM Communication/ Model Layer  
    ChunkAnalyzer and Synthesizer both use requests.post() to send a HTTP request to the model server and waits for a HTTP response.
        The request/response will be sent as structured JSON data
        The request is sent to 127.0.0.1:8080/v1/chat/completions
            127.0.0.1 refers to the machine that Python runs on
            8080 is the port where llama.cpp is listening
            /v1/chat/completions is llama.cpp API endpoint
        For the model we are using Qwen 3.5-4B 
        llama.cpp is the inference engine/server that loads and executes the model
        llama.cpp is configured to use 8 CPU threads for inference and a context size of 16,384 tokens.

Infrastructure
    In this network there are two computers
    Macbook air: the thin client 
        where I write/modify code
    Lenovo Thinkpad T14: the server/compute node
        Where Flask (127.0.0.1:5000), Python backend, llama.cpp(127.0.0.1:8080), Qwen3.5-4B is executed

    SSH is used to remotely administer. USing SSH Tunnel forwards the Mac local port 5000 to the T14's port 5000.
        ssh -L 5000:127.0.0.1:5000 t14
    This allows a private and secure connection to the Flask application


g7 bootup:
    ssh g7

    llama-g7

    MODEL=/root/.cache/huggingface/hub/models--lmstudio-community--Qwen3.5-4B-GGUF/blobs/25082a7dd3776cc3c741c6347d3bd04523f05796607b3fbc32fa3a25dfa1418c

    ./build/bin/llama-server \
    -m "$MODEL" \
    -ngl 99 \
    -c 16384 \
    --host 0.0.0.0 \
    --port 8080

t14 bootup:
    ssh -L 5000:127.0.0.1:5000 t14
    cd ~/services/local-summarizer
    source .venv/bin/activate
    python main.py