import json
import re
from bs4 import BeautifulSoup

# this script parses the scraped website data and structures it into json

# Step 1: read the scraped text file
with open("sample.txt", "r", encoding="utf-8") as file:
    raw_html = file.read()

# Step 2: Parse the HTML
soup = BeautifulSoup(raw_html, "html.parser")

# Step 3: Extract <li> text from the scraped content
items = [li.get_text(strip=True) for li in soup.find_all('li')]

# Step 4: Categorize extracted text into JSON fields
annual_fee_text = next((s for s in items if "annual fee" in s.lower()), "No Annual Fee")
annual_fee = 0 if "No Annual Fee" in annual_fee_text else int(re.findall(r"\d+", annual_fee_text)[0])

# Step 5: Store data in a simpler JSON format
card_data = {
    "name": "Hello",  # Placeholder, to be filled when extracting names
    "issuer": "Unknown",  # Placeholder for now
    "credit_needed": [],  # To be extracted later
    "annual_fee": annual_fee,
    "rewards": [s for s in items if "miles" in s.lower() or "points" in s.lower()],  # Extract reward-related text
    "perks": [s for s in items if "fee" in s.lower() or "credit" in s.lower() or "Pay with Miles" in s]  # Extract perks
}

# Step 4: Save to JSON file
with open("credit_cards.json", "w") as f:
    json.dump(card_data, f, indent=4)

# Step 5: Print Output
print(json.dumps(card_data, indent=4))

