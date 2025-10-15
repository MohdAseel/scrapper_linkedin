import os     
import time
import json
from selenium import webdriver     
from selenium.webdriver.common.by import By     
from selenium.webdriver.support.ui import WebDriverWait     
from selenium.webdriver.support import expected_conditions as EC     
from webdriver_manager.chrome import ChromeDriverManager     
from selenium.webdriver.chrome.service import Service     
from selenium.webdriver.chrome.options import Options     
from dotenv import load_dotenv  
from selenium.webdriver.common.keys import Keys

    
# Load credentials from .env or environment     
load_dotenv()     
EMAIL = os.getenv('LINKEDIN_EMAIL')     
PASSWORD = os.getenv('LINKEDIN_PASSWORD')   

# EMAIL = input("Enter your LinkedIn email: ")
# PASSWORD = input("Enter your LinkedIn password: ")
print(EMAIL, PASSWORD)  
if not EMAIL or not PASSWORD:     
    raise SystemExit('Set LINKEDIN_EMAIL and LINKEDIN_PASSWORD in env')     
    
# Chrome options (disable headless while developing because LinkedIn blocks headless sometimes)     
opts = Options()     
# opts.add_argument('--headless=new')   # enable later if needed
opts.add_argument('--no-sandbox')
opts.add_argument('--disable-dev-shm-usage')
opts.add_argument('--window-size=650,800') 

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=opts)
wait = WebDriverWait(driver, 15)

try:
    driver.get('https://www.linkedin.com')
    time.sleep(3)  # wait for page to load  
    #now click on sign in button
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'Sign in'))).click()
    # Login
    wait.until(EC.presence_of_element_located((By.ID, 'username'))).send_keys(EMAIL)
    time.sleep(1.50)
    driver.find_element(By.ID, 'password').send_keys(PASSWORD)
    wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[.//span[normalize-space(text())='Sign in'] or normalize-space(.)='Sign in']")
        )
    ).click()

    input("Press Enter after you've completed any 2FA if prompted...")

    
except Exception as e:
    print("An error occurred:", e)
print("Driver session is still active. You can continue coding and interacting with the browser.")


## we will click search and then search for the keyword entered 
keyword = input("enter the keyword for the people you want to search for : ")
# keyword = "data scientist"
#class="search-global-typeahead search-global-typeahead--semantic-rounded-search-box
#         global-nav__search-typeahead"
wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.search-global-typeahead__collapsed-search-button"))).click()
search_box = wait.until(EC.visibility_of_element_located(
    (By.CSS_SELECTOR, "input.search-global-typeahead__input[aria-label='Search']")))
search_box.clear()
search_box.send_keys(keyword)
search_box.send_keys(Keys.ENTER)

wait.until(EC.presence_of_element_located((By.CLASS_NAME, "search-reusables__filter-list")))
listy = driver.find_elements(By.CLASS_NAME, "search-reusables__primary-filter")
for i in listy:
    button = i.find_element(By.TAG_NAME, "button")
    if button.text.strip().lower() == "people":
        button.click()
        print("clicked on people filter")
        break


wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".linked-area.flex-1.cursor-pointer")))
cards = driver.find_elements(By.CSS_SELECTOR, ".linked-area.flex-1.cursor-pointer")

profiles = []

for card in cards:
    # --- Nested selections within each card ---


    try:
        pre = card.find_element(By.CSS_SELECTOR, ".t-roman.t-sans")
        name_tag = pre.find_element(By.TAG_NAME,"a")
        name = name_tag.text.strip()
        profile_link = name_tag.get_attribute("href")
    except:
        name, profile_link = None, None

    try:
        title = card.find_element(By.CSS_SELECTOR, ".t-14.t-black.t-normal").text
    except:
        title = None



 
    print(name, title, profile_link)
    profiles.append({
        "name": name,
        "title": title,
        "profile_link": profile_link
    })

json_output = json.dumps(profiles, indent=4)

file_name = input("Enter the filename to save the profiles (e.g., profiles.json): ")
with open(file_name, "w") as f:
    f.write(json_output)
print(f"Profiles saved to {file_name}")