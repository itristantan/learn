# -*- coding: utf-8 -*-
"""
Created on Sun Dec 25 11:40:19 2016

@author: tanxin
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

chromedriver = "d:/webdriver/chromedriver.exe"

TMP="r:/tmp"

user_agent="Mozilla/5.0 (iPad; CPU OS 6_1_3 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10B329 Safari/8536.25"

chromeOptions = webdriver.ChromeOptions()
prefs = {"download.default_directory": TMP}
chromeOptions.add_experimental_option("prefs", prefs)
chromeOptions.add_argument("-test-type")
#chromeOptions.add_argument("-start-minmized")
#chromeOptions.add_argument("--window-size=10,50")
chromeOptions.add_argument("--user-data-dir=%s"%TMP)
#chromeOptions.add_argument("--log-level=3")
chromeOptions.add_argument("--no-sandbox")
chromeOptions.add_argument("--disable-extensions")
chromeOptions.add_argument("--disable-gpu")
#chromeOptions.add_argument("--disable-software-rasterizer")
chromeOptions.add_argument("--disable-translate")
#chromeOptions.add_argument("--user-agent=%s"%user_agent)
chromeOptions.add_argument("--startup about:blank")
driver = webdriver.Chrome(executable_path=chromedriver,chrome_options=chromeOptions)
driver.set_script_timeout(5)

url="http://whatsmyuseragent.com/"

driver.get(url)

#print(driver.page_source())
    
driver.close()