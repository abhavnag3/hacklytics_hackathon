
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
    for i in range(65, 92): #dont actually let this run to 92. Play with it around 70 that way ur not waiting around alot
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
    with open("credit_card_names.txt", "w", encoding="utf-8") as file:
        for name in all_names:
            file.write(name + "\n")


def get_descriptions(letter ='A'):
    
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
    
    time.sleep(20)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    driver.quit()
    descriptions = []
    span_tags = soup.find('span', id = 'sh-quidget-4')
    if not span_tags:
        print(f"Span not found for id")
        #continue
    '''li_tags = span_tags.find_all('li')
    embedded_descrips = ""
    for li in li_tags:
        info = li.get_text(strip=True)
        embedded_descrips = embedded_descrips + info + "\n"
    print(f"DESCRIPS FOR SQ 4: {embedded_descrips}")'''
    for i in range(0,259):
        id = "sh-quidget-" + str(i)
        span_tags = soup.find('span', id = id)
        if not span_tags:
            #print(f"Span not found for id {id}")
            continue
        else:
            print(f"SPAN TAG FOUND FOR: {id}")  
            li_tags = span_tags.find_all('li')
            embedded_descrips = ""
            for li in li_tags:
                info = li.get_text(strip=True)
                embedded_descrips = embedded_descrips + info + "\n"
            if not embedded_descrips.strip() == "":
                descriptions.append(embedded_descrips)
    print("DESCRIPTIONS length: ", len(descriptions))
    with open("descriptions.txt", "w", encoding="utf-8") as file:
        for descrip in descriptions:
            pre = "Name:\nDescription: "
            file.write(pre + descrip + "\n" + "=" * 60 + "\n")
        
    #print(f'A TAGS: {a_tags}')
    
        



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


def join():
    names = []
    with open("credit_card_names.txt", "r") as names_file:
        names = [line.strip() for line in names_file if line.strip()]
    #print(names)
    
    i = 0
    lines = None
    with open("descriptions.txt", "r") as desc_file:
        lines = desc_file.readlines()
        
        #print(lines[3])
    
    
    with open("n_and_dA_to_C.txt", "w") as desc_file:
        #lines = desc_file.readlines()
        #print(lines[3])
        for line in lines:
            if line.startswith("Name:"):
                # Replace this line with the names joined by commas.
                updated_line = "Name: " + names[i] + "\n"
                desc_file.write(updated_line)
                i +=1
            else:
                desc_file.write(line)
            
def cards():
    lines = []
    with open('credit_card_data.txt', 'r') as file:
        lines = file.readlines()
    #print(lines)
    with open('credit_card_data.txt', 'w') as file:
        for line in lines:
            if line.startswith("Name:"):
                s = line.replace("Name:", "Credit Card Name:")
                file.write(s)
            else:
                file.write(line)
            

if __name__ == '__main__':

    num_args = len(sys.argv) - 1
    #scrap_page_using_selenium("https://www.cardratings.com/credit-card-list.html")
    #scrape_all_letters()
    #scrape_by_letter('D')
    #get_descriptions('A')
    #join()
    cards()
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