"""
=============================================================================
Applied GenAI Engineering Program
Week 1 · Section 3: Your First Real API Call
=============================================================================

WHAT THIS FILE DOES:
  Makes a real call to the OpenAI API (or Groq if you're using the free
  alternative) and prints the AI's response, along with token usage
  and cost.

WHY THIS MATTERS:
  This is the first time you talk to an AI model using Python code
  you wrote yourself. Everything in this 4-month program builds on
  this exact pattern: create a client, send messages, get a response.

BEFORE RUNNING:
  1. Your .env file must have OPENAI_API_KEY=sk-... (from Section 2)
  2. Your virtual environment must be active
  3. Run:  python week1_section3_first_api_call.py
=============================================================================
"""

# ─── IMPORTS ────────────────────────────────────────────────────────────────

import os               # os.getenv() reads environment variables (like our API key)

import time             # time.perf_counter() gives us a precise clock reading.
                        # We use it to measure how long the API call takes
                        # (call it before and after, subtract to get elapsed time).

from typing import Optional   # Optional[str] = "a string or None"


# ─── LOAD API KEY (same pattern from Section 2) ────────────────────────────
# This section file is self-contained, so we need to load the key here too.
# In the complete file, this only happens once.

from dotenv import load_dotenv     # Reads .env file into environment variables
load_dotenv()                       # Actually read the .env file now
api_key = os.getenv("OPENAI_API_KEY")  # Pull the key from environment


# ─── SECTION START ──────────────────────────────────────────────────────────
print("=" * 60)
print("  Section 3: Your first API call")
print("=" * 60)
print()


def first_api_call(api_key: str) -> Optional[str]:
    """
    Makes a simple call to the OpenAI API and returns the AI's response.

    THE PATTERN — memorise this, you'll use it every week:
      1. Import the OpenAI class from the openai package
      2. Create a client (your connection to OpenAI's servers)
      3. Call client.chat.completions.create() with your messages
      4. Extract the text from response.choices[0].message.content

    THE MESSAGES ARRAY:
      In Day 0 you learned that a conversation is a list of dicts.
      Each dict has two keys: "role" and "content".

      Roles:
        "system"    — Instructions to the AI (the user never sees this).
                       This is how you give the AI a persona or rules.
        "user"      — What the human said.
        "assistant" — What the AI previously said (for multi-turn chats).

    PARAMETERS:
      model       — Which AI brain to use. gpt-4o-mini = fast and cheap.
      messages    — The conversation so far (list of role/content dicts).
      max_tokens  — Maximum length of the response (1 token ≈ 0.75 words).
      temperature — 0.0 = always the same answer. 1.0 = creative and varied.
    """
    # ── Step 1: Import the OpenAI class ────────────────────────────────────
    # We import here (not at the top of the file) so this function can
    # give a clear error message if the package isn't installed.
    try:
        from openai import OpenAI
        # OpenAI is a CLASS — a blueprint for creating a "client" object
        # that knows how to talk to OpenAI's servers.
    except ImportError:
        print("  ❌ openai not installed. Run: pip install openai")
        return None

    # Guard clause: if no API key was provided, don't even try
    if not api_key:
        print("  ⚠️  No API key — skipping API call.")
        return None

    print("  🤖 Making your first API call...")

    # ── Step 2: Create the client ──────────────────────────────────────────
    # The client is your connection to OpenAI. You create it once and
    # reuse it for all your API calls. The api_key authenticates you.
    client = OpenAI(api_key=api_key)

    # ── Record the time BEFORE the call ────────────────────────────────────
    # time.perf_counter() returns the current time in seconds with
    # very high precision. We'll subtract this from the time AFTER
    # the call to see how long it took.
    start_time = time.perf_counter()

    # ── Step 3: Make the API call ──────────────────────────────────────────
    # client.chat.completions.create() sends our messages to OpenAI
    # and waits for a response. This is where the actual AI magic happens.
    response = client.chat.completions.create(

        model="gpt-4o-mini",       # Which model to use
                                    # gpt-4o-mini is fast and very cheap
                                    # Good for learning — costs fractions of a paisa

        messages=[                  # The conversation — a list of dicts
            {
                "role": "system",   # System message = instructions to the AI
                "content": (
                    "You are a supportive tutor for students learning "
                    "AI engineering. Keep responses to 2 sentences maximum. "
                    "Be encouraging."
                )
            },
            {
                "role": "user",     # User message = what we're asking
                "content": (
                    "I just made my very first API call to an AI model "
                    "using Python code. Tell me one exciting thing I'll "
                    "be able to build in 4 months."
                )
            }
        ],

        max_tokens=100,            # Limit: AI can use at most 100 tokens
                                    # (roughly 75 words) in its response

        temperature=0.7,           # 0.0 = always same answer (deterministic)
                                    # 0.7 = balanced creativity (good default)
                                    # 1.0 = maximum creativity (more random)
    )

    # ── Record the time AFTER the call ─────────────────────────────────────
    # Multiply by 1000 to convert seconds → milliseconds (easier to read)
    elapsed_ms = (time.perf_counter() - start_time) * 1000

    # ── Step 4: Extract the response text ──────────────────────────────────
    # The response object has a specific structure you navigate every time:
    #
    #   response
    #     .choices          ← a LIST of possible completions (usually just 1)
    #       [0]             ← the first (and only) completion
    #         .message      ← the message object
    #           .content    ← the actual text you want (a string)
    #           .role       ← "assistant"
    #     .usage
    #       .prompt_tokens       ← tokens used by your input messages
    #       .completion_tokens   ← tokens used by the AI's response
    #       .total_tokens        ← sum of both
    #
    ai_text = response.choices[0].message.content

    # ── Token usage — this maps directly to your API cost ──────────────────
    # Tokens are the units AI models think in. Roughly: 1 token ≈ 0.75 words.
    # You pay per token — so tracking usage tells you exactly what things cost.
    prompt_tokens     = response.usage.prompt_tokens      # input cost
    completion_tokens = response.usage.completion_tokens  # output cost
    total_tokens      = response.usage.total_tokens       # total

    # ── Cost estimate ──────────────────────────────────────────────────────
    # gpt-4o-mini pricing (early 2025):
    #   Input:  $0.150 per 1 million tokens
    #   Output: $0.600 per 1 million tokens
    # We divide by 1000 because the rates above are per million.
    cost_usd = (prompt_tokens * 0.00015 + completion_tokens * 0.00060) / 1000

    # ── Display results ────────────────────────────────────────────────────
    print(f"  ✅ Response received in {elapsed_ms:.0f}ms")
    # :.0f means "format as a float with 0 decimal places"
    print()
    print("  🗣️  The AI said:")
    print(f"     {ai_text}")
    print()
    print(f"  📊 Tokens used:  {prompt_tokens} prompt + "
          f"{completion_tokens} completion = {total_tokens} total")
    # :.6f means "format as a float with 6 decimal places"
    print(f"  💰 Cost:         ${cost_usd:.6f}  (less than 1 paisa)")
    print()

    return ai_text


# ─── RUN THE API CALL ──────────────────────────────────────────────────────
if api_key:
    ai_response = first_api_call(api_key)
    if ai_response:
        print("  🎉 Congratulations — you just talked to an AI with code!")
        print("     This exact pattern is how every AI app on earth works.\n")
else:
    print("  ⚠️  No API key found. Add your key to .env and re-run.")
    print("     (See Section 2 for instructions.)\n")
