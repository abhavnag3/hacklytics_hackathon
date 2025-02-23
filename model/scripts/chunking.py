import os, json

base_dir = os.path.dirname(os.path.abspath(__file__))
input_path = os.path.join(base_dir, "..", "data", "credit_cards.json")
output_path = os.path.join(base_dir, "..", "data", "chunked_credit_cards.json")

os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(input_path, "r", encoding="utf-8") as file:
    credit_cards = json.load(file)

chunked_data = []

def chunk_card(card):
    chunks = []
    card_name = card.get("name", "Unknown Card")
    credit_needed = card.get("credit_needed", "Not Specified")  

    for feature in card.get("features", []):
        chunks.append({
            "text": f"{card_name}: {feature}",
            "metadata": {
                "card_name": card_name,
                "credit_needed": credit_needed  
            }
        })

    return chunks

for card in credit_cards:
    if isinstance(card, dict):
        print(f"Processing: {card.get('name', 'Unknown Card')}")  
        chunks = chunk_card(card)
        chunked_data.extend(chunks)

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(chunked_data, f, indent=4)

print(f"✅ Chunked data saved to {output_path}")
