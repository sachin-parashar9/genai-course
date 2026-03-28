"""
=============================================================================
Applied GenAI Engineering Program
Week 1 · Section 2: How .env Files Protect Your Secrets
=============================================================================

WHAT THIS FILE DOES:
  Shows you the secure way to load an API key using a .env file.
  After running this, your API key will be loaded into memory
  WITHOUT it ever appearing in your code.

WHY THIS MATTERS:
  A developer pushed code to GitHub with his AWS key hardcoded.
  A bot found it within 60 seconds. By morning, $3,200 of
  crypto-mining had been billed to his account. True story.
  This happens weekly. The .env pattern prevents it.

BEFORE RUNNING:
  1. Create a file called .env in this same folder
  2. Add this one line to it:  OPENAI_API_KEY=sk-...your-key-here...
  3. Create a file called .gitignore and add this line: .env
  4. Run:  python week1_section2_env_file.py
=============================================================================
"""

# ─── IMPORTS ────────────────────────────────────────────────────────────────

import os               # os = "operating system" — lets us read environment
                        # variables (settings stored by the system, not in code).
                        # os.getenv("NAME") reads a variable by name.

# typing is Python's module for type hints — labels that describe what
# types a function accepts and returns. They don't change how code runs;
# they help humans and IDEs understand the code.
from typing import Optional
                        # Optional[str] means: "this could be a string OR None"
                        # We use it when a function might not return a value
                        # (e.g., the API key might be missing → return None)


# ─── SECTION START ──────────────────────────────────────────────────────────
print("=" * 60)
print("  Section 2: Loading your API key securely")
print("=" * 60)
print()


# ─── THE RULE ───────────────────────────────────────────────────────────────
print("  THE RULE:")
print("  ❌ NEVER do this:  api_key = 'sk-abc123...'")
print("  ✅ ALWAYS do this: api_key = os.getenv('OPENAI_API_KEY')")
print()


def load_api_key() -> Optional[str]:
    """
    Loads the OpenAI API key from a .env file — NOT hardcoded.

    HOW IT WORKS (5 steps):
      1. Create a file called .env in your project folder
      2. Add this line: OPENAI_API_KEY=sk-...your-key...
      3. Add .env to .gitignore so Git never touches it
      4. load_dotenv() reads the .env file and puts each KEY=VALUE
         into the operating system's environment variables
      5. os.getenv("OPENAI_API_KEY") retrieves the value by name

    RETURN TYPE: Optional[str]
      - Returns the key as a string if everything works
      - Returns None if the key is missing (so the rest of the code
        can handle that gracefully instead of crashing)
    """

    # ── Step 1: Import the dotenv library ──────────────────────────────────
    # We use try/except here because the student might not have installed
    # python-dotenv yet. If the import fails, we catch the error and
    # print a helpful message instead of crashing.
    try:
        from dotenv import load_dotenv
        # load_dotenv is a function from the python-dotenv package.
        # It reads a .env file and loads each line as an environment variable.
    except ImportError:
        # ImportError means Python couldn't find the package
        print("  ❌ python-dotenv not installed.")
        print("     Fix: pip install python-dotenv")
        return None     # None means "no value" — signals failure

    # ── Step 2: Load the .env file ─────────────────────────────────────────
    # load_dotenv() does the following:
    #   - Looks for a file called .env in the current directory
    #   - Reads each line like KEY=VALUE
    #   - Puts each KEY=VALUE into os.environ (the system's variables)
    #   - Returns True if it found the file, False if not
    #   - It does NOT overwrite variables that are already set
    loaded = load_dotenv()

    if not loaded:
        # The .env file wasn't found — most common cause: the student
        # is running the script from a different folder than where .env lives
        print("  ⚠️  No .env file found in the current directory.")
        print("     Create a file called .env and add:")
        print("     OPENAI_API_KEY=sk-...your-key-here...")
        print()
        return None

    # ── Step 3: Read the key from environment variables ────────────────────
    # os.getenv("NAME") reads a variable from the environment.
    # If the variable doesn't exist, it returns None (not an error).
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        # The .env file was found, but it doesn't contain OPENAI_API_KEY
        print("  ❌ OPENAI_API_KEY not found in your .env file.")
        print("     Make sure the line is exactly: OPENAI_API_KEY=sk-...")
        print()
        return None

    # ── Step 4: Display the key safely (NEVER print the full key) ──────────
    # We show only the first 7 characters + dots so students can confirm
    # the key loaded without exposing the full secret.
    # [:7] is a slice — it takes the first 7 characters of the string.
    # "•" * 10 creates a string of 10 bullet characters for masking.
    masked = api_key[:7] + "•" * 10 + "..."
    print(f"  ✅ API key loaded: {masked}")

    # len() returns the number of characters in a string
    # A valid OpenAI key is typically 50+ characters
    print(f"     Key length: {len(api_key)} characters")
    print()

    return api_key  # Return the actual key for use in later sections


# ─── RUN IT ─────────────────────────────────────────────────────────────────
# Call the function and store the result.
# api_key will be either a string (the key) or None (if something failed).
api_key = load_api_key()

if api_key:
    print("  You're ready for Section 3 — your first API call.\n")
else:
    print("  Fix the issue above, then re-run this file.\n")
