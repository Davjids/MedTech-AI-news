#  up#Force update trigger


import os
import json
import datetime
import urllib.request
import urllib.parse
from pathlib import Path

# --- CONFIGURATION & PATHS ---
HISTORY_FILE = Path("history.json")
OUTPUT_FILE = Path("index.html")

def load_history():
    """Load previously covered topic headlines from history.json."""
    if HISTORY_FILE.exists():
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_history(history):
    """Save updated topic history back to history.json."""
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)

def generate_content_with_llm(history):
    """
    Calls the LLM passing past history as negative constraints
    with dynamic sampling temperature.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Missing OPENAI_API_KEY environment variable.")

    # Fetch up to 25 recent topics to prevent repetition
    past_topics = history[-25:]

    system_prompt = (
        "You are an expert MedTech AI curator. Your job is to select and summarize 3 distinct, "
        "cutting-edge news items or breakthroughs in medical technology and artificial intelligence."
    )

    user_prompt = f"""
Select 3 fresh, impactful news items/developments in MedTech AI.

CRITICAL REQUIREMENT - DO NOT REPEAT PAST TOPICS:
Here is a list of recently published topics and headlines. You MUST NOT cover these or similar items again:
{json.dumps(past_topics, indent=2)}

Instructions:
1. Provide clean HTML output formatted as an article feed (semantic HTML5, direct cards/sections).
2. Return a JSON object with two keys:
   - "titles": A list of the 3 main headline titles generated today (for tracking history).
   - "html_body": The HTML string representing the 3 news items to be embedded into the website.
"""

    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4o-mini",
        "temperature": 0.8,  # Higher temperature forces unique selections each run
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    }

    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
    with urllib.request.urlopen(req) as response:
        res_data = json.loads(response.read().decode("utf-8"))
        content = json.loads(res_data["choices"][0]["message"]["content"])
        return content

def update_html_page(html_body):
    """Renders the final index.html with the new body content."""
    today_str = datetime.datetime.now().strftime("%B %d, %Y")
    
    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MedTech AI News Daily</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; max-width: 800px; margin: 0 auto; padding: 20px; background: #f8fafc; color: #1e293b; }}
        header {{ border-bottom: 2px solid #e2e8f0; padding-bottom: 15px; margin-bottom: 30px; }}
        h1 {{ margin: 0; color: #0f172a; font-size: 2rem; }}
        .date {{ color: #64748b; font-size: 0.9rem; margin-top: 5px; }}
        .news-card {{ background: white; padding: 24px; border-radius: 12px; margin-bottom: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); border: 1px solid #e2e8f0; }}
        .news-card h2 {{ margin-top: 0; color: #2563eb; font-size: 1.3rem; }}
        footer {{ text-align: center; margin-top: 40px; font-size: 0.85rem; color: #94a3b8; }}
    </style>
</head>
<body>
    <header>
        <h1>MedTech AI Daily Digest</h1>
        <div class="date">Updated: {today_str}</div>
    </header>
    <main>
        {html_body}
    </main>
    <footer>
        <p>Automated Daily Briefing • MedTech AI News</p>
    </footer>
</body>
</html>
"""
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(full_html)

def main():
    history = load_history()

    # Generate content using LLM
    result = generate_content_with_llm(history)
    
    new_titles = result.get("titles", [])
    html_body = result.get("html_body", "")

    # Update history and save output
    history.extend(new_titles)
    save_history(history)
    update_html_page(html_body)
    print(f"Successfully generated 3 articles. Updated history.json with: {new_titles}")

if __name__ == "__main__":
    main()
