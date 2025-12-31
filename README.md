# Local Context Adapter

A prototype exploring how end users can leverage their own compute to overcome context window limitations of LLMs.

## The Problem

Current LLMs have limited memory and context windows due to compute constraints. You:

- Models forget your preferences, past decisions, and personal context
- - Every conversation starts from zero
  - - Personalization is limited to what fits in the context window
   
    - ## The Proposal
   
    - What if users contributed their own compute to solve this?
   
    - This prototype demonstrates a **local context adapter** that:
   
    - 1. **Runs on the user's machine** – using their CPU/GPU resources
      2. 2. **Processes their full conversation history** – not limited by API context window
         3. 3. **Generates structured context packages** – ready to send to a cloud model for final verification
           
            4. The architecture splits the work:
           
            5. ```
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
               ...
               ```

               ## Why This Matters

               **Compute**: Users have idle compute on laptops and phones. Local models (Phi-3, LLama models) can run them.

               **Personalization**: Instead of fitting your history into a context window, the local adapter serves up your preferences and context to the cloud model.

               **Data Ownership**: Your personal data never leaves your machine. Only a structured context package is sent to the API.

               ## How It Works

               1. **Data Processing** (`load_data.py`): Parses ChatGPT export (581 conversations → embeddings)
              
               2. 2. **Semantic Index** (`build_index.py`): Creates vector embeddings using sentence-transformers
                 
                  3. 3. **Context Adapter** (`adapter.py`):
                     4.    - Takes a user query
                           -    - Finds the 5 most relevant chunks from personal history
                                -    - Asks local Phi-3 to generate a structured context package containing:
                                     -      - User intent
                                     -       - Relevant preferences from history
                                     -        - Context summary
                                     -         - Suggested approach for the cloud model
                                 
                                     -     ## Example Output
                                 
                                     - Query: "What should I eat for dinner?"
                                 
                                     - The adapter searches personal history, finds past conversations about cooking preferences.
                                 
                                     - ```json
                                       {
                                         "user_intent": "Seeking a simple dinner option",
                                         "relevant_preferences": [
                                           "Interest in self-cooked dinners without professional culinary skills",
                                           "Needs recipes accommodating vegetarian friends",
                                           "Prefers minimal cooking equipment"
                                         ],
                                         "context_summary": "User frequently asks about simple meals, has hosted vegetarian dinners",
                                         "suggested_approach": "Suggest simple vegetarian-friendly options that don't require advanced cooking techniques"
                                       }
                                       ...
                                       ```

                                       This context package would then be sent alongside the query to a cloud model (GPT-4, Claude, etc) to generate a more personalized response.

                                       ## Running It

                                       You'll need:
                                       - Python 3.9+
                                       - - Phi-3 Mini (4B model, ~2.4 GB)
                                         - - sentence-transformers
                                           - - A ChatGPT export JSON file
                                            
                                             - Steps:
                                            
                                             - 1. **Export your data** from ChatGPT
                                               2. 2. **Load and process** your conversation history:
                                                  3. ```bash
                                                     python load_data.py your_export.json
                                                     ```

                                                     3. **Build the semantic index**:
                                                     4. ```bash
                                                        python build_index.py
                                                        ```

                                                        4. **Run the context adapter**:
                                                        5. ```bash
                                                           python adapter.py
                                                           ```

                                                           Then, find this part at the end of the `generate_context_package` function:

                                                           ```python
                                                           response = ask_phi3(prompt)
                                                           return response, relevant
                                                           ```

                                                           Replace it with:

                                                           ```python
                                                           # Validate JSON
                                                           try:
                                                               valid_json = json.loads(response)
                                                           except json.JSONDecodeError:
                                                               # Retry if JSON is invalid
                                                               pass

                                                           if __name__ == "__main__":
                                                               # Test it
                                                               test_query = "Help me plan a trip"

                                                               print("\n=== Local Context Adapter ===")
                                                               print("Type a query to get personalized context, or 'quit' to exit.\n")

                                                               while True:
                                                                   query = input("Your query: ").strip()
                                                                   if query.lower() in ['quit', 'exit', 'q']:
                                                                       break

                                                                   if not query:
                                                                       continue

                                                                   print("\nGenerating context package...")
                                                                   result, relevant_chunks = generate_context_package(query)

                                                                   print("\n--- Relevant chunks found ---")
                                                                   for chunk, score in relevant_chunks:
                                                                       print(f"[{score:.3f}] {chunk['title']}: {chunk['text'][:500]}...")

                                                                   print("\n--- Context package ---")
                                                                   print(json.dumps(result, indent=2))
                                                                   print("\n" + "="*50 + "\n")
                                                           ```

                                                           ## What's Next

                                                           - Implement end-to-end integration with a cloud API
                                                           - - Add support for different local models
                                                             - - Test with different prompt engineering techniques
                                                               - - Explore streaming responses
                                                                 - - Add conversation memory to the adapter itself
                                                                  
                                                                   - ## Got ideas?
                                                                  
                                                                   - This is a prototype. If you have thoughts on:
                                                                   - - How to better extract context from personal history
                                                                     - - More efficient ways to package user context
                                                                       - - Privacy/security considerations
                                                                         - - Integration with different LLM providers
                                                                          
                                                                           - Drop an issue or PR!
