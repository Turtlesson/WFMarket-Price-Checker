from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import Chrome
import time
import winsound
import requests

# Constants
#SELLER_XPATH = "//*[@id='panel']/section[2]/div[3]/div[2]/div[2]/div/div[1]/div[4]/div"
SELLER_XPATH = "//*[@id='panel']/section[2]/div[3]/div[2]/div[2]/div/div/div[1]/div/div[1]"
#BUY_BUTTON_XPATH = "//*[@id='panel']/section[2]/div[3]/div[2]/div[2]/div/div[1]/div[6]/button"
BUY_BUTTON_XPATH = "//*[@id='panel']/section[2]/div[3]/div[2]/div[2]/div/div/div[1]/div/div[7]/button"
#PRICE_XPATH = "//*[@id='panel']/section[2]/div[3]/div[2]/div[2]/div/div[1]/div[4]/div/b"
PRICE_XPATH = "//*[@id='panel']/section[2]/div[3]/div[2]/div[2]/div/div/div[1]/div/div[4]/div/div"
# Ask the user for the desired pause time between scrapes
pause_time_input = input("Enter the desired pause time between scrapes (in seconds, don't spam): ")
pause_time = int(pause_time_input)  # Convert the input to an integer


class WarframeMarketScraper:
        def __init__(self):
            # Set up ChromeOptions with desired preferences
            self.browserProfile = webdriver.ChromeOptions()
            self.browserProfile.add_experimental_option("excludeSwitches", ['enable-logging'])
            self.browserProfile.add_experimental_option("prefs", {"intl.accept_languages" : "en, en_US" })
            self.browserProfile.add_argument("--incognito")
            # Use ChromeDriverManager to download and install ChromeDriver
            self.browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()) , options=self.browserProfile)

        def priceCheck(self):
            with open ("shopping_list.txt", "r", encoding="UTF-8") as file:
                for item in file.readlines():                    
                    # Construct URL for item on Warframe Market and navigate to it
                    item_url = "https://warframe.market/items/"+ ''.join(c for c in item if not c.isnumeric()).lower().rstrip().replace(' ','_')
                    self.browser.get(item_url)
                    
                    # Wait for seller visibility and retrieve price element
                    _seller_visibility = WebDriverWait(self.browser, 10).until(EC.visibility_of_all_elements_located((By.XPATH, SELLER_XPATH)))
                    price_element = self.browser.find_element("xpath", PRICE_XPATH)

                    # Convert price and target price to integers and compare
                    price = int(price_element.text)
                    target_price = int(item.split()[-1])

                    if price <= target_price:
                        # If price is less than or equal to target price, print success message and copy order message to clipboard
                        print(f"✔️ '{item.title().rstrip()}' costs {price} platinum, which is less than the amount you are willing to pay. ✔️")
                        # Play a sound to indicate that the script found a cheaper price
                        winsound.Beep(2500, 500)  # Replace with your preferred sound and duration
                        winsound.Beep(3500, 500)

                        _buybutton_clickability = WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.XPATH, BUY_BUTTON_XPATH))) 
                        buy_button = self.browser.find_element("xpath", BUY_BUTTON_XPATH)
                        buy_button.click()     

                        copy = webdriver.ActionChains(self.browser)
                        copy.key_down(Keys.CONTROL).send_keys('C').key_up(Keys.CONTROL).perform()         

                    else:
                        # If price is more than target price, print a message indicating that the item is too expensive         
                        print(f"❌ {price} platinum for '{''.join(c for c in item if not c.isnumeric()).rstrip()}' is more than the {item.split()[-1]} platinum you are willing to pay. ❌")
                
            self.browser.quit()

        
            
wfm = WarframeMarketScraper()
while True: 
    wfm.priceCheck()
    time.sleep(pause_time) # pause till it scrapes again
