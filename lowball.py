import asyncio, time
from pyppeteer import launch
from utils import CHROMEDRIVER

async def launch_browser(): # Launches Pyppetteer Browser
    browser = await launch(executablePath = CHROMEDRIVER, headless = False)
    page = await browser.newPage()
    
    return page, browser

async def find_element(page, selector): # Finds individual elements on page
    return await page.querySelector(selector)

async def find_elements(page, selector): # Finds all elements of selector type on page
     return await page.querySelectorAll(selector)

async def scroll(page): # Scrolls down page to a specific length
    pass

async def pull_urls(page): # pulls URLs from listings page
    pass
     
async def login(page, username, password): # Logins to the given facebook marketplace page
    user_input_box = await find_element(page,'input[id=":r10:"]')
    pass_input_box = await find_element(page, 'input[id=":r13:"]')
    login_button = await find_elements(page,'div[aria-label="Accessible login button"]')
    
    if user_input_box and pass_input_box and login_button:
        await user_input_box.click()
        await user_input_box.type(username)

        await pass_input_box.click()
        await pass_input_box.type(password)

        for item in login_button: # There's two elements on the homepage; slightly inefficient but works so whatever. Try-except clause needed for the one that isn't applicable
            try:
                await item.click()
            except:
                 continue    

    else:
        print("One or more input fields not found!")

async def algorithm(page): # Main algorithm for combing listings
    await page.goto('https://www.facebook.com/marketplace/')

    print("Input your Username Below:")
    FB_USER = input()

    print("Input your Password Below:")
    FB_PASS = input()

    print("Login credentials are:")
    print("USERNAME: " + FB_USER)
    print("PASSWORD:" + FB_PASS)

    await login(page, FB_USER, FB_PASS)
    #if # If clause when a CAPTCHA page is reached, do asyncio.sleep(60) to manually solve CAPTCHA

    await asyncio.sleep(1000) # Temporary for testing

async def main(): # Wrapper for algorithm calls
        page, browser = await launch_browser()
        await algorithm(page)
        await browser.close()  

asyncio.get_event_loop().run_until_complete(main())
