from pytrends.request import TrendReq
import requests
from bs4 import BeautifulSoup
import json
from pathlib import Path
from datetime import datetime, timedelta

# Path to data folder
DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def get_google_trends(country: str = "united_states") -> list[str]:
    """
    Fetches current Google trending searches for a given country.
    Uses the unofficial pytrends API.
    """
    try:
        pytrends = TrendReq(hl="en-US", tz=360, retries=2, backoff_factor=0.1)
        # Try trending_searches first, fallback to daily trends
        try:
            df = pytrends.trending_searches(pn=country)
            if df is not None and not df.empty:
                return df[0].tolist()
        except Exception:
            pass
        
        # Fallback: get daily trending searches
        try:
            df = pytrends.trending_searches(pn=country)
            if df is not None and not df.empty:
                return df[0].tolist()[:25]  # Limit to 25
        except Exception:
            pass
        
        return []
    except Exception as e:
        print("Error fetching Google Trends:", e)
        return []


def get_x_trends() -> list[str]:
    """
    Scrapes Trends24 for US Twitter trending topics.
    Uses a browser-like user-agent to bypass simple bot blocks.
    Gets trends from multiple time periods for more diversity.
    """
    url = "https://trends24.in/united-states/"

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        trends = []
        
        # Try multiple selectors for trend cards
        # Method 1: Get ALL trend cards (not just first one)
        trend_cards = soup.find_all("div", class_="trend-card")
        if trend_cards:
            # Get trends from first 3 cards (recent hours)
            for card in trend_cards[:3]:
                card_trends = [a.get_text(strip=True) for a in card.select("ol li a, ul li a")]
                trends.extend(card_trends)
        
        # Method 2: Try alternative selectors
        if not trends:
            trend_items = soup.select("ol.trend-list li a, ul.trend-list li a, .trend-item a, .trending-item a")
            trends = [item.get_text(strip=True) for item in trend_items if item.get_text(strip=True)]
        
        # Method 3: Look for any ordered/unordered lists with links
        if not trends:
            lists = soup.find_all(["ol", "ul"], limit=10)
            for lst in lists:
                links = lst.find_all("a")
                if links:
                    list_trends = [link.get_text(strip=True) for link in links if link.get_text(strip=True)]
                    trends.extend(list_trends)
        
        # Remove duplicates and clean
        trends = list(set([t for t in trends if t and len(t.strip()) > 2]))
        
        if not trends:
            print("Warning: No trend cards found on Trends24. HTML structure may have changed.")
            return []

        return trends[:30]  # Return up to 30 trends

    except Exception as e:
        print("Error fetching Trends24 trends:", e)
        return []


def get_upcoming_events(days: int = 30) -> list[str]:
    """
    Loads upcoming cultural events from events.json.
    Only returns events occurring within the next `days` days.
    """
    try:
        with open(DATA_DIR / "events.json") as f:
            events = json.load(f).get("events", [])
    except Exception as e:
        print("Error loading events.json:", e)
        return []

    today = datetime.today()
    cutoff = today + timedelta(days=days)

    upcoming = []
    for e in events:
        try:
            event_date = datetime.fromisoformat(e["date"])
            if today <= event_date <= cutoff:
                upcoming.append(e["name"])
        except Exception:
            continue

    return upcoming


def get_popular_topics() -> list[str]:
    """
    Returns a curated list of popular topics that are always relevant.
    These serve as fallback trends when other sources are limited.
    """
    return [
        "Music", "Movies", "Sports", "Technology", "Fashion",
        "Food", "Travel", "Fitness", "Gaming", "Art",
        "Books", "TV Shows", "Celebrities", "Social Media",
        "Climate", "Innovation", "Wellness", "Culture"
    ]


def get_all_trends() -> list[str]:
    """
    Merges:
      - Google trends
      - X/Twitter trends
      - Upcoming cultural events
      - Popular topics (fallback)
    Removes duplicates & cleans empty strings.
    """
    combined = set()

    # Google Trends
    google_trends = get_google_trends()
    combined.update(google_trends)

    # X Trends
    x_trends = get_x_trends()
    combined.update(x_trends)

    # Events
    events = get_upcoming_events()
    combined.update(events)

    # If we have very few trends, add popular topics as fallback
    if len(combined) < 10:
        combined.update(get_popular_topics())

    # Clean empty entries and filter out very short or problematic trends
    cleaned = [
        t for t in combined 
        if isinstance(t, str) 
        and t.strip() 
        and len(t.strip()) > 2
        and not t.strip().startswith("#")  # Remove hashtags
        and not t.strip().startswith("@")   # Remove mentions
    ]

    return sorted(cleaned)
