import logging
import time
import json
from selenium.webdriver.firefox.webdriver import FirefoxProfile

from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.webdriver import FirefoxProfile


from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

from victim_viewer.extractor import extract_videotrace_from_stderr
from victim_viewer.proxy import ProxyThread
from victim_viewer.viewer import Viewer
import victim_viewer.settings as se
from selenium import webdriver
from optparse import OptionParser
import sys


def __launch_browser_(proxy) -> webdriver:
    options = Options()
    options.profile = se.PROFILE_F
    options.headless = True  # Run Firefox in headless mode
    options.set_preference("browser.cache.disk.enable", False)
    options.set_preference("browser.cache.memory.enable", False)
    options.set_preference("browser.cache.offline.enable", False)
    options.set_preference("network.http.use-cache", False)

    webdriver.DesiredCapabilities.FIREFOX["proxy"] = {
        "httpProxy": proxy,
        "sslProxy": proxy,
        "proxyType": "MANUAL",
    }
    return webdriver.Firefox(options=options)


def __watch_youtube(url) -> tuple:
    browser = __launch_browser_(f"127.0.0.1:8899")
    start_end = {"start": -1}
    p_thread = ProxyThread()
    timestamped_data = []
    with p_thread:
        viewing = Viewer(url, browser, se.CSS_SELECTORS)
        with viewing as v:
            print("[/]wait and watch starts now.")
            timestamped_data, time_taken = v.wait_and_watch(120)

    if time_taken >= 120:
        video_traces = extract_videotrace_from_stderr(p_thread._stderr, timestamped_data)
        start_end["start"] = video_traces[0]
    else:
        print(f"[-]Video trace was less than expected {120} seconds. Trying again.")

    browser.quit()
    return start_end


def __options_() -> OptionParser:
    parser = OptionParser()
    parser.add_option(
        "-n", "--video_name", dest="video_name", help="Video Name", default=""
    )
    (options, args) = parser.parse_args()
    return options

if __name__ == "__main__":
    options = __options_()
    if len(options.video_name) == 0:
        logging.error("[-]Missing URL option.")
        sys.exit(-1)

    logging.info(f"[+]Victim Viewing session initated for {options.video_name}")
    print("-- OUTPUT --")
    video_url = "https://www.youtube.com/watch?v=" + options.video_name

    print(__watch_youtube(video_url))