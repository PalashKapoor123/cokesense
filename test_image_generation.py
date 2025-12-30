#!/usr/bin/env python3
"""
Quick test script for image and GIF generation
"""
import sys
from app.visual_engine import generate_image_url, generate_animated_gif_fallback

print("🧪 Testing Image Generation...")
print("=" * 50)

# Test 1: Generate an image
test_prompt = "Coca-Cola advertisement featuring Christmas, people celebrating together, joyful atmosphere, red and white colors"
print(f"\n1️⃣ Testing image generation with prompt:")
print(f"   '{test_prompt[:60]}...'")

try:
    image_url = generate_image_url(test_prompt)
    if image_url:
        print(f"✅ Image URL generated: {image_url[:80]}...")
        
        # Test 2: Download the image
        print(f"\n2️⃣ Testing image download...")
        import requests
        try:
            response = requests.get(image_url, timeout=60)
            if response.status_code == 200:
                print(f"✅ Image downloaded successfully! Size: {len(response.content)} bytes")
                
                # Test 3: Create GIF from image
                print(f"\n3️⃣ Testing GIF generation...")
                gif_path = generate_animated_gif_fallback(image_url)
                if gif_path:
                    import os
                    if os.path.exists(gif_path):
                        size = os.path.getsize(gif_path)
                        print(f"✅ GIF created successfully! Path: {gif_path}")
                        print(f"   Size: {size:,} bytes")
                    else:
                        print(f"❌ GIF path doesn't exist: {gif_path}")
                else:
                    print(f"❌ GIF generation returned None")
            else:
                print(f"❌ Image download failed! Status code: {response.status_code}")
        except Exception as e:
            print(f"❌ Image download error: {e}")
            import traceback
            traceback.print_exc()
    else:
        print(f"❌ Image generation returned None")
except Exception as e:
    print(f"❌ Image generation error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 50)
print("Test complete!")

