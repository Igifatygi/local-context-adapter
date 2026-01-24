import json
import numpy as np
from sentence_transformers import SentenceTransformer
import requests

# Load the index
print("Loading index...")
embeddings = np.load("embeddings.npy")
with open("chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)
model = SentenceTransformer('all-MiniLM-L6-v2')
print(f"Loaded {len(chunks)} chunks.")

def find_relevant_chunks(query, top_k=5):
    """Find the most relevant chunks for a query."""
    query_embedding = model.encode([query])[0]
    
    # Cosine similarity
    similarities = np.dot(embeddings, query_embedding) / (
        np.linalg.norm(embeddings, axis=1) * np.linalg.norm(query_embedding)
    )
    
    top_indices = np.argsort(similarities)[-top_k:][::-1]
    return [(chunks[i], similarities[i]) for i in top_indices]

def ask_phi3(prompt):
    """Send a prompt to Phi-3 Mini via Ollama."""
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "phi3:mini", "prompt": prompt, "stream": False}
    )
    return response.json()["response"]

def generate_context_package(user_query):
    """Main adapter function: query -> relevant context -> structured output."""
    
    # Step 1: Find relevant personal context
    relevant = find_relevant_chunks(user_query, top_k=5)
    
    # Step 2: Format context for Phi-3
    context_text = "\n\n".join([
        f"[From '{chunk['title']}' - {chunk['role']}]: {chunk['text'][:500]}"
        for chunk, score in relevant
    ])
    
    # Step 3: Ask Phi-3 to create structured output
    prompt = f"""You are a personal context adapter. Based on the user's query and their personal conversation history below, create a structured context package.

USER QUERY: {user_query}

RELEVANT PERSONAL HISTORY:
{context_text}

Respond with a JSON object containing:
- "user_intent": what the user is trying to accomplish
- "relevant_preferences": list of preferences/patterns you noticed from their history
- "context_summary": brief summary of relevant personal context
- "suggested_approach": how an AI assistant should approach this query given the user's background

Respond ONLY with valid JSON, no other text."""

    response = ask_phi3(prompt)
    
    # Try to parse and validate JSON
    try:
        # Clean up common issues
        cleaned = response.strip()
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]
        if cleaned.startswith("```"):
            cleaned = cleaned[3:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        
        parsed = json.loads(cleaned)
        return parsed, relevant
    except json.JSONDecodeError:
        # Return raw response if parsing fails
        return {"raw_response": response, "parse_error": True}, relevant

if __name__ == "__main__":
    # Test it
    test_query = "I want to Apply for a Open AI recidency, I need to know what should I include in my application from my experience in AI and ML"
    
    print(f"Query: {test_query}")
    print("\nGenerating context package...")
    
    result, relevant_chunks = generate_context_package(test_query)
    
    print("\n--- Relevant chunks found ---")
    for chunk, score in relevant_chunks:
        print(f"[{score:.3f}] {chunk['title']}: {chunk['text'][:100]}...")
    
    print("\n--- Context package from Phi-3 ---")
    print(result)
