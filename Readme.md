# How to use this  RAG AI Teaching assistant on your own data
## Step 1 -- Collect your videos
Move all your video files to the videos folder

## Step 2 -- Convert to mp3
Convert all the video files to mp3 by running video_to_mp3

This code scans a videos/ folder, extracts the tutorial number and name from each filename using regex and string splitting, then calls ffmpeg (a system-level video tool) via subprocess to strip the audio track and save it as an .mp3 into the audios/ folder it works sequentially (one video at a time) so it's not particularly fast, but ffmpeg itself is highly optimized for media conversion under the hood.

## Step 3 -- Convert mp3 to json
converts all the mp3 files to json by running mp3_to_json

This code loads OpenAI's Whisper large-v2 speech recognition model, loops through all .mp3 files in the audios/ folder, and for each one runs transcription + translation (from Hindi to English via task="translate")  Whisper processes each audio file and returns time-stamped segments which get packaged into structured chunks (with title, number, start/end times, and text) and stored in a data dict  though notably the file-saving code is commented out so currently no JSON is actually written to disk, and there's no parallelism so it processes one audio file at a time, making it slow for large collections since Whisper large-v2 is a heavyweight model that's accurate but computationally expensive.

## Step 4 -- Convert json files to Vectors
Use the file preporcess_json to convert the json files to a dataframe with embeddings and save it as a joblib pickle.

This code reads text chunks from 67 JSON files, sends them 8 at a time in parallel (via ThreadPoolExecutor) to a locally running Ollama server (localhost:11434), which uses the bge-m3 model to convert each text chunk into a numerical vector (embedding), then collects all those vectors back in order and saves the final chunk+embedding pairs into a compressed embeddings.joblib file using pandas it's fast because instead of waiting for one embedding to finish before starting the next, it fires 8 HTTP requests simultaneously, hiding the network/model wait time behind parallelism.

## Step 5 -- Prompt generation and feeding to LLM
Read the joblib file and load it into the memory, Then create a relevant prompt as per the user query and feed it to the LLM.

This is the RAG (Retrieval-Augmented Generation) query engine that ties everything together — it loads the prebuilt embeddings database, converts the user's question into an embedding via bge-m3, computes cosine similarity between the query vector and all stored chunk vectors to find the 6 most relevant video segments, then constructs a structured prompt injecting those chunks (with title, video number, and timestamps) and sends it to Llama3 running locally on Ollama to generate a natural language answer that tells the user exactly which video and timestamp contains what they're looking for — making it a fully local, private RAG pipeline where bge-m3 handles semantic search and Llama3 handles answer generation.