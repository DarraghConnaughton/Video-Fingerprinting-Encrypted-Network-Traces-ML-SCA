#!/usr/bin/env python3

"""
We discovered a Jackpot of Youtube URLs, however there is over 9000 of them. We need a script to distill the
list into a solely valid URLS.
"""

__author__ = "Darragh Connaughton"
__copyright__ = "Copyright (c) Darragh Connaughton, 2023"
__license__ = "MIT License"

import csv
import os
import re
import sys
from selenium import webdriver
from selenium.webdriver.firefox.webdriver import FirefoxProfile

CSV_BANNER = "URL,Views,Length,Subscribers"
OUTPUT_FILE = "./jackpot_valid_urls.txt"
SUBSCRIBERS_PATTERN = r'"subscriberCountText":{"accessibility":{"accessibilityData":{"label":"(.*?) subscribers"}'
TIME_DURATION_PATTERN = r'<span class="ytp-time-duration">((?:\d+:)?\d+:\d+)</span>'
VIEWS_PATTERN = r'"views":{"simpleText":"(.*?) views"}'
PROFILE_F = "/Users/darraghconnaughton/Library/Application Support/Firefox/Profiles/m3e7vaoq.default-release-1"


def __launch_browser_() -> webdriver:
    firefox_profile = FirefoxProfile(PROFILE_F)
    firefox_profile.set_preference("browser.cache.disk.enable", False)
    firefox_profile.set_preference("browser.cache.memory.enable", False)
    firefox_profile.set_preference("browser.cache.offline.enable", False)
    firefox_profile.set_preference("network.http.use-cache", False)
    return webdriver.Firefox(firefox_profile)

def __read_from_disk(fpath):
    with open(fpath, "r") as file:
        return file.read().split("\n")

def __handle_match(match):
    if match:
        return match.group(1)

    print(f"[-]WARNING! match not found.")
    return "N/A"

def __valid_url(views):
    view_split = views.split(":")

    if len(view_split) == 3:
        return True

    if len(view_split) == 1:
        return False

    return int(view_split[0]) >= 2

def __continue_where_left_off(urls, output_file):
    if os.path.exists(output_file):
        print(f"[+]{output_file} found. Retrieving last processed URL.")

        with open(output_file, "r") as csv_file:
            t_urls = [row[0] for row in csv.reader(csv_file)]
            if len(t_urls) > 0:
                last_url = t_urls[-1]

                for index in range(len(urls)):
                    if urls[index] == last_url:
                        print(f"[+]URL found {urls[index]} at index {index}")
                        return urls[index:]

    else:
        print(f"[+]Writing CSV Banner: {CSV_BANNER}")
        with open(output_file, "w") as file:
            file.write(f"{CSV_BANNER}\n")

    return urls

BROWSER = __launch_browser_()

if __name__ == "__main__":
    urls = __continue_where_left_off(__read_from_disk("./URLJackpot.txt"), OUTPUT_FILE)
    print(f"len: {len(urls)}")
    with open(OUTPUT_FILE, "a") as file:

        for url in urls:
            trimmed_url = url.strip()

            try:
                session = BROWSER.get(f"https://www.youtube.com/watch?v={trimmed_url}")
                html_snippet = BROWSER.page_source

                time_duration = __handle_match(re.search(TIME_DURATION_PATTERN, html_snippet))
                if __valid_url(time_duration):

                    subscriber_count = __handle_match(re.search(SUBSCRIBERS_PATTERN, html_snippet))
                    views_count = __handle_match(re.search(VIEWS_PATTERN, html_snippet))

                    csv_row = f"{trimmed_url},{views_count},{time_duration},{subscriber_count}"
                    print(f"[+]{csv_row}")
                    file.write(f"{csv_row}\n")

                else:
                    print(f"[-]invalid: {trimmed_url},{time_duration}")

            except Exception as ex:
                print(f"[-]Exception encountered: {ex}. Continuing.")

    print("[+]Finished.")
    BROWSER.quit()
