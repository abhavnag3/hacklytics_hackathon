import os, json
import re
import unicodedata

# Function to remove trademark symbols and special characters
def clean_text(text):
    return unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")

# Step 0: Get directories for /data
base_dir = os.path.dirname(os.path.abspath(__file__))
input_path = os.path.join(base_dir, "..", "data", "raw_data.txt")
output_path = os.path.join(base_dir, "..", "data", "credit_cards.json")
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Step 1: Read the scraped text file
with open(input_path, "r", encoding="utf-8") as file:
    raw_data = file.read()

# Step 2: Extract each card
cards = raw_data.split("=" * 60)  # Split using separator line
parsed_cards = []

# Keywords for feature extraction
FEATURE_KEYWORDS = ["miles", "points", "earn", "cash back", "bonus", "fee", "credit", 
                    "foreign transaction", "no annual fee", "protection", "apr"]

# first script in the pipeline

def extract_features(text):
    """Returns True if a line contains useful card details."""
    return any(word in text.lower() for word in FEATURE_KEYWORDS)

for card in cards:
    lines = [line.strip() for line in card.split("\n") if line.strip()]
    card_data = {"features": []}  # Store all relevant info here
    current_key = None

    for line in lines:
        if line.startswith("Credit Card Name:"):
            card_data["name"] = clean_text(line.replace("Credit Card Name:", "").strip())
        elif ":" in line:  # Key: Value pairs
            key, value = line.split(":", 1)
            current_key = key.strip().lower().replace(" ", "_")
            card_data[current_key] = clean_text(value.strip())

            # Store feature if it matches relevant keywords
            if extract_features(value):
                card_data["features"].append(clean_text(value.strip()))

        elif current_key:  # Handle multiline values
            card_data[current_key] += " " + line.strip()
            if extract_features(line):
                card_data["features"].append(clean_text(line.strip()))

    # Apply Unicode cleaning to features
    card_data["features"] = [clean_text(f) for f in card_data["features"]]

    # Remove description if redundant
    card_data.pop("description", None)

    if card_data:
        parsed_cards.append(card_data)

# Step 3: Save the parsed data as JSON
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(parsed_cards, f, indent=4)

print(f"✅ Processed {len(parsed_cards)} credit cards and saved to {output_path}")
