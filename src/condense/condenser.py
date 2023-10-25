#!/usr/bin/env python3

"""
Consenser Service
"""

__author__ = "Darragh Connaughton, Deborah Djon"
__copyright__ = "Copyright (c) Darragh Connaughton, 2023"
__license__ = "MIT License"


import concurrent.futures
import git
import os
import pandas as pd
import pickle
import shutil
import sys
import time
import threading
import numpy as np
import glob

PROJECT_ROOT = os.getcwd()

class PullFetchThread(threading.Thread):

    def __init__(self, remote):
        threading.Thread.__init__(self, name=remote)
        self._remote = remote
        self._ref = str(remote).split("\t")[1]
        self._tmp_dir = 'tmp/'+str(self._ref.split("/")[2])

        self._exp_backoff = 1
        self._repo = self.__clean_repo(
            self._tmp_dir,
            "git@gitlab.computing.dcu.ie:connaud5/streamingdatarepository.git",
            self._tmp_dir)


    def __clean_repo(self, tdir, repo_name, project_dir):
        try:
            if os.path.exists(tdir):
                print(f"[/]previous version detected, removing {tdir}.")
                # Remove directory and its contents recursively
                shutil.rmtree(tdir)

                # recreate temporary directory.
                os.mkdir(tdir)
            else:
                print(f"[/]temporary directory not found, creating {tdir}.")
                os.mkdir(tdir)

            return git.Repo.clone_from("git@gitlab.computing.dcu.ie:connaud5/streamingdatarepository.git", project_dir)
        except Exception as ex:
            print(f"Exception encountered; proceeding {ex}")

    def __pull_ref(self):
        try:
            print(f"[+]Fetch/Pull: {str(self._remote)}")
            self._repo.git.pull('origin', self._ref)
        except Exception as ex:
            print(f"[-]Error encountered during pull. Backing off: {self._exp_backoff}")
            time.sleep(self._exp_backoff * 2)
            self._exp_backoff*=2
            self.__pull_ref()

    def run(self):

        self.__pull_ref()
        # try:
        # shutil.copytree(os.getcwd()+"/"+self._tmp_dir, os.getcwd()+"/"+self._tmp_dir+"/put_data_here/"+self._ref.split("/")[2])
        # except Exception as ex:
        #     print(f"Exception encountered when attempting to copy file, skipping: {ex}")


    def stop(self):
        return self

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *args, **kwargs):
        return 1


def gather_remotes():
    if not os.path.exists("./tmp"):
        os.mkdir("./tmp")

    if os.path.exists("./master"):
        shutil.rmtree("./master")

    repo = git.Repo.clone_from("git@gitlab.computing.dcu.ie:connaud5/streamingdatarepository.git", "master")

    repo.git.fetch('--all')
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        p_threads = []
        for remote in repo.git.ls_remote('--heads', 'origin').split("\n"):
            p_thread = PullFetchThread(remote)
            p_threads.append(p_thread)
            executor.submit(p_thread.start())

        completed = False
        while not completed:
            time.sleep(30)
            completed = True
            for p in p_threads:
                if p.is_alive():
                    completed = False

def condense_to_disk(tdir, pandas, url):

    condense = []

    for pfile in pandas:

        tmp = pd.read_pickle(os.path.join(tdir, pfile))
        video_id = url.split(".")[0]
        
        try: 
            tmp["data"] = tmp["data"].apply(int) # Fix string error
            data = {
                "timestamp": [list(tmp["timestamp"].values)],
                "data": [list(tmp["data"].values) ],
                "video_id": video_id
            }
            condense.append(pd.DataFrame(data))
        except: # applies if tmp is not a single record
            tmp["video_id"] = pd.Series([video_id])
            for column in ["data", "timestamp", "quality"]:
             tmp[column] = tmp[column].apply(lambda x: x[0] if len(x)==1 else x)
            condense.append(tmp)

       


    if not os.path.exists(PROJECT_ROOT + "/data"):
        os.mkdir(PROJECT_ROOT + "/data")

    return_dframe = pd.concat(condense, ignore_index=True)
    return_dframe.to_pickle(
        PROJECT_ROOT + "/data/" + url,
        compression="infer",
        protocol=4,
        storage_options=None,
    )
    return return_dframe


def df_append(frame, fpath):
    condense = [frame]

    for file in glob.glob(f'{fpath}*.pd'):
        tmp = pd.read_pickle(file)
        video_id = fpath.split("/")[-1]

        try: 
            tmp["data"] = tmp["data"].apply(int) # Fix string error
            data = {
                "timestamp": [list(tmp["timestamp"].values)],
                "data": [list(tmp["data"].values)],
                "video_id": video_id
            }
            condense.append(pd.DataFrame(data))
        except: # applies if tmp is not a single record
            tmp["video_id"] = pd.Series([video_id])
            for column in ["data", "timestamp", "quality"]:
             tmp[column] = tmp[column].apply(lambda x: x[0] if len(x)==1 else x)
            condense.append(tmp)
    return pd.concat(condense, ignore_index=True)


def condense(inputdir):
    previously_processed = set()
    closed_world_mega_frame = []
    open_world_mega_frame = pd.DataFrame()

    for item in os.listdir(inputdir):
        file_path = os.path.join(inputdir, item)
        if os.path.isdir(file_path):
            for subitem in os.listdir(file_path):
                tmp_path = os.path.join(file_path, subitem)
                if not subitem in previously_processed and os.path.isdir(tmp_path):
                    pandas = [x for x in os.listdir(tmp_path) if ".pd" in x]
                    if len(pandas) == 50:
                        closed_world_mega_frame.append(condense_to_disk(tmp_path, pandas, subitem+".pd"))
                    elif len(pandas) > 0:
                        open_world_mega_frame = df_append(open_world_mega_frame, os.path.join(tmp_path, subitem))

                    previously_processed.add(subitem)


    pd.concat(closed_world_mega_frame, axis=0).to_pickle(
        PROJECT_ROOT + "/data/" + "closed_world_mega_frame.pd",
        compression="infer",
        protocol=4,
        storage_options=None,
    )

    open_world_mega_frame.to_pickle(
        PROJECT_ROOT + "/data/" + "open_world_mega_frame.pd",
        compression="infer",
        protocol=4,
        storage_options=None,
    )


if __name__ == "__main__":   
    data_location = "tmp/streamingdatarepository"
    gather_remotes()  # comment out if it crashes
    condense(os.getcwd()+"/tmp/")
    #shutil.rmtree(os.getcwd()+"/tmp/") # comment out if it crashes
    sys.exit(-1)
