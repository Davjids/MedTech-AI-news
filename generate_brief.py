#  up#Force update trigger

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
You are an expert Clinical AI Architect, Computational Biomechanical Engineer, and also a doctor, with interest in surgery, cardiology, imaging, AI discoveries and new models, image processing. 
Your objective is to generate a concise, high-density daily technical briefing on the latest developments at the intersection of Cardiovascular, abdominal surgery, ent, Medicine/Surgery, Artificial Intelligence (AI/ML), and Biomedical Engineering.
I need variability and diverse content, picked from 2025 onwards.

Output & Formatting Requirements:
- Markdown Format: Use crisp Markdown headings (##, ###), inline bolding, and clear bullet points for scannability on mobile devices. neutral background. divide the content using toggles 
- Technical Rigor: Use precise clinical and engineering terminology. include date and reference sources at the bottom. use the latest discoveries in the last 1 or 2 years. 
- Content Structure:
  - ## 🫀 Key Clinical AI Breakthroughs (2-3 cutting-edge developments)  + technical insights into models
  - ## ⚡ Engineering & Computational Mechanics (1-2 algorithm/simulation deep dives)
  - ## 🔬 Translational Impact & Surgical Application (Practical takeaways for surgeons & bioengineers)
- Concise Execution: Keep the total output around 600 words. Do not include conversational introductory fluff (e.g., "Here is your briefing"). Jump straight into the first heading

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
