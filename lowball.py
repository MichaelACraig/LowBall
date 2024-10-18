from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time, os

# Chrome Webdriver Initalizer
def connect(url='https://www.facebook.com/marketplace'):
  driver = webdriver.Chrome()
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
  time.sleep(100)
  return driver

def main():
  driver = connect()
  driver = input_user_credentials(driver)

main()