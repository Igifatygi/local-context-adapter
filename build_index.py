import json
import numpy as np
from sentence_transformers import SentenceTransformer
from load_data import load_conversations

def build_index():
    """Create embeddings for all chunks and save them."""
    print("Loading conversations...")
    chunks = load_conversations()
    
    print("Loading embedding model (first time takes a minute)...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    print(f"Creating embeddings for {len(chunks)} chunks...")
    texts = [f"{c['title']}: {c['text']}" for c in chunks]
    embeddings = model.encode(texts, show_progress_bar=True)
    
    # Save everything
    print("Saving index...")
    np.save("embeddings.npy", embeddings)
    with open("chunks.json", "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False)
    
    print(f"Done! Saved {len(chunks)} chunks with embeddings.")

if __name__ == "__main__":
    build_index()
