import asyncio, time
from pyppeteer import launch
from utils import CHROMEDRIVER

"""
Notes:
- We could redo the makeup of find_element(s) w/ a try-except clause to pinpoint issues easier
    * Not super necessary now, but a good thought we could do for later for OOP Principals
"""
async def launch_browser(): # Launches Pyppetteer Browser
    browser = await launch(executablePath = CHROMEDRIVER, headless = False)
    page = await browser.newPage()
    
    return page, browser

async def find_element(page, selector): # Finds individual elements on page
    try:
        element = await page.waitForSelector(selector, timeout=5000) # Wait for the element to appear
        return element
    except Exception as e:
        print(f'Error in find_element: {e}')
        
    return None

async def find_elements(page, selector): # Finds all elements of selector type on page
    try:
        elements = await page.querySelectorAll(selector)
        return elements
    except Exception as e:
        print(f'Error in find_elements: {e}')
        
    return None

async def get_element_position(page, selector): # Finds the position of a passed in selector element on page; Possibly second-option if traditional find_element search doesn't work
    try:
        element = await find_element(page, selector)

        if element:
            bounds = await element.boundingBox()
            if bounds:
                x = bounds['x']
                y = bounds['y']

                return x,y
    except Exception as e:
        print(f"Error in get_element_position: {e}")

    return None    
                
async def click_position(page, x, y): # Clicks at a specific position
    return await page.mouse.click(x, y)

async def scroll(page, length): # Scrolls down page to a specific length
    pass

async def pull_urls(page): # pulls URLs from listings page
    pass

async def keyword(page):
    print("Input your Search Keyword:")
    keyword = input()

    if not keyword:
        await pull_urls(page)
    else:
        try:
            market_search_box =  await get_element_position(page, 'input[aria-label="Search Marketplace"]')

            if market_search_box:
                print("Search box found")
                await market_search_box.click()
                await market_search_box.type(keyword)
                await market_search_box.press('Enter')  

        except Exception as e:
            print(f"Error in keyword method: {e}")

async def login(page): # Logins to the given facebook marketplace page
    print("Input your Username Below:")
    FB_USER = input()

    print("Input your Password Below:")
    FB_PASS = input()

    print("Login credentials are:")
    print("USERNAME: " + FB_USER)
    print("PASSWORD:" + FB_PASS)

    user_input_box = await find_element(page,'input[id=":r10:"]')
    pass_input_box = await find_element(page, 'input[id=":r13:"]')
    login_button = await find_elements(page,'div[aria-label="Accessible login button"]')
    
    if user_input_box and pass_input_box and login_button:
        await user_input_box.click()
        await user_input_box.type(FB_USER)

        await pass_input_box.click()
        await pass_input_box.type(FB_PASS)

        for item in login_button: # There's two elements on the homepage; slightly inefficient but works so whatever. Try-except clause needed for the one that isn't applicable
            try:
                await item.click()
            except:
                 continue   
            
        await page.waitForNavigation()     
    else:
        print("One or more input fields not found!")    

async def algorithm(page): # Main algorithm for combing listings
    await page.goto('https://www.facebook.com/marketplace/')
    
    await login(page) # updates page after login
    #if # If clause when a CAPTCHA page is reached, do asyncio.sleep(60) to manually solve CAPTCHA
    await keyword(page)
    
    # await find_elements(page, ) # Finds all listings currently loaded on page
    await asyncio.sleep(1000) # Temporary for testing

async def main(): # Wrapper for algorithm calls
        page, browser = await launch_browser()
        await algorithm(page)
        await browser.close()  

asyncio.get_event_loop().run_until_complete(main())
