# Evas-Tel Interview Task

This task is to create an API endpoint in Python to scrape products data from OLX website and then store scraped items in MongoDB then send sample results to an email given in query parameters 

## Technology Used:
* FastAPI
* MongoDB
* Selenium
* Mailgun


## Installation

Python should be installed on your machine or you can install it from here 
[Python](https://www.python.org/downloads/)

We should create a virtual environment for the project to install the dependencies inside this environment

for example, we can use this environment name: evas

```bash
python -m venv evas 
```
then we activate it through:

for Windows:
```bash
evas\scripts\activate
```
for macOS:
```bash
source /path/to/venv/bin/activate
```

then we install the task dependencies:

Use the package manager
[pip](https://pip.pypa.io/en/stable/)

```bash
pip install -r requirements.txt
```
## MongoDB Setup

The task uses MongoDB Atlas Cluster to store the scraped data in documents on the cloud. We should create a free account on [MongoDB](https://www.mongodb.com/) and then set up a free tier cluster to get an "ALTAS_URI" string which will be used in establishing the database connection [Free Tier](https://www.mongodb.com/docs/atlas/tutorial/deploy-free-tier-cluster/)

## MailGun API

We use "MailGun API" service for sending emails 

A free account should be created at [MailGun](https://www.mailgun.com/) to obtain an 'API KEY' and 'Domain'

## Contents of ".env" file

* DB_NAME=<database name>  -> evas
* DB_COLLECTION=<collection name>  -> products
* DB_TERMS_COLLECTION=<collection search terms name>  -> searched_terms
* ATLAS_URI=<Atlas Cluster String>
* MAILGUN_API_KEY=<MailGun Api key>
* MAILGUN_DOMAIN=<MailGun Domain>


## Usage

Run main.py file
```
python main.py
```

The server will be run at [http://localhost:8000/](http://localhost:8000/)

Then to test the search endpoint with 3 query parameters like this:

http://localhost:8000/items/search?search_term=your_search_term&email=recipient_email&size=number_of_sample_results



