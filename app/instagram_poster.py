"""
Instagram posting functionality for CokeSense campaigns.
Uses Instagram Graph API to post images with captions.
"""

import requests
import os
import time
from typing import Optional


def post_to_instagram(
    image_url: str,
    caption: str,
    access_token: str,
    trend: str = None,
    audio_bytes: bytes = None,
    gif_path: str = None
) -> dict:
    """
    Posts an image to Instagram using the Graph API.
    
    Args:
        image_url: URL of the image to post
        caption: Caption text for the post
        access_token: Instagram access token
    
    Returns:
        dict with success status and post ID or error message
    """
    try:
        # Step 1: Get Instagram Business Account ID
        # The token should give us access to the Instagram account
        user_url = f"https://graph.instagram.com/me?fields=id,username&access_token={access_token}"
        user_response = requests.get(user_url)
        
        if user_response.status_code != 200:
            error_text = user_response.text
            return {
                "success": False,
                "error": f"Failed to get user info (Status {user_response.status_code}): {error_text}. Check if token is valid and has correct permissions."
            }
        
        user_data = user_response.json()
        account_id = user_data.get("id")
        username = user_data.get("username", "Unknown")
        
        if not account_id:
            return {
                "success": False,
                "error": "Could not get Instagram account ID from token response"
            }
        
        # Step 2: Create video with audio if audio provided, otherwise use image
        video_path = None
        created_video_path = None
        
        if audio_bytes:
            try:
                from .video_creator import create_video_with_audio
                print(f"🎬 Attempting to create video with audio...")
                # Use GIF if available, otherwise use static image
                video_path = create_video_with_audio(image_url, audio_bytes, gif_path=gif_path)
                created_video_path = video_path  # Store for download
                media_type = "animated GIF" if gif_path else "image"
                print(f"✅ Successfully created video with audio from {media_type}: {video_path}")
            except Exception as e:
                print(f"⚠️ Could not create video with audio: {e}")
                print(f"   Error type: {type(e).__name__}")
                import traceback
                print(f"   Traceback: {traceback.format_exc()}")
                # Fall back to image posting if video creation fails
                video_path = None
                created_video_path = None
        
        # Step 3: Create media container
        # Note: Instagram Graph API requires videos to be at a public URL
        # We can't upload files directly, so we'll post the image and provide video for download
        media_url = f"https://graph.instagram.com/{account_id}/media"
        
        # Post as image (original behavior or fallback)
        # Check if image URL is accessible
        try:
            image_check = requests.head(image_url, timeout=5, allow_redirects=True)
            if image_check.status_code != 200:
                return {
                    "success": False,
                    "error": f"Image URL is not accessible (Status {image_check.status_code}). Instagram requires publicly accessible image URLs."
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"Cannot access image URL: {str(e)}. Make sure the image URL is publicly accessible."
            }
        
        # Create media container with image URL and caption
        media_params = {
            "image_url": image_url,
            "caption": caption[:2200],  # Instagram caption limit is 2200 characters
            "access_token": access_token
        }
        
        media_response = requests.post(media_url, data=media_params)
        
        if media_response.status_code != 200:
            error_text = media_response.text
            return {
                "success": False,
                "error": f"Failed to create media container (Status {media_response.status_code}): {error_text}. Make sure token has 'instagram_content_publish' permission."
            }
        
        media_data = media_response.json()
        creation_id = media_data.get("id")
        
        if not creation_id:
            return {
                "success": False,
                "error": f"Could not get creation ID. Response: {media_data}"
            }
        
        # Step 4: Wait for media to be ready, then publish
        # Instagram needs time to process the image from the URL
        max_retries = 15  # Try for up to 45 seconds (Instagram can be slow)
        retry_delay = 3   # Wait 3 seconds between retries
        
        for attempt in range(max_retries):
            # Try to publish - Instagram will tell us if it's ready
            publish_url = f"https://graph.instagram.com/{account_id}/media_publish"
            publish_params = {
                "creation_id": creation_id,
                "access_token": access_token
            }
            
            publish_response = requests.post(publish_url, data=publish_params)
            
            if publish_response.status_code == 200:
                publish_data = publish_response.json()
                post_id = publish_data.get("id")
                
                # Save post to history
                try:
                    from .post_history import save_post
                    save_post(
                        post_id=post_id,
                        trend=trend if trend else "Unknown",
                        caption=caption[:200],  # Truncate for storage
                        image_url=image_url
                    )
                except Exception as e:
                    print(f"Note: Could not save post to history: {e}")
                
                result = {
                    "success": True,
                    "post_id": post_id,
                    "message": f"Successfully posted to Instagram (@{username})!"
                }
                
                # Add video path if video was created
                if created_video_path:
                    result["video_path"] = created_video_path
                    result["video_created"] = True
                    result["message"] += " (Video with audio created - see download option)"
                
                return result
            else:
                # Check the error
                try:
                    error_data = publish_response.json()
                    error_code = error_data.get("error", {}).get("code")
                    error_subcode = error_data.get("error", {}).get("error_subcode")
                    
                    # Error code 9007 with subcode 2207027 means "not ready yet"
                    if error_code == 9007 and error_subcode == 2207027:
                        # Still processing, wait and retry
                        if attempt < max_retries - 1:
                            time.sleep(retry_delay)
                            continue
                        else:
                            return {
                                "success": False,
                                "error": f"Media still processing after {max_retries * retry_delay} seconds. Instagram is downloading/processing the image. This can take up to 60 seconds. Please try again in a moment."
                            }
                    else:
                        # Different error - return it
                        error_text = publish_response.text
                        return {
                            "success": False,
                            "error": f"Failed to publish (Status {publish_response.status_code}): {error_text}"
                        }
                except:
                    # If we can't parse the error, return the raw response
                    error_text = publish_response.text
                    return {
                        "success": False,
                        "error": f"Failed to publish (Status {publish_response.status_code}): {error_text}"
                    }
        
        # If we get here, we exhausted all retries
        return {
            "success": False,
            "error": f"Media container created but not ready after {max_retries * retry_delay} seconds. Instagram may still be processing the image. Please wait a moment and try posting again."
        }
            
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": f"Network error: {str(e)}. Check your internet connection."
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Error posting to Instagram: {str(e)}"
        }


def format_campaign_caption(
    hero_concept: str,
    slogan: str,
    social_post: str,
    trend: str
) -> str:
    """
    Formats the campaign content into an Instagram caption.
    Creates a concise, social media-friendly caption.
    """
    # Clean up trend name for hashtag (remove spaces, special chars)
    trend_hashtag = trend.replace(" ", "").replace("'", "").replace("-", "")
    
    # Build Instagram-friendly caption
    # Use social_post as the main content (it's already optimized for social)
    # Add slogan as a highlight
    # Skip the long hero_concept narrative - it's too script-like for Instagram
    
    caption_parts = [
        f"🎨 {slogan}",
        "",
        social_post,  # This is already optimized for social media
        "",
        f"✨ Celebrating {trend} with Real Magic moments",
        "",
        f"#CocaCola #RealMagic #CokeSense #{trend_hashtag} #Marketing #AICreative"
    ]
    
    return "\n".join(caption_parts)


def get_instagram_auth_url(client_id: str, redirect_uri: str) -> str:
    """
    Generates Instagram OAuth authorization URL.
    User needs to visit this URL to authorize the app.
    """
    scopes = "user_profile,user_media"
    auth_url = (
        f"https://api.instagram.com/oauth/authorize"
        f"?client_id={client_id}"
        f"&redirect_uri={redirect_uri}"
        f"&scope={scopes}"
        f"&response_type=code"
    )
    return auth_url

