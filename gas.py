from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

options = Options()
#options.add_argument('--headless')
options.add_argument("disable-infobars")

browser = webdriver.Chrome(options=options)

while True:
    browser.get('https://etherscan.io/gastracker#historicaldata')
    WebDriverWait(browser, 8).until(EC.visibility_of_element_located((By.ID,'spanLowPrice')))
    lowgas = int(browser.find_element(By.ID, ('spanLowPrice')).text)
    print(lowgas)
    if lowgas <= 60:
        print(f'Gas is {lowgas} right now.')
    time.sleep(5)
