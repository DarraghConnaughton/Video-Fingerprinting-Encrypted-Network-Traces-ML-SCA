#!/usr/bin/env python3

"""
Responsible for initiating and the tracking of video traces.
"""

__author__ = "Darragh Connaughton"
__co_author__ = "Deborah Djon"
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

import pandas as pd
import time

from data_harvester.viewer import Viewer



# =======
# FEATURE:
# =======

# * Find the appropriate video directory locally.

# * Determine where we left off by searching the file names in this directory.

# =======


# PROBABLY BEST TO CHANGE THIS NAME

class Harvester:
    def __init__(self, proxy, video, githandler):
        self.browser = self.__launch_browser_(proxy)
        self.githandler = githandler
        self.video = video
        self.pport = proxy.split(":")[1]

    def __enter__(self):
        # for video in self.videos:
        if len(self.video) > 0:
            video_url = "https://www.youtube.com/watch?v=" + self.video
            print(f"[+]video_uid: {self.video}; video_url {video_url};")
            self.__gather_n_traces_of_video(video_url)

    def __exit__(self, exc_type, exc_value, traceback):
        print(f"[/]exc_type:{exc_type},exc_value:{exc_value},traceback:{traceback}")
        print(f"[+]Harvester shutting down.")
        self.browser.close()
        self.browser.quit()
        print(f"[+]Selenum resource clean up: close() and quit() complete.")

    def __launch_browser_(self, proxy) -> webdriver:

        firefox_profile = FirefoxProfile(se.PROFILE_F)
        
        firefox_profile.set_preference("browser.cache.disk.enable", False)
        firefox_profile.set_preference("browser.cache.memory.enable", False)
        firefox_profile.set_preference("browser.cache.offline.enable", False)
        firefox_profile.set_preference("network.http.use-cache", False)

        webdriver.DesiredCapabilities.FIREFOX["proxy"] = {
            "httpProxy": proxy,
            "sslProxy": proxy,
            "proxyType": "MANUAL",
        }

        return webdriver.Firefox(firefox_profile)

    def __gather_n_traces_of_video(self, url):
        if not os.path.exists(f"{se.PROJECT_ROOT}/tmp/{self.video}/streamingdatarepository/{self.video}"):
            print(
                f"[+]{se.PROJECT_ROOT}/tmp/{self.video}/streamingdatarepository/{self.video} doesn't exist. Creating directory."
            )
            os.makedirs(f"{se.PROJECT_ROOT}/tmp/{self.video}/streamingdatarepository/{self.video}")
            print(f"[+]Directory created.")

        for i in range(se.TRACES_TO_CAPTURE):
            p_thread = ProxyThread(self.pport)
            timestamped_data = []
            with p_thread:
                viewing = Viewer(url, self.browser, se.CSS_SELECTORS)
                with viewing as v:
                    print("[/]wait and watch starts now.")
                    timestamped_data = v.wait_and_watch(120)

            video_traces = extract_videotrace_from_stderr(p_thread._stderr, timestamped_data)
            print(f"video_traces: {video_traces}")

            for k,v in video_traces.items():
                video_traces[k]=[v]

            for k,v in video_traces.items():
                video_traces[k]=[v]
            
            df = pd.DataFrame(video_traces)


            file_name = f"{se.PROJECT_ROOT}/tmp/{self.video}/streamingdatarepository/{self.video}/{self.video}.{int(time.time())}.pd"
            df.to_pickle(
                file_name,
                compression="infer",
                protocol=4,
                storage_options=None,
            )

            self.githandler.push_data_to_remote([file_name], f"[AUTOMATED COMMIT]: Adding trace {i} of {self.video}")

