# 🛹 generateTricks

**generateTricks** is an automation project that scrapes skateboarding resources and produces a comprehensive `tricks.yaml` file containing descriptions, inventors, years, and tutorial videos for hundreds of skateboard tricks.

This repo powers my [Trick of the Day] project — a GitHub Pages site that displays a new random skate trick every day.

---

## ⚡ Features
- Scrapes [skateboardingtrickslist.com](https://skateboardingtrickslist.com/all-skateboard-tricks/) for trick names & descriptions.
- Enriches data with inventors and years from [skateboarding.fandom.com](https://skateboarding.fandom.com).
- Automatically finds a top tutorial video on YouTube (excluding Braille Skateboarding).
- Outputs everything to a clean `tricks.yaml`.

Example YAML entry:
```yaml
- name: Kickflip
  description: The skater flicks the front foot off the board’s edge to make it spin once along its axis.
  video: https://www.youtube.com/embed/example123
  invented_by: Rodney Mullen
  year: 1983
```

---

## 🚀 How It Works
1. **Input**: `tricks.txt` — a text file with a giant list of trick names.
2. **Generator Script**: `generateTricks.py` scrapes, enriches, and compiles data.
3. **GitHub Actions Workflow**:
   - Runs the generator script.
   - Publishes the output `tricks.yaml` as a GitHub Release asset.
4. **Output**: always-available latest trick list release → consumed by [TrickOfTheDay]

---

## 🔧 Usage
### Local
```bash
pip install requests beautifulsoup4 pyyaml rapidfuzz
python generateTricks.py
```
Outputs `tricks.yaml`.

### GitHub Actions
- The repo has a workflow in `.github/workflows/main.yaml`.
- On push or manual run, it regenerates `tricks.yaml` and publishes a release called **Latest Tricks YAML**.

---

## 📦 Release
The latest generated file is always available here:  
👉 [**Download tricks.yaml**]

---

## 💡 Why?
This repo was built as part of my **GitHub Actions Certificate** project on LinkedIn Learning.  
Instead of a generic workflow, I wanted something fun for the skateboarding community.

---

## ✨ Next Steps
- Add more trick metadata (difficulty level, stance variations, etc.)
- Improve history data (fill in missing inventors/years)
- Hook directly into TrickOfTheDay’s daily workflow

---

## 🏴 Credits
- Skateboarding descriptions from [skateboardingtrickslist.com](https://skateboardingtrickslist.com/all-skateboard-tricks/)
- History from [skateboarding.fandom.com](https://skateboarding.fandom.com)
- Videos via YouTube (excluding Braille Skateboarding)

---

🛹 *Built with love, code, and skate culture.*
