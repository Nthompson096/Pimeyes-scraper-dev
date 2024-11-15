from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

use_proxy = False  # Set to True to use proxy, False to use your host IP

if use_proxy:
    import getProxy

url = "https://pimeyes.com/en"

def upload(url, path, use_proxy):
    driver = None
    results = None
    currenturl = None

    try:
        print("Initializing driver...")
        if use_proxy:
            prox = getProxy.fetchsocks5()  # FORMAT = USERNAME:PASS@IP:PORT
            options = {
                'proxy': {
                    'http': prox,
                    'https': prox,
                    'no_proxy': 'localhost,127.0.0.1'
                }
            }
            driver = Driver(uc=True, seleniumwire_options=options)
        else:
            driver = Driver(uc=True)
                
        print("Navigating to URL...")
        driver.get(url)
                
        # Wait for the cookie consent dialog and accept it
        try:
            print("Checking for cookie consent dialog...")
            cookie_accept_button = WebDriverWait(driver, 300).until(
                EC.element_to_be_clickable((By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"))
            )
            print("Clicking cookie accept button...")
            cookie_accept_button.click()
        except (TimeoutException, NoSuchElementException):
            print("Cookie consent dialog not found or not clickable. Proceeding...")
                
        print("Waiting for upload button...")
        upload_button = WebDriverWait(driver, 300).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="hero-section"]/div/div[1]/div/div/div[1]/button[2]'))
        )
                
        print("Scrolling upload button into view...")
        driver.execute_script("arguments[0].scrollIntoView(true);", upload_button)
                
        print("Clicking upload button...")
        driver.execute_script("arguments[0].click();", upload_button)
                
        print("Waiting for file input...")
        file_input = WebDriverWait(driver, 300).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type=file]'))
        )
                
        print(f"Sending file path: {path}")
        file_input.send_keys(path)

        # Wait for and click each checkbox
        checkboxes = WebDriverWait(driver, 300).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.permissions input[type='checkbox']"))
        )
                
        print("Clicking agreement checkboxes...")
        for checkbox in checkboxes:
            if not checkbox.is_selected():
                driver.execute_script("arguments[0].click();", checkbox)

        # Wait for the "Start Search" button to become clickable
        print("Waiting for Start Search button to be clickable...")
                
        start_search_button_selector = "div.step.start-search button:not(.disabled)"
                
        start_search_button = WebDriverWait(driver, 300).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, start_search_button_selector))
        )

        # Check if the button is displayed and enabled before clicking
        if start_search_button.is_displayed() and start_search_button.is_enabled():
            print("Clicking Start Search button...")
            driver.execute_script("arguments[0].click();", start_search_button)
            print("Start Search button clicked.")
        else:
            print("Start Search button is not displayed or enabled.")

        print("Waiting for face selection...")
        faces = WebDriverWait(driver, 300).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.choose-uploaded-faces div.faces button"))
        )

        if faces:
            print("Selecting the first face...")
            driver.execute_script("arguments[0].click();", faces[0])

            print("Waiting for 'Proceed to the Face Search' button to be clickable...")
            proceed_button = WebDriverWait(driver, 300).until(
                EC.element_to_be_clickable((By.XPATH, "//button/span[contains(text(), 'Proceed to the Face Search')]"))
            )

            print("Clicking 'Proceed to the Face Search' button...")
            driver.execute_script("arguments[0].click();", proceed_button)
        else:
            print("No faces found to select.")

        print("Waiting for new 'Start Search' button to be clickable...")
        new_start_search_button = WebDriverWait(driver, 300).until(
            EC.element_to_be_clickable((By.XPATH, "//button/span[contains(text(), 'Start Search')]"))
        )

        print("Clicking new 'Start Search' button...")
        driver.execute_script("arguments[0].click();", new_start_search_button)

        print("Waiting for results...")
        time.sleep(5)  # Optional: Adjust as needed based on page behavior.

        resultsXPATH = '//*[@id="results"]/div/div/div[3]/div/div/div[1]/div/div[1]/button/div/span/span'

        print(f"Using XPath: {resultsXPATH}")

        try:
            results = WebDriverWait(driver, 300).until(
                EC.visibility_of_element_located((By.XPATH, resultsXPATH))
            ).text
            print("Results found:", results)
        except TimeoutException:
            print("Timed out waiting for results.")

    except Exception as e:
        print(f"An exception occurred: {e}")
        print(f"Exception type: {type(e).__name__}")
        import traceback
        traceback.print_exc()

    finally:
        print("Results: ", results)
        print("URL: ", currenturl)
        if driver:
            driver.quit()

def main():
    path = input("Enter path to the image: ")
    upload(url, path, use_proxy)

if __name__ == "__main__":
    main()
