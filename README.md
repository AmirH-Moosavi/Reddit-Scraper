# Reddit-scraper

This project aims to scrape the Reddit website to compile posts from two different subreddits and make analytical comparisons between them. This project was developed in two phases.

# 1. Reddit Scraper:
During the first stage of the project, we aim to develop a Python web crawler to collect posts from our desired subreddits and store them in two separate CSV files. To run the script, you'll need Python 3.7 or later installed on your system. You can install the required dependencies by running:

## Installation:
```sh
pip3 install -r requirements.txt
```
# Usage:
To start the scraper, run the following command:
```sh
python Reddit_scraper.py subreddit1,subreddit2
```

Replace subreddit1 and subreddit2 with your desired subreddits. For instance:
```sh
python Reddit_scraper.py vim,emacs
```

 ## Code Architecture Overview:
 ### Error Handlers
The script incorporates robust error handling to manage unsuccessful requests. After any failed request, the script retries up to five times before giving up.

 ### Post Extraction and Storage
The process of extracting posts from Reddit involves addressing the challenges posed by the platform's intricate request-response mechanism. Reddit's method of handling requests, predominantly through GraphQL – a data query language for APIs, encrypts data transmission, making the task of scraping and processing data considerably complex.

<br> While Selenium could have been a viable option for web scraping, this project didn't involve that approach. Instead, an API was leveraged to access posts and subreddit data from the past months. This API served as a gateway to extract relevant posts from the specified subreddits, allowing retrieval of valuable information.

<br> The extracted posts, obtained through this API, were then systematically stored in separate CSV files. This storage setup facilitated the subsequent analytical phase by providing structured datasets ready for analysis and comparison between the selected subreddits.

 ### Output
The scraper generates informative messages about the status of requests during scraping. If unexpected interruptions occur, the collected data is still stored in the CSV file, enabling the process to resume from the point of interruption.
#### Example output
 ![image](https://github.com/AmirH-Moosavi/Reddit-scraper/assets/68806656/88bb3f62-e52b-4d78-a0d4-543dd148b641)
 
# 2. Reddit Analyzer
Following the collection of our dataset, the next step involves implementing both analytical and behavioral approaches to unearth patterns within user behavior and post interactions. To achieve this, a series of plots have been generated, allowing for the visualization of appropriate information. These visual representations serve as invaluable tools, empowering us to discern patterns, trends, and inherent characteristics embedded within the subreddits.

 ### Test
 You are able to test the functionality of this scraper using the following command in the root directory:
```sh
pytest
```
