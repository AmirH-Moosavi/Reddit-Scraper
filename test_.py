import pytest
import pandas as pd
from datetime import datetime
from unittest.mock import patch
from Reddit_scraper import RedditScraper
import responses


@pytest.fixture
def reddit_scraper():
    return RedditScraper()


def test_convert_timestamp():
    scraper = RedditScraper()
    timestamp = 1614765600  # March 3, 2021
    expected_date = "2021-03-03"
    assert scraper.convert_timestamp(timestamp) == expected_date


def test_is_outside_date_range(reddit_scraper):
    post_timestamp_inside_range = "2023-01-01"
    post_timestamp_outside_range = "2021-01-01"
    reddit_scraper.start_date = datetime.strptime("2022-01-01", "%Y-%m-%d")
    assert not reddit_scraper.is_outside_date_range(post_timestamp_inside_range)
    assert reddit_scraper.is_outside_date_range(post_timestamp_outside_range)


def test_add_post_to_dataframe(reddit_scraper):
    post_data = {
        "name": "12345",
        "ups": 100,
        "upvote_ratio": 0.95,
        "num_comments": 50,
        "title": "Test Title",
        "subreddit_subscribers": 1000
    }
    reddit_scraper.add_post_to_dataframe(post_data)
    assert isinstance(reddit_scraper.df, pd.DataFrame)
    assert len(reddit_scraper.df) == 1
    assert reddit_scraper.df.iloc[0]["identifier"] == "12345"


@patch('Reddit_scraper.requests.get')
def test_fetch_data(mock_requests_get):
    url = "https://www.reddit.com/r/asb/new.json?sort=new&limit=100"
    mock_response_json = {"data": {"children": []}}

    responses.add(
        responses.GET, url,
        json=mock_response_json,
        status=200
    )

    data = reddit_scraper.fetch_data(url, None)
    assert data == mock_response_json