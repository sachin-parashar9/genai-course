import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),             # ← change to GROQ_API_KEY for Groq
)

MODEL = "gpt-4o-mini"

print("=" * 60)
print("  PART 1: Single Message — The Simplest API Call")
print("=" * 60)

messages = [
    {"role": "system", "content": "You are a helpful assistant. Keep answers to 2 sentences."},
    {"role": "user", "content": "What is Python?"},
]

response = client.chat.completions.create(
    model=MODEL,
    messages=messages,
    temperature=0.7,
)

print(f"\n  User:      What is Python?")
print(f"  Assistant: {response.choices[0].message.content}")
print(f"  Tokens:    {response.usage.total_tokens}")

print("\n" + "=" * 60)
print("  PART 2: What Happens WITHOUT History")
print("=" * 60)

# First call: tell the AI your name
messages_call_1 = [
    {"role": "system", "content": "You are a friendly assistant. Keep answers brief."},
    {"role": "user", "content": "My name is Sachin."},
]

response_1 = client.chat.completions.create(model=MODEL, messages=messages_call_1)
ai_reply_1 = response_1.choices[0].message.content
print(f"\n  Call 1 — User:      My name is Sachin.")
print(f"  Call 1 — Assistant: {ai_reply_1}")

# Second call: ask the AI what your name is — but WITHOUT sending history
messages_call_2 = [
    {"role": "system", "content": "You are a friendly assistant. Keep answers brief."},
    {"role": "user", "content": "What is my name?"},
]

response_2 = client.chat.completions.create(model=MODEL, messages=messages_call_2)
ai_reply_2 = response_2.choices[0].message.content
print(f"\n  Call 2 — User:      What is my name?")
print(f"  Call 2 — Assistant: {ai_reply_2}")
print(f"\n  ⚠️  The AI doesn't know! Because we didn't send the history.")


print("\n" + "=" * 60)
print("  PART 3: With History — The AI 'Remembers'")
print("=" * 60)

# Same second question, but now we include the full conversation
messages_call_2_fixed = [
    {"role": "system", "content": "You are a friendly assistant. Keep answers brief."},
    {"role": "user", "content": "My name is Sachin."},           # ← previous user message
    {"role": "assistant", "content": ai_reply_1},                 # ← previous AI reply
    {"role": "user", "content": "What is my name?"},              # ← new question
]

response_2_fixed = client.chat.completions.create(model=MODEL, messages=messages_call_2_fixed)
ai_reply_2_fixed = response_2_fixed.choices[0].message.content
print(f"\n  Call 2 (with history) — User:      What is my name?")
print(f"  Call 2 (with history) — Assistant: {ai_reply_2_fixed}")
print(f"\n  ✅ Now it knows! Because we sent the full conversation.")

print("\n" + "=" * 60)
print("  PART 4: Watch the Messages Array Grow")
print("=" * 60)

# Start with system message
history = [
    {"role": "system", "content": "You are a math tutor. Keep explanations to 1-2 sentences."},
]

questions = [
    "What is 2 + 2?",
    "Now multiply that result by 3.",
    "Is that result a prime number?",
]

for i, question in enumerate(questions, 1):
    # Add the user's message to history
    history.append({"role": "user", "content": question})

    # Send the FULL history to the API
    response = client.chat.completions.create(model=MODEL, messages=history)
    ai_reply = response.choices[0].message.content

    # Add the AI's reply to history (so the NEXT call includes it)
    history.append({"role": "assistant", "content": ai_reply})

    # Show what's happening
    print(f"\n  Turn {i}:")
    print(f"    User:      {question}")
    print(f"    Assistant: {ai_reply}")
    print(f"    Messages in array: {len(history)}  (1 system + {i} user + {i} assistant)")

print(f"\n  📊 Final messages array has {len(history)} messages.")
print(f"     Every turn adds 2 messages (user + assistant).")
print(f"     This is why long conversations use more tokens — and cost more.")

print("\n" + "=" * 60)
print("  KEY TAKEAWAYS")
print("=" * 60)
print("""
  1. Every API call needs a messages array with role + content.
  2. The AI has NO memory — you must send the full history each time.
  3. The messages array grows by 2 each turn (user + assistant).
  4. More messages = more tokens = more cost.
  5. This is exactly how ChatGPT works behind the scenes —
     it sends your entire conversation with every message.
""")

