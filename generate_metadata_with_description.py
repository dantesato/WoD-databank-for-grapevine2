import os
import json

# Root folder of your databank
ROOT_DIR = r"C:\Users\marti\WoD-databank-for-grapevine2"

# Output folder for metadata files
OUTPUT_DIR = os.path.join(ROOT_DIR, "metadata")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def infer_category(filename):
    """Guess category based on filename keywords."""
    name = filename.lower()
    if "vampire" in name:
        return "Vampire: The Masquerade"
    elif "werewolf" in name:
        return "Werewolf: The Apocalypse"
    elif "mage" in name:
        return "Mage: The Ascension"
    else:
        return "Shared / Other"

def generate_metadata(file_path):
    """Create metadata dictionary for a single text file."""
    title = os.path.splitext(os.path.basename(file_path))[0]
    category = infer_category(title)
    tags = [tag for tag in title.split() if len(tag) > 3]

    # Extract first line as description
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            first_line = f.readline().strip()
    except Exception:
        first_line = ""

    metadata = {
        "title": title,
        "source": category,
        "category": category,
        "tags": tags,
        "description": first_line,
        "filename": os.path.basename(file_path),
        "relative_path": os.path.relpath(file_path, ROOT_DIR)
    }
    return metadata

def main():
    all_metadata = []
    for root, _, files in os.walk(ROOT_DIR):
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)
                meta = generate_metadata(file_path)
                all_metadata.append(meta)

                # Save individual JSON file
                json_path = os.path.join(OUTPUT_DIR, f"{meta['title']}.json")
                with open(json_path, "w", encoding="utf-8") as f:
                    json.dump(meta, f, indent=4)

    # Save master index
    index_path = os.path.join(OUTPUT_DIR, "index.json")
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(all_metadata, f, indent=4)

    print(f"✅ Metadata with descriptions generated for {len(all_metadata)} files.")

if __name__ == "__main__":
    main()
