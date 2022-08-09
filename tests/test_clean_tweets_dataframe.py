from clean_tweets_dataframe import Clean_Tweets
from extract_dataframe import TweetDfExtractor
from extract_dataframe import read_json
import unittest
import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join("../")))


sampletweetsjsonfile = "data/sample.json"
_, tweet_list = read_json(sampletweetsjsonfile)

columns = [
    "created_at",
    "source",
    "original_text",
    "sentiment",
    "polarity",
    "subjectivity",
    "lang",
    "favorite_count",
    "retweet_count",
    "original_author",
    "screen_count",
    "followers_count",
    "friends_count",
    "possibly_sensitive",
    "hashtags",
    "user_mentions",
    "place",
]

tweet = TweetDfExtractor(tweet_list)
df = tweet.get_tweet_df(save=False)


class TestClean_Tweets(unittest.TestCase):
    # def setUp(self):
    #     self.clean_tweets = Clean_Tweets(df)

    def test_remove_non_english_tweets(self):
        self.assertEqual(
            Clean_Tweets(df).remove_non_english_tweets(df).lang.nunique(), 1
        )

    def test_drop_duplicates(self):
        self.assertEqual(
            Clean_Tweets(df).drop_duplicate(df).duplicated(subset='original_text', keep='first').sum(), 0)

    def test_convert_to_datetime(self):
        self.assertEqual(Clean_Tweets(df).convert_to_datetime(
            df).created_at.dtype, 'datetime64[ns, UTC]')


if __name__ == "__main__":
    unittest.main()
