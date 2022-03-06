from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from datetime import datetime

import csv
import json
import sys
import telebot
import time
import telegram_send
import telebot
from telegram import error
import threading

targeted_asset = input('Type asset name:\n')

options = webdriver.ChromeOptions()
options.add_argument("user-data-dir=/home/rocketdey/.config/google-chrome")
browser = webdriver.Chrome(chrome_options=options)
browser.get('https://devops-deploy.azurewebsites.net/marketplace?sort=price+asc&status=buy_now')
browser.implicitly_wait(30)
browser.maximize_window()

while True:
    windows = browser.window_handles
    if len(windows) == 2:
        browser.switch_to.window(windows[1])
        browser.find_element(By.TAG_NAME,'input').send_keys('password')
        browser.find_element(By.TAG_NAME,'button').click()
        break

windows = browser.window_handles
browser.switch_to.window(windows[0])
WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.CLASS_NAME,'infinite-scroll-component')))

infinite_scroll = browser.find_element(By.CLASS_NAME,'infinite-scroll-component')
links = infinite_scroll.find_elements(By.TAG_NAME,'a')
assets = infinite_scroll.find_elements(By.TAG_NAME,'div')
classname = assets[0].get_attribute('class')
first_asset_name = assets[0].text.split('\n')[1]

for x in range(0,len(assets)):
    if assets[x].text == first_asset_name:
        asset_name_class = assets[x].get_attribute('class')
        break

asset_name_list = browser.find_elements(By.CLASS_NAME,asset_name_class)
for x in range(0,len(links)):
    if asset_name_list[x].text == targeted_asset:
        browser.get(links[x].get_attribute("href"))
        break

found = False
found2 = False
WebDriverWait(browser, 5).until(EC.presence_of_all_elements_located((By.TAG_NAME,'div')))
while True:
    try:
        while True:
            path_list = browser.find_elements(By.TAG_NAME,'path')
            if len(path_list) > 10:
                break
 
        div_list = browser.find_elements(By.TAG_NAME,'div')
        print(len(div_list))
        for x in range(0,len(div_list)):
            try:
                balance_text = div_list[x].text
            except StaleElementReferenceException:
                div_list = browser.find_elements(By.TAG_NAME,'div')
                balance_text = div_list[x].text
            if balance_text == 'View balance':
                print(balance_text)
                div_list[x].click()
                balance_number = x
                found = True
                break
 
        if found == True:
            while True:
                windows = browser.window_handles
                if len(windows) == 2:
                    browser.switch_to.window(windows[1])
                    time.sleep(2)
                    WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.CLASS_NAME,'btn-primary')))
                    browser.find_element(By.CLASS_NAME,'btn-primary').click()
                    WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.TAG_NAME,'button')))
                    WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.CLASS_NAME,'btn-link')))
                    browser.find_element(By.CLASS_NAME,'btn-link').click()
                    WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.TAG_NAME,'input')))
                    gas = browser.find_element(By.TAG_NAME,'input').get_attribute('value')
                    for x in range(0,len(gas) - 1):
                        browser.find_element(By.TAG_NAME,'input').send_keys(Keys.BACKSPACE)
                    gas2 = int(gas)*2
                    browser.find_element(By.TAG_NAME,'input').send_keys(Keys.LEFT)
                    browser.find_element(By.TAG_NAME,'input').send_keys(gas2)
                    browser.find_element(By.TAG_NAME,'input').send_keys(Keys.END)
                    browser.find_element(By.TAG_NAME,'input').send_keys(Keys.BACKSPACE)
                    buttons = browser.find_elements(By.TAG_NAME,'button')
                    found = False
                    while True:
                        for z in range(0,len(buttons)):
                            if 'High' in buttons[z].text:
                                buttons[z].click()
                                for y in range(0,len(buttons)):
                                    if buttons[y].text == 'Approve':
                                        buttons[y].click()
                                        found = True
                        if found == True:
                            break
                    break
            break
        else:
            break
    except StaleElementReferenceException:
        continue
browser.switch_to.window(windows[0])
while True:
    try:
        div_list = browser.find_elements(By.TAG_NAME,'div')
        print('found')
        time.sleep(1)
        button_list = browser.find_elements(By.TAG_NAME,'button')
        button_number = 0
        while True:
            if button_number == 0:
                for x in range(0,len(button_list)):
                    if button_list[x].text == 'Buy Now':
                        button_class = button_list[x].get_attribute('class')
                        button_number = x
                        button_list[x].click()
                        time.sleep(1)
                        windows = browser.window_handles
                        if len(windows) == 2:
                            break
            else:
                if button_list[button_number].text == 'Buy Now':
                        button_list[x].click()
                        time.sleep(1)
                        windows = browser.window_handles
                        if len(windows) == 2:
                            break
            while True:
                windows = browser.window_handles
                if len(windows) == 2:
                    browser.switch_to.window(windows[1])
                    time.sleep(1)
                    found = False
                    while True:
                        button_list = browser.find_elements(By.TAG_NAME,'button')
                        WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.CLASS_NAME,'btn-link')))
                        browser.find_element(By.CLASS_NAME,'btn-link').click()
                        WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.TAG_NAME,'input')))
                        gas = browser.find_element(By.TAG_NAME,'input').get_attribute('value')
                        for x in range(0,len(gas) - 1):
                            browser.find_element(By.TAG_NAME,'input').send_keys(Keys.BACKSPACE)
                        gas2 = int(gas)*2
                        browser.find_element(By.TAG_NAME,'input').send_keys(Keys.LEFT)
                        browser.find_element(By.TAG_NAME,'input').send_keys(gas2)
                        browser.find_element(By.TAG_NAME,'input').send_keys(Keys.END)
                        browser.find_element(By.TAG_NAME,'input').send_keys(Keys.BACKSPACE)
                        buttons = browser.find_elements(By.TAG_NAME,'button')
                        while True:
                            for z in range(0,len(buttons)):
                                if 'High' in buttons[z].text:
                                    buttons[z].click()
                                    for y in range(0,len(buttons)):
                                        if buttons[y].text == 'Approve':
                                            buttons[y].click()
                                            found = True
                                            break
                                    break
                        if found == True:
                            break
                    break
        break
    except StaleElementReferenceException:
        continue
print('Bought')
