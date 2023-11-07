## Python Advertising Statistics with www.arbeitsagentur.de

This application was made to scrap data about Python advertisements
from www.arbeitsagentur.de (German national job agency web resource) and make
statistics analyse of this data.
With it, You can find out in which city python developers are most needed,
which companies send most requests for python developers,
what education You should have to receive a dev job,
what technologies You have to know to receive a dev job

## Installing / Getting started

A quick introduction of the minimal setup you need to get the data and make analyse.

### Python3 must be already installed!

```shell
git clone https://github.com/arturiermolenko/python_jobs_in_germany_analyse
cd python_jobs_in_germany_analyse
python3 -m venv venv 
source venv/bin/activate
pip install -r requirements.txt
scrapy crawl arbeitsagentur -O data.csv
```

## Read statistics
To see the statistics just go to "stats_analyse" folder and start main.ipynb.
Run all cells one by one to see the plots.


### About .env file
First of all, rename .env_sample to .env !!!

In this file variables are for receiving fake headers, fake "User Agent"`s and indication the search word.
Read the info about "search word" below.

With existing code, it is not necessary to use fake headers and fake "User Agent"`s, because we are making creating only two webdriver.Chrome.
In case You would like to add requests to script, You can use fake headers or/and fake "User-Agent".
You need to create an account on https://scrapeops.io/. Then go to https://scrapeops.io/app/headers and 
fill in .env_sample with Your API key and response URL.
Also, You should uncomment lines 64 and 65 in settings.py to use fake headers middlewares. 


## Other search requests
If You want to analyse the jobs, by different from "Python" search word You can change SEARCH_WORD parameter in .env file to Your search word.

## Features:
- scraping data from www.arbeitsagentur.de by "Python" search word
- possibility to scrap info by any other search word
- find out in which German city python developers are most needed
- which companies send most requests for python developers
- what education You should have to receive a python-dev job
- what technologies You have to know to receive a python-dev job



