import feedparser
import time

# SEC RSS feed for Tesla filings
RSS_URL = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&CIK=&type=&company=&dateb=&owner=include&start=0&count=40&output=atom"

# store last seen entry to detect new filings
last_seen_id = None

while True:
    feed = feedparser.parse(RSS_URL)
    print(feed)
    time.sleep(10)  # check every 60 seconds
