import os
import sys
from google import genai

# Verify secret is present in GitHub Actions
if not os.environ.get("GEMINI_API_KEY"):
    print("Error: GEMINI_API_KEY environment variable is missing in GitHub secrets.")
    sys.exit(1)

try:
    # The client automatically picks up GEMINI_API_KEY from environment variables
    client = genai.Client()

    prompt = """
    You are a daily creative tech curator. 
    Synthesize 3 cutting-edge developments, open-source breakthroughs, or architectural patterns in AI, edge computing, and local-first tech.
    Format output cleanly in Markdown:
    - Include today's date at the top as an <h1> title
    - Use '###' subheadings for each item
    - End each section with a '> Builder Perspective:' callout blockquote.
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    with open("content.md", "w", encoding="utf-8") as f:
        f.write(response.text)

    print("Success: content.md updated!")

except Exception as e:
    print(f"Execution failed: {e}")
    sys.exit(1)
