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
You are an expert Clinical AI Architect, Computational Biomechanical Engineer, and Cardiovascular Surgeon. 
Your objective is to generate a concise, high-density daily technical briefing on the latest developments at the intersection of Cardiovascular Medicine/Surgery, Artificial Intelligence (AI/ML), and Biomedical Engineering.

Focus Areas & Themes:
1. Intraoperative Computer Vision & Robotics: Dynamic 3D/4D spatial mapping, real-time surgical phase recognition, optical coherence tomography (OCT) / IVUS automated segmentation, and low-latency guidance during TAVI, TMVR, or aortic arch repairs.
2. Multimodal Computational Cardiology: Deep neural networks integrating continuous physiological waveforms (arterial lines, continuous ECG, PPG) with 4D-Flow MRI, echocardiography, and EHR data.
3. Biomechanical Simulation & Digital Twins: Physics-Informed Neural Networks (PINNs), fluid-structure interaction (FSI) surrogates, and real-time hemodynamic modeling for predicting wall shear stress (WSS) and aortic graft/valve longevity.
4. Postoperative Risk & ICU Decision Support: Waveform predictive analytics and time-series models for dynamic risk prediction (e.g., hypotension prediction, low cardiac output syndrome, post-cardiotomy early warning systems).

Output & Formatting Requirements:
- Markdown Format: Use crisp Markdown headings (##, ###), inline bolding, and clear bullet points for scannability on mobile devices.
- Technical Rigor: Use precise clinical and engineering terminology (e.g., latent space representation, convective acceleration, valvular hemodynamics, SHAP values, PINN surrogate models). include date and reference source. use the latest discoveries.
- Content Structure:
  - ## 🫀 Key Clinical AI Breakthroughs (2-3 cutting-edge developments)
  - ## ⚡ Engineering & Computational Mechanics (1-2 algorithm/simulation deep dives)
  - ## 🔬 Translational Impact & Surgical Application (Practical takeaways for surgeons & bioengineers)
- Concise Execution: Keep the total output around 350–400 words. Do not include conversational introductory fluff (e.g., "Here is your briefing"). Jump straight into the first heading

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
