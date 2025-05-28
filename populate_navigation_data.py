from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options
import time

def load_urls(file_path):
    with open(file_path, 'r') as file:
        return [f"https://{line.strip()}" for line in file if line.strip()]

def is_page_loaded(driver, timeout=5):
    """Check if the page is fully loaded."""
    try:
        # Check if the page's readyState is 'complete'
        return driver.execute_script('return document.readyState;') == 'complete'
    except WebDriverException:
        return False
def open_websites(urls, page_timeout=2, load_timeout=3):
    profile_path = r"/Users/a.f/Library/Application Support/Firefox/Profiles/9zc105ih.test-sem-10k"
    options = Options()
    options.profile = profile_path
    options.page_load_strategy = 'normal'  # Default is normal
    # Set up Firefox WebDriver
    driver = webdriver.Firefox(
        service=Service(GeckoDriverManager().install()),
        options=options
    )
    # Set the initial page load timeout, count_fails and count_success variables
    driver.set_page_load_timeout(page_timeout)
    count_fails=1 
    count_success=1
    for url in urls:
        try:
            print(f"Opening: {url}")
            driver.get(url)
            # Wait for the page to fully load (with a custom timeout)
            start_time = time.time()
            while not is_page_loaded(driver) and (time.time() - start_time) < load_timeout:
                time.sleep(0.5)  # Check every half second if the page is fully loaded
            if not is_page_loaded(driver):
                print(f"Page did not finish loading in {load_timeout} seconds: {url}")
                count_fails += 1
                print(f"Pages which did not finish loading in {load_timeout} seconds: {count_fails}")
            else:
                print(f"Successfully loaded: {url}")
                count_success += 1
                print(f"Count of pages successfully loaded: {count_success}")
        except TimeoutException:
            print(f"Timeout while loading the page: {url}")
        except WebDriverException as e:
            print(f"Error while handling the page: {url} - {e}")
        # No delay before moving to the next URL
    # driver.quit()
if __name__ == "__main__":
    urls = load_urls('web_data.txt')  # one URL per line
    open_websites(urls)
