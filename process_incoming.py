import requests
import os
import json
import pandas as pd
import joblib
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity



def create_embedding(text_list):
    embeddings = []

    for text in text_list:
        r = requests.post(
            "http://localhost:11434/api/embeddings",
            json={
                "model": "bge-m3",
                "prompt": text
            }
        )

        embeddings.append(r.json()["embedding"])

    return embeddings

def inference(prompt):
    r = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )
    reponse = r.json()
    print(reponse)
    return reponse
    

df= joblib.load('embeddings.joblib')
incoming_query = input("Ask A Question: ")

question_embedding = create_embedding([incoming_query])[0]


# convert embeddings column into matrix
embedding_matrix = np.vstack(df["embedding"].values)

similarities = cosine_similarity(embedding_matrix, [question_embedding]).flatten()

top_results= 6
top_indices = similarities.argsort()[::-1][:top_results]


new_df = df.iloc[top_indices]

print("\nTop Matching Chunks:\n")
print(new_df[["title", "number", "text"]])

prompt = f'''  I am teaching Python programming language.
Here are video chunck contatining video title, video number, start time in seconds, end time in seconds and the text content of the chunk.
the text at that time:
{new_df[["title", "number","start", "end", "text"]].to_json()}

"{incoming_query}"
User asked this question related to the video chunk, you have to answer where and how much content is taught in which video
(in which video and at what timestamp)
and guide the user to that particular video
If user asks unrelated question, tell hum you can only answer questions related to the course
'''
with open("prompt.txt", "w") as f:
    f.write(prompt)

response = inference(prompt)["response"]    
print(response)

with open("response.txt", "w") as f:
    f.write(response)
# for index, item in new_df.iterrows():
#     print(index, item["title"], item["number"], item["text"], item["start"], item["end"])