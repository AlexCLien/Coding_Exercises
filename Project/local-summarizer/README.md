DOCUMENTATION:

Architecture:
Front end we are using Flask
Back end is coded in python
For the model we are using Qwen 3.5-4B using 8 cores and a context window of 16384

Backend Pipeline:
Inputs file_input and user_prompt are recieved through Flask

the file_input is then processed through ReadDocument to decode the input document into strings.

The string document is then sent through TextChunker to dicide the work into smaller sections. These chunks are taken into ChunkAnalyzer where we build a request to the llm to preproccess the chunks and extract relevant information for the user_prompt and is sent through request.post(). The response is returned and appended into a list.

The synthesizer takes all the processed chunks in the responses list and builds another request to the llm to create an analysis of all the sections and synthesize the answer to the user's prompt. it is sent through request.post() and returns the response where we use the synthesize method to return the synthesized data. 

we return the response with render_template as the endpoint for the front end.