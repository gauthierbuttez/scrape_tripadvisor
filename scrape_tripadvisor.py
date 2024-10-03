import random
import re

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sqlite3
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

# Utilisation de codes ANSI pour changer la couleur du texte
def print_error(message):
    RED = "\033[91m"
    RESET = "\033[0m"
    print(f"{RED}{message}{RESET}")


urls_dic={
    "Boat Tours & Water Sports": "https://www.tripadvisor.co.uk/Attractions-g187479-Activities-c47-Tenerife_Canary_Islands.html#category=55",
    "Sights & Landmarks": None,  # Pas de lien pour cette catégorie
    "Nightlife": "https://www.tripadvisor.co.uk/Attractions-g187479-Activities-c47-Tenerife_Canary_Islands.html#category=20",
    "Nature & Parks": "https://www.tripadvisor.co.uk/Attractions-g187479-Activities-c47-Tenerife_Canary_Islands.html#category=57",
    "Spas & Wellness": "https://www.tripadvisor.co.uk/Attractions-g187479-Activities-c47-Tenerife_Canary_Islands.html#category=40",
    "Fun & Games": "https://www.tripadvisor.co.uk/Attractions-g187479-Activities-c47-Tenerife_Canary_Islands.html#category=56",
    "Classes & Workshops": "https://www.tripadvisor.co.uk/Attractions-g187479-Activities-c47-Tenerife_Canary_Islands.html#category=41",
    "Museums": "https://www.tripadvisor.co.uk/Attractions-g187479-Activities-c47-Tenerife_Canary_Islands.html#category=49",
    "Water & Amusement Parks": "https://www.tripadvisor.co.uk/Attractions-g187479-Activities-c47-Tenerife_Canary_Islands.html#category=52",
    "Zoos & Aquariums": "https://www.tripadvisor.co.uk/Attractions-g187479-Activities-c47-Tenerife_Canary_Islands.html#category=48",
    "Casinos & Gambling": "https://www.tripadvisor.co.uk/Attractions-g187479-Activities-c47-Tenerife_Canary_Islands.html#category=53"
}


url_list="https://www.tripadvisor.co.uk/Attractions-g187479-Activities-c47-Tenerife_Canary_Islands.html"

xpath_I_accept_cokkies="//button[ext()='I Accept']"
xpath_currency="//button//*[text()='GBP']"
xpath_tab_currency="//button[text()='Currency']"
xpath_EURO="//button//*[text()='EUR']"

xpath_excursion_from_list="//section//div[contains(@data-tracking-title,'attraction_product')]"
xpath_h3_title_excursion="//h3"
xpath_rate="//a[contains(@href,'#REVIEWS')]//*[name()='svg']"
xpath_reviews="//a[contains(@href,'#REVIEWS')]//span"
xpath_url="//h3/parent::a"
xpath_duration="//div[contains(text(),'hours') or contains(text(),'days') or contains(text(),'hour') or contains(text(),'day')]"
xpath_description="//a//span[string-length(normalize-space(text())) > 125]"
xpath_price="//div[@data-automation='cardPrice']"
xpath_next_page="//a[@aria-label='Next page']"



# Utility function for opening the database and ensuring the table is set up
def init_db():
    conn = sqlite3.connect('excursions.db')
    cursor = conn.cursor()

    # Create the 'excursions' table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS excursions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            url TEXT UNIQUE,
            rating REAL,
            reviews_count INTEGER,
            description TEXT,
            duration TEXT,
            price TEXT,
            full_description TEXT
        )
    ''')

    conn.commit()
    return conn


def clean_url(url):
    return re.sub(r'\?.*', '', url)


def findOneByXPath(p_driver, xpath, time=1):
    try:
        elmt = WebDriverWait(p_driver, time).until(EC.presence_of_element_located((By.XPATH, xpath)))
        return elmt
    except Exception as ex:
        return None


def findAllByXPath(p_driver, xpath, time=1):
    try:
        return WebDriverWait(p_driver, time).until(EC.presence_of_all_elements_located((By.XPATH, xpath)))
    except Exception as ex:
        return None


def click_on_element(p_driver, element):
    try:
        p_driver.execute_script("arguments[0].click();", element)
        p_driver.implicitly_wait(10)
        print("We click on element method 1")
        time.sleep(random.uniform(2.1, 5.3))
    except Exception as ex:
        print_error((f"We could'nt click on element. Let's try another way : {ex}"))
        try:
            element.click()
            p_driver.implicitly_wait(10)
            print("We click on element method 2")
            time.sleep(random.uniform(2.1, 5.3))
        except Exception as ex:
            print_error((f"We could'nt click on button. Let's give up : {ex}"))



# Main function to run the scraper
def main():
    # Initialize the database
    conn = init_db()

    # Configuration of Selenium driver (geckodriver for Firefox)
    options = Options()
    # options.add_argument("--headless")  # Uncomment to run headless (without opening a browser window)
    driver = webdriver.Firefox(options=options)

    driver = uc.Chrome(headless=True, use_subprocess=False)
    driver.get('https://nowsecure.nl')


    try:
        url = "https://www.tripadvisor.co.uk/Attractions-g187479-Activities-c42-Tenerife_Canary_Islands.html"
        driver.get(url)
        time.sleep(8)
        # click I accept cocokies
        # click currency
        cookies_I_Accept_elt = findOneByXPath(driver, xpath_I_accept_cokkies)
        if cookies_I_Accept_elt is not None:
            click_on_element(driver, cookies_I_Accept_elt)
        # click currency
        currency_elt = findOneByXPath(driver, xpath_currency)
        if currency_elt is not None:
            click_on_element(driver,currency_elt)
            tab_currency = findOneByXPath(driver, xpath_currency)
            if tab_currency is not None:
                click_on_element(driver, tab_currency)
                EURO = findOneByXPath(driver, xpath_EURO)
                if EURO is not None:
                    click_on_element(driver, EURO)

    except Exception as ex:
        print_error(f"ERROR click currency : {ex}")


    try:
        # Get a list of existing excursion URLs from the database to avoid scraping them again
        cursor = conn.cursor()
        cursor.execute("SELECT url FROM excursions")
        existing_excursions = set(url_tuple[0] for url_tuple in cursor.fetchall())
        print(f"Found {len(existing_excursions)} already scraped excursions in the database.")
        for el in existing_excursions:
            print(el)

        # Scrape new excursions (Phase 1)
        scrape_excursions(driver, conn, existing_excursions)

        # Scrape detailed information for excursions without full details (Phase 2)
        scrape_excursion_details(driver, conn)

    except Exception as ex:
        print_error(f"ERROR during scraping: {ex}")
    finally:
        # Quit the driver and close the database connection
        driver.quit()
        conn.close()


# Function to scrape the main list of excursions (Phase 1)
def scrape_excursions(driver, conn, existing_excursions):
    print(100 * "*")
    print(" 1 scrape_excursions *****************************************")

    try:

        while True:
            # Find all excursions on the page
            excursions = findAllByXPath(driver, xpath_excursion_from_list)
            if excursions is not None:
                print(f"Found {len(excursions)} elements on this page!")
                for excursion in excursions:
                    try:
                        # Scrape the title
                        title_elem = findOneByXPath(excursion, xpath_h3_title_excursion)
                        title = title_elem.text if title_elem else None
                        print(f"title : {title}")
                        # Scrape the URL
                        url_elem = findOneByXPath(excursion, xpath_url)
                        excursion_url = clean_url(url_elem.get_attribute("href")) if url_elem else None
                        print(f"excursion_url : {excursion_url}")
                        # Skip if the URL is already in the database
                        if excursion_url in existing_excursions:
                            print(f"Skipping already scraped excursion: {excursion_url}")
                            continue

                        # Scrape the rating, reviews, duration, description, price
                        rate_elem = findOneByXPath(excursion, xpath_rate)
                        rate = rate_elem.text if rate_elem else None
                        print(f"rate : {rate}")

                        reviews_elem = findOneByXPath(excursion, xpath_reviews)
                        reviews = reviews_elem.text if reviews_elem else None
                        print(f"reviews : {reviews}")

                        duration_elem = findOneByXPath(excursion, xpath_duration)
                        duration = duration_elem.text if duration_elem else None
                        print(f"duration : {duration}")

                        description_elem = findOneByXPath(excursion, xpath_description)
                        description = description_elem.text if description_elem else None
                        print(f"description : {description}")

                        price_elem = findOneByXPath(excursion, xpath_price)
                        price = price_elem.text if price_elem else None
                        print(f"price : {price}")

                        # Insert the data into the database
                        cursor = conn.cursor()
                        cursor.execute('''
                            INSERT INTO excursions (title, url, rating, reviews_count, description, duration, price)
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                        ''', (title, excursion_url, rate, reviews, description, duration, price))
                        conn.commit()
                        print(f"Inserted excursion: {title} - {excursion_url}")
                        existing_excursions.append(excursion_url)

                    except Exception as e:
                        print(f"Error scraping excursion: {e}")

                # Handle pagination: click 'Next Page'
                next_page_button = findOneByXPath(driver, xpath_next_page)
                if next_page_button:
                    driver.execute_script("arguments[0].click();", next_page_button)
                    time.sleep(2)  # Wait for the page to load
                else:
                    print("No more pages.")
                    break

    except Exception as ex:
        print(f"ERROR scrape_excursions : {ex}")

# Function to scrape detailed information (Phase 2)
def scrape_excursion_details(driver, conn):
    print(100*"*")
    print(" 2 scrape_excursion_details *****************************************")
    cursor = conn.cursor()
    # Get the URLs of excursions that need detailed scraping
    excursions = cursor.execute("SELECT url FROM excursions WHERE full_description IS NULL").fetchall()

    for excursion_url_tuple in excursions:
        excursion_url = excursion_url_tuple[0]
        print(f"Scraping detailed information for {excursion_url}")
        driver.get(excursion_url)
        time.sleep(3)

        try:
            # Scrape the full description
            full_description_elem = findOneByXPath(driver, xpath_description)
            full_description = full_description_elem.text if full_description_elem else None

            # Update the excursion data in the SQLite database
            cursor.execute('''
                UPDATE excursions SET full_description = ?
                WHERE url = ?
            ''', (full_description, excursion_url))
            conn.commit()
            print(f"Updated excursion: {excursion_url}")

        except Exception as e:
            print(f"Error scraping details for {excursion_url}: {e}")


if __name__ == "__main__":
    main()






