"""
=============================================================================
Applied GenAI Engineering Program
Week 1 · Section 4: Understanding What the API Returned
=============================================================================

WHAT THIS FILE DOES:
  Makes a real API call, then shows you the ACTUAL raw response
  the API sent back — so you can see its structure for yourself.

WHY THIS MATTERS:
  In Section 3, we used dot notation (response.choices[0].message.content)
  to extract the text. But what does the FULL response look like?
  When you're debugging a production app or reading logs, you need
  to understand the actual shape of the data.

HOW TO RUN:
  python week1_section4_json_response.py
=============================================================================
"""

# ─── IMPORTS ────────────────────────────────────────────────────────────────

import os
import json             # json is Python's built-in module for working with
                        # JSON (JavaScript Object Notation) — the format that
                        # almost every web API uses to send and receive data.
                        #
                        # Key function we'll use here:
                        #   json.dumps(dict, indent=2)  → converts a Python dict
                        #                                  to a nicely formatted string

from dotenv import load_dotenv
from openai import OpenAI

# ─── SETUP ──────────────────────────────────────────────────────────────────

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# ─── SECTION START ──────────────────────────────────────────────────────────
print("=" * 60)
print("  Section 4: JSON — reading the API response structure")
print("=" * 60)
print()

if not api_key:
    print("  ⚠️  No API key found. Add your key to .env and re-run.")
    print("     (See Section 2 for instructions.)")
    exit()


# ═══════════════════════════════════════════════════════════════════════════
# STEP 1: Make a quick API call (same pattern from Section 3)
# ═══════════════════════════════════════════════════════════════════════════

client = OpenAI(api_key=api_key)

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "Reply in exactly one sentence."},
        {"role": "user",   "content": "What is JSON and why do APIs use it?"}
    ],
    max_tokens=60,
    temperature=0.7,
)

# We already know how to get the text (from Section 3):
ai_text = response.choices[0].message.content
print(f"  🗣️  AI said: {ai_text}")
print()


# ═══════════════════════════════════════════════════════════════════════════
# STEP 2: See the ACTUAL full response
# ═══════════════════════════════════════════════════════════════════════════
# In Section 3, we only extracted .choices[0].message.content
# But the API sent back much more. Let's see ALL of it.
#
# response.model_dump() converts the SDK object → a plain Python dict
# json.dumps() then converts that dict → a nicely formatted string

raw_dict = response.model_dump()       # SDK object → Python dict
pretty_json = json.dumps(raw_dict, indent=2)  # dict → formatted string

print("  ── The FULL response from OpenAI ──")
print()
print(pretty_json)
print()

# ═══════════════════════════════════════════════════════════════════════════
# STEP 3: Navigate it safely with .get()
# ═══════════════════════════════════════════════════════════════════════════
# Now that you can SEE the structure, let's navigate it as a dict.
#
# Two ways to read a dict value:
#   dict["key"]       → CRASHES with KeyError if key doesn't exist
#   dict.get("key")   → returns None safely if key doesn't exist
#
# In production, ALWAYS use .get() for API responses. APIs can change,
# fields can be missing in error responses — .get() keeps your app alive.

print("  ── Navigating the response safely with .get() ──")
print()

# Drill into the nested structure, step by step:
choices     = raw_dict.get("choices", [])          # Get the list (or empty list)
first       = choices[0] if choices else {}         # First item (or empty dict)
message     = first.get("message", {})              # The message dict
text        = message.get("content", "")            # The actual AI text
reason      = first.get("finish_reason", "")        # Why the model stopped
total_tokens = raw_dict.get("usage", {}).get("total_tokens", 0)
# ↑ Chained .get() — first get "usage" dict, then get "total_tokens" from it

print(f"  Text:         {text[:60]}...")
print(f"  Finish reason: {reason}")
print(f"     'stop'   = model finished naturally")
print(f"     'length' = model hit the max_tokens limit (got cut off)")
print(f"  Total tokens: {total_tokens}")
print()

# ── Why .get() matters ────────────────────────────────────────────────────
print("  💡 KEY HABIT:")
print("     dict['key']  → crashes if key is missing   (KeyError)")
print("     dict.get('key') → returns None safely")
print("     Always use .get() when reading API responses.")
print()


# ─── PART 1 SUMMARY ────────────────────────────────────────────────────────
print("=" * 60)
print("  Part 1 Complete!")
print()
print("  ✅ Verified your Python environment        (Section 1)")
print("  ✅ Loaded your API key securely from .env   (Section 2)")
print("  ✅ Made your first real API call             (Section 3)")
print("  ✅ Understood the JSON response structure    (Section 4)")
print()
print("  Part 2 (Sunday): Python patterns for production AI code.")
print("=" * 60)
