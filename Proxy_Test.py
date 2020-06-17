import os
from selenium import webdriver
import time

browser = webdriver.Edge('C:\\Users\\premj\\Downloads\\MicrosoftWebDriver.exe')
time.sleep(2)
browser.get("https://www.google.com")

