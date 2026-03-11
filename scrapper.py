from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, csv, os

URL = "https://www.ebay.com/globaldeals/tech"
CSV_FILE = "ebay_tech_deals.csv"


def setup_driver() -> WebDriver:
    options = Options()

    options.add_argument("--headless")  # Run browser in headless mode (no GUI)
    print("Opened in Headless mode")
    options.add_argument("--disable-gpu")
    # options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--start-maximized")

    # Adding a User Agent using a detectable default one
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    )

    # service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(options=options)

    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )

    return driver


def scroll_page(driver: WebDriver):
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

        new_height = driver.execute_script("return document.body.scrollHeight")

        time.sleep(2)
        if new_height == last_height:
            break

        last_height = new_height


def scrape_products(driver: WebDriver, wait: WebDriverWait[WebDriver]):

    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".dne-itemtile")))

    products = driver.find_elements(By.CSS_SELECTOR, ".dne-itemtile")

    data = []
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for product in products:
        try:
            title = product.find_element(By.CLASS_NAME, "dne-itemtile-title").text
        except:
            title = "N/A"

        try:
            price = product.find_element(By.CLASS_NAME, "dne-itemtile-price").text

        except:
            price = "N/A"

        try:
            original_price = product.find_element(
                By.CLASS_NAME, "dne-itemtile-original-price"
            ).text
        except:
            original_price = "N/A"

        try:
            shipping = product.find_element(By.CLASS_NAME, "dne-itemtile-delivery").text
        except:
            shipping = "N/A"

        try:
            item_url = product.find_element(By.TAG_NAME, "a").get_attribute("href")
        except:
            item_url = "N/A"

        data.append([timestamp, title, price, original_price, shipping, item_url])

    return data


def save_to_csv(data):

    file_exists = os.path.isfile(CSV_FILE)

    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(
                [
                    "timestamp",
                    "title",
                    "price",
                    "original_price",
                    "shipping",
                    "item_url",
                ]
            )

        writer.writerows(data)


def main() -> None:
    print("setting up the driver")
    driver = setup_driver()
    wait = WebDriverWait(driver, 10)
    driver.get(URL)

    wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "dne-itemtile")))

    scroll_page(driver)

    data = scrape_products(driver, wait)
    save_to_csv(data)
    driver.quit()
    print(f"{len(data)} products scraped successfully")


if __name__ == "__main__":
    main()
