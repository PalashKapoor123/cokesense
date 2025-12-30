import requests
import urllib.parse
import random
import time
from .config import openai_client, IMAGE_MODEL

# Base visual instructions for Coca-Cola "Real Magic" style
BASE_VISUAL_PROMPT = """
Create a Coca-Cola inspired advertisement in the 'Real Magic' style.

Guidelines:
- Dominant Coca-Cola red and white color palette.
- Joyful, uplifting, human-centric moment.
- Emphasize connection, celebration, and refreshment.
- Show a realistic Coca-Cola bottle or can prominently and clearly.
- Soft glow, subtle sparkles, and a magical, cinematic atmosphere.
- Photorealistic or high-quality cinematic style.
- Avoid modifying or distorting the Coca-Cola logo or typography.
- Avoid any political, violent, or controversial imagery.
"""


def build_dalle_prompt(trend: str, moodboard: str) -> str:
    """
    Creates a HIGHLY PERSONALIZED image prompt specific to the trend.
    The prompt is designed to generate images that are unmistakably about this specific trend.
    """
    trend_lower = trend.lower()
    
    # Build trend-specific visual scene description
    trend_scene = _build_trend_specific_scene(trend, trend_lower, moodboard)
    
    return f"""{BASE_VISUAL_PROMPT}

CRITICAL: This image is specifically for {trend}. Every visual element must directly relate to {trend}.

TREND-SPECIFIC VISUAL SCENE:
{trend_scene}

MOODBOARD VISUAL ELEMENTS:
{moodboard}

COMPOSITION REQUIREMENTS:
- The scene must be unmistakably about {trend} - anyone looking at the image should immediately recognize it's about {trend}
- Include specific objects, settings, colors, and people that are directly associated with {trend}
- Show the unique atmosphere, energy, and emotions of {trend}
- Make it feel authentic and genuine to {trend}, not generic or vague
- The Coca-Cola bottle/can should be naturally integrated into the {trend} scene

TECHNICAL SPECS:
- Square format (1024x1024)
- Digital poster style for social media and OOH
- Cinematic, photorealistic quality
- High contrast, vibrant colors
""".strip()


def _build_trend_specific_scene(trend: str, trend_lower: str, moodboard: str) -> str:
    """
    Builds a highly specific visual scene description based on the trend.
    """
    # Sports trends
    if any(word in trend_lower for word in ["super bowl", "nfl", "football", "sports", "game", "championship", "olympics", "wimbledon", "tennis", "basketball", "soccer"]):
        return f"""A vibrant scene capturing the essence of {trend}: Fans gathered together, wearing team colors or {trend}-themed apparel, cheering and celebrating. Stadium or viewing party atmosphere with {trend} branding visible. People sharing Coca-Cola bottles while watching or celebrating {trend}. The energy is electric, with high-fives, hugs, and shared excitement. Include specific {trend} elements like footballs, trophies, scoreboards, or {trend}-specific decorations."""
    
    # Entertainment/Music trends
    elif any(word in trend_lower for word in ["coachella", "festival", "concert", "music", "grammy", "oscar", "award", "movie", "film", "show", "concert", "tour"]):
        return f"""A dynamic scene celebrating {trend}: People gathered at a {trend} event or watching {trend} together. Friends sharing reactions, dancing, or experiencing {trend} moments. Include {trend}-specific elements like stages, screens, red carpets, musical instruments, or {trend} branding. The atmosphere is energetic and celebratory, with people connecting over shared love of {trend} while enjoying Coca-Cola."""
    
    # Holiday trends
    elif any(word in trend_lower for word in ["christmas", "valentine", "easter", "halloween", "thanksgiving", "new year", "holiday", "hanukkah", "diwali", "ramadan"]):
        return f"""A heartwarming scene during {trend}: People celebrating {trend} traditions together. Include {trend}-specific decorations, colors, and symbols. Families or friends gathered, sharing {trend} moments and Coca-Cola. The atmosphere is warm, joyful, and filled with {trend} spirit. Show authentic {trend} elements like decorations, food, or {trend}-specific activities."""
    
    # Cultural/Social trends
    elif any(word in trend_lower for word in ["pride", "mardi gras", "carnival", "cultural", "heritage", "tradition"]):
        return f"""A vibrant celebration of {trend}: Diverse groups of people coming together to celebrate {trend}. Colorful {trend}-themed decorations, costumes, or symbols. People sharing joy, connection, and Coca-Cola during {trend} festivities. The scene captures the inclusive, celebratory spirit of {trend}."""
    
    # Shopping trends
    elif any(word in trend_lower for word in ["black friday", "cyber monday", "shopping", "sale"]):
        return f"""An energetic scene during {trend}: People shopping, finding deals, and celebrating {trend} together. Shopping bags, {trend} signage, and people sharing the excitement of {trend} while enjoying Coca-Cola. The atmosphere is bustling and joyful."""
    
    # Technology/Tech trends
    elif any(word in trend_lower for word in ["tech", "innovation", "ai", "digital", "gaming", "streaming"]):
        return f"""A modern scene featuring {trend}: People engaging with {trend} technology or content together. Screens, devices, or {trend}-related elements visible. Friends sharing the {trend} experience while enjoying Coca-Cola. The atmosphere is contemporary and connected."""
    
    # Food/Dining trends
    elif any(word in trend_lower for word in ["food", "dining", "restaurant", "cuisine", "cooking"]):
        return f"""A social dining scene around {trend}: People gathered around tables, sharing {trend} food and Coca-Cola. The atmosphere is warm and convivial, with {trend}-specific dishes or settings visible. Friends and family connecting over {trend}."""
    
    # Travel trends
    elif any(word in trend_lower for word in ["travel", "vacation", "beach", "adventure", "explore"]):
        return f"""A scenic travel moment inspired by {trend}: People experiencing {trend} destinations together, sharing adventures and Coca-Cola. Beautiful {trend}-specific locations, landmarks, or settings. The atmosphere is adventurous and joyful."""
    
    # Default - use moodboard to create specific scene
    else:
        # Extract key visual words from moodboard
        moodboard_words = [w.strip() for w in moodboard.split(",") if len(w.strip()) > 3]
        key_elements = ", ".join(moodboard_words[:5]) if moodboard_words else "celebration and connection"
        
        return f"""A specific scene celebrating {trend}: People gathered together, experiencing {trend} in an authentic way. Include {trend}-specific elements, settings, and details that make it unmistakably about {trend}. The scene features {key_elements}. People are sharing Coca-Cola while engaging with {trend}, creating genuine moments of connection and joy."""


def _optimize_prompt_for_pollinations(full_prompt: str) -> str:
    """
    Optimizes the prompt for Pollinations.ai by extracting key visual elements
    and creating a highly detailed, trend-specific prompt.
    Uses advanced prompt engineering techniques for better results.
    """
    # Extract trend name
    trend = ""
    if "specifically for" in full_prompt.lower():
        parts = full_prompt.split("specifically for")
        if len(parts) > 1:
            trend = parts[1].split(".")[0].strip()
    
    # Extract scene description (the most important part)
    scene_start = full_prompt.find("TREND-SPECIFIC VISUAL SCENE:")
    scene_end = full_prompt.find("MOODBOARD VISUAL ELEMENTS:")
    if scene_start > 0 and scene_end > 0:
        scene = full_prompt[scene_start:scene_end].replace("TREND-SPECIFIC VISUAL SCENE:", "").strip()
    else:
        scene = ""
    
    # Extract moodboard
    moodboard_start = full_prompt.find("MOODBOARD VISUAL ELEMENTS:")
    moodboard_end = full_prompt.find("COMPOSITION REQUIREMENTS:")
    if moodboard_start > 0 and moodboard_end > 0:
        moodboard = full_prompt[moodboard_start:moodboard_end].replace("MOODBOARD VISUAL ELEMENTS:", "").strip()
    else:
        moodboard = ""
    
    # Build highly optimized prompt with better structure
    # Use prompt engineering: subject + details + style + quality
    optimized_parts = [
        f"Coca-Cola advertisement featuring {trend}",
        scene,
        moodboard,
        "photorealistic, cinematic lighting, 8k quality, professional photography",
        "Coca-Cola red (#F40009) and white color scheme",
        "joyful atmosphere, human connection, celebration",
        "trending on artstation, highly detailed, sharp focus"
    ]
    
    optimized = ", ".join([p for p in optimized_parts if p])
    
    # Limit length but prioritize trend-specific content
    if len(optimized) > 600:
        # Keep trend name and scene, trim the rest
        trend_part = f"Coca-Cola advertisement featuring {trend}, {scene}"
        remaining = optimized[len(trend_part):]
        if len(trend_part) + len(remaining) > 600:
            remaining = remaining[:600-len(trend_part)]
        optimized = trend_part + remaining
    
    return optimized


def generate_image_url_pollinations(prompt: str) -> str:
    """
    Generates image using Pollinations.ai (FREE, no API key needed).
    Returns the image URL with a unique seed to ensure different images each time.
    Always returns a URL (even if Pollinations is down, returns a placeholder URL).
    """
    try:
        # Pollinations.ai free API - no key needed!
        base_url = "https://image.pollinations.ai/prompt/"
        
        # Optimize prompt for Pollinations (more concise, trend-focused)
        optimized_prompt = _optimize_prompt_for_pollinations(prompt)
        
        # Encode the prompt
        encoded_prompt = urllib.parse.quote(optimized_prompt)
        
        # Generate a random seed to ensure unique images each time
        # Using timestamp + random number for better uniqueness
        random_seed = int(time.time() * 1000) + random.randint(1, 10000)
        
        # Build URL with parameters
        # model=flux for high quality, width/height for square format
        # seed=random_seed ensures different images each time (not cached)
        image_url = f"{base_url}{encoded_prompt}?model=flux&width=1024&height=1024&seed={random_seed}"
        
        # Pollinations generates images on-demand, so we return the URL directly
        # The image will be generated when the URL is accessed
        # If Pollinations is down, the GIF fallback will create a placeholder
        return image_url
            
    except Exception as e:
        print(f"Error generating image with Pollinations: {e}")
        # Return a placeholder URL that will trigger the GIF fallback
        # This ensures we always have something to work with
        return "https://placeholder.pollinations.ai/1024x1024/F40009/FFFFFF?text=Coca-Cola"


def generate_image_url(prompt: str) -> str:
    """
    Generates an image URL using available services.
    Priority: OpenAI DALL-E (if available, paid) > Enhanced Pollinations.ai (FREE)
    
    NOTE: By default, uses Pollinations.ai which is 100% FREE.
    Only uses OpenAI DALL-E if you have an OpenAI API key (paid).
    """
    # Try OpenAI DALL-E first (best quality, but PAID - requires API key)
    if openai_client:
        try:
            result = openai_client.images.generate(
                model=IMAGE_MODEL,
                prompt=prompt,
                size="1024x1024",
            )
            return result.data[0].url
        except Exception as e:
            print(f"OpenAI DALL-E error: {e}, using free alternative...")
    
    # Use enhanced Pollinations.ai (100% FREE, improved prompts for better personalization)
    return generate_image_url_pollinations(prompt)


def build_video_prompt(trend: str, moodboard: str, campaign_concept: str = "") -> str:
    """
    Creates a video prompt optimized for AI video generation.
    Videos work best with dynamic, action-oriented descriptions.
    """
    trend_lower = trend.lower()
    
    # Build dynamic scene description for video
    if any(word in trend_lower for word in ["super bowl", "nfl", "football", "sports", "game", "championship"]):
        video_scene = f"Dynamic scene: Fans celebrating {trend}, cheering, high-fives, people sharing Coca-Cola bottles. Camera moves through the crowd, capturing joyful moments. Stadium atmosphere with {trend} energy."
    elif any(word in trend_lower for word in ["coachella", "festival", "concert", "music"]):
        video_scene = f"Energetic scene: People at {trend}, dancing, music playing, friends sharing Coca-Cola. Camera follows the celebration, capturing the vibrant {trend} atmosphere."
    elif any(word in trend_lower for word in ["christmas", "valentine", "easter", "holiday"]):
        video_scene = f"Heartwarming scene: Families celebrating {trend} together, sharing moments and Coca-Cola. Warm, joyful atmosphere with {trend} decorations visible."
    else:
        video_scene = f"Celebratory scene: People gathered for {trend}, sharing joy and Coca-Cola. Dynamic, uplifting atmosphere capturing the essence of {trend}."
    
    # Optimize for video generation (shorter, action-focused)
    optimized_parts = [
        f"Coca-Cola advertisement video: {trend}",
        video_scene,
        "smooth camera movement, cinematic, professional",
        "Coca-Cola red and white colors",
        "joyful, energetic, human connection"
    ]
    
    return ", ".join([p for p in optimized_parts if p])


def generate_video_url_huggingface(image_url: str) -> str | None:
    """
    Generates video using Hugging Face's free Stable Video Diffusion API.
    Uses image-to-video: takes the generated image and creates a short animated video (3-5 seconds).
    
    Free tier: ~30 requests/hour, perfect for testing!
    """
    try:
        # Download the image first
        print(f"Downloading image from {image_url[:50]}...")
        img_response = requests.get(image_url, timeout=60)
        if img_response.status_code != 200:
            print(f"Failed to download image: {img_response.status_code}")
            return None
        
        image_data = img_response.content
        
        # Determine image format from content or URL
        content_type = "image/png"  # Default
        # Check URL extension
        if image_url.lower().endswith(('.jpg', '.jpeg')):
            content_type = "image/jpeg"
        # Check actual image content (more reliable)
        elif img_response.headers.get('content-type', '').startswith('image/jpeg'):
            content_type = "image/jpeg"
        elif img_response.headers.get('content-type', '').startswith('image/png'):
            content_type = "image/png"
        
        # Hugging Face Stable Video Diffusion model (image-to-video)
        # This model takes an image and creates a short video from it
        # Note: Model name might need to be updated - using the most common one
        hf_api_url = "https://api-inference.huggingface.co/models/stabilityai/stable-video-diffusion-img2vid-xt"
        
        # Hugging Face free tier - no auth required for public models
        # But the API expects the image in the request body, not as Content-Type header
        # Actually, we should send it as binary data
        headers = {}  # Hugging Face API handles image format automatically
        
        # Send image to Hugging Face API
        # Note: First request may take longer as model loads (cold start ~30-60s)
        # Hugging Face API expects the image as binary data in the request body
        print("Sending image to Hugging Face for video generation...")
        try:
            response = requests.post(
                hf_api_url,
                headers=headers,
                data=image_data,
                timeout=180  # Video generation can take 60-120 seconds
            )
        except requests.exceptions.RequestException as e:
            print(f"Request exception: {e}")
            return None
        
        if response.status_code == 200:
            # Success! Save the video
            import tempfile
            
            # Create a temporary file for the video
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
                tmp_file.write(response.content)
                video_path = tmp_file.name
            
            print(f"Video generated successfully: {video_path}")
            # Return the file path - Streamlit can display local video files
            return video_path
            
        elif response.status_code == 503:
            # Model is loading (cold start) - this is normal for free tier
            try:
                error_data = response.json()
                estimated_time = error_data.get("estimated_time", 30)
                print(f"Model is loading, estimated wait: {estimated_time} seconds")
                # Return a special indicator that we need to wait
                return f"LOADING:{estimated_time}"
            except:
                return "LOADING:30"  # Default wait time
            
        elif response.status_code == 429:
            # Rate limit exceeded
            print("Rate limit exceeded - free tier has limits")
            return None
            
        else:
            # Other error
            try:
                error_data = response.json()
                error_text = str(error_data)
            except:
                error_text = response.text
            print(f"Hugging Face API error ({response.status_code}): {error_text[:200]}")
            return None
            
    except requests.exceptions.Timeout:
        print("Hugging Face API timeout - video generation takes time (up to 2 minutes)")
        return None
    except Exception as e:
        print(f"Error generating video with Hugging Face: {e}")
        import traceback
        traceback.print_exc()
        return None


def generate_animated_gif_fallback(image_url: str) -> str | None:
    """
    Fallback: Creates a simple animated GIF from the image.
    This ensures we always have video output even if external APIs fail.
    
    Creates a subtle animation with zoom/pan effects - perfect for social media!
    """
    try:
        from PIL import Image, ImageEnhance, ImageDraw, ImageFont
        import tempfile
        import io
        
        # Download the image with retry
        print("Creating animated GIF from image...")
        img_response = None
        for attempt in range(2):  # Try 2 times
            try:
                img_response = requests.get(image_url, timeout=30)
                if img_response.status_code == 200:
                    break
            except Exception as e:
                print(f"  Download attempt {attempt + 1} failed: {e}")
                if attempt < 1:
                    import time
                    time.sleep(1)
        
        # If download failed, create a placeholder image
        if not img_response or img_response.status_code != 200:
            print("  ⚠️ Image download failed, creating placeholder image...")
            # Create a simple placeholder with Coca-Cola branding
            placeholder = Image.new('RGB', (1024, 1024), color='#F40009')  # Coca-Cola red
            draw = ImageDraw.Draw(placeholder)
            # Add text
            try:
                # Try to use a larger font
                font_size = 80
                from PIL import ImageFont
                try:
                    font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
                except:
                    font = ImageFont.load_default()
                text = "Coca-Cola"
                bbox = draw.textbbox((0, 0), text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                position = ((1024 - text_width) // 2, (1024 - text_height) // 2)
                draw.text(position, text, fill='white', font=font)
            except:
                # If font fails, just draw a simple rectangle
                draw.rectangle([200, 400, 824, 624], fill='white', outline='white', width=5)
            
            # Use the placeholder directly
            image = placeholder
        else:
            # Open the downloaded image
            image = Image.open(io.BytesIO(img_response.content))
        
        # Convert to RGB if needed (GIFs need RGB)
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Resize if too large (GIFs work better at reasonable sizes)
        max_size = 1024
        if image.width > max_size or image.height > max_size:
            image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
        
        # Create frames for animation (subtle zoom/pan effect)
        frames = []
        num_frames = 20  # 20 frames for smooth animation
        duration = 100  # 100ms per frame = 2 seconds total
        
        # Create subtle animation: slight zoom in + brightness pulse
        for i in range(num_frames):
            # Calculate zoom factor (1.0 to 1.1)
            zoom = 1.0 + (0.1 * i / num_frames)
            
            # Calculate crop box (center crop with zoom)
            width, height = image.size
            new_width = int(width / zoom)
            new_height = int(height / zoom)
            left = (width - new_width) // 2
            top = (height - new_height) // 2
            
            # Crop and resize back to original size
            frame = image.crop((left, top, left + new_width, top + new_height))
            frame = frame.resize((width, height), Image.Resampling.LANCZOS)
            
            # Add subtle brightness pulse (1.0 to 1.15)
            brightness_factor = 1.0 + (0.15 * (0.5 + 0.5 * (i / num_frames)))
            enhancer = ImageEnhance.Brightness(frame)
            frame = enhancer.enhance(brightness_factor)
            
            frames.append(frame)
        
        # Create reverse frames for smooth loop (zoom out)
        for i in range(num_frames - 2, 0, -1):
            zoom = 1.0 + (0.1 * i / num_frames)
            width, height = image.size
            new_width = int(width / zoom)
            new_height = int(height / zoom)
            left = (width - new_width) // 2
            top = (height - new_height) // 2
            
            frame = image.crop((left, top, left + new_width, top + new_height))
            frame = frame.resize((width, height), Image.Resampling.LANCZOS)
            
            brightness_factor = 1.0 + (0.15 * (0.5 + 0.5 * (i / num_frames)))
            enhancer = ImageEnhance.Brightness(frame)
            frame = enhancer.enhance(brightness_factor)
            
            frames.append(frame)
        
        # Save as animated GIF
        with tempfile.NamedTemporaryFile(delete=False, suffix='.gif') as tmp_file:
            frames[0].save(
                tmp_file.name,
                save_all=True,
                append_images=frames[1:],
                duration=duration,
                loop=0,  # Infinite loop
                optimize=True
            )
            gif_path = tmp_file.name
        
        print(f"Animated GIF created: {gif_path}")
        return gif_path
        
    except ImportError:
        print("PIL/Pillow not installed - cannot create GIF fallback")
        return None
    except Exception as e:
        print(f"Error creating animated GIF: {e}")
        import traceback
        traceback.print_exc()
        return None


def generate_video_url(prompt: str, image_url: str = None) -> str | None:
    """
    Generates a video using Hugging Face's free Stable Video Diffusion API.
    Takes the generated image and creates a short animated video (3-5 seconds).
    
    If Hugging Face fails, falls back to creating an animated GIF from the image.
    
    Free tier: ~30 requests/hour - perfect for testing!
    """
    if not image_url:
        print("No image URL provided for video generation")
        return None
    
    # Try Hugging Face's free image-to-video API first
    video_result = generate_video_url_huggingface(image_url)
    
    # If Hugging Face fails or returns loading state, use GIF fallback
    if not video_result or video_result.startswith("LOADING:"):
        print("Hugging Face unavailable, using animated GIF fallback...")
        return generate_animated_gif_fallback(image_url)
    
    return video_result
