#!/usr/bin/env python3

"""
Creates datasets for linear regression models
"""

__author__ = "Deborah Djon"
__copyright__ = "Copyright (c) Deborah Djon, 2023"
__license__ = "MIT License"

import pandas as pd

class LinearRegressionModeler():
    def __init__(self, 
                 data:pd.DataFrame,
                 features_file:str, 
                 train_file:str, 
                 test_file:str, 
                 validation_proportion:float=0.3, 
                 fdr_level:float = 0.05) -> None:
        self.model = None
        self.features_file = features_file
        self.train_file = train_file
        self.test_file = test_file
        self.fdr_level = fdr_level
        self.data = data
        self.validation_split_i = int(len(data)*validation_proportion)
        

    def transform_data(data_frame: pd.DataFrame) -> pd.DataFrame:
        data["id"] = data.index
        data.rename({"video_id": "target", "data":0}, axis=1, inplace=True)

        y = data["target"]
        data.drop("target", axis = 1, inplace = True )

        # Explode the 'measurements' column
        exploded_df = data.explode(0)

        # Add the 'time' column
        exploded_df['time'] = exploded_df.groupby('id').cumcount()

        # Reset the index
        exploded_df.reset_index(drop=True, inplace=True)

        # Reorder the columns
        data = exploded_df[['id', 'time', 0]]
        data[0] = data[0].map(float)

    def extraxct_features(self)->None: pass
    
    def select_features(self): pass
    
    def train(self): pass

    def evaluate(self): pass

    def create_model(self): pass


# input_file = 'data/wafer/Wafer.csv'

# features_file = 'data/wafer/features.csv'

# train_file = 'data/wafer/train.csv'
# test_file = 'data/wafer/test.csv'

#validation_split_i = 1000

# the bigger, the more features selected
# default is 0.05
				




# import time
# import threading

# import pandas as pd

# from subprocess import Popen, PIPE
# import logging
# import threading

# from datetime import datetime

# import re
# import git

# import sys
# import json
# import os
# from optparse import OptionParser
# from datetime import datetime
# import hashlib
# from http.cookies import SimpleCookie

# from data_harvester.githandler import GitHandler
# from data_harvester.harvester import Harvester
# from data_harvester.proxy import ProxyThread
# import data_harvester.settings as se


# class DataHarvestor(threading.Thread):

#     def _generate_uid(self, port):
#         return hashlib.sha256(f"{port}".encode("utf8")).hexdigest()[:8]

#     def __init__(self, port, project_root:str, url:str):
#         threading.Thread.__init__(self, name=self._generate_uid(port))
#         self.stop_event = threading.Event()
#         self.project_root = project_root
#         self.githandler = GitHandler(se.REPO_NAME, self.project_root, f"{url}-{port}-{se.TIMESTAMP}", url)
#         self.thread_name = threading.current_thread()
#         self.url = url
#         self.port = port

#     def run(self):
#         print('Thread {thread} started'.format(thread=threading.current_thread()))
#         with self.githandler:
#             print(f"[{self.thread_name}]GIT HANDLER:: {self.githandler} initiated.")
#             with Harvester(f"127.0.0.1:{self.port}", self.url, self.githandler) as h:
#                 print(f"[{self.thread_name}]Data Harvester commencing {h}.")

#     def stop(self):
#         return self

#     def __enter__(self):
#         self.start()
#         return self

#     def __exit__(self, *args, **kwargs):
#         return 1


