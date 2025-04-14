import csv
import logging
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import ElementNotInteractableException,TimeoutException


# Inicijuoja WebDriveri ir grazina jo objekta
def init_driver():

    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    return driver

def load_restaurant_links(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            links = [line.strip() for line in file if line.strip()]
        logging.info(f"Found {len(links)} links from file {file_path}")
        return links
    except Exception as e:
        logging.error(f'Failed to load file {file_path}: {e}')
        return []

# Spaudzia cookies mygtuka
def accept_cookies(driver):
    try:
        button = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Priimti viską"]')
        button.click()
        time.sleep(1)
    except Exception as e:
        print(f"Cookie acception button not found or already accepted: {e}")

# Gauname restorano pavadinima is puslapio
def get_restaurant_name(driver):
    time.sleep(1)
    try:
        name_element = driver.find_element(By.CSS_SELECTOR, '.DUwDvf.lfPIob').text.strip()
        return name_element
    except Exception as e:
        logging.error(f"Can't find restaurant name: {e}")
        return 'Restaurant is unknown'

# Spaudzia atsiliepimai/apzvalgos mygtuka
def click_reviews_button(driver):
    try:
        review_button = driver.find_element(By.XPATH, '//button[contains(@aria-label, "Atsiliepimai")]')
        review_button.click()
        time.sleep(2)
    except Exception as e:
        logging.error(f"Could not click reviews button: {e}")
        raise

# Grazina atsliepimu konteineri
def get_reviews_container(driver, wait):
    try:
        container = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'div[role="main"] .m6QErb.DxyBCb.kA9KIf.dS8AEf.XiKgde')
            )
        )
        return container
    except TimeoutException:
        logging.error("Reviews container not found.")
        return None

# Puslapio skrolinimas kad uzkrauto daugiau atsiliepimu
def scroll_reviews_container(driver, container):
    driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", container)
    time.sleep(1.5)


# Ieskome informacijos
def parse_review(comment, restaurant_name):
    # Gauti komentatoriaus vardą
    try:
        reviewer_name = comment.get_attribute('aria-label').strip()
    except Exception:
        reviewer_name = ''

    # Ieskome ivertinimo
    try:
        star_element = comment.find_element(By.CSS_SELECTOR, "span.kvMYJc[role='img']")
        star_score = star_element.get_attribute('aria-label').strip()
    except Exception:
        star_score = ''

    # Ieskome datos
    try:
        review_date = comment.find_element(By.XPATH, ".//span[@class='rsqaWe']").text.strip()
    except Exception:
        review_date = ''

    # Spaudziame daugiau mygtuka, kad rodytu visa komentara
    try:
        more_button = comment.find_element(By.XPATH, ".//button[contains(@aria-label, 'Žr. daugiau')]")
        driver = comment.parent
        driver.execute_script("arguments[0].click();", more_button)
        time.sleep(0.5)
    except Exception:
        pass

    # Gauname atsiliepimo teksta
    try:
        comment_text = comment.find_element(By.XPATH, ".//span[@class='wiI7pd']").text.strip()
    except Exception:
        comment_text = ''

    return (restaurant_name, reviewer_name, star_score, review_date, comment_text)

def scrape_reviews_from_url(url, driver):
    reviews = []
    seen_reviews = set()
    logging.info(f"Scraping {url}")
    driver.get(url)
    time.sleep(3)

    # Priimame cookies
    accept_cookies(driver)

    # Gauname restorano pavadinima
    restaurant_name = get_restaurant_name(driver)

    # Spaudziame atsiliepimu mygtuka
    try:
        click_reviews_button(driver)
    except Exception:
        logging.error(f"Can't open reviews button on {url}")
        return reviews

    wait = WebDriverWait(driver, 10)
    reviews_container = get_reviews_container(driver, wait)
    if not reviews_container:
        return reviews

    previous_height = -1
    while True:
        try:
            scroll_reviews_container(driver, reviews_container)
        except (TimeoutException, ElementNotInteractableException) as e:
            logging.error(f"Slinkimas nepavyko: {e}")
            break

        comment_elements = reviews_container.find_elements(By.CSS_SELECTOR, "div.jftiEf.fontBodyMedium")
        for comment in comment_elements:
            review_data = parse_review(comment, restaurant_name)
            if review_data not in seen_reviews:
                seen_reviews.add(review_data)
                reviews.append(review_data)

        current_height = driver.execute_script("return arguments[0].scrollHeight", reviews_container)
        if current_height == previous_height:
            logging.info("Visi atsiliepimai užkrauti.")
            break
        previous_height = current_height

    return reviews

# Issaugome komentarus i CSV faila
def write_reviews_to_csv(csv_file_name, reviews, header):
    try:
        with open(csv_file_name, mode='w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(header)
            writer.writerows(reviews)
        logging.info(f"Data successfully saved to {csv_file_name}")
    except Exception as e:
        logging.error(f"Error writing CSV file: {e}")

def main():
    file_path = "C:/Users/simas/PycharmProjects/selenium_project/data/raw/restaurant_links.txt"
    urls = load_restaurant_links(file_path)
    if not urls:
        logging.error("Restaurants links are empty.")
        return

    driver = init_driver()
    all_reviews = []

    for url in urls:
        reviews = scrape_reviews_from_url(url, driver)
        all_reviews.extend(reviews)
        time.sleep(2)

    csv_file_name = "../../data/raw/review_comments.csv"
    header = ["Restaurant Name", "Reviewer Name", "Star Score", "Review Date", "Comment"]
    write_reviews_to_csv(csv_file_name, all_reviews, header)
    driver.quit()

if __name__ == "__main__":
    main()
