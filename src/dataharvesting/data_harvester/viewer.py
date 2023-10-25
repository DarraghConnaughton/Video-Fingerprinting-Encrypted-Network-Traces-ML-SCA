#!/usr/bin/env python3

"""
Responsible for initiating and the tracking of video traces.
"""

__author__ = "Darragh Connaughton"
__copyright__ = "Copyright (c) Darragh Connaughton, 2023"
__license__ = "MIT License"

import data_harvester.settings as se
from data_harvester.proxy import ProxyThread
from data_harvester.extractor import extract_videotrace_from_stderr


from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import sys
import json
import os
from optparse import OptionParser
from datetime import datetime
from http.cookies import SimpleCookie

from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.webdriver import FirefoxProfile


from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.action_chains import ActionChains

import pandas as pd
import time

class Viewer:

    def wait_and_watch(self, n) -> list:
        timestamped_data = []
        quality_data = []
        start_time = datetime.now().timestamp()
        current_timestamp = start_time
        i = 0
        while current_timestamp - start_time < n:
            current_timestamp = datetime.now().timestamp()
            time.sleep(1)
        
        print(f"[+]Total time: {start_time-current_timestamp}")
            # if i % 2 == 0:
            #     try:
            #         tmp_quality = self.innerClass.text

            #         quality_data.append(tmp_quality)
            #         timestamped_data.append(current_timestamp)
            #     except:
            #         print("unable to find inner element....")
                
                
        return timestamped_data

    def _safe_click(self, browser, css_selector, sleep):
        try:
            WebDriverWait(self.browser, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector))
            ).click()
        except:
            print(f"[/]{css_selector} did not occur, continuing.")
        finally:
            time.sleep(sleep)

    def __find_hidden_elements(self):
        time.sleep(1)
        try:
            movie_player = self.browser.find_element(By.XPATH, '//*[@id="movie_player"]')
            ytp_panel = None

            for element in movie_player.find_elements(By.CSS_SELECTOR, "*"):
                class_name = element.get_attribute('class')
                if class_name and "ytp-panel" in class_name:
                    ytp_panel = elements

                elif class_name and "settings-button" in class_name:
                    element.click()

            for element in ytp_panel.find_elements(By.CSS_SELECTOR, "*"):
                inner_classname = element.get_attribute('class')

                if inner_classname and "ytp-menu-label-secondary" in inner_classname:
                    innerClass = element
            self.innerClass = innerClass
        except:
            print("Unable to find hidden elements.")


    def __init__(self, url, browser, css_selectors):
        self.url = url
        self.browser = browser
        self.innerClass = None
        self.css_selectors = css_selectors

    def __enter__(self):
        self.browser.get(self.url)
        for css_selector in self.css_selectors:
            self._safe_click(self.browser, css_selector, 3)
        # self.__find_hidden_elements()
        return self


    def __exit__(self, exc_type, exc_value, traceback):
        return self
