# Covid Graphs

![Pylint](https://github.com/sloschert/covid_graphs/workflows/Pylint/badge.svg)

- This program provides statistical graphs about the current state of Covid-19. <br>
- You can specify country and time span. <br>
- The data is based on "[JHU CSSE COVID-19 Data](https://github.com/CSSEGISandData/COVID-19)" from the John Hopkins University.


## Usage

Execute the python-file `covid_graphs.py`, passing two arguments:


* Country name. (See `country_names.txt` for a list of valid country names.)
* Number of days to look back.


## Example

    $ python covid_graphs.py -c Germany -d 100
    
![Graph Germany last 100 days](https://github.com/sloschert/covid_graphs/blob/master/img/covid_graphs.png?raw=True)    
