import asyncio, time
from pyppeteer import launch
from utils import CHROMEDRIVER, FB_USER, FB_PASS


async def pull_urls():
        pass

async def find_element(page, selector):
    return await page.querySelector(selector)

async def find_elements(page, selector):
     return await page.querySelectorAll(selector)

async def login(page, username, password):
    user_input = await find_element(page,'input[id=":r10:"]')
    pass_input = await find_element(page, 'input[id=":r13:"]')
    login_button = await find_elements(page,'div[aria-label="Accessible login button"]')
    
    if user_input and pass_input and login_button:
        await user_input.click()
        await user_input.type(username)

        await pass_input.click()
        await pass_input.type(password)

        for item in login_button: # There's two elements on the homepage; slightly inefficient but works so whatever. Try-except clause needed for the one that isn't applicable
            try:
                await item.click()
            except:
                 continue    

    else:
        print("One or more input fields not found!")      

async def main():
        browser = await launch(executablePath = CHROMEDRIVER, headless = False)
        page = await browser.newPage()

        await page.goto('https://www.facebook.com/marketplace/')
        await login(page, FB_USER, FB_PASS)
        await asyncio.sleep(1000)
        await browser.close()  

asyncio.get_event_loop().run_until_complete(main())
