import json
import logging
import os
import sys
import colorlog

import time
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

import pandas as pd
import requests


class RedditScraper:
    """
       Let's scrape Reddit

       Parameters:
       - sub_reddit (str): The name of the subreddit to scrape.
       - start_date (str): The start date in the format 'YYYY-MM-DD'.
       - end_date (str): The end date in the format 'YYYY-MM-DD'.
    """
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    }
    REQUEST_TIMEOUT = 8
    NUMBER_OF_RETRIES = 5

    def __init__(self):
        self.columns = ["identifier", "ups", "User Engagement Ratio", "upvote ratio", "nummber of comments",
                        "title length"]
        self.df = pd.DataFrame(columns=self.columns)
        self.start_date = datetime.strptime(str(date.today()), "%Y-%m-%d")
        self.end_date = datetime.strptime(str(date.today() - relativedelta(months=3)), "%Y-%m-%d")
        self.total_success = 0

        # Set up console logging with color
        self.logger = logging.getLogger("RedditScraper")
        self.logger.setLevel(logging.INFO)
        console_handler = colorlog.StreamHandler()
        console_handler.setLevel(logging.INFO)
        formatter = colorlog.ColoredFormatter(
            "%(log_color)s%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            }
        )
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def fetch_data(self, url, after):
        """
        Fetches Reddit data using a HTTP GET request.

        Parameters:
        - url (str): The URL for the Reddit API request.
        - after (str): The post identifier for pagination.

        Returns:
        - dict or None: The JSON response data or None if the request fails.
        """
        number_of_retries = self.NUMBER_OF_RETRIES
        params = {"params": {'after': after}} if after else {}

        while number_of_retries > 0:
            try:
                response = self.make_request(url, params)
                if response.status_code == 200 and self.is_json(response):
                    return self.handle_success(response)
                else:
                    self.handle_failure(response.status_code)
                    number_of_retries -= 1
            except (requests.Timeout, requests.ConnectionError):
                self.handle_retry()
                number_of_retries -= 1

        self.logger.error("Max retries exceeded. Give up.")
        return None

    def is_json(self, response: requests.Response):
        try:
            json.loads(response.text)
            return True
        except json.JSONDecodeError:
            self.logger.warning("Response is not a valid JSON.")
            return False

    def make_request(self, url, params):
        try:
            return requests.get(url, headers=self.HEADERS, timeout=self.REQUEST_TIMEOUT, **params)
        except (requests.Timeout, requests.ConnectionError):
            raise

    def handle_success(self, response: requests.Response):
        self.total_success += 1
        self.logger.info(f"[{self.total_success}] Successful! [200]")
        return response.json()

    def handle_failure(self, status_code: int):
        self.logger.warning(f"Request failed with status code {status_code}. Retrying...")

    def handle_retry(self):
        self.logger.warning("Request timed out or connection error. Retrying...")
        time.sleep(0.1)

    def scrape(self, url):
        """
           Scrapes Reddit posts within the specified date range and stores them in a DataFrame.

           Returns:
           - pd.DataFrame: The DataFrame containing scraped Reddit post data.
        """
        after = None
        while True:
            data = self.fetch_data(url, after)
            after, flag = self.extract_posts(data)
            if not after or flag:
                self.logger.info(f"End of scraping")
                break
        

        return self.df

    def extract_posts(self, data):
        """
        Extracts Reddit posts from the data and add them to the DataFrame.

        Parameters:
        - data (dict): The JSON response data from Reddit API.

        Returns:end_date
        - Tuple[Optional[str], bool]: The post identifier for pagination and a flag indicating the end of scraping.
        """
        after, flag = None, False

        if "data" in data and "children" in data.get('data', []):
            for child in data["data"]["children"]:
                post_data = child.get("data", {})
                post_timestamp = self.convert_timestamp(post_data.get("created_utc", 0))


                if self.end_date <= datetime.strptime(post_timestamp, "%Y-%m-%d") <= self.start_date:
                    self.add_post_to_dataframe(post_data)
                elif self.is_outside_date_range(post_timestamp):
                    return post_data.get("name"), True

                after = post_data.get("name", None)

        return after, flag

    @staticmethod
    def convert_timestamp(timestamp):
        """
            Convert the Unix timestamp to a string in the format "%Y-%m-%d".

            Parameters:
            - timestamp (int): Unix timestamp.

            Returns:
            - str: String representation of the timestamp in the format "%Y-%m-%d".
        """
        return datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d")

    def add_post_to_dataframe(self, post_data: dict):
        """
            Add post data to the DataFrame.

        """
        subscribers = post_data.get('subreddit_subscribers', 0)
        u_engagement_ratio = post_data.get("ups", 0) / max(subscribers, 1)

        # Metrics
        new_data = [
            post_data.get("name"),
            post_data.get("ups"),
            u_engagement_ratio,
            post_data.get("upvote_ratio"),
            post_data.get("num_comments"),
            len(post_data.get("title"))
        ]
        self.df.loc[len(self.df)] = new_data

    def is_outside_date_range(self, post_timestamp):
        """
            Checks if the post timestamp is outside the specified date range.
        
        """
        return datetime.strptime(post_timestamp, "%Y-%m-%d") < self.start_date

    def save_to_csv(self, df, subreddit):
        """
            Saves the DataFrame to a CSV file.

        """
        
        try:
            directory = "Datasets"
            if not os.path.exists(directory):
                os.makedirs(directory)
            filepath = os.path.join(directory, f"{subreddit}.csv")
            df.to_csv(filepath, index=False)
            self.logger.info(f"DataFrame saved to {filepath}")
        except Exception as e:
            self.logger.error(f"Error occurred while saving DataFrame: {e}")
        return None

    def main (self):
        subreddits = sys.argv[1] if len(sys.argv) > 1 else ""  # Your custom subreddits.
        assert subreddits != "", "subreddits could not be empty."

        subreddits = subreddits.split(',')
        assert len(subreddits) == 2, "Enter two valid subreddits."

        for subreddit in subreddits:
            self.logger.info(f"\nScraping subreddit: {subreddit}")
            url = f"https://www.reddit.com/r/{subreddit}/new.json?sort=new&limit=100"
            result_df = scraper.scrape(url)

            self.save_to_csv(result_df, subreddit)
   

if __name__ == "__main__":
    scraper = RedditScraper()
    scraper.main()
