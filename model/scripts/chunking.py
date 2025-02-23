import os, json

# Step 1: Define paths
base_dir = os.path.dirname(os.path.abspath(__file__))
input_path = os.path.join(base_dir, "..", "data", "credit_cards.json")
output_path = os.path.join(base_dir, "..", "data", "chunked_credit_cards.json")

# Ensure the output directory exists
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Step 2: Read the processed credit card JSON
with open(input_path, "r", encoding="utf-8") as file:
    credit_cards = json.load(file)

chunked_data = []

# Step 3: Chunk each card into meaningful sections
def chunk_card(card):
    """ Breaks a credit card's data into individual chunks while keeping metadata """
    chunks = []
    card_name = card.get("name", "Unknown Card")

    # Process each feature as a separate chunk
    for feature in card.get("features", []):
        chunks.append({
            "text": f"{card_name}: {feature}",
            "metadata": {"card_name": card_name}
        })

    return chunks

# Step 4: Process each credit card
for card in credit_cards:
    if isinstance(card, dict):
        print(f"Processing: {card.get('name', 'Unknown Card')}")  # Debugging
        chunks = chunk_card(card)
        chunked_data.extend(chunks)

# Step 5: Save chunked data
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(chunked_data, f, indent=4)

print(f"✅ Chunked data saved to {output_path}")
