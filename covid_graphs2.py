#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 21:41:33 2020

@author: sloschert
"""

import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def clean_data(df):
    """
    This function cleans and transposes the dataframe.
    """
    df.set_index(["Country/Region", "Province/State"], inplace=True)
    df.drop(["Lat", "Long"], axis=1, inplace=True)
    df = df.transpose()
    df.index = pd.to_datetime(df.index)
    df.index.name = "Date"
    return df


# get data from john hopkins university
conf = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/\
COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/\
time_series_covid19_confirmed_global.csv")
death = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/\
COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/\
time_series_covid19_deaths_global.csv")

dates = conf.columns[4:]
days_available = len(dates)

DEFAULT_COUNTRY = "Germany"
DEFAULT_DAYS = 100
COUNTRY = DEFAULT_COUNTRY
DAYS_TO_LOOK_BACK = DEFAULT_DAYS

# user input
if len(sys.argv) == 2:
    COUNTRY = sys.argv[1]
    DAYS_TO_LOOK_BACK = DEFAULT_DAYS
    print("setting days to default value")
elif len(sys.argv) > 2:
    COUNTRY = sys.argv[1]
    DAYS_TO_LOOK_BACK = int(sys.argv[2])
else:
    COUNTRY = DEFAULT_COUNTRY
    DAYS_TO_LOOK_BACK = DEFAULT_DAYS
    print("setting days and country to default values")

if DAYS_TO_LOOK_BACK > days_available:
    DAYS_TO_LOOK_BACK = days_available
    print("setting days to maximum available")

chosen_days = dates[days_available - (DAYS_TO_LOOK_BACK):]
INFO_PROMPT = "Data for {} for last {} days\
\n(Last data ingestion: {})"\
    .format(COUNTRY, DAYS_TO_LOOK_BACK, chosen_days[-1])

conf = clean_data(conf)
death = clean_data(death)

# PLOT
plt.figure(figsize=(8, 8))
plt.suptitle(INFO_PROMPT)

plt.subplot(2, 2, 1)
conf[COUNTRY].apply(sum, axis=1)[-DAYS_TO_LOOK_BACK:].plot(color="b")
plt.title(COUNTRY + " (confirmed)")

plt.subplot(2, 2, 2)
death[COUNTRY].apply(sum, axis=1)[-DAYS_TO_LOOK_BACK:].plot(color="r")
plt.title(COUNTRY + " (deaths)")

plt.subplot(2, 1, 2)
(conf[COUNTRY].apply(sum, axis=1)[-DAYS_TO_LOOK_BACK:].diff()*100 /
    conf[COUNTRY].apply(sum, axis=1)[-DAYS_TO_LOOK_BACK:]).\
        plot(label="cases growth rate")
(death[COUNTRY].apply(sum, axis=1)[-DAYS_TO_LOOK_BACK:].diff()*100 /
    death[COUNTRY].apply(sum, axis=1)[-DAYS_TO_LOOK_BACK:]).\
        plot(label="death growth rate")
plt.title(COUNTRY + " (rates)")
plt.ylabel("Percentage")
plt.legend()

plt.tight_layout()
plt.show()
