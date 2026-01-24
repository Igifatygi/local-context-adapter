import json

def load_conversations(filepath="conversations.json"):
    """Load and parse ChatGPT export."""
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    print(f"Found {len(data)} conversations")
    
    # Extract just the text content from each conversation
    chunks = []
    for convo in data:
        title = convo.get("title", "Untitled")
        
        # Get all messages in this conversation
        if "mapping" in convo:
            for node_id, node in convo["mapping"].items():
                msg = node.get("message")
                if msg and msg.get("content") and msg["content"].get("parts"):
                    # Handle both string and dict parts
                    parts = msg["content"]["parts"]
                    text_parts = []
                    for part in parts:
                        if isinstance(part, str):
                            text_parts.append(part)
                        elif isinstance(part, dict):
                            # Try common keys for text content
                            text_parts.append(part.get("text", part.get("content", "")))
                    text = " ".join(text_parts)
                    role = msg.get("author", {}).get("role", "unknown")
                    
                    # Only keep substantial messages
                    if len(text) > 50:
                        chunks.append({
                            "title": title,
                            "role": role,
                            "text": text[:1000]  # Truncate very long messages
                        })
    
    print(f"Extracted {len(chunks)} text chunks")
    return chunks

if __name__ == "__main__":
    chunks = load_conversations()
    
    # Show a few examples
    print("\n--- Sample chunks ---")
    for chunk in chunks[:3]:
        print(f"\n[{chunk['role']}] from '{chunk['title']}':")
        print(chunk['text'][:200] + "...")
