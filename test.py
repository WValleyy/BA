import asyncio
import csv
from twitter_search import read_keywords_from_file, run_search_user, filter_users, login,crawl_tweets_from_KOLs

app = login()
import ipdb; ipdb.set_trace()
# Run the search and save function
keywords = read_keywords_from_file("keywords.txt")
run_search_user(keywords, app, pages_num = 1, wait_times = 2, cursor_ = None) #cusor is the page that looking up-to