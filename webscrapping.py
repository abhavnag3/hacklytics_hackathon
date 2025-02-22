import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_whole_website():
    """Scrapes credit card names and descriptions for letters D-Z and writes them to a .txt file."""
    
    with open("credit_card_data.txt", "w", encoding="utf-8") as file:
        for letter in "DGHIMNPSTUW":  # Iterating over letters D-Z
            print(f"\n========== Scraping letter {letter} ==========")

            # Get page source
            page_source = change_page(letter)
            if not page_source:
                print(f"Skipping {letter} due to page retrieval failure.")
                continue  # Skip this letter if the page couldn't be loaded

            # Get names and descriptions
            card_names = scrape_all_letters(letter, page_source)
            bullet_points = get_bulletpoints(page_source)

            # Write to file
            for i, name in enumerate(card_names):
                description = bullet_points[i].text.strip() if i < len(bullet_points) else "No description available"
                file.write(f"Credit Card Name: {name}\n")
                file.write(f"Description: {description}\n")
                file.write("=" * 60 + "\n")  # Separator for readability

            print(f"Found {len(card_names)} cards for {letter}")

    print("\n✅ Data scraping complete! Credit card details saved to 'credit_card_data.txt'.")



#----------------------------------------------------------------------------------------------------------------------#
def get_bulletpoints(page_source):
    """
    Parse the HTML content from Selenium's page_source using BeautifulSoup,
    and select all elements with the class 'shortDescription' for ONE card.
    """
    soup = BeautifulSoup(page_source, "html.parser")

    bullets = soup.find_all("div", class_="longDescription") # Find returns the first matching thing it finds
    if bullets is None:
        bullets = ""

    return bullets



#----------------------------------------------------------------------------------------------------------------------#
def change_page(letter):
    """
    Launches a Chrome webdriver, navigates to the main page, clicks the letter link,
    waits for the content to load, and returns the page source.
    
    Parameters:
      letter (str): The letter corresponding to the desired page (e.g., "A", "B", etc.).
      
    Returns:
      str: The HTML content of the letter page if successful, or an empty string if not.
    """
    driver = webdriver.Chrome()
    url = "https://www.cardratings.com/credit-card-list.html"
    driver.get(url)
    
    try:
        # Build the CSS selector for the letter link. For example, for letter "A": "a.div_A"
        letter_selector = f"a.div_{letter}"
        # Wait until the letter link is present on the page
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, letter_selector))
        )
        # Find and click the letter link
        letter_link = driver.find_element(By.CSS_SELECTOR, letter_selector)
        letter_link.click()
        
        # Wait for the new page to load by waiting for an element with class "shortDescription"
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".shortDescription"))
        )
        
        # Once loaded, capture the page source
        page_source = driver.page_source
    except Exception as e:
        print(f"ERROR WHEN TRYING TO RUN SELECTOR: {e}")
        page_source = ""
    finally:
        driver.quit()
    
    return page_source



#----------------------------------------------------------------------------------------------------------------------#
def scrape_by_letter(page_source, letter):
    """Extracts credit card names from the given page source, filtering by the letter."""
    if not page_source:
        return []  # Return an empty list if the page source could not be retrieved

    soup = BeautifulSoup(page_source, 'html.parser')
    a_tags = soup.find_all('a', class_='sh-active-client sh-quidget-rendered')

    unwanted_texts = [
        '', 
        'See Rates and Fees', 
        'See Rates and Fees;terms apply', 
        'See Rates and Fees; terms apply'
    ]
    
    credit_card_names = [
        a.get_text(strip=True)
        for a in a_tags
        if a.get_text(strip=True) not in unwanted_texts
    ]

    # **Filter out names that do not start with the given letter**
    filtered_names = [name for name in credit_card_names if name.startswith(letter)]

    return filtered_names


def scrape_all_letters(letter, page_source):
    """Scrapes all credit card names from a given letter page."""
    if not page_source:
        return []  # Return an empty list if the page source is invalid
    
    # Fetch credit card names for the given letter
    names_of_letter = scrape_by_letter(page_source, letter)    
    return names_of_letter

        

scrape_whole_website()
