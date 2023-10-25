"""
Functions for transforming and cleaning time byte stream series data.
"""

__author__ = "Deborah Djon"
__copyright__ = "Copyright (c) Deborah Djon, 2023"
__license__ = "MIT License"


from typing import List
from datetime import timedelta, datetime
from collections import defaultdict
import bisect
import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq
from pandas import DataFrame

# Aggregate

def bin_per_period(bt:List[int], e:int, t:int)->List[int]: 
    """
    Aggregate the bps sequence according to Algorithm 1 in the paper. 
    @param bt: throughput per second
    @param e: throughput threshold
    @param t: maximum time interval of one period
    """
    aggregated = []
    bt_aggregate = [] # buffer
    idx = 0
    while idx < len(bt):
        if(len(bt_aggregate)<t):
            if(bt[idx]>e):
                bt_aggregate.append(bt[idx])
            else: 
                if(len(bt_aggregate)):
                    aggregated.append(sum(bt_aggregate))
                # Reset the buffer
                bt_aggregate = []     
        else:
            # Reset the buffer
            aggregated.append(sum(bt_aggregate))
            bt_aggregate = []
        idx+=1
    if(len(bt_aggregate)):
        aggregated.append(sum(bt_aggregate))
    return aggregated

def get_bin_end_idx(sorted_list, target):
    """
    Find the end of the binned array. 
    """
    index = bisect.bisect_right(sorted_list, target)
    if index > 0:
        return index
    else:
        return None

def aggregate_to_interval(timestamps: List[datetime], bpts: List[int], bin_size: timedelta) -> tuple[List[datetime], List[int]]:
    """
    Aggregate a BPTS (bytes per time stamp) series into BPI (bytes per binning interval). 
    @param timestamps: List with the timestamps at which each value was collected
    @param bpts: List  with the number of bytes collected at the specific timestamp (byte per time stamp)
    @param bin_size: Defines the length of the period for one bin
    @return: A list of BPP measures where 
    """

    # Create dictionary that maps all timestamps to their byte sizes
    bpts_dict = defaultdict(int)
    for timestamp, byte_count in zip(timestamps, bpts):
        bpts_dict[timestamp] += byte_count
    
    # Sort timestamps and bpts by timestamp
    timestamps = sorted(list(bpts_dict.keys()))
    bpts = [bpts_dict[timestamps[i]] for i in range(len(timestamps))]

    # Aggregate 
    bin_start_idx = 0
    bin_starts = []
    bytes_per_interval = []
    while bin_start_idx < len(timestamps): 
        bin_start = timestamps[bin_start_idx]
        bin_starts.append(bin_start) 
        bin_end = bin_start + bin_size

        bin_end_idx = get_bin_end_idx(timestamps[bin_start_idx:], bin_end)
        bin_end_idx+=bin_start_idx

        bin_values =  bpts[bin_start_idx:bin_end_idx]     
              
        bytes_per_interval.append(sum(bin_values))
        bin_start_idx = bin_end_idx
    return [bin_starts, bytes_per_interval]

def count_timestamps_per_interval(timestamps: List[datetime], interval_size: timedelta) -> List[int]:
    """
    Counts the number of timestamps in the given interval width
    @param timestamps: List with the timestamps at which each value was collected
    @param interval_size: Defines the length of the intervals to count the timestamps in
    @return: A list of number of timestamps per interval
    """
    timestamps = sorted(timestamps)
    interval_start_idx = 0
    counts = []
    while interval_start_idx < len(timestamps): 
        interval_start = timestamps[interval_start_idx]
        interval_end = interval_start + interval_size

        interval_end_idx = get_bin_end_idx(timestamps[interval_start_idx:], interval_end)
        interval_end_idx+=interval_start_idx

        timestamps_count =  len(timestamps[interval_start_idx:interval_end_idx])         
        counts.append(timestamps_count)
        interval_start_idx = interval_end_idx
    return counts

def get_sliding_windows(measures: list, step_size:int =1, window_size:int=3)->List[List[int]]:
    """Give a list of widening window fingerprints for a given array. 
    @param measures: data points list
    @param step_size: intervals of increasing window size
    ☺param start_site: min window site
    """
    windows = []

    for i in range(0, len(measures), step_size):
        if (i+window_size < len(measures)):
            windows.append(measures[i:i+window_size])
        else:
            return windows
    return windows

def get_widening_windows(measures: np.ndarray, step_size:int =1, start_size:int=3)->List[List[int]]:
    """Give a list of widening window fingerprints for a given array. 
    @param measures: data points list
    @param step_size: intervals of increasing window size
    ☺param start_site: min window site
    """
    windows = []

    for i in range(start_size, len(measures), step_size):
        windows.append(measures[:i])
    return windows

def stretch_measures_to_seconds(timestamps: List[datetime], measures: List[float]) -> List[float]:
    """stretch byte measures array into a sparse list, where every index represents one second in the array
    @param timestamps: timestamp list
    @param measires: list of measures to stretch
    @return: an sparse array containing the original measures at a given second in the time interval
    """
    result = np.zeros(120)
    result[0] = measures[0]
    last_idx = 0
    for i in range(1,len(measures)-2):
        diff_to_last = int((timestamps[i]-timestamps[i-1]).seconds) if type(timestamps[i]) == datetime else int((timestamps[i]-timestamps[i-1]) /np.timedelta64(1, "s"))
        idx = last_idx+diff_to_last
        if idx<120:
            result[idx] = measures[i] if result[idx] == 0 else result[idx] + measures[i] #prevents errors, when there is an identical timestamp
            last_idx = idx
    return result

def get_seconds_from_measures_timestamps(timestamps: List[datetime], measures: List[float]) -> List[float]:
    """stretch byte measures array into a sparse list, where every index represents one second in the array
    @param timestamps: timestamp list
    @param measires: list of measures to stretch
    @return: an sparse array containing the original measures at a given second in the time interval
    """
    seconds = []
    last_second = 0
    for i in range(1,len(timestamps)-2):

        diff_to_last_ts = int((timestamps[i]-timestamps[i-1]).seconds) if type(timestamps[i]) == timedelta else int((timestamps[i]-timestamps[i-1]) /np.timedelta64(1, "s"))
        second = last_second+diff_to_last_ts
        if second<=120:
            seconds.append(second)
            last_second = seconds[-1]
    return seconds, measures[:len(seconds)]


# Clean

def replace_zeros_with_ones(array: List[float])-> List[float]:
    return [1 if x == 0 else x for x in array]

def extend_list_with_fill_value(array: List[float], max_length: int, filling_value: int) -> List[float]:
    current_length = len(array)
    if current_length < max_length:
        array.extend([filling_value] * (max_length - current_length))
    return array

# TODO
# def extend_list_with_warp(array: List[float], max_length: int, filling_value: int) -> List[float]:
#     current_length = len(array)
#     if current_length < max_length:
#         array.extend([filling_value] * (max_length - current_length))
#     return array


def list_to_float(array: List[float])->List[float]:
    return[float(x) for x in array]

def list_timestamp(array: List[float]) -> List[datetime]:
    return [datetime.fromtimestamp(x) for x in array]

def remove_leading_zeros(data: List[float], timestamps: List[datetime]) -> tuple[List[datetime], List[float]]:
    # Source: chatgpt; prompt: python code to remove the first set of numbers from an array if they are the value 0
     # Find the index of the first non-zero element
    non_zero_index = next((i for i, num in enumerate(data) if num != 0), None)
    
    # If all elements are zero or the array is empty, return an empty array
    if non_zero_index is None:
        return [timestamps[0]], [0]
    # Remove the elements before the first non-zero element
    return timestamps[non_zero_index:], data[non_zero_index:]

def get_measures_from_first_2_min(data: List[float], timestamps: List[datetime]) -> tuple[List[datetime], List[float]]:
    """Remove all data points outside 2min range starting at the beginning.
    @param data: array of measures
    @timestamps: array of timestamps corresponding to data
    @return: tuple of cropped timestamps and measures
    """
    data = np.array(data)
    timestamps = np.array(timestamps)

    start_ts = min(timestamps)

    keep = np.where(timestamps < start_ts+timedelta(seconds=121))
    data = list(data[keep])
    timestamps = list(timestamps[keep])

    return timestamps, data


# Fingerprint

def SDF(number_array: List[float]) -> List[float]:
    """
    Create a simple difference fingerprint for a given list of numbers
    @param number_array: list of numbers to be fingerprinted
    @return: simple difference fingerprint
    """
    df_array=[]
    for i in range(len(number_array)-1):
        df = number_array[i+1]-number_array[i]
        df_array.append(df)
    return df_array

def DF(number_array: List[float]) -> List[float]:
    """
    Create a differential fingerprint for a given list of numbers
    @param number_array: list of numbers to be fingerprinted
    @return: differential fingerprint
    """
    df_array=[]
    for i in range(len(number_array)-1):
        df = (number_array[i+1]-number_array[i])/(number_array[i])
        df_array.append(df)
    return df_array

def MPDF(number_array: List[float]) -> List[float]:
    """
    Create a magnitude-preserving differential fingerprint for a given list of numbers
    @param number_array: list of numbers to be fingerprinted
    @return: magnitude-preserving differential fingerprint
    """
    df_array=[]
    for i in range(len(number_array)-1):
        df = (number_array[i+1]-number_array[i])/(max((number_array[i+1],number_array[i])))
        df_array.append(df)
    return df_array

def NDF(number_array: List[float]) -> List[float]:
    """
    Create a normalised differential between 0 and 1 fingerprint for a given list of numbers. 
    @param number_array: list of numbers to be fingerprinted
    @return: normalised differential fingerprint
    """
    df_array=[]
    for i in range(len(number_array)-1):
        df = (number_array[i+1]-number_array[i])/(number_array[i+1]+number_array[i])
        df_array.append(df)
    return df_array

def ADF(number_array: List[float]) -> List[float]:
    """
    Create an absolute difference fingerprint for a given list of numbers.
    @param number_array: list of numbers to be fingerprinted
    @return: absolute difference fingerprint
    """
    df_array=[]
    for i in range(len(number_array)-1):
        df = abs(number_array[i+1]-number_array[i])
        df_array.append(df)
    return df_array



# Handle I/O operations
def read_parquet_to_pandas(filename:str )-> DataFrame:
    parquet_table = pq.read_table(filename)
    data = parquet_table.to_pandas()
    return data

def save_pandas_to_parquet(filename:str, data_df:DataFrame)->None:
    table = pa.Table.from_pandas(data_df)
    pq.write_table(table, filename)

import json

def key_encoder(obj):
    """
    Custom JSON encoder function to convert numeric keys represented as strings to actual numbers.
    """
    if isinstance(obj, str):
        if obj.isnumeric():
            return int(obj)
    return obj

def read_json(fp) ->None:
    with open(fp, "r") as f:
        dictionary = json.load(f)
    return dictionary

def write_json(fn, json_object) -> dict:
    with open(fn, "w") as f: 
        json.dump(json_object, f, indent=4, sort_keys=True, default=key_encoder)
    try:
        saved_file =  read_json(fn)
        print("Successfully saved file to: ", fn)
        saved_file
    except:
        print("File could not be saved")
