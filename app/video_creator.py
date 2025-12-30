"""
Video Creation Module - Combines images and audio into videos for Instagram
"""
from io import BytesIO
import requests
import tempfile
import os
from PIL import Image


def create_video_with_audio(image_url: str, audio_bytes: bytes, duration: float = None, gif_path: str = None) -> str:
    """
    Creates a video by combining an image/GIF with audio.
    If a GIF is provided, it will be used instead of the static image for a more dynamic video.
    
    Args:
        image_url: URL of the image to use (fallback if no GIF)
        audio_bytes: Audio file as bytes (MP3)
        duration: Duration of video in seconds (default: audio length)
        gif_path: Optional path to a GIF file (will be used instead of image if provided)
    
    Returns:
        Path to the created video file
    """
    try:
        # Try new import structure (moviepy 2.x)
        try:
            from moviepy import ImageClip, AudioFileClip, CompositeVideoClip, VideoFileClip, concatenate_videoclips
        except ImportError:
            # Fall back to old import structure (moviepy 1.x)
            from moviepy.editor import ImageClip, AudioFileClip, CompositeVideoClip, VideoFileClip, concatenate_videoclips
    except ImportError as e:
        raise ImportError(f"moviepy not installed. Install with: pip install moviepy. Error: {e}")
    
    try:
        # Use GIF if provided, otherwise use image
        use_gif = gif_path and os.path.exists(gif_path)
        
        if use_gif:
            # Use the GIF file directly
            media_path = gif_path
            print(f"Using animated GIF: {gif_path}")
        else:
            # Download image
            img_response = requests.get(image_url, timeout=30)
            if img_response.status_code != 200:
                raise Exception(f"Failed to download image: {img_response.status_code}")
            
            # Save image temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as img_file:
                img_file.write(img_response.content)
                media_path = img_file.name
        
        # Save audio temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as audio_file:
            audio_file.write(audio_bytes)
            audio_path = audio_file.name
        
        try:
            # Load audio to get duration
            audio_clip = AudioFileClip(audio_path)
            audio_duration = audio_clip.duration
            
            # Video duration MUST match audio duration exactly
            # If we try to make video longer than audio, MoviePy will error
            # Use provided duration only if it's shorter than or equal to audio
            if duration and duration <= audio_duration:
                video_duration = duration
            else:
                video_duration = audio_duration  # Always use audio duration as the limit
            
            # Ensure reasonable bounds (but never exceed audio duration)
            # Minimum 0.5 seconds, maximum 60 seconds (Instagram limits)
            video_duration = max(0.5, min(60, video_duration))
            
            # Final check: video duration cannot exceed audio duration
            video_duration = min(video_duration, audio_duration)
            
            # Create clip from GIF or image
            if use_gif:
                # Load GIF as video clip (GIFs are already animated)
                image_clip = VideoFileClip(media_path)
                gif_duration = image_clip.duration
                
                # If GIF is shorter than audio, loop it to match audio duration
                # If GIF is longer, trim it to audio duration
                if gif_duration < audio_duration:
                    # Loop the GIF to match audio length
                    num_loops = int(audio_duration / gif_duration) + 1
                    from moviepy import concatenate_videoclips
                    image_clip = concatenate_videoclips([image_clip] * num_loops)
                    # Trim to exact audio duration
                    image_clip = image_clip.with_duration(audio_duration)
                    video_duration = audio_duration
                else:
                    # GIF is longer, trim to audio duration
                    image_clip = image_clip.with_duration(audio_duration)
                    video_duration = audio_duration
                # Don't resize GIF - keep its original animation
            else:
                # Create static image clip
                image_clip = ImageClip(media_path, duration=video_duration)
                
                # Resize image to Instagram-friendly size (square, 1080x1080 recommended)
                target_size = (1080, 1080)
                image_clip = image_clip.resized(target_size)
            
            # Set FPS (required for video)
            image_clip = image_clip.with_fps(30)
            
            # Combine image/GIF with audio
            final_video = CompositeVideoClip([image_clip]).with_audio(audio_clip)
            # Match duration to audio (or GIF if shorter)
            final_video = final_video.with_duration(video_duration)
            
            # Create output video file
            output_path = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4').name
            final_video.write_videofile(
                output_path,
                fps=30,
                codec='libx264',
                audio_codec='aac',
                temp_audiofile=tempfile.NamedTemporaryFile(delete=False, suffix='.m4a').name,
                remove_temp=True,
                logger=None
            )
            
            # Cleanup
            audio_clip.close()
            final_video.close()
            image_clip.close()
            # Only delete if we created a temp file (not if we used provided GIF)
            if not use_gif:
                os.unlink(media_path)
            os.unlink(audio_path)
            
            return output_path
            
        except Exception as e:
            # Cleanup on error
            if not use_gif and os.path.exists(media_path):
                os.unlink(media_path)
            if os.path.exists(audio_path):
                os.unlink(audio_path)
            raise e
            
    except Exception as e:
        print(f"Error creating video: {e}")
        raise e

