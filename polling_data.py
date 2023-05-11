#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Last updated: on Wednesday Apr 18 17:03 2022

@author: Ethan Masters

Purpose: Polling Data Processing Script

Python Version: Python 3.9.13 (main, Aug 25 2022, 18:29:29) 
"""

from pprint import pprint
import pandas as pd
import re
import plotly.express as px
import os
import threading
import queue
from datetime import datetime

def clean_date(date):
    return int(re.search(r'\d*/\d*/(\d{4})',date).group(1))

def isolate_surveys(df):
    return df.drop_duplicates(subset = ["BegDate","EndDate","SampleSize"], keep='first') 

def data_visualization(df):
    df = df.groupby(["year"]).size().reset_index()
    df.columns = ['year','count']
    return px.bar(df,x="year", y="count",title=f"Polling Data over the years",labels={"variable":"Key"})

class DataClean():
    def __init__(self,df):
        self.df = df
        super().__init__()
    def run(self):
        self.df['year'] = self.df.BegDate.apply(clean_date)
        prev_len = len(self.df)
        pprint(self.df)
        print(self.df.columns)
        self.df = isolate_surveys(self.df)
        curr_len = len(self.df)

        print(f"{prev_len-curr_len} values out of a total {prev_len} values will be dropped.")
        print(f"This is {(prev_len-curr_len)/prev_len*100} percent of the data.")

        figure = data_visualization(self.df)
        figure.show()

        cwd = os.getcwd()
        datapath = cwd + "/assets/"
        # file = 'roper-folder-toplines-asof-20230127'
        file = 'polling_data'
        file += '.csv'
        self.df.to_csv(datapath + "clean_" + file)

class Worker(threading.Thread):
    def __init__(self, q, lock):
        self.q = q
        self.lock = lock
        super().__init__()
    def run(self):
        while True:
            try:
                work = self.q.get(timeout=3)
            except queue.Empty:
                return
            
            cwd = os.getcwd()
            datapath = cwd + "/assets/"
            file = work + '.csv'
            df = pd.read_csv(datapath + "/" + file)
            self.lock.acquire()
            print('Starting ' + work)
            self.lock.release()
            DataClean(df).run()
            self.lock.acquire()
            print('Completed cleaning ' + work)
            self.lock.release()

            self.q.task_done()

q = queue.Queue()

# q.put_nowait('roper-folder-toplines-asof-20230127')
q.put_nowait('polling_data')


starttime = datetime.now()

lock = threading.Lock()

for _ in range(1):
    Worker(q,lock).start()
q.join()

# ======= Summary Statistics ======= #

# from correlation import statistics_summary
# statistics_summary(test=6)