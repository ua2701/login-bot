import asyncio
from playwright.async_api import async_playwright

def run_login_if_authorized(username):
    result = asyncio.run(login_to_bank_of_guam(username))
    return result

async def login_to_bank_of_guam(username):
    try:
        async with async_playwright() as p:
            # Launch browser with better options for headless environment
            browser = await p.chromium.launch(
                headless=True,
                args=[
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-web-security',
                    '--disable-features=VizDisplayCompositor'
                ]
            )
            context = await browser.new_context(
                viewport={'width': 1280, 'height': 720},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            )
            page = await context.new_page()

            print("Navigating to Bank of Guam login page...")
            await page.goto("https://online.bankofguam.com/bankofguamonline_41/Uux.aspx#/login")
            
            # Wait for page to fully load
            await page.wait_for_load_state("networkidle", timeout=30000)
            
            print("Page loaded, looking for login elements...")
            
            # Debug: Take screenshot and log page info
            try:
                await page.screenshot(path="debug_page.png")
                print(f"Page title: {await page.title()}")
                print(f"Current URL: {page.url}")
            except:
                pass  # Screenshots might not work in some environments
            
            # Wait for username field with multiple selector attempts
            username_selectors = [
                'input[test-id="inputField"][type="text"]',
                'input[type="text"]',
                'input[placeholder*="username" i]',
                'input[placeholder*="user" i]',
                '#username',
                '.username-input'
            ]
            
            username_field = None
            for selector in username_selectors:
                try:
                    await page.wait_for_selector(selector, timeout=10000)
                    username_field = selector
                    print(f"Found username field with selector: {selector}")
                    break
                except:
                    continue
            
            if not username_field:
                # Debug: List all input fields
                inputs = await page.locator("input").all()
                print(f"Found {len(inputs)} input fields:")
                for i, input_elem in enumerate(inputs):
                    input_type = await input_elem.get_attribute("type")
                    placeholder = await input_elem.get_attribute("placeholder")
                    test_id = await input_elem.get_attribute("test-id")
                    print(f"Input {i}: type='{input_type}', placeholder='{placeholder}', test-id='{test_id}'")
                
                return "Error: Could not find username input field"
            
            # Fill username
            await page.fill(username_field, username)
            print("Username filled")
            
            # Wait for password field
            password_selectors = [
                'input[test-id="inputField"][type="password"]',
                'input[type="password"]',
                'input[placeholder*="password" i]',
                '#password',
                '.password-input'
            ]
            
            password_field = None
            for selector in password_selectors:
                try:
                    await page.wait_for_selector(selector, timeout=10000)
                    password_field = selector
                    print(f"Found password field with selector: {selector}")
                    break
                except:
                    continue
            
            if not password_field:
                return "Error: Could not find password input field"
            
            # Fill password
            await page.fill(password_field, "HelloWorld123")
            print("Password filled")
            
            # Wait a moment for any JavaScript to process
            await page.wait_for_timeout(2000)
            
            # Try multiple selectors for the login button
            login_button_selectors = [
                "button:has-text('Log In')",
                "button:has-text('Login')",
                "button:has-text('Sign In')",
                "input[type='submit']",
                "button[type='submit']",
                "button.login-btn",
                "button.btn-login",
                "#login-button",
                "[data-testid*='login']",
                "button:has-text('SIGN IN')"  # In case it's uppercase
            ]
            
            login_clicked = False
            for selector in login_button_selectors:
                try:
                    await page.wait_for_selector(selector, timeout=5000)
                    await page.click(selector)
                    print(f"Successfully clicked login button with selector: {selector}")
                    login_clicked = True
                    break
                except Exception as e:
                    print(f"Failed to click with selector '{selector}': {str(e)}")
                    continue
            
            if not login_clicked:
                # Debug: List all buttons
                buttons = await page.locator("button").all()
                print(f"Found {len(buttons)} buttons:")
                for i, button in enumerate(buttons):
                    text = await button.text_content()
                    class_name = await button.get_attribute("class")
                    button_type = await button.get_attribute("type")
                    print(f"Button {i}: text='{text}', class='{class_name}', type='{button_type}'")
                
                # Try clicking the first submit button or button with login-related text
                for button in buttons:
                    text = (await button.text_content()).lower()
                    if any(word in text for word in ['log', 'sign', 'submit', 'enter']):
                        await button.click()
                        print(f"Clicked button with text: {text}")
                        login_clicked = True
                        break
                
                if not login_clicked:
                    return "Error: Could not find or click login button"
            
            # Wait for potential redirect or response
            try:
                await page.wait_for_load_state("networkidle", timeout=15000)
            except:
                pass  # Continue even if this times out
            
            await page.wait_for_timeout(3000)
            
            final_url = page.url
            print(f"Final URL after login attempt: {final_url}")
            
            await browser.close()
            
            return f"Login attempted successfully. Final URL: {final_url}"

    except Exception as e:
        print(f"Exception details: {str(e)}")
        return f"Error occurred: {str(e)}"