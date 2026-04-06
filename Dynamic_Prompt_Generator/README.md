---

📘 README.md — Scholarly Prompt Studio

`markdown

Scholarly Prompt Studio
A modular, mode‑aware cognitive writing environment built with Python and KivyMD.

Scholarly Prompt Studio is a lightweight, mobile‑friendly research companion designed to support structured thinking, academic writing, and cognitive workflow refinement. It features a plugin‑driven architecture, awareness‑mode switching, suggestion engines, and a clean AMOLED‑friendly interface optimized for Android (Pydroid3) and desktop environments.

---

✨ Features

🧠 Awareness Modes
Switch between cognitive modes such as:
- Default  
- Phenomenological  
- Architecture  
- Systemic  
- Reflective  
- Analytical  
- Plugin‑defined modes  

Each mode influences the engine’s behavior and UI feedback.

🎛️ Mode‑Aware Interface
- Dynamic mode badge  
- Kernel activity indicator  
- Brain icon pulse animation  
- Clean, distraction‑free layout  

🔍 Intelligent Suggestion Engine
Real‑time suggestions for:
- Task  
- Context  
- Requirements  
- Style  

Suggestions adapt to user input and plugin extensions.

🧩 Plugin Architecture
Drop‑in Python modules for:
- Suggestions  
- Modes  
- Refinement logic  
- Output formatting  

Plugins auto‑load at startup.

📝 Generate + Refine Pipelines
- Structured text generation  
- Iterative refinement  
- Metadata‑rich history tracking  

📱 Android‑Friendly
Runs smoothly in Pydroid3 with KivyMD 0.104.2.

---

📦 Project Structure

`
src/
  scholarly_studio.py        # Main controller
  main.kv                    # UI layout
  studio_engine.py           # Core engine logic
  plugins/
    suggestions/
    modes/
    refinement/
    output/
  assets/
  settings.json              # User settings (ignored in git)
  history.json               # Output history (ignored in git)
`

---

🚀 Installation & Running

Android (Pydroid3)
1. Install Pydroid3 from Google Play  
2. Install dependencies via Pydroid pip:
   `
   pip install kivy kivymd
   `
3. Clone the repository:
   `
   git clone https://github.com/<your-username>/Scholarly-Prompt-Studio
   `
4. Open scholarly_studio.py in Pydroid  
5. Run the app

Desktop (Windows/macOS/Linux)
`
pip install kivy kivymd
python scholarly_studio.py
`

---

🧩 Plugin System

Plugins live in src/plugins/ and must define:

`python
def register(engine):
    # Extend engine.modes, engine.suggestions, etc.
`

The app automatically discovers and loads all plugin modules at startup.

---

🛠️ Development

Requirements
- Python 3.10+  
- Kivy 2.3+  
- KivyMD 0.104.2 (or latest stable)  

Contributing
Pull requests are welcome.  
See CONTRIBUTING.md for guidelines.

---

📄 License

This project is licensed under the MIT License.  
See LICENSE for details.

---

🌐 Project Status

Actively developed as part of the Architecture of Awareness research initiative.  
Future updates will include:
- Enhanced mode‑aware UI feedback  
- Plugin marketplace  
- Cognitive‑state visualization  
- Desktop‑optimized layout  
`

---