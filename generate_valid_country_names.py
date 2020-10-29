"""
Generates textfile with valid country names
"""

import pandas as pd

conf = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/\
    master/csse_covid_19_data/csse_covid_19_time_series/\
    time_series_covid19_confirmed_global.csv")

country_names_array = conf["Country/Region"].unique()

with open("country_names.txt", "w") as f:
    for row in country_names_array:
        f.write(row + "\n")
