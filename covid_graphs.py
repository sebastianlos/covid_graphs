#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 21:41:33 2020

@author: sloschert
"""

import argparse
import textwrap
import pandas as pd
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent("""Statistical graphs about the current state \
of Covid-19.
The data is based on JHU CSSE COVID-19\
Data from the John Hopkins University."""))
parser.add_argument("country",
                    help="The country you want to receive data about.",
                    type=str)
parser.add_argument("days",
                    help="The time span (days) you want to look back.",
                    type=int)
args = parser.parse_args()


def clean_data(df_x):
    """
    This function cleans and transposes the original dataframe.
    """
    df_x.set_index(["Country/Region", "Province/State"], inplace=True)
    df_x.drop(["Lat", "Long"], axis=1, inplace=True)
    df_x = df_x.transpose()
    df_x.index = pd.to_datetime(df_x.index)
    df_x.index.name = "Date"
    return df_x


plt.style.use("seaborn-bright")

conf = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/\
COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/\
time_series_covid19_confirmed_global.csv")
death = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/\
COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/\
time_series_covid19_deaths_global.csv")

dates = conf.columns[4:]
days_available = len(dates)

COUNTRY = args.country
DAYS_TO_LOOK_BACK = args.days

if DAYS_TO_LOOK_BACK > days_available:
    DAYS_TO_LOOK_BACK = days_available
    print("setting days to maximum available")

chosen_days = dates[days_available - (DAYS_TO_LOOK_BACK):]
INFO_PROMPT = "Data for {} for last {} days\
\n(Last ingestion: {})"\
    .format(COUNTRY, DAYS_TO_LOOK_BACK, chosen_days[-1])

conf = clean_data(conf)
death = clean_data(death)

plt.figure(figsize=(10, 8))
plt.suptitle(INFO_PROMPT)

plt.subplot(3, 2, 1)
conf[COUNTRY].apply(sum, axis=1)[-DAYS_TO_LOOK_BACK:].\
    plot(ax=plt.gca(), color="b")
plt.xlabel("")
plt.title("Cases, accumulated")

plt.subplot(3, 2, 2)
death[COUNTRY].apply(sum, axis=1)[-DAYS_TO_LOOK_BACK:].\
    plot(ax=plt.gca(), color="r")
plt.xlabel("")
plt.title("Deaths, accumulated")

plt.subplot(3, 1, 2)
(conf[COUNTRY].apply(sum, axis=1)[-DAYS_TO_LOOK_BACK:].diff()*100 /
 conf[COUNTRY].apply(sum, axis=1)[-DAYS_TO_LOOK_BACK:]).\
        plot(ax=plt.gca(), label="cases growth rate", color="b")
(death[COUNTRY].apply(sum, axis=1)[-DAYS_TO_LOOK_BACK:].diff()*100 /
 death[COUNTRY].apply(sum, axis=1)[-DAYS_TO_LOOK_BACK:]).\
        plot(ax=plt.gca(), label="death growth rate", color="r")
plt.title("Rates of growth in percent")
plt.ylabel("Percentage")
plt.xlabel("")
plt.legend()
plt.grid(True)

plt.subplot(3, 2, 5)
conf[COUNTRY].apply(sum, axis=1)[-DAYS_TO_LOOK_BACK:].diff().\
    plot(ax=plt.gca(), color="b", legend=False)
plt.xlabel("")
plt.title("New cases per day")

plt.subplot(3, 2, 6)
plt.title("New deaths per day")
death[COUNTRY].apply(sum, axis=1)[-DAYS_TO_LOOK_BACK:].diff().\
    plot(ax=plt.gca(), color="r", legend=False)
plt.xlabel("")

plt.tight_layout()
plt.show()
