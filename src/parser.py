import time
import feedparser
from bs4 import BeautifulSoup
from typing import Dict, Any

def strip_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text().strip()

def fetch_feed_data(rss_url: str) -> Dict[str, Any]:
    # fetches a single feed.
    # returns dict format: { "Feed Title": { "Article Label": { "content": ..., "link": ... } } }
    try:
        feed = feedparser.parse(rss_url)
    except Exception:
        return {"Error": {}}

    feed_title = getattr(feed.feed, 'title', rss_url)
    items = {}

    for entry in feed.entries:
        title = getattr(entry, 'title', 'No Title')
        link = getattr(entry, 'link', '')
        
        if hasattr(entry, 'published_parsed') and entry.published_parsed:
            date_str = time.strftime("%Y-%m-%d", entry.published_parsed)
        else:
            date_str = "Unknown" # if no date is available
            
        summary = getattr(entry, 'summary', 'No Content')
        stripped_summary = strip_html(summary)

        # label for the tree node
        label = f"{date_str} | {title}"
        
        items[label] = {
            "content": stripped_summary,
            "link": link,
            "title": title
        }

    return {feed_title: items}