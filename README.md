# Sports Betting Scraper API

This project scrapes sports betting data from [PMU.ch](https://racingaustralia.horse/FreeFields/Calendar_Scratchings.aspx?State=NSW) using Selenium, stores the data in a MongoDB database, and provides a RESTful API to trigger the scraping process.

## Steps to Set Up and Run the Project

### 1. Install Python

First, make sure Python 3.8+ is installed on your machine. If it isn't, you can download it from the [official Python website](https://www.python.org/downloads/).

### 2. Install Required Libraries

Next, you need to install the required Python libraries. Open a terminal or command prompt and run the following commands:

powershell or command

`pip install Flask`
`pip install selenium`
`pip install beautifulsoup4`
`pip install pymongo`

### 3. Start Project

powershell or command

`python index.py`

### 4. Get Data

To install Postman on your PC, follow these steps:

Download Postman from the official website: `https://www.postman.com/downloads/`

Install it on your computer by following the on-screen instructions.
Once Postman is installed, you can make requests to your API, using the following parameters to represent Australian states and territories:

`New South Wales → NSW`
`Victoria → VIC`
`Queensland → QLD`
`Western Australia → WA`
`South Australia → SA`
`Tasmania → TAS`
`Australian Capital Territory → ACT`
`Northern Territory → NT`

For example, to send a request for New South Wales (NSW), use the following URL in Postman:
`http://127.0.0.1:5000/scrape/NSW`