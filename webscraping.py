
import requests
from bs4 import BeautifulSoup
import csv
import sys
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

'''def scrap_page_using_bs(url):
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/90.0.4430.93 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    
    soup = BeautifulSoup(response.text, 'html.parser')
    if response.status_code != 200:
        print(f"error to get {url}. Error presented is: {response.status_code}")
    a_tags = soup.find_all('a', class_ = 'sh-active-client')
    print(f'A TAGS: {a_tags}')
    credit_card_names = [a.get_text(strip=True) for a in a_tags]
    for card in credit_card_names:
        print(f"Credit Card: {card}")
'''

def get_all_url_names(url = ""):

    div_by_letter = url
    url_names = []
    for i in range(97, 123):
        div_by_letter = div_by_letter + "#div_" + chr(i)
        url_names.append(div_by_letter)
        div_by_letter = url
    return url_names

def get_all_credit_names(names_list):

    names = set()

    for url_name in names_list:
        scrap_page_using_selenium(url_name)

def scrape_all_letters():
    all_names = []
    for i in range(65, 70):
        print(f"\n==================So far we have {len(all_names)} total names\n=================")
        #convert ascii of character a-z ot char
        print(f"=====================\nGoing to get card names from letter {chr(i)}\n================\n")
        names_of_letter = scrape_by_letter(chr(i))
        delimiter = 49 #index of last credit card name that starts with C
        if i == 65:
            delimiter = 0
            all_names = all_names + names_of_letter[delimiter:]
        if i == 66 or i == 67 or len(names_of_letter) == 49:
            continue #skip if either the letter is 'A' or 'B' or if there are no credit card names in that letter
        else:
            all_names = all_names + names_of_letter[delimiter:]
        print(f"\n==================So far we have {len(all_names)} total names\n=================")
        
    print(name for name in all_names)
    print(f"NAMES: \n{all_names}")
        
        



def scrape_by_letter(letter = "A"):
    driver = webdriver.Chrome()
    url = "https://www.cardratings.com/credit-card-list.html"
    driver.get(url)
    try:

        letter_selector = f"a.div_{letter}"
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, letter_selector))
        )
        # Find and click the letter link
        letter_link = driver.find_element(By.CSS_SELECTOR, letter_selector)
        letter_link.click()
    except Exception as e:
        print(f"============\n===============\nERROR WHEN TRYING TO RUN SELECTOR: {e}")
        driver.quit()
        return []

    time.sleep(15)
    page_source= driver.page_source
    #-----------------------CHANGE CODE TO GET DESCRIPTION FROM THIS LINE---------------
    soup = BeautifulSoup(page_source, 'html.parser')
    driver.quit()
    a_tags = soup.find_all('a', class_ = 'sh-active-client sh-quidget-rendered')
    #print(f'A TAGS: {a_tags}')
    unwanted_texts = ['', 'See Rates and Fees', 'See Rates and Fees;terms apply', 'See Rates and Fees; terms apply']
    credit_card_names = [
        a.get_text(strip=True) 
        for a in a_tags
        if a.get_text(strip = True) not in unwanted_texts
    ]
    return credit_card_names

    #print(credit_card_names)
    #print(f"===================\n====================\n=============\nLength of credit card name array: {len(credit_card_names)}")
    #print(f"===================\n====================\n=============\nLast element of 'C' is index 48. Which is card name: ${credit_card_names[48]}")
    



def scrap_page_using_selenium(url):
    driver = webdriver.Chrome()
    print(f"DRIVER: {driver}")
    driver.get(url)
    print("DOING TIME SLEEP (3 SEC)")
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()
    a_tags = soup.find_all('a', class_ = 'sh-active-client sh-quidget-rendered')
    span_tag = soup.find('span', id='sh-quidget-2')
    if not span_tag:
        print("Span not found")
        return

    # Find all the <li> elements within the <span>
    li_tags = span_tag.find_all('li')
    for li in li_tags:
        info = li.get_text(strip=True)
        print(info)

    '''credit_card_names = [
        a.get_text(strip=True) 
        for a in a_tags
        if a.get_text(strip = True) not in unwanted_texts
    ]'''
    

    #print(credit_card_names)
    #print(f"===================\n====================\n=============\nLength of credit card name array: {len(credit_card_names)}")
    
    '''
    
    =======================
    Above code for getting all names from first rendered page 
    =======================
    
    '''



if __name__ == '__main__':

    num_args = len(sys.argv) - 1
    #scrap_page_using_selenium("https://www.cardratings.com/credit-card-list.html")
    scrape_all_letters()
    #scrape_by_letter('D')
    '''if num_args == 0:
        print('no URL provided')
        sys.exit()
    
    scraper_type = sys.argv[1]
    if scraper_type == 'bs':
        url = sys.argv[2]
        scrap_page_using_bs(url)
    elif scraper_type == 'sel':
        url = sys.argv[2]
        scrap_page_using_selenium(url)
    elif scraper_type == 'name':
        url = sys.argv[2]
        get_all_url_names(url)'''