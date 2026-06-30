import os
import json

ROOT_DIR = r"C:\Users\marti\WoD-databank-for-grapevine2"
METADATA_DIR = os.path.join(ROOT_DIR, "metadata")

# --- PRIMARY CATEGORIES ---
PRIMARY = {
    "Vampire": [
        "vampire", "cainite", "kindred", "blood", "vitae", "embrace",
        "ghoul", "masquerade", "camarilla", "sabbat", "anarch",
        "clan", "generation", "diablerie", "bruja", "toreador",
        "ventrue", "nosferatu", "malkavian", "lasombra", "tzimisce",
        "ravnos", "gangrel", "assamite", "banu haqim", "ministry"
    ],
    "Werewolf": [
        "garou", "werewolf", "caern", "sept", "pack", "wyrm", "weaver",
        "wyld", "umbra", "gnosis", "rage", "tribe", "silver fang",
        "black spiral dancer", "red talon", "glass walker", "fianna",
        "shadow lord", "bone gnawer", "get of fenris"
    ],
    "Mage": [
        "mage", "awakened", "paradox", "avatar", "chantry", "tradition",
        "technocracy", "horizon realm", "sphere", "prime", "entropy",
        "correspondence", "forces", "matter", "mind", "spirit", "time",
        "verbena", "sons of ether", "order of hermes", "virtual adept"
    ],
    "Wraith": [
        "wraith", "shadowlands", "oblivion", "spectre", "fetters",
        "haunts", "stygia", "legion", "passion", "pathos"
    ],
    "Changeling": [
        "changeling", "fae", "glamour", "banality", "dreaming",
        "kith", "seelie", "unseelie", "sidhe", "redcap", "sluagh"
    ]
}

# --- SUBDIVISIONS / FACTIONS / THEMES ---
SUBTAGS = {
    "Camarilla": ["camarilla", "ivory tower", "justicar", "prince"],
    "Sabbat": ["sabbat", "black hand", "pack priest", "ductus"],
    "Anarch": ["anarch", "barony", "free state"],
    "Technocracy": ["technocracy", "iteration x", "new world order", "progenitors"],
    "Traditions": ["tradition", "order of hermes", "verbena", "choristers"],
    "Umbra": ["umbra", "spirit world", "gauntlet"],
    "Wyrm": ["wyrm", "pentex", "black spiral"],
    "Wyld": ["wyld"],
    "Weaver": ["weaver"],
    "Kiths": ["sidhe", "redcap", "boggan", "troll", "sluagh"],
    "Clans": ["ventrue", "toreador", "malkavian", "gangrel", "lasombra", "tzimisce"],
    "Spheres": ["prime", "entropy", "forces", "matter", "mind", "spirit", "time", "correspondence"]
}

def detect_primary(text):
    text = text.lower()
    for category, words in PRIMARY.items():
        if any(w in text for w in words):
            return category
    return "Shared / Other"

def detect_subtags(text):
    text = text.lower()
    found = []
    for tag, words in SUBTAGS.items():
        if any(w in text for w in words):
            found.append(tag)
    return found

def update_metadata():
    updated = 0

    for file in os.listdir(METADATA_DIR):
        if not file.endswith(".json") or file == "index.json":
            continue

        json_path = os.path.join(METADATA_DIR, file)
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        txt_path = os.path.join(ROOT_DIR, data["relative_path"])
        if not os.path.exists(txt_path):
            continue

        with open(txt_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        # Detect primary category
        primary = detect_primary(content)
        data["category"] = primary
        data["source"] = primary

        # Detect subtags
        subtags = detect_subtags(content)

        # Merge tags
        existing = {t.lower() for t in data["tags"]}
        for tag in subtags:
            if tag.lower() not in existing:
                data["tags"].append(tag)

        # Add primary category tag if missing
        if primary.lower() not in existing:
            data["tags"].append(primary)

        # Save
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

        updated += 1

    print(f"✅ Updated categories and subtags for {updated} files.")

if __name__ == "__main__":
    update_metadata()
