from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def open_and_click_download_button(url):
    # Configure Chrome options (no custom download directory)
    chrome_options = webdriver.ChromeOptions()
    prefs = {
        "download.prompt_for_download": False,       # Disable download prompts
        "safebrowsing.enabled": True                 # Enable safe browsing
    }
    chrome_options.add_experimental_option("prefs", prefs)

    # Initialize WebDriver with Chrome options
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Open the specified URL
        driver.get(url)

        # Wait for the page to load (you can adjust this as needed)
        time.sleep(5)

        # Locate the "Download image" button using the provided XPath
        download_button_xpath = "//span[@class='label-jFqVJoPk' and text()='Download image']"
        download_button = driver.find_element(By.XPATH, download_button_xpath)

        # Click the "Download image" button to trigger the download
        download_button.click()

        # Wait for the download process to complete (adjust time as needed)
        time.sleep(5)  # Adjust if necessary
        print("Download image button clicked. Image should be saved to the default download directory.")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the browser
        driver.quit()

# Example usage
open_and_click_download_button("https://www.tradingview.com/chart/?symbol=NSE%3ATATAMOTORS")
