"""
Local Context Adapter

Main adapter that processes user queries and generates personalized context packages.
"""

import json
from typing import Dict, Tuple, List
from build_index import SemanticIndex
from load_data import load_data, parse_conversations


class ContextAdapter:
      """Adapter for generating personalized context from local conversation history."""

    def __init__(self, data_path: str):
              self.index = SemanticIndex()
              self.data = load_data(data_path)
              self.conversations = parse_conversations(self.data)
              self.index.build(self.conversations)

    def generate_context_package(self, query: str) -> Tuple[Dict, List]:
              """Generate context package for a user query."""
              # Find relevant chunks
              relevant = self.index.search(query, top_k=5)

        context_package = {
                      "user_intent": query,
                      "relevant_preferences": [],
                      "context_summary": "",
                      "suggested_approach": ""
        }

        return context_package, relevant


if __name__ == "__main__":
      print("=== Local Context Adapter ===")
