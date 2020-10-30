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
INFO_PROMPT = "Data for {} for last {} days\n(Data available for {} days)\n\
    Last data ingestion: {}"\
    .format(COUNTRY, DAYS_TO_LOOK_BACK, days_available, chosen_days[-1])

# per COUNTRY
country_conf = conf.groupby("Country/Region").get_group(COUNTRY)
country_death = death.groupby("Country/Region").get_group(COUNTRY)

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
        INCR = 0                # instead of infinite: 0
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


plt.figure(figsize=(8, 8))

plt.subplot(2, 2, 1)
conf.set_index(["Country/Region", "Province/State"]).loc[COUNTRY].\
    iloc[:, -DAYS_TO_LOOK_BACK:].sum().\
    plot(label=f"confirmed: {format(conf_numbers[-1])}")
plt.title(COUNTRY + " (confirmed)")
plt.xticks(rotation=45)
plt.legend()


plt.subplot(2, 2, 2)
death.set_index(["Country/Region", "Province/State"]).loc[COUNTRY].\
    iloc[:, -DAYS_TO_LOOK_BACK:].sum().\
    plot(label=f"death: {format(death_numbers[-1])}")
plt.plot([], [], " ", label="(deaths/conf = {:.2%})"
         .format(death_numbers[-1]/conf_numbers[-1]))
plt.title(COUNTRY + " (deaths)")
plt.xticks(rotation=45)
plt.legend()


plt.subplot(2, 2, 3)
plt.plot(np.arange(DAYS_TO_LOOK_BACK - 1), incrDList,
         label="death growth rate")
plt.plot(np.arange(DAYS_TO_LOOK_BACK - 1), incrCList, label="new cases rate")
plt.title(COUNTRY + " (rates)")
plt.xlabel("Days")
plt.ylabel("Percentage")
# calculating ylim from mean
plt.ylim(0, max(pd.Series(incrCList).mean(),
                pd.Series(incrDList).mean()) * 3.5)
plt.legend()

plt.subplot(2, 2, 4)
plt.xticks(())
plt.yticks(())
plt.text(0.5, 0.5, INFO_PROMPT, ha='center', va='center',
         size=13, alpha=1)
ax = plt.gca()
ax.spines["top"].set_color('none')
ax.spines["bottom"].set_color('none')
ax.spines["left"].set_color('none')
ax.spines["right"].set_color('none')


plt.tight_layout()
plt.show()
