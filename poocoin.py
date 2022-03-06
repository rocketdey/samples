from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, NoSuchElementException, TimeoutException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import telebot
import time

bot = telebot.TeleBot('api-key')

capa = DesiredCapabilities.CHROME
capa["pageLoadStrategy"] = "none"
browser = webdriver.Chrome(desired_capabilities=capa)
browser.get('https://poocoin.app/ape')
WebDriverWait(browser, 8).until(EC.visibility_of_element_located((By.CLASS_NAME,'form-select')))
form = browser.find_element(By.CLASS_NAME,'form-select')
form.click()
form.send_keys(Keys.DOWN)
form.send_keys(Keys.ENTER)
WebDriverWait(browser, 8).until(EC.visibility_of_element_located((By.TAG_NAME,'table')))
table = browser.find_element(By.TAG_NAME,'table')
WebDriverWait(browser, 8).until(EC.visibility_of_element_located((By.TAG_NAME,'tbody')))
tbody = table.find_element(By.TAG_NAME,'tbody')
WebDriverWait(browser, 8).until(EC.visibility_of_element_located((By.TAG_NAME,'tr')))
coins = tbody.find_elements(By.TAG_NAME,'tr')
while True:
    coins = tbody.find_elements(By.TAG_NAME,'tr')
    if int(coins[0].find_element(By.TAG_NAME,'span').text.replace('Since creation', '').replace(':', '').replace('0', '')) < 100:
        print(coins[0])
        time.sleep(10)
        break
firsttab = browser.current_window_handle
foundedcoins = []
while True:
    coins = tbody.find_elements(By.TAG_NAME,'tr')
    urls = []
    names = []
    for i, v in enumerate(coins):
        if v.find_elements(By.TAG_NAME,'a')[0].text.split('\n')[1] in foundedcoins:
            continue
        if v.find_elements(By.TAG_NAME,'a')[0].text.split('\n')[1] in names:
            continue
        if i == 15:
            break
        urls.append(v.find_elements(By.TAG_NAME,'a')[0].get_attribute('href'))
        names.append(v.find_elements(By.TAG_NAME,'a')[0].text.split('\n')[1])
    browser.execute_script("window.open('');")
    browser.switch_to.window(browser.window_handles[1])
    for i, url in enumerate(urls):
        browser.get(url)
        print(names[i])
        action = ActionChains(browser)
        action.send_keys(Keys.END).perform()
        try:
            WebDriverWait(browser, 8).until(EC.visibility_of_element_located((By.CLASS_NAME,'TokenFeed_tokenFeed__10Pbr')))
            tokenfeed = browser.find_element(By.CLASS_NAME,'TokenFeed_tokenFeed__10Pbr')
            WebDriverWait(browser, 8).until(EC.visibility_of_element_located((By.CLASS_NAME,'ReactVirtualized__Table')))
            tradecount = int(tokenfeed.find_element(By.CLASS_NAME,'ReactVirtualized__Table').get_attribute('aria-rowcount'))
        except TimeoutException:
            continue
        if tradecount == 0:
            continue
        else:
            WebDriverWait(browser, 8).until(EC.visibility_of_element_located((By.CLASS_NAME,'ReactVirtualized__Table__row')))
            totalprice = 0
            rows = []
            finished = False
            tradedatas2 = []
            while True:
                tradedatas = tokenfeed.find_elements(By.CLASS_NAME,'ReactVirtualized__Table__row')
                if finished is True:
                    break
                elif tradedatas2 == tradedatas:
                    break
                for value,tradedata in enumerate(tradedatas):
                    rownumber = tradedata.get_attribute('aria-rowindex')
                    if rownumber in rows:
                        continue
                    rows.append(rownumber)
                    price = tradedata.find_elements(By.CLASS_NAME,'ReactVirtualized__Table__rowColumn')[1]
                    if price.find_element(By.TAG_NAME,'span').get_attribute('class') == 'text-success':
                        try:
                            print(float(price.text.split('\n')[0].replace('$', '')))
                        except ValueError:
                            continue
                        else:
                            totalprice += float(price.text.split('\n')[0].replace('$', ''))
                    if totalprice > 800:
                        foundedcoins.append(names[i])
                        mt = browser.find_elements(By.CLASS_NAME,'mt-1')
                        for x in range(0,len(mt)):
                            if mt[x].text == 'Trade':
                                bscscan = mt[x - 1].find_element(By.TAG_NAME,'a').get_attribute('href')
                        message = message = f"Name: <a href='{url}'>{names[i]}</a>\nTotal price: {totalprice}\nThis coin has total price over 800. <a href='{bscscan}'>Bscscan Link</a>"
                        try:
                            bot.send_message(chat_id, message, parse_mode='HTML')
                        except Exception:
                            bot = telebot.TeleBot(api_key)
                            bot.send_message(chat_id, message, parse_mode='HTML')
                        finished = True
                        break
                action = ActionChains(browser)
                action.click(tokenfeed).send_keys(Keys.PAGE_DOWN).perform
                time.sleep(0.2)
                tradedatas2 = tradedatas
    browser.close()
    browser.switch_to.window(firsttab)
    table = browser.find_element(By.TAG_NAME,'table')
    tbody = table.find_element(By.TAG_NAME,'tbody')
