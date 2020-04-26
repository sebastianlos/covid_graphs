#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 21:41:33 2020

@author: sebas
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys

# user input
if len(sys.argv) == 2:
    country = sys.argv[1]
elif len(sys.argv) > 2:
    country = sys.argv[1]
    days_to_look_back = int(sys.argv[2])
else:
    country = "United Kingdom"
    days_to_look_back = 20

# read files
conf = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv")
death = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv")
                    
dates = conf.columns[4:]
days_available = len(dates) 
chosen_days = dates[days_available - (days_to_look_back):]
info_prompt = "Data for {} for last {} days\n(Data available for {} days)\nLast data ingestion: {}"\
    .format( country, days_to_look_back, days_available, chosen_days[-1])



# per country
country_conf = conf.groupby("Country/Region").get_group(country)
country_death = death.groupby("Country/Region").get_group(country)

# on chosen dates
conf_numbers = []
death_numbers = []
for date in chosen_days:
    conf_numbers.append(country_conf[date].sum())
    death_numbers.append(country_death[date].sum())
  
# deathrate in last x days
incrDList = []
for i in range(1, days_to_look_back):
    if death_numbers[-i-1] != 0:
        incr = (death_numbers[-i] - death_numbers[-i-1])/death_numbers[-i-1]
    else:
        incr = 0                # instead of infinite: 0
    incrDList.append(incr*100)
incrDList = incrDList[::-1]

# rate of new confirmed cases
incrCList = []
for i in range(1, days_to_look_back):
    if conf_numbers[-i-1] != 0:
        incr = (conf_numbers[-i] - conf_numbers[-i-1])/conf_numbers[-i-1]
    else:
        incr = 0                # instead of infinite: 0
    incrCList.append(incr*100)
incrCList = incrCList[::-1]


plt.figure(figsize=(8, 8))

plt.subplot(2, 2, 1)
conf.set_index(["Country/Region", "Province/State"]).loc[country].iloc[:,-days_to_look_back:].sum().plot(label=f"confirmed: {format(conf_numbers[-1])}")
plt.title(country + " (confirmed)")
plt.xticks(rotation=45)
plt.legend()


plt.subplot(2, 2, 2)
death.set_index(["Country/Region", "Province/State"]).loc[country].iloc[:,-days_to_look_back:].sum().plot(label=f"death: {format(death_numbers[-1])}")
plt.plot([], [], " ", label="(deaths/conf = {:.2%})".format(death_numbers[-1]/conf_numbers[-1]))
plt.title(country + " (deaths)")
plt.xticks(rotation=45)
plt.legend()


plt.subplot(2, 2, 3)
plt.plot(np.arange(days_to_look_back - 1), incrDList, label="death growth rate")
plt.plot(np.arange(days_to_look_back - 1), incrCList, label="new cases rate")
plt.title(country + " (rates)")
plt.xlabel("Days")
plt.ylabel("Percentage")
plt.ylim(0, max(pd.Series(incrCList).mean(), pd.Series(incrDList).mean()) * 3.5) # calculating ylim from mean
plt.legend()

plt.subplot(2, 2, 4)
plt.xticks(())
plt.yticks(())
plt.text(0.5, 0.5, info_prompt, ha='center', va='center',
        size=13, alpha=1)
ax = plt.gca()
ax.spines["top"].set_color('none')
ax.spines["bottom"].set_color('none')
ax.spines["left"].set_color('none')
ax.spines["right"].set_color('none')


plt.tight_layout()
plt.show()

