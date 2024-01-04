![image](https://github.com/AmirH-Moosavi/Reddit-scraper/assets/68806656/d637f88b-b4b3-4943-9314-72be659b5fc3)# Reddit-scraper

This project aims to scrape the Reddit website to compile posts from two different subreddits and make analytical comparisons between them. This project was developed in two phases.

# 1. Reddit Scraper:
During the first stage of the project, we aim to develop a Python web crawler to collect posts from our desired subreddits and store them in two separate CSV files. To run the script, you'll need Python 3.7 or later installed on your system. You can install the required dependencies by running:

 '''sh
pip3 install -r requirements.txt
 '''
To start the scraper, run the following command:
'''sh
python Reddit_scraper.py subreddit1,subreddit2
'''

Replace subreddit1 and subreddit2 with your desired subreddits. For instance:
'''sh
python Reddit_scraper.py vim,emacs
'''
 ## Architecture of the code
 #### Error Handlers
 This script provided proper functions to handle errors related to unsuccessful requests. To achieve this, after any unsuccessful requests, we try four more times to crawl the posts. However, after five unsuccessful prompts, we give up and break the loop. 

 #### Post Extraction and Storage
 Here we are with the most challenging part of this project. Reddit is one of those websites with a really high rate of difficulty to scrape. This is due to its mysterious mechanism of sending the request to the server and consequently getting the response from it. As far as I am concerned, Reddit utilizes a send/receive  mechanism with graphql which is a data query language for APIs and query runtimes. Through this, data would be encrypted which make the crawiinga and processing of the data harder than usual. Anyways, Selenium could be a proper option to crawl data from the Reddit website. However, it was not the objective of this project. Thus, I utilized an API that provides posts and information about subreddits related to the last couple of months. After extracting posts belong to our subreddits, information would be stored in two separate CSV files for the following analytical phase. 

 #### Output
 During the scraping, relavent messages related to the status of the requests would be generated and even if unexpected interruption occurs during the scraping, collected data would be stored in the CSV file. This would allow us to continue the collection process from the exact point that interuption occured, 
 Here is an example of the output:
 ![image](https://github.com/AmirH-Moosavi/Reddit-scraper/assets/68806656/88bb3f62-e52b-4d78-a0d4-543dd148b641)


# 2. Reddit Analyzer
With the posts in hand, it is time to analyze and investigate relationships from our collected datasets. 
