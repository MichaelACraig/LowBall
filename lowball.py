from dotenv import load_dotenv
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import pyautogui, time, os, json

# Chrome Webdriver Initalizer
def connect(url='https://www.facebook.com/marketplace'):

  chrome_options = Options() # Add headless mode later on
  chrome_options.add_argument("--window-size=1920x1080")
  
  driver = webdriver.Chrome(options=chrome_options)

  driver.get(url)
  
  return driver

# Helper for input_user_credentials to ennsure input fields are found.
def retrieve_input_fields(driver):
   try:
    user_field = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id=":r10:"]')))
    pass_field = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id=":r13:"]')))
    login = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="login_popup_cta_form"]/div/div[5]/div/div')))

    return user_field, pass_field, login
   except:
      return None, None, None
   
# Input login credentials to Facebook Marketplace; Technically don't need to do this; Simple secondary check. Shouldn't be an issue unless you have bad internet
def input_user_credentials(driver):
  load_dotenv()
  username = os.getenv('USERNAME')
  password = os.getenv('PASSWORD')

  # Need some sort of clause for if the username and password are not present
  
  user_field, pass_field, login = retrieve_input_fields(driver)
  if user_field is None:
    retrieve_input_fields(driver)
  
  user_field.click()
  user_field.send_keys(username)
  
  pass_field.click()
  pass_field.send_keys(password)

  login.click()
  time.sleep(10)

  return driver

# Searches an for an item given it finds a search bar
def search_item(driver, item):
  search_url = 'https://www.facebook.com/marketplace/category/search/?query='
  item_split = item.split(" ")
  
  # URL Edit for search
  if len(item_split) == 1:
      search_url += item_split[0]
  else:
    for i in item_split:
        if i == item_split[0]:
           search_url += i
        else:
            search_url += f'%{i}'
  
  driver.get(search_url) 
  
  return driver

# Scrape listings and collect the necessary data
def scrape_listings(driver):
  soup = BeautifulSoup(driver.page_source, 'html.parser')
  listings = soup.find_all('div',class_='x9f619 x78zum5 x1r8uery xdt5ytf x1iyjqo2 xs83m0k x1e558r4 x150jy0e x1iorvi4 xjkvuk6 xnpuxes x291uyu x1uepa24')
  listing_data = []
  for listing in listings:
    data = {}
    try:
      link_layer = listing.find('a', class_='x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g x1sur9pj xkrqix3 x1lku1pv')
      if link_layer and 'href' in link_layer.attrs:
        href = link_layer['href']
        link = f'https://www.facebook.com{href}'
        data['link'] = link
    except:
      data['link'] = ''
    
    try: # Issue with this one for slashed out prices due to discounts
      price = listing.find('span', class_='x193iq5w xeuugli x13faqbe x1vvkbs xlh3980 xvmahel x1n0sxbx x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x4zkp8e x3x7a5m x1lkfr7t x1lbecb7 x1s688f xzsf02u')
      price_text = price.text
      data['price'] = price_text
    except:
      data['price'] = ''

    try:
      layer = listing.find('div', class_='xyqdw3p x4uap5 xjkvuk6 xkhd6sd')
      name = layer.find('span', class_='x1lliihq x6ikm8r x10wlt62 x1n2onr6')
      name_text = name.text
      data['name'] = name_text
    except:
      data['name'] = ''

    try:
      location = listing.find('span', class_='x1lliihq x6ikm8r x10wlt62 x1n2onr6 xlyipyv xuxw1ft')
      location_text = location.text
      data['location'] = location_text
    except:
      data['location'] = ''

    if data.get('link', '') == '' and data.get('price', '') == '' and data.get('name', '') == '' and data.get('location', '') == '':
      continue
    
    listing_data.append(data)

  return listing_data
    
# Go to specific location (FUNCTION CANNOT BE HEADLESS IN ORDER TO RUN)
#WIP
def define_location(driver, zipcode=None, radius=None):
  # Random coordinates on webpage to remove Notifications blocker
  screen_width, screen_height = pyautogui.size()
  x = 627
  y = 250
  pyautogui.moveTo(x, y)
  pyautogui.click()
  
  location_change = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="seo_filters"]/div[1]/div[1]/div/span')))
  location_change.click()

  # Change radius around location (WIP Doesn't work right now)
  if radius is not None:
    radius_menu = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="mount_0_0_XL"]/div/div[1]/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div[3]/div/div[1]/div[3]/div/div/div')))
    radius_menu.click()
    time.sleep(10)

  location_search_x = 600
  location_search_y = 550
  pyautogui.moveTo(location_search_x, location_search_y)
  time.sleep(1)
  pyautogui.click()
  
  if zipcode is not None:
     pyautogui.typewrite(zipcode)
  
  pyautogui.press('enter')

  return driver

# Converts data to a json
def to_json(data):
  timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
  filename = f'{timestamp}_listings.json'
  with open(filename, 'w') as json_file:
      json.dump(data, json_file, indent=4)

# Applies all filters that user has put parameters in for
def apply_filters(driver):
  return driver

def main():
  driver = connect()
  driver = input_user_credentials(driver)
  driver = search_item(driver, "Summer house rent")
  data = scrape_listings(driver)
  to_json(data)
  time.sleep(5)
  driver.quit()

main()