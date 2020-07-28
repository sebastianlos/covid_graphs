# covid_graphs
Statistical graphs about the current state of Covid-19. <br>
You can specify country and time span and will receive graphs that show the trend of confirmed cases, number of death and the rate of increase of both. <br>
The data is based on "[JHU CSSE COVID-19 Data](https://github.com/CSSEGISandData/COVID-19)" from the John Hopkins University. The John Hopkins University offers a usefull [Dashboard](https://www.arcgis.com/apps/opsdashboard/index.html#/bda7594740fd40299423467b48e9ecf6) by themself, but if you are looking for a more minimalistic presentation, easily retrievable from terminal, you might want to use this small python program. <br>



Usage
---------

Execute the python-file `covid_graphs.py` from terminal, passing two arguments:

<ul>
<li> Country (see `country_names.txt` for a list of valid country names) </li>
<li> Number of days you want to retrieve data for. </li>
</ul>

Example
---------

    $ python covid_graphs.py "United Kingdom" 30
