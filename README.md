# Local Context Adapter

A prototype exploring how end users can leverage their own compute to overcome context window limitations in large language models.

## The Problem

Current LLMs have limited memory and context windows due to compute constraints. Your conversation history with ChatGPT might span thousands of exchanges, but the model can only "see" a small window at a time. This means:

- Models forget your preferences, past decisions, and personal context
- Every conversation starts from zero
- Personalization is limited to what fits in the context window

## The Proposal

What if users contributed their own compute to solve this?

This prototype demonstrates a **local context adapter** that:

1. **Runs on the user's machine** — using their CPU/GPU resources
2. **Processes their full conversation history** — not limited by API context windows
3. **Generates structured context packages** — ready to send to a cloud model for final response

The architecture splits the work:
```
User Query
    ↓
[LOCAL: User's Computer]
    → Semantic search over full personal history
    → Local LLM extracts relevant preferences and context
    → Outputs structured JSON context package
    ↓
[CLOUD: API Model]
    → Receives query + personalized context package
    → Generates final response with full user context
```

## Why This Matters

**Compute**: Users have idle compute on laptops and phones. Local models (Phi-3, LLaMA, etc.) are now capable enough to handle context curation tasks.

**Personalization**: Instead of fitting your history into a context window, the local adapter searches your entire history and extracts only what's relevant.

**Data Ownership**: Your personal data never leaves your machine. Only a structured summary is sent to the cloud model — you control what context gets shared.

## How It Works

1. **Data Processing** (`load_data.py`): Parses ChatGPT export (581 conversations → 5858 searchable chunks)

2. **Semantic Index** (`build_index.py`): Creates vector embeddings using sentence-transformers for similarity search

3. **Context Adapter** (`adapter.py`): 
   - Takes a user query
   - Finds the 5 most relevant chunks from personal history
   - Asks local Phi-3 to generate a structured context package containing:
     - User intent
     - Relevant preferences from history
     - Context summary
     - Suggested approach for the cloud model

## Example Output

Query: "What should I eat for dinner?"

The adapter searches personal history, finds past conversations about cooking preferences, dietary constraints, and meal planning, then generates:
```json
{
  "user_intent": "Seeking a simple dinner option",
  "relevant_preferences": [
    "Interest in self-cooked dinners without professional culinary skills",
    "Needs recipes accommodating vegetarian friends",
    "Prefers minimal cooking equipment"
  ],
  "context_summary": "User frequently asks about simple meals, has hosted vegetarian guests before, expressed interest in pasta dishes and quick recipes",
  "suggested_approach": "Suggest simple vegetarian-friendly options that don't require complex preparation"
}
```

This context package would then be sent alongside the query to a cloud model (GPT-4, Claude, etc.) for the final response.

## Requirements

- Python 3.11+
- 8GB+ RAM
- ~2GB disk space for models

## Setup

1. Install dependencies:
```
pip install requests sentence-transformers numpy
```

2. Install Ollama and pull Phi-3:
```
ollama pull phi3:mini
```

3. Export your ChatGPT data (Settings → Data Controls → Export) and place `conversations.json` in this folder

4. Build the search index:
```
python build_index.py
```

5. Run the adapter:
```
python adapter.py
```

## Limitations

- Prototype only — not production-ready
- Local inference is slow on CPU (~30-60 seconds per query)
- JSON output sometimes malformed (Phi-3 limitation)
- No integration with cloud API yet (intentionally scoped down)

## Future Directions

- **Incremental indexing**: Update the index as new conversations happen
- **Preference learning**: Fine-tune a small LoRA on user's communication style
- **Privacy controls**: Let users exclude sensitive topics from the index
- **Multi-source support**: Discord, email, notes — not just ChatGPT
- **Client integration**: Browser extension or native app that intercepts queries

## Author

Built as a prototype for exploring user-owned AI personalization.


