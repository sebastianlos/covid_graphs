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

# read files
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

conf.set_index(["Country/Region", "Province/State"], inplace=True)
conf.drop(["Lat", "Long"], axis=1, inplace=True)
conf = conf.transpose()
conf.index = pd.to_datetime(conf.index)
conf.index.name = "Date"

conf["United Kingdom"].apply(sum, axis=1).plot()

death


# per COUNTRY
country_conf = conf.groupby("Country/Region").get_group(COUNTRY)
country_death = death.groupby("Country/Region").get_group(COUNTRY)
country_conf

# on chosen dates
conf_numbers = []
death_numbers = []
for date in chosen_days:
    conf_numbers.append(country_conf[date].sum())
    death_numbers.append(country_death[date].sum())

# deathrate in last x days
incrDList = []
for i in range(1, DAYS_TO_LOOK_BACK):
    if death_numbers[-i-1] != 0:
        INCR = (death_numbers[-i] - death_numbers[-i-1])/death_numbers[-i-1]
    else:
        # instead of infinite: 0
        INCR = 0
    incrDList.append(INCR*100)
incrDList = incrDList[::-1]

# rate of new confirmed cases
incrCList = []
for i in range(1, DAYS_TO_LOOK_BACK):
    if conf_numbers[-i-1] != 0:
        INCR = (conf_numbers[-i] - conf_numbers[-i-1])/conf_numbers[-i-1]
    else:
        INCR = 0                # instead of infinite: 0
    incrCList.append(INCR*100)
incrCList = incrCList[::-1]

# PLOT
plt.figure(figsize=(8, 8))
plt.suptitle(INFO_PROMPT)

ax1 = plt.subplot(2, 2, 1)
conf_plot = conf.set_index(["Country/Region", "Province/State"]).loc[COUNTRY].\
    iloc[:, -DAYS_TO_LOOK_BACK:].sum()
line1, = ax1.plot_date(pd.to_datetime(conf_plot.keys().values),
                       conf_plot.values, "b",
                       label=f"confirmed: {format(conf_numbers[-1])}")
ax1.xaxis.set_major_formatter(mdates.DateFormatter("%m/%d"))
ax1.set_title(COUNTRY + " (confirmed)")
ax1.tick_params(axis="x", labelrotation=30)
ax1.legend()


ax2 = plt.subplot(2, 2, 2)
death_plot = death.set_index(["Country/Region",
                              "Province/State"]).loc[COUNTRY].\
    iloc[:, -DAYS_TO_LOOK_BACK:].sum()
ax2.plot_date(pd.to_datetime(death_plot.keys().values),
              death_plot.values, "r",
              label=f"death: {format(death_numbers[-1])}")
ax2.xaxis.set_major_formatter(mdates.DateFormatter("%m/%d"))
ax2.plot([], [], " ", label="(deaths/conf = {:.2%})"
         .format(death_numbers[-1]/conf_numbers[-1]))
ax2.set_title(COUNTRY + " (deaths)")
ax2.tick_params(axis="x", labelrotation=30)
ax2.legend()


ax3 = plt.subplot(2, 1, 2)
ax3.plot(np.arange(DAYS_TO_LOOK_BACK - 1), incrDList,
         label="death growth rate")
ax3.plot(np.arange(DAYS_TO_LOOK_BACK - 1), incrCList, label="new cases rate")
ax3.set_title(COUNTRY + " (rates)")
ax3.set_xlabel("Days")
ax3.set_ylabel("Percentage")
# calculating ylim from mean
# plt.ylim(0, max(pd.Series(incrCList).mean(),
#                 pd.Series(incrDList).mean()) * 3.5)
ax3.legend()

plt.tight_layout()
plt.show()
