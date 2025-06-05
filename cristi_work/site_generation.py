from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options
import time
import csv

def load_urls(file_path):
    """Load URLs from a text file."""
    with open(file_path, 'r') as file:
        return [f"https://{line.strip()}" for line in file if line.strip()]

def is_page_loaded(driver, timeout=5):
    """Check if the page is fully loaded."""
    try:
        return driver.execute_script('return document.readyState;') == 'complete'
    except WebDriverException:
        return False

def open_websites(urls, page_timeout=5, load_timeout=10):
    """Open websites, extract titles, and save to a CSV."""
    profile_path = r"C:\Users\crist\AppData\Roaming\Mozilla\Firefox\Profiles\er69oo10.real_10k_entries"
    options = Options()
    options.profile = profile_path
    options.page_load_strategy = 'normal'

    driver = webdriver.Firefox(
        service=Service(GeckoDriverManager().install()),
        options=options
    )
    driver.set_page_load_timeout(page_timeout)

    count_success = 0
    count_fails = 0
    log_csv_path = "website_titles.csv"

    try:
        with open(log_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['URL', 'Title'])

            for url in urls:
                try:
                    print(f"Opening: {url}")
                    driver.get(url)

                    start_time = time.time()
                    while not is_page_loaded(driver) and (time.time() - start_time) < load_timeout:
                        time.sleep(0.5)

                    if not is_page_loaded(driver):
                        print(f"Page did not finish loading in {load_timeout} seconds: {url}")
                        title = "LOAD TIMEOUT"
                        count_fails += 1
                    else:
                        title = driver.title.strip() if driver.title else "NO TITLE"
                        print(f"Successfully loaded: {url} — {title}")
                        count_success += 1

                except TimeoutException:
                    title = "TIMEOUT EXCEPTION"
                    print(f"Timeout while loading the page: {url}")
                    count_fails += 1
                except WebDriverException as e:
                    title = f"WEBDRIVER ERROR: {str(e)}"
                    print(f"Error while handling the page: {url} — {e}")
                    count_fails += 1

                csvwriter.writerow([url, title])
                time.sleep(1)



    finally:
        # Do NOT close the browser
        print("\n=== Process Complete ===")
        print(f"Successfully loaded: {count_success} pages")
        print(f"Failed/Timed out: {count_fails} pages")
        print("Firefox browser remains open.")


if __name__ == "__main__":
    urls = load_urls('web_data.txt')  # One URL per line
    open_websites(urls)
