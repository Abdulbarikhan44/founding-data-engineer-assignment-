from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

def generate_embedding(text):
    emb = model.encode(text)
    
    if len(emb) == 0:
        print("Empty embedding detected")  # anomaly check
    
    return emb.tolist()

# def test():
#     print(generate_embedding("hello world"))
