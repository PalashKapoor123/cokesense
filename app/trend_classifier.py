"""
Trend classifier for CokeSense:
- Filters out unsafe/political trends
- Categorizes trends into sports, entertainment, or general
"""

RISKY_KEYWORDS = [
    # Politics & governance
    "election", "president", "prime minister", "senate",
    "congress", "parliament", "vote", "voting", "ballot",
    "campaign", "republican", "democrat", "gop",

    # Violence / sensitive topics
    "war", "conflict", "battle", "attack", "bomb",
    "shooting", "genocide", "terror", "hostage",

    # Crime & legal issues
    "arrest", "crime", "lawsuit", "trial", "court",
]

SPORT_KEYWORDS = [
    "nfl", "nba", "mlb", "nhl", "ufc",
    "soccer", "football", "basketball", "baseball",
    "fifa", "world cup", "super bowl", "champions league",
    "tennis", "wimbledon", "olympics"
]

ENTERTAINMENT_KEYWORDS = [
    "movie", "film", "trailer", "actor", "actress",
    "show", "series", "episode",
    "album", "song", "music", "concert", "tour",
    "festival", "oscars", "grammys", "emmys"
]


def classify_trend(term: str) -> str:
    """
    Returns one of:
        - "skip" (unsafe or political)
        - "sports"
        - "entertainment"
        - "general"
    """
    if not term:
        return "general"

    t = term.lower()

    # Safety filter
    if any(word in t for word in RISKY_KEYWORDS):
        return "skip"

    # Sports category
    if any(word in t for word in SPORT_KEYWORDS):
        return "sports"

    # Entertainment category
    if any(word in t for word in ENTERTAINMENT_KEYWORDS):
        return "entertainment"

    return "general"
