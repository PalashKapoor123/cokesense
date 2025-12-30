"""
Post History & Analytics Module
Tracks Instagram posts and fetches their performance statistics
"""
import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional
import requests


# Database setup
DB_PATH = "data/post_history.db"


def init_database():
    """Initialize the SQLite database for storing post history."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id TEXT UNIQUE,
            trend TEXT,
            caption TEXT,
            image_url TEXT,
            posted_at TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'active'
        )
    ''')
    # Add status column if it doesn't exist (for existing databases)
    try:
        c.execute('ALTER TABLE posts ADD COLUMN status TEXT DEFAULT "active"')
    except sqlite3.OperationalError:
        pass  # Column already exists
    conn.commit()
    conn.close()


def save_post(post_id: str, trend: str, caption: str, image_url: str = None):
    """Save a post to the database."""
    init_database()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute('''
            INSERT OR REPLACE INTO posts (post_id, trend, caption, image_url, posted_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (post_id, trend, caption, image_url, datetime.now().isoformat()))
        conn.commit()
    except Exception as e:
        print(f"Error saving post: {e}")
    finally:
        conn.close()


def get_all_posts(include_deleted: bool = True) -> List[Dict]:
    """Get all posts from the database."""
    init_database()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if include_deleted:
        c.execute('SELECT * FROM posts ORDER BY posted_at DESC')
    else:
        c.execute("SELECT * FROM posts WHERE status != 'deleted' ORDER BY posted_at DESC")
    posts = []
    for row in c.fetchall():
        posts.append({
            'id': row[0],
            'post_id': row[1],
            'trend': row[2],
            'caption': row[3],
            'image_url': row[4],
            'posted_at': row[5],
            'created_at': row[6],
            'status': row[7] if len(row) > 7 else 'active'
        })
    conn.close()
    return posts


def mark_post_deleted(post_id: str):
    """Mark a post as deleted in the database."""
    init_database()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('UPDATE posts SET status = ? WHERE post_id = ?', ('deleted', post_id))
    conn.commit()
    conn.close()


def get_post_insights(post_id: str, access_token: str) -> Optional[Dict]:
    """
    Fetch Instagram post insights using Graph API.
    
    Returns:
        Dictionary with likes, comments, shares, reach, impressions, engagement_rate
        Returns None if post is deleted or inaccessible
    """
    try:
        # Get basic post metrics
        url = f"https://graph.instagram.com/{post_id}"
        params = {
            "fields": "like_count,comments_count,permalink",
            "access_token": access_token
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code != 200:
            error_data = response.json() if response.text else {}
            error_code = error_data.get('error', {}).get('code')
            error_message = error_data.get('error', {}).get('message', '').lower()
            
            # Check if post is deleted (common error codes: 100, 803, or "does not exist")
            if error_code in [100, 803] or 'does not exist' in error_message or 'not found' in error_message:
                # Mark as deleted in database
                mark_post_deleted(post_id)
                return {'deleted': True}
            
            print(f"Error fetching post data: {response.status_code} - {response.text}")
            return None
        
        data = response.json()
        
        # Get insights (requires business account)
        insights_url = f"https://graph.instagram.com/{post_id}/insights"
        insights_params = {
            "metric": "impressions,reach,engagement",
            "access_token": access_token
        }
        
        insights_response = requests.get(insights_url, params=insights_params, timeout=10)
        
        insights_data = {}
        if insights_response.status_code == 200:
            insights_json = insights_response.json()
            for metric in insights_json.get('data', []):
                if metric['name'] == 'impressions':
                    insights_data['impressions'] = metric['values'][0]['value']
                elif metric['name'] == 'reach':
                    insights_data['reach'] = metric['values'][0]['value']
                elif metric['name'] == 'engagement':
                    insights_data['engagement'] = metric['values'][0]['value']
        
        # Calculate engagement rate
        likes = data.get('like_count', 0)
        comments = data.get('comments_count', 0)
        reach = insights_data.get('reach', 0)
        
        engagement_rate = 0
        if reach > 0:
            engagement_rate = ((likes + comments) / reach) * 100
        
        return {
            'likes': likes,
            'comments': comments,
            'shares': 0,  # Shares not always available via API
            'reach': insights_data.get('reach', 0),
            'impressions': insights_data.get('impressions', 0),
            'engagement': insights_data.get('engagement', 0),
            'engagement_rate': round(engagement_rate, 2),
            'permalink': data.get('permalink', ''),
            'total_engagement': likes + comments
        }
        
    except Exception as e:
        print(f"Error fetching insights: {e}")
        return None


def get_all_posts_with_insights(access_token: str, include_deleted: bool = True) -> List[Dict]:
    """
    Get all posts with their current Instagram statistics.
    
    Args:
        access_token: Instagram access token
        include_deleted: Whether to include deleted posts
    
    Returns:
        List of posts with insights data
    """
    posts = get_all_posts(include_deleted=include_deleted)
    posts_with_insights = []
    
    for post in posts:
        # Skip if already marked as deleted and we're not including deleted
        if post.get('status') == 'deleted' and not include_deleted:
            continue
            
        insights = get_post_insights(post['post_id'], access_token)
        if insights:
            if insights.get('deleted'):
                # Post was deleted on Instagram
                post.update({
                    'status': 'deleted',
                    'likes': 0,
                    'comments': 0,
                    'shares': 0,
                    'reach': 0,
                    'impressions': 0,
                    'engagement_rate': 0,
                    'total_engagement': 0,
                    'deleted': True
                })
            else:
                post.update(insights)
                post['status'] = 'active'
        else:
            # If insights fail, still show the post with basic info
            post.update({
                'likes': 0,
                'comments': 0,
                'shares': 0,
                'reach': 0,
                'impressions': 0,
                'engagement_rate': 0,
                'total_engagement': 0
            })
            # Keep existing status if available
            if 'status' not in post:
                post['status'] = 'active'
        posts_with_insights.append(post)
    
    return posts_with_insights

