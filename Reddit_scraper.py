# import libraries
from datetime import datetime
import pandas as pd
import requests

class RedditScraper:
    # Initialize RedditScraper with subreddit name, start date, and end date.
    def __init__(self, subreddit: str, start_date: str, end_date: str):
        self.subreddit = subreddit
        self.url = f"https://www.reddit.com/r/{subreddit}/new.json?sort=new&limit=100"
        self.start_date = datetime.strptime(start_date, "%Y-%m-%d")
        self.end_date = datetime.strptime(end_date, "%Y-%m-%d")
        self.columns = ['identifier', 'ups', 'downs', 'upvote_ratio', 'num_comments', 'time']
        self.df = pd.DataFrame(columns=self.columns)

    #Fetch Reddit data using HTTP GET request and return status code and JSON response.
    def fetch_data(self, url: str, headers: dict):
        # try, except
        try:
            response = requests.get(url, headers=headers)
            # Check if the request status to inform it was successful
            status_code = response.status_code
            if status_code == 200:
                return status_code, response.json()
            # If we fail to collect the data due to network problems or limited access to the data this error will occur and assert the cause of failure
            else:
                print(f"Failed to fetch data. Status Code: {status_code}")
        
        # If the request could not be handled, we will encounter this error
        except requests.RequestException as e:
            print(f"Error occurred during HTTP request: {e}")

    def scrape(self):
        after = None
        while True:
            status_code, data = self.fetch_data(self.url if after is None else f"{self.url}&after={after}", {'User-agent': 'your bot 0.1'})
            if status_code == 200:
                after, flag = self.extract_posts(data)
                if not after or flag:
                    break
            else:
                break
        return self.df
    
# Example usage:
if __name__ == "__main__":
    subreddit = "emacs"
    start_date = "2020-09-21"
    end_date = "2023-12-20"
    
    scraper = RedditScraper(subreddit, start_date, end_date)
    result_df = scraper.scrape()
    print(result_df)
