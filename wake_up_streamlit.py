from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.keys import Keys
from streamlit_app import STREAMLIT_APPS
import datetime

# Set up Selenium webdriver
options = webdriver.ChromeOptions()
#options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

# Initialize log file
with open("wakeup_log.txt", "a") as log_file:
    log_file.write(f"Execution started at: {datetime.datetime.now()}\n")

    # Iterate through each URL in the list
    for url in STREAMLIT_APPS:
        try:
            # Navigate to the webpage
            driver.get(url)
            
            # Wait for the page to load
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

            # Check if the wake up button exists
            try:
                button = WebDriverWait(driver, 30).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[text()='Yes, get this app back up!']"))
                )
                # button = driver.find_element(By.XPATH, "//button[text()='Yes, get this app back up!']")
                if button.is_displayed() and button.is_enabled():
                    try:
                        # button.click()
                        # button.send_keys(Keys.RETURN)
                        driver.execute_script("arguments[0].click();", button) #Try javascript click
                    except Exception as click_error:
                        log_file.write(f"[{datetime.datetime.now()}] Error clicking button at {url}: {str(click_error)}\n")
                else:
                    log_file.write(f"[{datetime.datetime.now()}] Button not displayed or enabled at: {url}\n")
                driver.save_screenshot(f"screenshot_{url}.png")
                log_file.write(f"[{datetime.datetime.now()}] Screenshot saved: screenshot_{url}.png\n")

                with open(f"page_source_{url}.html", "w", encoding="utf-8") as f:
                    f.write(driver.page_source)
                log_file.write(f"[{datetime.datetime.now()}] Page source saved: page_source_{url}.html\n")

                log_file.write(f"[{datetime.datetime.now()}] Successfully woke up app at: {url}\n")
            except TimeoutException:
                log_file.write(f"[{datetime.datetime.now()}] Button not found for app at: {url}\n")
        
        except Exception as e:
            log_file.write(f"[{datetime.datetime.now()}] Error for app at {url}: {str(e)}\n")

# Close the browser
driver.quit()
