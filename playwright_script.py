import asyncio
from playwright.async_api import async_playwright

def run_login_if_authorized(username):
    result = asyncio.run(login_to_bank_of_guam(username))
    return result

async def login_to_bank_of_guam(username):
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()

            await page.goto("https://online.bankofguam.com/bankofguamonline_41/Uux.aspx#/login")
            await page.wait_for_selector('input[test-id="inputField"][type="text"]')
            await page.fill('input[test-id="inputField"][type="text"]', username)
            await page.fill('input[test-id="inputField"][type="password"]', "HelloWorld123")
            await page.click("button:has-text('Log In')")
            await page.wait_for_timeout(5000)
            await browser.close()

            return "Login attempted successfully"

    except Exception as e:
        return f"Error occurred: {str(e)}"
