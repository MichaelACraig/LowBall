from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import pyautogui, time, os

# Chrome Webdriver Initalizer
def connect(url='https://www.facebook.com/marketplace'):
  
  # I don't know why, but headless mode opens a white box when it shouldn't be opening anything
  # Fix later!
  chrome_options = Options()
  #chrome_options.add_argument("--headless")
  #chrome_options.add_argument("--disable-gpu")
  #chrome_options.add_argument("--no-sandbox")
  chrome_options.add_argument("--window-size=1920x1080")

  driver = webdriver.Chrome(options=chrome_options)
  driver.get(url)
  
  return driver

# Input login credentials to Facebook Marketplace; Technically don't need to do this
def input_user_credentials(driver):
  load_dotenv()
  username = os.getenv('USERNAME')
  password = os.getenv('PASSWORD')
  
  user_field = driver.find_element(By.XPATH, '//*[@id=":r1:"]')
  pass_field = driver.find_element(By.XPATH, '//*[@id=":r4:"]')
  login = driver.find_element(By.XPATH, '//*[@id="login_popup_cta_form"]/div/div[5]')

  # Gotta swap this out soon, but good temp for if user is already logged in
  if user_field is None:
    return driver
  
  user_field.click()
  user_field.send_keys(username)
  
  pass_field.click()
  pass_field.send_keys(password)

  login.click()
  
  # Add WebDriverWait sometime later when we finnd a good login element
  # Can't find one right now so good temp fix
  time.sleep(10)

  cookies = driver.get_cookies()

  return driver, cookies

# Searches an for an item given it finds a search bar
def search_item(driver, item, cookies=None):
  search_url = 'https://www.facebook.com/marketplace/category/search/?query='
  item_split = item.split(" ")
  
  # URL Edit for search
  if len(item_split) == 1:
      search_url += i
  else:
    for i in item_split:
        if i == item_split[0]:
           search_url += i
        else:
            search_url += f'%{i}'
  
  driver.get(search_url) 
  
  return driver

# Go to specific location
def define_location(driver, cookies=None):
  screen_width, screen_height = pyautogui.size()
  # Random coordinates on webpage to remove Notifications blocker
  x = 627
  y = 250

  pyautogui.moveTo(x, y)
  pyautogui.click()

  location_change = driver.find_element(By.XPATH, '//*[@id="seo_filters"]/div[1]/div[1]/div/span')
  location_change.click()

  return driver

# Fully encompassing function that adjusts all features for item search 
def apply_filters(driver):
  return driver

def main():
  driver = connect()
  driver, cookies = input_user_credentials(driver)
  driver = search_item(driver, "Fortnite Battle Pass")
  driver = define_location(driver)
  time.sleep(10)
  driver.quit()

main()