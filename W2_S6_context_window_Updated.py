# WEEK 2 — SECTION 6: Context Window
# The model's total working memory — everything must fit inside

import tiktoken

enc = tiktoken.encoding_for_model("gpt-4o-mini")

# Count tokens in a simple sentence
text = "Hello, my name is Saurav and I teach AI engineering."
tokens = enc.encode(text)
print(f"Text: '{text}'")
print(f"Tokens: {len(tokens)}")
print(f"Token IDs: {tokens}")

# GPT-4o-mini context window = 128,000 tokens
# Let's see how fast a chatbot fills it up
system_prompt = "You are a helpful assistant."
user_msg = "How do I read a CSV file in Python?"
assistant_reply = "You can use pandas: import pandas as pd, then df = pd.read_csv('file.csv')"

total = len(enc.encode(system_prompt)) + len(enc.encode(user_msg)) + len(enc.encode(assistant_reply))
print(f"\nOne exchange = {total} tokens")
print(f"Context window = 128,000 tokens")
print(f"That's {128_000 // total} exchanges before it fills up")
print(f"\nSounds like a lot — but add long code snippets and it shrinks fast!")
