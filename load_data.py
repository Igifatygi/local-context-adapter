"""
Data Processing Module

Parses ChatGPT export and prepares data for semantic indexing.
"""

import json
from typing import List, Dict

def load_data(filepath: str) -> List[Dict]:
      """Load ChatGPT export data from JSON file."""
      with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data

def parse_conversations(data: List[Dict]) -> List[Dict]:
      """Extract conversation text from ChatGPT export format."""
    conversations = []
    for item in data:
              if 'conversation_id' in item:
                            conversations.append({
                                              'id': item.get('conversation_id'),
                                              'title': item.get('title', ''),
                                              'text': item.get('text', '')
                            })
                    return conversations

if __name__ == "__main__":
      # Example usage
      print("ChatGPT Data Loader")
