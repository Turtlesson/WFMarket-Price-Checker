import threading
import time
import winsound
import requests
import datetime
import signal
import sys
import keyboard
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import Chrome
from selenium.common.exceptions import TimeoutException
from apscheduler.schedulers.blocking import BlockingScheduler

# Constants
SELLER_XPATH = "//*[@id='panel']/section[2]/div[3]/div[2]/div[2]/div/div/div[1]/div/div[1]"
BUY_BUTTON_XPATH = "//*[@id='panel']/section[2]/div[3]/div[2]/div[2]/div/div/div[1]/div/div[6]/button"
PRICE_XPATH = "//*[@id='panel']/section[2]/div[3]/div[2]/div[2]/div/div/div[1]/div/div[4]/div/div"

# Ask the user for the desired pause time between scrapes
pause_time_input = input("Enter the desired pause time between scrapes (in seconds): ")
pause_time = int(pause_time_input)  # Convert the input to an integer


class WarframeMarketScraper:
        def __init__(self):
            # Set up ChromeOptions with desired preferences
            self.browserProfile = webdriver.ChromeOptions()
            self.browserProfile.add_experimental_option("excludeSwitches", ['enable-logging'])
            self.browserProfile.add_experimental_option("prefs", {"intl.accept_languages" : "en, en_US" })
            self.browserProfile.add_argument("--incognito --headless")
            # Use ChromeDriverManager to download and install ChromeDriver
            self.browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()) , options=self.browserProfile)
        
        def priceCheck(self):
            with open ("shopping_list.txt", "r", encoding="UTF-8") as file:
                for item in file.readlines():
                    if not item.lstrip().startswith("#"):
                        # Construct URL for item on Warframe Market and navigate to it
                        item_url = "https://warframe.market/items/" + ''.join(c for c in item if not c.isnumeric()).lower().rstrip().replace(' ', '_')
                        self.browser.get(item_url)

                        # Wait for seller visibility and retrieve price element, hopefully catching exceptions if thrown
                        try:
                            _seller_visibility = WebDriverWait(self.browser, 10).until(EC.visibility_of_all_elements_located((By.XPATH, SELLER_XPATH)))
                            price_element = self.browser.find_element("xpath", PRICE_XPATH)
                        except TimeoutException as e:
                            print(f"TimeoutError: {e}")
                            continue

                        # Convert price and target price to integers and compare
                        price = int(price_element.text)
                        target_price = int(item.split()[-1])

                        if price <= target_price:
                            # If price is less than or equal to target price, print success message and copy order message to clipboard
                            print(f"{datetime.datetime.now()} ✔️ '{item.title().rstrip()}' costs {price} platinum, which is less than the amount you are willing to pay. ✔️")
                            # Play a sound to indicate that the script found a cheaper price
                            winsound.Beep(2500, 1000)  # Replace with your preferred sound and duration
                            winsound.Beep(3500, 1000)

                            _buybutton_clickability = WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.XPATH, BUY_BUTTON_XPATH)))
                            buy_button = self.browser.find_element("xpath", BUY_BUTTON_XPATH)
                            buy_button.click()

                            copy = webdriver.ActionChains(self.browser)
                            copy.key_down(Keys.CONTROL).send_keys('C').key_up(Keys.CONTROL).perform()

                        else:
                            # If price is more than target price, print a message indicating that the item is too expensive         
                            print(f"{datetime.datetime.now()} ❌ {price} platinum for '{''.join(c for c in item if not c.isnumeric()).rstrip()}' is more than the {item.split()[-1]} platinum you are willing to pay. ❌")       

def main():
    wfm = WarframeMarketScraper()
    scheduler = BlockingScheduler()

    # Do the initial scrape
    wfm.priceCheck()

    job = scheduler.add_job(wfm.priceCheck, 'interval', seconds=pause_time)

    def sigterm_handler(signal, frame):
        print("Script interrupted. Shutting down scheduler and exiting.")
        scheduler.shutdown()
        sys.exit(0)

    signal.signal(signal.SIGTERM, sigterm_handler)

    try:
        scheduler.start()
    except KeyboardInterrupt:
        print("Script interrupted. Shutting down scheduler and exiting.")
        scheduler.shutdown()
        sys.exit(0)

if __name__ == "__main__":
    main()
