#!/usr/bin/env python3

"""
Data Harvestering functionality.
"""

__author__ = "Darragh Connaughton"
__copyright__ = "Copyright (c) Darragh Connaughton, 2023"
__license__ = "MIT License"

import time
import threading

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
import hashlib
from http.cookies import SimpleCookie

from data_harvester.githandler import GitHandler
from data_harvester.harvester import Harvester
from data_harvester.proxy import ProxyThread
import data_harvester.settings as se


class DataHarvestor(threading.Thread):

    def _generate_uid(self, port):
        return hashlib.sha256(f"{port}".encode("utf8")).hexdigest()[:8]

    def __init__(self, port, project_root:str, url:str):
        threading.Thread.__init__(self, name=self._generate_uid(port))
        self.stop_event = threading.Event()
        self.project_root = project_root
        self.githandler = GitHandler(se.REPO_NAME, self.project_root, f"{url}-{port}-{se.TIMESTAMP}", url)
        self.thread_name = threading.current_thread()
        self.url = url
        self.port = port

    def run(self):
        print('Thread {thread} started'.format(thread=threading.current_thread()))
        with self.githandler:
            print(f"[{self.thread_name}]GIT HANDLER:: {self.githandler} initiated.")
            with Harvester(f"127.0.0.1:{self.port}", self.url, self.githandler) as h:
                print(f"[{self.thread_name}]Data Harvester commencing {h}.")

    def stop(self):
        return self

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *args, **kwargs):
        return 1


