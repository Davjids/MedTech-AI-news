import os
from google import genai

# Initialize Gemini Client using your secret key
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

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

# Write output to content.md
with open("content.md", "w", encoding="utf-8") as f:
    f.write(response.text)
