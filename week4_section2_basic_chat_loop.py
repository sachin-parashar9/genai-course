import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    # base_url="https://api.groq.com/openai/v1",   # ← uncomment for Groq
    api_key=os.getenv("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"),             # ← change to GROQ_API_KEY for Groq
)
MODEL = "gpt-4o-mini"

def run_chatbot():
    """A simple chatbot that maintains conversation history."""

    # ── System prompt — sets the AI's behavior ─────────────────────────
    system_prompt = (
        "You are a helpful, friendly assistant. "
        "Keep your answers concise — 2 to 4 sentences unless the user "
        "asks for more detail. Be warm but professional."
    )

    # ── Conversation history — starts with just the system message ─────
    history = [
        {"role": "system", "content": system_prompt},
    ]

    # ── Welcome message ────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("  🤖 Simple Chatbot")
    print("  Type your message and press Enter.")
    print("  Type /quit to exit.")
    print("=" * 60)

    # ── The loop ───────────────────────────────────────────────────────
    while True:
        # Step 1: Get user input
        user_input = input("\n  You: ").strip()

        # Step 2: Handle exit command
        if user_input.lower() == "/quit":
            print("\n  👋 Goodbye! Chat ended.")
            break

        # Step 3: Handle empty input (user just pressed Enter)
        if not user_input:
            print("  (Empty message — type something or /quit to exit)")
            continue

        # Step 4: Add the user's message to history
        history.append({"role": "user", "content": user_input})

        # Step 5: Send the FULL history to the API
        response = client.chat.completions.create(
            model=MODEL,
            messages=history,
            temperature=0.7,
        )

        # Step 6: Extract the AI's reply
        ai_reply = response.choices[0].message.content

        # Step 7: Add the AI's reply to history (for next turn)
        history.append({"role": "assistant", "content": ai_reply})

        # Step 8: Print the response
        print(f"\n  🤖: {ai_reply}")

        # Bonus: show how many messages are in the history
        turns = (len(history) - 1) // 2  # subtract system, divide by 2
        print(f"  [Turn {turns} · {len(history)} messages in history]")



if __name__ == "__main__":
    run_chatbot()