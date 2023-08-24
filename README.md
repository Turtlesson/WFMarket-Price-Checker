# WFMarket-Price-Checker

WF Market Price Checker is a Python script that automates the process of checking prices for items in the Warframe marketplace (https://warframe.market) using selenium. It reads a list of items and prices from a text file, and checks the current prices for each item on the website. If the price is lower than or equal to the specified price, it clicks the "Buy" button and copies the order message to the clipboard.

# Installation

To use WF Market Price Checker, you need to have Python 3.x and the following packages installed:

- selenium
+ webdriver_manager

You can install these packages using pip:

```
pip install -r requirements.txt
```

You also need to have the Chrome browser installed, since the script uses the ChromeDriver to automate the browser.

# Usage

To use WF Market Price Checker, follow these steps:

1. If it's not already there, create a text file called shopping_list.txt in the same directory as the script.
2. In the text file, list the items you want to buy and the maximum price you are willing to pay, separated by a space. For example:
```
Vulkar Wraith 30
prova vandal 40
Hildryn Prime Chassis Blueprint 15
quanta vandal 50
mara detron 30
```
3. Run the script using Python
4. The script will open a Chrome browser window and start checking the prices for each item on the list. If the price is lower than or equal to the specified price, it will click the "Buy" button and copy the order message to the clipboard.
