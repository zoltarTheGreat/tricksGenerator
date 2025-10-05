import requests
from bs4 import BeautifulSoup
import yaml
import urllib.parse
import re
import time
import os

INPUT_FILE = "tricks.txt"
OUTPUT_FILE = "tricks.yaml"

PARSEBOT_URL = "https://api.parse.bot/scraper/1871f800-c527-45f3-9a95-cdfd06e7cfa0/run"
API_KEY = os.environ['PARSE_API_KEY']
EXCLUDE_CHANNEL = "Braille Skateboarding"

def load_tricks_txt():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        tricks = [line.strip() for line in f if line.strip()]
    return tricks

def scrape_trick_list():
    url = "https://skateboardingtrickslist.com/all-skateboard-tricks/"
    r = requests.get(url, timeout=15)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")
    tricks = {}

    for p in soup.select("p"):
        strong = p.find("strong")
        em = p.find("em")
        if strong and em:
            raw_name = strong.get_text()
            name = re.sub(r'^\d+\.\s*', '', raw_name).strip()
            desc = em.get_text().strip()
            tricks[name.lower()] = desc
    return tricks

def scrape_fandom(trick_name):
    base_url = "https://skateboarding.fandom.com/wiki/"
    url = base_url + urllib.parse.quote(trick_name.replace(" ", "_"))
    info = {"invented_by": "Unknown", "year": "Unknown", "description": "Unknown"}

    try:
        r = requests.get(url, timeout=10)
        if r.status_code != 200:
            return info

        soup = BeautifulSoup(r.text, "html.parser")

        para = soup.select_one("div.mw-parser-output > p")
        if para and para.get_text(strip=True):
            info["description"] = para.get_text(strip=True)

        text = soup.get_text(" ", strip=True)

        if "invented" in text.lower():
            idx = text.lower().find("invented")
            snippet = text[idx:idx+200]
            info["invented_by"] = snippet

        years = re.findall(r"(19\d{2}|20\d{2})", text)
        if years:
            info["year"] = years[0]

    except Exception:
        pass
    return info

def get_youtube_video(trick):
    payload = {
        "query": f"how to {trick} skateboarding",
        "exclude_channel": EXCLUDE_CHANNEL
    }
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": API_KEY
    }
    try:
        r = requests.post(PARSEBOT_URL, json=payload, headers=headers, timeout=15)
        r.raise_for_status()
        data = (r.json()).get('data')
        if 'url' in data:
            return data['url']
    except Exception as e:
        print(f"YouTube fetch failed for {trick}: {e}")
    return "Unknown"

def get_description(trick, desc_map):
    trick_lower = trick.lower()
    if trick_lower in desc_map:
        return desc_map[trick_lower]
    for key, desc in desc_map.items():
        if trick_lower.startswith(key) or key.startswith(trick_lower):
            return desc
    first_word = trick_lower.split()[0]
    for key, desc in desc_map.items():
        if key.startswith(first_word):
            return desc
    return "Unknown"

def generate_yaml(trick_names, desc_map):
    data = []
    for i, trick in enumerate(trick_names, start=1):
       
        description = get_description(trick, desc_map)

        fandom_info = scrape_fandom(trick)
        if not description or description == "Unknown":
            description = fandom_info["description"]

        video = get_youtube_video(trick)

        entry = {
            "name": trick,
            "description": description,
            "video": video,
            "invented_by": fandom_info["invented_by"],
            "year": fandom_info["year"]
        }
        data.append(entry)

        print(f"[{i}/{len(trick_names)}]  {trick}")

        time.sleep(2)
    return data

def save_yaml(data):
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        yaml.dump(data, f, sort_keys=False, allow_unicode=True)

if __name__ == "__main__":
    trick_names = load_tricks_txt()
    print(f"Loaded {len(trick_names)} tricks from {INPUT_FILE}")

    desc_map = scrape_trick_list()
    print(f"Scraped {len(desc_map)} tricks from skateboardingtrickslist.com")
    
    data = generate_yaml(trick_names, desc_map)
    save_yaml(data)

    print(f"Generated {OUTPUT_FILE} with {len(data)} tricks")
