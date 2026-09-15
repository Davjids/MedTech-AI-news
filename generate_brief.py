# Force update trigger

import os
import sys
from google import genai

api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    print("Error: GEMINI_API_KEY secret is not set in GitHub settings!")
    sys.exit(1)

try:
    client = genai.Client(api_key=api_key)

    prompt = """
    You are a daily creative tech curator. 
    Synthesize 3 cutting-edge developments, open-source breakthroughs, or architectural patterns in AI, edge computing, and local-first tech.
    Format output cleanly in Markdown:
    - Include today's date at the top as an <h1> title
    - Use '###' subheadings for each item
    - End each section with a '> Builder Perspective:' callout blockquote.
    """

    # Updated to the current supported model string
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    with open("content.md", "w", encoding="utf-8") as f:
        f.write(response.text)

    print("Successfully generated content.md!")

except Exception as e:
    print(f"Failed to generate brief: {e}")
    sys.exit(1)
