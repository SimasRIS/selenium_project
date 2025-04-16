import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import ElementNotInteractableException,TimeoutException

file = 'C:/Users/simas/PycharmProjects/selenium_project/data/raw/restaurant_links.txt'

# Issaugome URL
def save_links_to_file(links, file_path=file):
    out = Path(file_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as f:
        for link in links:
            f.write(link + "\n")
    print(f"Saved {len(links)} links → {out.resolve()}")

def main():
    # Inicijuojame WebDriver
    url = 'https://www.google.com/maps/?entry=wc'
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    restaurant_links = []

    restaurant_searh_input = input("Please enter type of restaurant and choose city you want to search : ")

    # Priimti cookies
    try:
        accept_everything_button =  driver.find_element(By.CSS_SELECTOR,'button[aria-label="Priimti viską"]')
        accept_everything_button.click()
    except Exception as e:
        print(f"Cookie acception button not found or already accepted: {e}")

    # Ivedame ko ieskome
    search_field = driver.find_element(By.ID,'searchboxinput')
    search_field.clear()
    search_field.send_keys(restaurant_searh_input)
    time.sleep(2)

    # Paieskos mygtuko pasupaudimas
    search_button = driver.find_element(By.ID,"cell0x0")
    search_button.click()
    time.sleep(2)

    # Ieskome restoranu konteineriu
    try:
        restaurant_container = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="main"] div[aria-label]'))
        )
    except TimeoutException:
        print("Restaurants container not found.")
        driver.quit()
        exit()

    previous_height = -1

    while True:
        try:
            # Scrollinam konteineriu zemyn
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", restaurant_container)
            time.sleep(1)
        except (TimeoutException, ElementNotInteractableException) as e:
            print(f"Scrolling down failed: {e}")
            break

        # Ieskome konteineriu linku
        try:
            restaurant_containers = restaurant_container.find_elements(By.CSS_SELECTOR, 'a')
            for rastaurant in restaurant_containers:
                link = rastaurant.get_attribute('href')
                if link not in restaurant_links:
                    restaurant_links.append(link)
        except Exception as e:
            print(f"Could not retrive restaurant links: {e}")
            break

        # Tikriname konteinerio auksti
        height = driver.execute_script("return arguments[0].scrollHeight", restaurant_container)
        if height == previous_height:
            print("All restaurants were found.")
            break
        previous_height = height

    print(f"Found {len(restaurant_links)} restaurants.")

    save_links_to_file(restaurant_links)

    driver.quit()

if __name__ == "__main__":
    main()










