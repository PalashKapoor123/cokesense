#!/usr/bin/env python3
"""
Quick test script to verify trend fetching is working.
"""

from app.trend_fetcher import get_google_trends, get_x_trends, get_upcoming_events, get_all_trends

def test_trends():
    print("=" * 60)
    print("TESTING TREND FETCHER")
    print("=" * 60)
    
    # Test 1: X/Twitter Trends
    print("\n1. Testing X/Twitter Trends...")
    x_trends = get_x_trends()
    if x_trends:
        print(f"   ✓ Found {len(x_trends)} X trends")
        print(f"   Sample: {x_trends[:5]}")
    else:
        print("   ✗ No X trends found")
    
    # Test 2: Upcoming Events
    print("\n2. Testing Upcoming Events...")
    events = get_upcoming_events(days=30)
    if events:
        print(f"   ✓ Found {len(events)} upcoming events")
        print(f"   Events: {events}")
    else:
        print("   ✗ No upcoming events found")
    
    # Test 3: Google Trends (expected to fail)
    print("\n3. Testing Google Trends (may fail)...")
    google_trends = get_google_trends()
    if google_trends:
        print(f"   ✓ Found {len(google_trends)} Google trends")
        print(f"   Sample: {google_trends[:5]}")
    else:
        print("   ⚠ Google Trends returned empty (expected)")
    
    # Test 4: All Trends Combined
    print("\n4. Testing Combined Trends...")
    all_trends = get_all_trends()
    if all_trends:
        print(f"   ✓ Found {len(all_trends)} total trends")
        print(f"   First 10 trends:")
        for i, trend in enumerate(all_trends[:10], 1):
            print(f"      {i}. {trend}")
    else:
        print("   ✗ No trends found at all")
    
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"X Trends: {'✓ Working' if x_trends else '✗ Not working'}")
    print(f"Events: {'✓ Working' if events else '✗ Not working'}")
    print(f"Google Trends: {'✓ Working' if google_trends else '⚠ Not working (expected)'}")
    print(f"Combined: {'✓ Working' if all_trends else '✗ Not working'}")
    
    return len(all_trends) > 0

if __name__ == "__main__":
    success = test_trends()
    exit(0 if success else 1)

