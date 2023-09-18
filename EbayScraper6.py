import time
from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up Tor proxy configuration - run "sudo tor" in the background
tor_proxy = "socks5://127.0.0.1:9050"
profile = webdriver.FirefoxProfile()
profile.set_preference("network.proxy.type", 1)
profile.set_preference("network.proxy.socks", "127.0.0.1")
profile.set_preference("network.proxy.socks_port", 9050)
profile.update_preferences()

# Create a new Firefox WebDriver instance with the configured profile
driver = webdriver.Firefox(firefox_profile=profile)

# Initialize page number
page_num = 1

# Initialize empty list to store the extracted data
all_items = []

while len(all_items) < 10000:  # Continue until you have 10,000 items
    ebay_url = f"https://www.ebay.com/sch/i.html?_nkw=laptop&_sacat=0&LH_Sold=1&_fsrp=1&rt=nc&_pgn={page_num}"
    driver.get(ebay_url)

    # Scroll down to load more results (you may need to adjust this based on your needs)
    scroll_count = 5
    for _ in range(scroll_count):
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_DOWN)
        time.sleep(2)

    # Extract sold listings' titles and prices
    titles = driver.find_elements(By.XPATH, "//div[@class='s-item__title']")
    prices = driver.find_elements(By.XPATH, "//span[@class='s-item__price']")
    conditions = driver.find_elements(By.XPATH, "//div[@class='s-item__subtitle']/span[1]")
    shipping = driver.find_elements(By.XPATH, "//span[@class='s-item__shipping s-item__logisticsCost']")

    # Loop through the elements and extract data
    for title_element, price_element, condition_element, shipping_element in zip(titles, prices, conditions, shipping):
        title = title_element.text
        price = price_element.text
        condition = condition_element.text
        ship = shipping_element.text
        # Create a dictionary to store the data for each item
        item_data = {
            "Title": title,
            "Price": price,
            "Condition": condition,
            "Shipping": ship
        }
        # Append the item dictionary to the list
        all_items.append(item_data)

    # Increment the page number
    page_num += 1

    # Print the current number of items
    #print(all_items)
    print(f"Total items: {len(all_items)}")
    
# Quit the driver when done
# driver.quit()

#add a way to check for duplicate items
#add date of sale to item_data
#save all items to database
#add functionality to get more than 10,000 items


