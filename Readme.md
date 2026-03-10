# RAG AI Teaching Assistant — Setup Guide

This guide explains how to run the **RAG AI Teaching Assistant** on your **own video data**.  
The pipeline converts video lectures into **text embeddings** that can later be used for **retrieval-augmented generation (RAG)**.

---

# 1. Collect Your Videos

Move all your tutorial video files into the project **videos/** folder.

Example structure:
project/
│
├── videos/
│ ├── tutorial_01_intro.mp4
│ ├── tutorial_02_variables.mp4
│ └── tutorial_03_functions.mp4
│
├── audios/
├── json/
└── embeddings/


---

# 2. Convert Videos to MP3

Run the script:
video_to_mp3.py


This script performs the following steps:

- Scans the **videos/** folder for video files
- Extracts the **tutorial number and title** using regex and string parsing
- Uses **FFmpeg** through Python's `subprocess` module
- Extracts the **audio track from each video**
- Saves the result as **.mp3 files in the audios/ folder**

### Key Characteristics

- Processes videos **sequentially (one at a time)**
- Uses **FFmpeg**, which is highly optimized for media processing
- Reliable but **not optimized for speed when many videos exist**

---

# 3. Convert MP3 to JSON Transcripts

Run the script:
mp3_to_json.py

This script converts audio lectures into **structured transcript data**.

### What the Script Does

- Loads **OpenAI Whisper `large-v2` speech recognition model**
- Iterates through all `.mp3` files inside **audios/**
- Performs:

  - **Speech transcription**
  - **Translation from Hindi → English**

This is done using:
task="translate"


### Output Structure

Whisper returns **time-stamped segments**, which are stored as structured chunks containing:

- Tutorial title
- Tutorial number
- Start timestamp
- End timestamp
- Transcript text

Example chunk:
{
"title": "Python Functions",
"tutorial_number": 5,
"start": 12.5,
"end": 18.3,
"text": "Functions allow us to reuse code efficiently."
}


### Important Notes

- The **JSON saving code is currently commented out**
- No files are written to disk unless this section is enabled
- Processing is **sequential**, so transcription may be **slow**
- Whisper `large-v2` is **accurate but computationally expensive**

---

# 4. Convert JSON Data to Vector Embeddings

Run the preprocessing script:
pre_process_json.py


This step converts transcript chunks into **vector embeddings** for semantic search.

### How the Script Works

1. Reads transcript chunks from **67 JSON files**
2. Sends the text chunks to a **local Ollama server**
http://localhost:11434


3. Uses the embedding model:
bge-m3


4. Converts each text chunk into a **numerical embedding vector**

### Parallel Processing

The script uses:


ThreadPoolExecutor


to process **8 embedding requests simultaneously**.

This significantly improves performance by:

- Reducing waiting time
- Running multiple embedding requests in parallel

### Final Output

The final dataset contains:

- Text chunk
- Metadata
- Embedding vector

This data is saved as a compressed file:


embeddings.joblib


using **Pandas + Joblib**.

---

# Pipeline Summary


Videos (.mp4)
      │
      ▼
Audio Extraction
(video_to_mp3.py)
      │
      ▼
MP3 Audio Files
      │
      ▼
Speech Recognition
(mp3_to_json.py)
      │
      ▼
Transcript JSON
      │
      ▼
Embedding Generation
(preprocess_json.py)
      │
      ▼
embeddings.joblib

---

# Technologies Used

- **Python**
- **FFmpeg**
- **OpenAI Whisper**
- **Ollama**
- **bge-m3 embedding model**
- **Pandas**
- **Joblib**
- **ThreadPoolExecutor**

---

# Notes

- Whisper `large-v2` requires **significant GPU/CPU resources**
- Embedding generation requires **Ollama running locally**
- Parallel embedding improves speed but depends on **system resources**

---

# Future Improvements

Possible enhancements to the pipeline:

- Enable **JSON saving**
- Add **parallel Whisper transcription**
- Implement **GPU acceleration**
- Add **vector database integration (FAISS / Chroma / Weaviate)**
- Build a **chat interface for the RAG assistant**

---

# Result

After completing these steps, you will have a **fully prepared embedding dataset** that can be used to build a **Retrieval-Augmented Generation (RAG) AI teaching assistant** capable of answering questions based on your video lectures.



