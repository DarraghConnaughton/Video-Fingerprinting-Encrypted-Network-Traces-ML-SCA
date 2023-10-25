#!/usr/bin/env python3

"""
Data Harvestering functionality.
"""

__author__ = "Darragh Connaughton"
__copyright__ = "Copyright (c) Darragh Connaughton, 2023"
__license__ = "MIT License"

import time

import pandas as pd

from subprocess import Popen, PIPE
import logging
import threading

from datetime import datetime

import re
import git

import sys
import json
import os
from optparse import OptionParser
from datetime import datetime
from http.cookies import SimpleCookie

from data_harvester.data_harvester import DataHarvestor
import data_harvester.harvester as har
import data_harvester.settings as se
from multiprocessing.pool import ThreadPool
import concurrent.futures

from selenium.webdriver.firefox.webdriver import FirefoxProfile
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By



def __options_() -> OptionParser:
    parser = OptionParser()
    parser.add_option(
        "-n", "--video_name", dest="video_name", help="Video Name", default="bird1"
    )
    (options, args) = parser.parse_args()
    return options



def __gather_urls(filename):

    if not os.path.exists(filename):
        print("[-]URLs not found, exiting.")
        sys.exit(-1)

    with open(filename, "r") as f:
        return f.read().split("\n")


def __viewing_session(d_threads):
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = []
        for d_thread in d_threads:
            futures.append(executor.submit(d_thread.start))

        # Manage rollover between sessions.
        completed = False
        while not completed:
            time.sleep(30)
            completed = True
            for d in d_threads:
                if d.is_alive():
                    completed = False


if __name__ == "__main__":

    #__gather_urls("https://random-ize.com/random-youtube/")
    #sys.exit(-1)

    se.PROJECT_ROOT = os.getcwd()
    options = __options_()

    if not os.path.exists("./tmp"):
        os.mkdir("tmp")

    view_ptr = 0
    d_threads = []
    for url in __gather_urls(options.video_name):
        
        d_threads.append(DataHarvestor(8899+(view_ptr%3), se.PROJECT_ROOT, url))
        view_ptr+=1

        if view_ptr%3 == 0:

            __viewing_session(d_threads)
            print("[+]Viewing session completed, proceeding.")

            view_ptr = 0
            d_threads = []
            se.TIMESTAMP = str(time.time()).split(".")[0]
