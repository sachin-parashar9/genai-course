import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    # base_url="https://api.groq.com/openai/v1",   # ← uncomment for Groq
    api_key=os.getenv("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"),             # ← change to GROQ_API_KEY for Groq
)
MODEL = "gpt-4o-mini"

import time

print("=" * 60)
print("  PART 1: Normal vs Streaming — Feel the Difference")
print("=" * 60)

test_messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Explain what an API is in 3 sentences."},
]

# ── Normal call: wait for everything ───────────────────────────────────
print("\n  ⏳ Normal call (wait for full response)...")
start = time.time()

response_normal = client.chat.completions.create(
    model=MODEL,
    messages=test_messages,
    temperature=0.7,
)

elapsed = time.time() - start
print(f"  Waited {elapsed:.1f}s, then got everything at once:")
print(f"  {response_normal.choices[0].message.content}\n")

# ── Streaming call: see words appear ───────────────────────────────────
print("  ⚡ Streaming call (words appear as generated)...")
start = time.time()

stream = client.chat.completions.create(
    model=MODEL,
    messages=test_messages,
    temperature=0.7,
    stream=True,          # ← This is the ONLY change
)

# Each "chunk" contains a small piece of the response
first_token_time = None
full_response = ""

print("  ", end="", flush=True)  # Start on same line
for chunk in stream:
    # chunk.choices[0].delta.content has the new text
    # (it's called "delta" because it's the CHANGE — just the new piece)
    content = chunk.choices[0].delta.content

    if content is not None:
        if first_token_time is None:
            first_token_time = time.time() - start

        print(content, end="", flush=True)  # Print without newline
        full_response += content             # Collect for history

elapsed = time.time() - start
print(f"\n\n  First word appeared in: {first_token_time:.2f}s")
print(f"  Total time: {elapsed:.1f}s")
print(f"  Same total time — but the user saw output almost instantly!")


def run_streaming_chatbot():
    """Chatbot with streaming responses — words appear in real time."""

    system_prompt = (
        "You are a helpful, friendly assistant. "
        "Keep your answers concise — 2 to 4 sentences unless asked for more."
    )

    history = [{"role": "system", "content": system_prompt}]

    print("\n" + "=" * 60)
    print("  🤖 Streaming Chatbot")
    print("  Type your message and press Enter.")
    print("  Type /quit to exit.")
    print("=" * 60)

    while True:
        user_input = input("\n  You: ").strip()

        if user_input.lower() == "/quit":
            print("\n  👋 Goodbye!")
            break

        if not user_input:
            continue

        history.append({"role": "user", "content": user_input})

        # ── Make a streaming API call ──────────────────────────────────
        stream = client.chat.completions.create(
            model=MODEL,
            messages=history,
            temperature=0.7,
            stream=True,
        )

        # ── Print each chunk as it arrives ─────────────────────────────
        print("\n  🤖: ", end="", flush=True)

        full_response = ""
        for chunk in stream:
            content = chunk.choices[0].delta.content
            if content is not None:
                print(content, end="", flush=True)
                full_response += content

        print()  # New line after the response is complete

        
        history.append({"role": "assistant", "content": full_response})

        turns = (len(history) - 1) // 2
        print(f"  [Turn {turns}]")



if __name__ == "__main__":
    print("\n  Starting streaming chatbot...\n")
    run_streaming_chatbot()
