"""
Fiunctions for visualising bytestream time series data.
"""

__author__ = "Deborah Djon"
__copyright__ = "Copyright (c) Deborah Djon, 2023"
__license__ = "MIT License"

import matplotlib.pyplot as plt
from typing import Literal
import pandas as pd
import seaborn as sns
import numpy as np
from tslearn.barycenters import dtw_barycenter_averaging
from modelling_utilities.constants import ACCENT_COLOR, ACCENT_COLOR_DARK, ACCENT_COLOR_LIGHT
from typing import List


# Data visualisation

def show_traces(traces: list, title:str="", trace_names:list=None, trace_unit:Literal["MB", "B", "KB", "GB", "original"] = None, x_label="", y_label="", unify_ranges:bool =False, plot_type:Literal["bar", "line"]="bar") -> None:
    """
    Visualise a set of bpp traces as a set of barplots. 
    @param traces: list of traces
    @param title: title of the plt
    """

    trace_unit_factors = {
        "B":  1, 
        "KB": 1000, 
        "MB": 1000000, 
        "GB": 1000000000,
        "original" : 1
    }

    if (type(traces[0]) == float) or (type(traces[0]) == int):
        print(type(traces[0]))
        plt.title(title)
        y = list(traces)
        x = list(range(len(y)))
        if(plot_type=="line"):
            sns.lineplot(x=x, y=y, color=ACCENT_COLOR)
        else:
            sns.barplot(x=x, y=y, color=ACCENT_COLOR)

    else:
        len_data = len(traces)
        max_trace_len = max([len(tr) for tr in traces])
        max_trace_value = max([x for y in traces for x in y])
        fig, axs = plt.subplots(nrows=len_data,  figsize=(8,int(len_data)), sharex='col', gridspec_kw={'hspace': 1.5})
        for i in range(len_data):
            y = traces[i]
            x = list(range(len(y)))
            if(plot_type=="line"):
                axs[i].plot(x,y, color=ACCENT_COLOR)
            else:
                axs[i].bar(x,y, color=ACCENT_COLOR)


            axs[i].set_xlim(0,max_trace_len)

            if(trace_names):
                axs[i].set_title(trace_names[i])

            # Change y-axis to decimal notation and fix unit
            if(trace_unit!=None):
                axs[i].ticklabel_format(style='plain', axis='y')
                ytick_labels = axs[i].get_yticks()*(1/trace_unit_factors[trace_unit])  
                axs[i].set_yticklabels(ytick_labels)
                if(unify_ranges
            ): 
                    axs[i].set_ylim([0,max_trace_value+10])
            else: 
                axs[i].set_yticklabels([])
        if(trace_names):
                axs[0].set_title(title+"\n"+trace_names[0])
        else:
            axs[0].set_title(title)
        plt.ylabel(y_label)
        plt.xlabel(x_label)
    plt.show()

def average_sequences(sequence: list)-> np.ndarray:
    return dtw_barycenter_averaging(sequence, max_iter=50, tol=1e-3)


def barycenter_plot_helper(barycenter, sequences, ax):
    # plot all points of the data set
    for s in sequences:
        ax.plot(pd.Series(s).ravel(), "gray", alpha=.2)
    # plot the given barycenter of them
    ax.plot(barycenter.ravel(), ACCENT_COLOR_DARK, linewidth=2)




def plot_barycenters(sequences:list, sequences_names:list, title="DBA (vectorized version of Petitjean's EM)", x_label = "", y_label = "")->None:
    """
    @param title:  Name of the plot
    @param sequences: 2d list of sequences to average
    @param sequences_names: list of titles per sequence element in sequences
    @param x_lim: x-axis range
    """
    print(title)

    x_max = max([len(sub_seq) for seq in sequences for sub_seq in seq])
    num_sequences = len(sequences)
    #ax1 = plt.subplot(num_plots, 1, 1)
    fig, axs = plt.subplots(nrows=num_sequences,  figsize=(8,int(num_sequences*0.8)), sharex='col', gridspec_kw={'hspace': 0.7})

    for i in range(0,num_sequences):
        axs[i].set_title(sequences_names[i])
        axs[i].set_xlabel(x_label)
        axs[i].set_ylabel(y_label)

        data = sequences[i]
        avg = average_sequences(data)
        barycenter_plot_helper(avg, data, axs[i])

    plt.ylabel(y_label)
    plt.xlabel(x_label)

    plt.tight_layout()
    plt.show()


def show_traces(traces: List[List[float]] or List[float], traces_names:List[str] or str = None, title:str="" , trace_unit:Literal["MB", "B", "KB", "GB"] = None, x_label="", y_label="", unify_y_ranges:bool =False) -> None:
    """
    Visualise a set of bpp traces as a set of barplots. 
    @param traces: list of traces
    @param title: title of the plt
    @param TODO
    """

    trace_unit_factors = {
        "B":  1, 
        "KB": 1000, 
        "MB": 1000000, 
        "GB": 1000000000,
        "original":1
    }

    # Only one trace to visualise
    if (type(traces[0]) == float) or (type(traces[0]) == int):
        if(traces_names and (type(traces_names)==str)):
            title = title +"\n"+traces_names
        else:
            plt.title(title)
        
        y = list(traces)
        x = list(range(len(y)))
        sns.barplot(x=x, y=y, color=ACCENT_COLOR)
    # More than one trace to visualise
    else:
        len_data = len(traces)
        max_trace_len = max([len(tr) for tr in traces])
        max_trace_value = max([x for y in traces for x in y])
        fig, axs = plt.subplots(nrows=len_data,  figsize=(8,int(len_data*0.8)), sharex='col', gridspec_kw={'hspace': 0.7})
        for i in range(len_data):
            y = traces[i]
            x = list(range(len(y)))
            axs[i].bar(x,y, color=ACCENT_COLOR)
            axs[i].set_xlim(0,max_trace_len)

            # Change y-axis to decimal notation and fix unit
            if(trace_unit!=None):
                axs[i].ticklabel_format(style='plain', axis='y')
                ytick_labels = axs[i].get_yticks()*(1/trace_unit_factors[trace_unit])  
                axs[i].set_yticklabels(ytick_labels)
                if(unify_y_ranges): 
                    axs[i].set_ylim([0,max_trace_value+10])
            else: 
                axs[i].set_yticklabels([])
        if(traces_names ):
            title = title+"\n\n"+traces_names[0]
            for i in range(len_data):
                axs[i].set_title(traces_names[i])
        axs[0].set_title(title)
        plt.ylabel(y_label)
        plt.xlabel(x_label)
    plt.show()