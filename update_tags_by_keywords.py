import os
import json

# Root folder of your databank
ROOT_DIR = r"C:\Users\marti\WoD-databank-for-grapevine2"
METADATA_DIR = os.path.join(ROOT_DIR, "metadata")

# Keyword map: add or adjust as needed
KEYWORD_MAP = {
    "vampire": ["vampire", "cainite", "blood", "embrace", "clan", "masquerade", "ghoul"],
    "werewolf": ["werewolf", "garou", "wyrm", "pack", "caern", "rage"],
    "mage": ["mage", "awakened", "paradox", "tradition", "chantry", "avatar"],
    "wraith": ["wraith", "shadowlands", "oblivion", "spectre", "haunt"],
    "changeling": ["changeling", "fae", "glamour", "dreaming", "kith", "seelie"],
}

def detect_category(text):
    """Return category based on keyword matches."""
    text_lower = text.lower()
    for category, keywords in KEYWORD_MAP.items():
        if any(word in text_lower for word in keywords):
            return category.capitalize()
    return "Shared / Other"

def update_metadata_tags():
    """Scan all metadata files and update tags based on content keywords."""
    updated_count = 0

    for file in os.listdir(METADATA_DIR):
        if file.endswith(".json") and file != "index.json":
            json_path = os.path.join(METADATA_DIR, file)

            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Read corresponding text file
            txt_path = os.path.join(ROOT_DIR, data["relative_path"])
            if not os.path.exists(txt_path):
                continue

            with open(txt_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            # Detect category and update tags
            category = detect_category(content)
            data["category"] = category
            data["source"] = category

            # Add category tag if missing
            if category.lower() not in [t.lower() for t in data["tags"]]:
                data["tags"].append(category)

            # Save updated metadata
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)

            updated_count += 1

    print(f"✅ Updated tags and categories for {updated_count} files.")

if __name__ == "__main__":
    update_metadata_tags()
