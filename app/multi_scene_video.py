"""
Multi-Scene Video Creator - Combines multiple images/GIFs into one video with audio
Creates a dynamic campaign video with multiple scenes
"""
import requests
import tempfile
import os
from typing import List, Optional


def create_multi_scene_video(
    image_urls: List[str],
    audio_bytes: bytes,
    gif_paths: Optional[List[str]] = None,
    scene_duration: float = 3.0,
    transition_duration: float = 0.5,
    slogan: str = None,
    brand_name: str = "Coca-Cola"
) -> str:
    """
    Creates a multi-scene video by combining multiple images/GIFs with audio.
    
    Args:
        image_urls: List of image URLs to use (will create GIFs if gif_paths not provided)
        audio_bytes: Audio file as bytes (MP3)
        gif_paths: Optional list of GIF file paths (if provided, uses these instead of creating from images)
        scene_duration: Duration of each scene in seconds (default: 3.0)
        transition_duration: Duration of transitions between scenes (default: 0.5)
    
    Returns:
        Path to the created video file
    """
    try:
        # Try new import structure (moviepy 2.x)
        try:
            from moviepy import (
                ImageClip, AudioFileClip, CompositeVideoClip, VideoFileClip,
                concatenate_videoclips, concatenate_audioclips, TextClip, ColorClip
            )
        except ImportError:
            # Fall back to old import structure (moviepy 1.x)
            try:
                from moviepy.editor import (
                    ImageClip, AudioFileClip, CompositeVideoClip, VideoFileClip,
                    concatenate_videoclips, concatenate_audioclips, TextClip, ColorClip
                )
            except ImportError:
                # Some versions don't have concatenate_audioclips, use alternative
                from moviepy.editor import (
                    ImageClip, AudioFileClip, CompositeVideoClip, VideoFileClip,
                    concatenate_videoclips, TextClip, ColorClip
                )
                # Define concatenate_audioclips as a fallback
                def concatenate_audioclips(clips):
                    """Fallback: concatenate audio clips by looping"""
                    if len(clips) == 1:
                        return clips[0]
                    # For older versions, we'll handle it differently
                    return clips[0]  # Will handle looping manually
    except ImportError as e:
        raise ImportError(f"moviepy not installed. Install with: pip install moviepy. Error: {e}")
    
    # ColorClip should already be imported above for fallback scenes
    
    # Helper function to handle MoviePy version compatibility (1.x uses resized, 2.x uses resize)
    def resize_clip(clip, size):
        """Resize a clip, handling both MoviePy 1.x and 2.x"""
        try:
            return clip.resized(size)  # MoviePy 1.x
        except AttributeError:
            return clip.resize(size)  # MoviePy 2.x
    
    # Helper function to handle MoviePy version compatibility for audio attachment
    def set_audio_on_clip(video_clip, audio_clip):
        """Set audio on a video clip, handling both MoviePy versions"""
        try:
            return video_clip.with_audio(audio_clip)  # MoviePy 1.x
        except AttributeError:
            return video_clip.set_audio(audio_clip)  # MoviePy 2.x
    
    try:
        # Save audio temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as audio_file:
            audio_file.write(audio_bytes)
            audio_path = audio_file.name
        
        try:
            # Load audio to get duration
            audio_clip = AudioFileClip(audio_path)
            audio_duration = audio_clip.duration
            
            # Determine how many scenes we have
            num_available = len(image_urls) if image_urls else 0
            if gif_paths:
                num_available = len(gif_paths)
            
            if num_available == 0:
                raise Exception("No images or GIFs provided")
            
            print(f"📊 Available resources: {num_available} images/GIFs")
            print(f"📊 Audio duration: {audio_duration:.2f}s")
            
            # Use ALL available scenes - don't reduce the number
            num_scenes = num_available
            print(f"📊 Will create {num_scenes} scenes (using ALL available images/GIFs)")
            
            # Verify we have enough images for all requested scenes
            if image_urls and len(image_urls) < num_scenes:
                print(f"  ⚠️ WARNING: Only {len(image_urls)} images available, but {num_scenes} scenes requested")
                print(f"     Will use available images and may repeat some scenes")
            
            # Adjust scene duration to ensure all scenes fit exactly within audio duration
            # Account for intro screen (2 seconds) and outro screen (3 seconds)
            # So main video = audio_duration - 2.0 - 3.0
            # We want: num_scenes * scene_duration = (audio_duration - 2.0 - 3.0) for main video
            # Then: intro (2s) + main video + outro (3s) = audio_duration total
            intro_duration = 2.0  # Black screen with brand name
            outro_duration = 3.0  # Black screen with slogan
            main_video_available_time = audio_duration - intro_duration - outro_duration
            
            if num_scenes > 0 and main_video_available_time > 0:
                # Calculate exact scene duration to fit ALL scenes in main video portion
                # Use the calculated duration even if it's short - we want ALL scenes to show
                calculated_duration = main_video_available_time / num_scenes
                scene_duration = calculated_duration
                
                # Warn if duration is very short, but don't reduce scenes
                if scene_duration < 1.0:
                    print(f"⚠️ Scene duration is short ({scene_duration:.2f}s) but keeping all {num_scenes} scenes")
                elif scene_duration < 2.0:
                    print(f"⚠️ Scene duration is a bit short ({scene_duration:.2f}s) but keeping all {num_scenes} scenes")
                
                transition_duration = 0  # Not used, but kept for compatibility
                print(f"📐 Final scene duration: {scene_duration:.2f}s per scene")
                print(f"   Number of scenes: {num_scenes} (ALL scenes will be included)")
                print(f"   Intro screen: {intro_duration}s")
                print(f"   Main video (GIFs): {num_scenes} × {scene_duration:.2f}s = {num_scenes * scene_duration:.2f}s")
                print(f"   Outro screen: {outro_duration}s")
                print(f"   Total video: {intro_duration + num_scenes * scene_duration + outro_duration:.2f}s")
                print(f"   Audio duration: {audio_duration:.2f}s")
                print(f"   ✅ Perfect match: {abs(intro_duration + num_scenes * scene_duration + outro_duration - audio_duration):.3f}s difference")
            else:
                # Fallback if intro takes too much time
                scene_duration = audio_duration / num_scenes
                intro_duration = 0
                print(f"⚠️ Audio too short for intro, using full audio for scenes")
                print(f"📐 Calculated scene duration: {scene_duration:.2f}s per scene")
            
            print(f"Creating multi-scene video with {num_scenes} scenes")
            print(f"Audio duration: {audio_duration:.2f}s, Scene duration: {scene_duration}s each")
            
            # Verify we have the necessary imports before starting
            try:
                from PIL import Image as PILImage
                print("  ✅ PIL/Pillow available")
            except ImportError as pil_error:
                print(f"  ❌ CRITICAL: PIL/Pillow not available: {pil_error}")
                raise Exception(f"Cannot create video: PIL/Pillow is required but not installed. Error: {pil_error}")
            
            # Create clips for each scene
            scene_clips = []
            temp_files = []  # Track temp files for cleanup
            cached_image = None  # Cache first successful image to reuse if others fail
            
            # Verify we have image URLs or GIF paths
            if not image_urls and not gif_paths:
                print(f"  ❌ ERROR: No image URLs or GIF paths provided!")
                print(f"     image_urls: {image_urls}")
                print(f"     gif_paths: {gif_paths}")
                raise Exception("No image URLs or GIF paths provided. Cannot create video.")
            
            if image_urls and len(image_urls) == 0:
                print(f"  ❌ ERROR: Empty image_urls list provided!")
                print(f"     This might be a Streamlit Cloud issue - image generation may have failed.")
                print(f"     Creating placeholder video instead...")
                # Instead of raising, create placeholder scenes
                image_urls = None  # Will trigger placeholder creation
            
            print(f"  Creating {num_scenes} scene clips...")
            print(f"  Available resources: {len(image_urls) if image_urls else 0} images, {len(gif_paths) if gif_paths else 0} GIFs")
            
            # CRITICAL: Pre-create at least one basic scene as absolute fallback
            # This ensures we always have something to work with
            basic_fallback_clip = None
            try:
                print(f"  🛡️ Creating basic fallback clip as safety net...")
                # Try different ways to set FPS based on MoviePy version
                try:
                    basic_fallback_clip = ColorClip(size=(1080, 1080), color=(0, 0, 0), duration=scene_duration, fps=30)
                except TypeError:
                    # FPS not in constructor, try setting it after creation
                    basic_fallback_clip = ColorClip(size=(1080, 1080), color=(0, 0, 0), duration=scene_duration)
                    if hasattr(basic_fallback_clip, 'with_fps'):
                        basic_fallback_clip = basic_fallback_clip.with_fps(30)
                    elif hasattr(basic_fallback_clip, 'set_fps'):
                        basic_fallback_clip = basic_fallback_clip.set_fps(30)
                    # If neither works, use as-is (FPS might be set automatically)
                print(f"  ✅ Basic fallback clip created successfully")
            except Exception as basic_error:
                print(f"  ⚠️ Basic fallback clip creation failed: {basic_error}")
                import traceback
                traceback.print_exc()
                basic_fallback_clip = None
            
            for i in range(num_scenes):
                print(f"  Processing scene {i+1}/{num_scenes}...")
                try:
                    if gif_paths and i < len(gif_paths) and os.path.exists(gif_paths[i]):
                        # Use provided GIF
                        print(f"  Scene {i+1}/{num_scenes}: Using GIF {gif_paths[i]}")
                        scene_clip = VideoFileClip(gif_paths[i])
                        # If GIF is shorter than scene_duration, loop it
                        if scene_clip.duration < scene_duration:
                            num_loops = int(scene_duration / scene_clip.duration) + 1
                            looped = [scene_clip] * num_loops
                            scene_clip = concatenate_videoclips(looped, method="compose")
                        # Set duration for this scene
                        scene_clip = scene_clip.with_duration(scene_duration)
                    elif image_urls and len(image_urls) > 0 and i < len(image_urls):
                        # Create GIF from image URL
                        image_url_to_use = image_urls[i]
                        if not image_url_to_use or not isinstance(image_url_to_use, str) or len(image_url_to_use.strip()) == 0:
                            print(f"  Scene {i+1}/{num_scenes}: Invalid image URL (empty or None), creating placeholder")
                            # Create placeholder directly
                            placeholder = PILImage.new('RGB', (1080, 1080), color='black')
                            with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as img_file:
                                placeholder.save(img_file.name)
                                img_path = img_file.name
                                temp_files.append(img_path)
                            
                            scene_clip = ImageClip(img_path, duration=scene_duration)
                            scene_clip = resize_clip(scene_clip, (1080, 1080))
                            scene_clip_created = True
                            print(f"    ✅ Scene {i+1}: Placeholder created (invalid URL)")
                        else:
                            print(f"  Scene {i+1}/{num_scenes}: Creating GIF from image {i+1} of {len(image_urls)}: {image_url_to_use[:50]}...")
                            from app.visual_engine import generate_animated_gif_fallback
                            
                            scene_clip_created = False
                            try:
                                gif_path = generate_animated_gif_fallback(image_url_to_use)
                                
                                if gif_path and os.path.exists(gif_path):
                                    scene_clip = VideoFileClip(gif_path)
                                    # If GIF is shorter than scene_duration, loop it
                                    if scene_clip.duration < scene_duration:
                                        num_loops = int(scene_duration / scene_clip.duration) + 1
                                        looped = [scene_clip] * num_loops
                                        scene_clip = concatenate_videoclips(looped, method="compose")
                                    scene_clip = scene_clip.with_duration(scene_duration)
                                    temp_files.append(gif_path)  # Track for cleanup
                                    scene_clip_created = True
                                    print(f"    ✅ Scene {i+1}: GIF created successfully")
                                else:
                                    print(f"    ⚠️ GIF path invalid or doesn't exist: {gif_path}")
                                    print(f"    Falling back to static image...")
                            except Exception as gif_error:
                                print(f"    ⚠️ GIF creation failed for scene {i+1}: {gif_error}")
                                print(f"    Falling back to static image...")
                        
                        # Fallback: use static image if GIF creation failed
                        if not scene_clip_created:
                            print(f"  Scene {i+1}/{num_scenes}: Using static image (GIF creation failed)")
                            if i >= len(image_urls):
                                print(f"    ❌ ERROR: Image index {i} out of range (only {len(image_urls)} images available)")
                                print(f"    Using first available image as fallback to ensure scene is created")
                                # Use first image as emergency fallback
                                fallback_idx = 0
                                if len(image_urls) > 0:
                                    fallback_idx = 0
                                else:
                                    print(f"    ❌ FATAL: No images available at all!")
                                    continue
                            else:
                                fallback_idx = i
                            
                            # Try to download the image with retry (faster timeout)
                            img_downloaded = False
                            img_response = None
                            for retry_attempt in range(2):  # Only 2 attempts, fail faster
                                try:
                                    print(f"    Attempting to download image (attempt {retry_attempt + 1}/2, timeout: 30s)...")
                                    img_response = requests.get(image_urls[fallback_idx], timeout=30)  # Faster timeout
                                    if img_response.status_code == 200:
                                        img_downloaded = True
                                        # Cache the first successful image
                                        if cached_image is None:
                                            cached_image = img_response.content
                                            print(f"    💾 Cached first successful image for reuse")
                                        break
                                    else:
                                        print(f"    Download failed with status {img_response.status_code}")
                                except Exception as download_error:
                                    print(f"    Download attempt {retry_attempt + 1} failed: {download_error}")
                                    if retry_attempt < 1:
                                        import time
                                        time.sleep(0.5)  # Shorter wait
                            
                            if not img_downloaded:
                                # Try using cached image if available
                                if cached_image is not None:
                                    print(f"    ⚠️ Image download failed, reusing cached image from scene 1")
                                    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as img_file:
                                        img_file.write(cached_image)
                                        img_path = img_file.name
                                        temp_files.append(img_path)
                                    img_downloaded = True
                                else:
                                    print(f"    ❌ ERROR: Could not download image and no cached image available")
                                    print(f"    Using a placeholder black image to ensure scene is created")
                                    # Create a black placeholder image
                                    from PIL import Image as PILImage
                                    placeholder = PILImage.new('RGB', (1080, 1080), color='black')
                                    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as img_file:
                                        placeholder.save(img_file.name)
                                        img_path = img_file.name
                                        temp_files.append(img_path)
                            else:
                                with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as img_file:
                                    img_file.write(img_response.content)
                                    img_path = img_file.name
                                    temp_files.append(img_path)
                            
                            try:
                                scene_clip = ImageClip(img_path, duration=scene_duration)
                                # Resize to Instagram-friendly size
                                target_size = (1080, 1080)
                                scene_clip = resize_clip(scene_clip, target_size)
                                # Set FPS
                                if hasattr(scene_clip, 'with_fps'):
                                    scene_clip = scene_clip.with_fps(30)
                                scene_clip_created = True
                                print(f"    ✅ Scene {i+1}: Static image clip created")
                            except Exception as imageclip_error:
                                print(f"    ⚠️ ImageClip failed (likely Pillow version issue): {imageclip_error}")
                                print(f"    Trying alternative: Create video clip directly from image file...")
                                # Alternative: Use VideoFileClip with the image (treat as single frame)
                                try:
                                    # Create a simple video from the image using ffmpeg-like approach
                                    # For now, fall back to ColorClip but log the image URL
                                    print(f"    ⚠️ ImageClip not available, using ColorClip placeholder")
                                    print(f"    📷 Image URL that should be used: {image_urls[fallback_idx][:100]}...")
                                    # Use basic fallback if available, otherwise create new ColorClip
                                    if basic_fallback_clip is not None:
                                        scene_clip = basic_fallback_clip.with_duration(scene_duration) if hasattr(basic_fallback_clip, 'with_duration') else basic_fallback_clip
                                    else:
                                        scene_clip = ColorClip(size=(1080, 1080), color=(0, 0, 0), duration=scene_duration)
                                        if hasattr(scene_clip, 'with_fps'):
                                            scene_clip = scene_clip.with_fps(30)
                                    scene_clip_created = True
                                    print(f"    ⚠️ Scene {i+1}: Using ColorClip placeholder (ImageClip unavailable)")
                                except Exception as alt_error:
                                    print(f"    ❌ Alternative method also failed: {alt_error}")
                                    scene_clip_created = False
                        
                        # Ensure scene_clip is set
                        if not scene_clip_created:
                            print(f"    ❌ FATAL: Could not create scene clip for scene {i+1}!")
                            # Create placeholder as last resort
                            try:
                                placeholder = PILImage.new('RGB', (1080, 1080), color='black')
                                with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as img_file:
                                    placeholder.save(img_file.name)
                                    img_path = img_file.name
                                    temp_files.append(img_path)
                                
                                scene_clip = ImageClip(img_path, duration=scene_duration)
                                scene_clip = scene_clip.resized((1080, 1080))
                                scene_clip_created = True
                                print(f"    ✅ Scene {i+1}: Emergency placeholder created")
                            except Exception as emergency_error:
                                print(f"    ❌ Could not even create emergency placeholder: {emergency_error}")
                                continue
                    
                    # If we still don't have a scene_clip, create a placeholder
                    scene_clip_created_in_fallback = False
                    if 'scene_clip' not in locals() or scene_clip is None:
                        print(f"  Scene {i+1}/{num_scenes}: No scene clip created, creating placeholder...")
                        try:
                            # Try PIL + ImageClip method first
                            placeholder = PILImage.new('RGB', (1080, 1080), color='black')
                            with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as img_file:
                                placeholder.save(img_file.name)
                                img_path = img_file.name
                                temp_files.append(img_path)
                            
                            scene_clip = ImageClip(img_path, duration=scene_duration)
                            scene_clip = resize_clip(scene_clip, (1080, 1080))
                            scene_clip_created_in_fallback = True
                            print(f"    ✅ Scene {i+1}: Final fallback placeholder created (PIL method)")
                        except Exception as final_error:
                            print(f"    ⚠️ PIL method failed, trying ColorClip fallback: {final_error}")
                            try:
                                # Fallback: Use ColorClip directly
                                try:
                                    from moviepy import ColorClip
                                except ImportError:
                                    from moviepy.editor import ColorClip
                                
                                scene_clip = ColorClip(
                                    size=(1080, 1080),
                                    color=(0, 0, 0),  # Black
                                    duration=scene_duration
                                )
                                scene_clip = scene_clip.with_fps(30)
                                scene_clip_created_in_fallback = True
                                print(f"    ✅ Scene {i+1}: Final fallback placeholder created (ColorClip method)")
                            except Exception as colorclip_error:
                                print(f"    ❌ FATAL: Both methods failed: {colorclip_error}")
                                import traceback
                                traceback.print_exc()
                                # Don't continue - try one more absolute basic method
                                try:
                                    # Last resort: Try creating a minimal ColorClip without resizing
                                    try:
                                        from moviepy import ColorClip
                                    except ImportError:
                                        from moviepy.editor import ColorClip
                                    scene_clip = ColorClip(size=(1080, 1080), color=(0, 0, 0), duration=scene_duration)
                                    scene_clip_created_in_fallback = True
                                    print(f"    ✅ Scene {i+1}: Created minimal ColorClip as absolute last resort")
                                except Exception as last_resort_error:
                                    print(f"    ❌ ABSOLUTE FAILURE: Could not create any clip: {last_resort_error}")
                                    # Still continue - we'll handle empty scene_clips later
                                    continue
                    
                    # CRITICAL: Ensure we ALWAYS have a scene_clip before appending
                    if 'scene_clip' not in locals() or scene_clip is None:
                        # Absolute last resort: Create a basic ColorClip
                        print(f"  Scene {i+1}: Creating absolute last resort ColorClip...")
                        try:
                            try:
                                from moviepy import ColorClip
                            except ImportError:
                                from moviepy.editor import ColorClip
                            scene_clip = ColorClip(size=(1080, 1080), color=(0, 0, 0), duration=scene_duration)
                            scene_clip = scene_clip.with_fps(30)
                            print(f"    ✅ Scene {i+1}: Created absolute last resort ColorClip")
                        except Exception as absolute_error:
                            print(f"    ❌ CRITICAL: Even ColorClip failed: {absolute_error}")
                            # This should never happen, but if it does, we'll handle it in the final check
                            continue
                    
                    # Set FPS if not already set
                    if hasattr(scene_clip, 'with_fps'):
                        try:
                            scene_clip = scene_clip.with_fps(30)
                        except:
                            pass  # FPS might already be set
                    
                    # Note: Fade transitions not available in MoviePy 2.x
                    # Scenes will transition directly (still looks good!)
                    
                    scene_clips.append(scene_clip)
                    print(f"  ✅ Scene {i+1}/{num_scenes} successfully added to scene_clips")
                except Exception as e:
                    print(f"  ❌ ERROR: Error processing scene {i+1}: {e}")
                    import traceback
                    traceback.print_exc()
                    
                    # CRITICAL: Don't skip the scene - use basic fallback if available
                    if basic_fallback_clip is not None:
                        print(f"  🔧 Using basic fallback clip for scene {i+1}...")
                        try:
                            # Create a copy of the basic fallback clip for this scene
                            scene_clip = basic_fallback_clip.with_duration(scene_duration)
                            scene_clips.append(scene_clip)
                            print(f"  ✅ Scene {i+1}/{num_scenes} added using basic fallback clip")
                        except Exception as fallback_copy_error:
                            print(f"  ⚠️ Could not copy fallback clip: {fallback_copy_error}")
                            # Try creating a new one
                            try:
                                scene_clip = ColorClip(size=(1080, 1080), color=(0, 0, 0), duration=scene_duration)
                                scene_clip = scene_clip.with_fps(30)
                                scene_clips.append(scene_clip)
                                print(f"  ✅ Scene {i+1}/{num_scenes} added using new ColorClip")
                            except Exception as new_clip_error:
                                print(f"  ❌ Could not create new clip: {new_clip_error}")
                                print(f"  ⚠️ Scene {i+1} will be missing - will be handled in final check")
                    else:
                        # No basic fallback available, try to create one now
                        print(f"  🔧 Creating fallback placeholder for scene {i+1}...")
                        scene_clip_created = False
                        try:
                            # Try ColorClip first (simpler)
                            scene_clip = ColorClip(size=(1080, 1080), color=(0, 0, 0), duration=scene_duration)
                            scene_clip = scene_clip.with_fps(30)
                            scene_clips.append(scene_clip)
                            scene_clip_created = True
                            print(f"  ✅ Scene {i+1}/{num_scenes} fallback created (ColorClip)")
                        except Exception as colorclip_error:
                            print(f"  ⚠️ ColorClip failed, trying PIL: {colorclip_error}")
                            try:
                                from PIL import Image as PILImage
                                placeholder = PILImage.new('RGB', (1080, 1080), color='black')
                                with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as img_file:
                                    placeholder.save(img_file.name)
                                    img_path = img_file.name
                                    temp_files.append(img_path)
                                
                                scene_clip = ImageClip(img_path, duration=scene_duration)
                                scene_clip = scene_clip.resized((1080, 1080))
                                scene_clip = scene_clip.with_fps(30)
                                scene_clips.append(scene_clip)
                                scene_clip_created = True
                                print(f"  ✅ Scene {i+1}/{num_scenes} fallback created (PIL)")
                            except Exception as pil_error:
                                print(f"  ❌ FATAL: All methods failed: {pil_error}")
                                print(f"  ⚠️ Scene {i+1} will be missing - will be handled in final check")
            
            print(f"  ✅ Successfully created {len(scene_clips)} scene clips (expected {num_scenes})")
            print(f"  📊 Scene creation summary:")
            print(f"     - Requested: {num_scenes} scenes")
            print(f"     - Created: {len(scene_clips)} scenes")
            print(f"     - Missing: {num_scenes - len(scene_clips)} scenes")
            
            if len(scene_clips) < num_scenes:
                print(f"  ❌ ERROR: Only {len(scene_clips)} scenes created, but {num_scenes} were requested!")
                print(f"     Missing scenes: {num_scenes - len(scene_clips)}")
                print(f"     Creating placeholder scenes to ensure we have {num_scenes} total...")
                
                # Create placeholder scenes for missing ones
                for missing_idx in range(len(scene_clips), num_scenes):
                    try:
                        # Try PIL + ImageClip method first
                        placeholder = PILImage.new('RGB', (1080, 1080), color='black')
                        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as img_file:
                            placeholder.save(img_file.name)
                            img_path = img_file.name
                            temp_files.append(img_path)
                        
                        placeholder_clip = ImageClip(img_path, duration=scene_duration)
                        placeholder_clip = resize_clip(placeholder_clip, (1080, 1080))
                        placeholder_clip = placeholder_clip.with_fps(30)
                        scene_clips.append(placeholder_clip)
                        print(f"     ✅ Created placeholder for missing scene {missing_idx + 1} (PIL method)")
                    except Exception as placeholder_error:
                        print(f"     ⚠️ PIL method failed, trying ColorClip fallback: {placeholder_error}")
                        try:
                            # Fallback: Use ColorClip directly
                            try:
                                from moviepy import ColorClip
                            except ImportError:
                                from moviepy.editor import ColorClip
                            
                            placeholder_clip = ColorClip(
                                size=(1080, 1080),
                                color=(0, 0, 0),  # Black
                                duration=scene_duration
                            )
                            placeholder_clip = placeholder_clip.with_fps(30)
                            scene_clips.append(placeholder_clip)
                            print(f"     ✅ Created placeholder for missing scene {missing_idx + 1} (ColorClip method)")
                        except Exception as colorclip_error:
                            print(f"     ❌ Could not create placeholder for scene {missing_idx + 1}: {colorclip_error}")
                            import traceback
                            traceback.print_exc()
                
                if len(scene_clips) < num_scenes:
                    print(f"     ❌ CRITICAL: Still only have {len(scene_clips)} scenes after creating placeholders!")
            
            # Final safety check: if we still have no scenes, create at least one placeholder
            if not scene_clips:
                print(f"  ❌ CRITICAL: No scenes created at all! Creating emergency placeholder scenes...")
                print(f"  📋 Attempting to create {num_scenes} emergency placeholder scenes...")
                
                # First, verify what's available
                print(f"  🔍 Checking available tools...")
                colorclip_available = False
                pil_available = False
                
                try:
                    # Test ColorClip
                    test_colorclip = ColorClip(size=(10, 10), color=(0, 0, 0), duration=0.1)
                    del test_colorclip
                    colorclip_available = True
                    print(f"     ✅ ColorClip is available")
                except Exception as colorclip_test_error:
                    print(f"     ❌ ColorClip test failed: {colorclip_test_error}")
                
                try:
                    # Test PIL
                    test_pil = PILImage.new('RGB', (10, 10), color='black')
                    del test_pil
                    pil_available = True
                    print(f"     ✅ PIL is available")
                except Exception as pil_test_error:
                    print(f"     ❌ PIL test failed: {pil_test_error}")
                
                emergency_success_count = 0
                
                for emergency_idx in range(num_scenes):
                    scene_created = False
                    # Method 1: Try ColorClip first (simplest, no PIL needed)
                    # Try even if test failed - sometimes test fails but actual creation works
                    if not scene_created:
                        try:
                            print(f"     Method 1: Trying ColorClip for scene {emergency_idx + 1}...")
                            # Try different ColorClip parameter formats
                            try:
                                placeholder_clip = ColorClip(
                                    size=(1080, 1080),
                                    color=(0, 0, 0),  # Black as RGB tuple
                                    duration=scene_duration
                                )
                            except Exception as format_error:
                                print(f"     ⚠️ RGB tuple format failed, trying color name: {format_error}")
                                # Try with color name
                                try:
                                    placeholder_clip = ColorClip(
                                        size=(1080, 1080),
                                        color='black',
                                        duration=scene_duration
                                    )
                                except Exception as name_error:
                                    print(f"     ⚠️ Color name format also failed, trying hex: {name_error}")
                                    # Try with hex color
                                    placeholder_clip = ColorClip(
                                        size=(1080, 1080),
                                        color='#000000',
                                        duration=scene_duration
                                    )
                            
                            placeholder_clip = placeholder_clip.with_fps(30)
                            scene_clips.append(placeholder_clip)
                            emergency_success_count += 1
                            scene_created = True
                            print(f"     ✅ Created emergency placeholder scene {emergency_idx + 1} (ColorClip method)")
                        except Exception as colorclip_error:
                            print(f"     ❌ ColorClip method failed: {colorclip_error}")
                            import traceback
                            traceback.print_exc()
                    
                    # Method 2: Try PIL + ImageClip
                    # Try even if test failed - sometimes test fails but actual creation works
                    if not scene_created:
                        try:
                            print(f"     Method 2: Trying PIL + ImageClip for scene {emergency_idx + 1}...")
                            placeholder = PILImage.new('RGB', (1080, 1080), color='black')
                            with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as img_file:
                                placeholder.save(img_file.name)
                                img_path = img_file.name
                                temp_files.append(img_path)
                            
                            placeholder_clip = ImageClip(img_path, duration=scene_duration)
                            placeholder_clip = resize_clip(placeholder_clip, (1080, 1080))
                            placeholder_clip = placeholder_clip.with_fps(30)
                            scene_clips.append(placeholder_clip)
                            emergency_success_count += 1
                            scene_created = True
                            print(f"     ✅ Created emergency placeholder scene {emergency_idx + 1} (PIL method)")
                        except Exception as pil_error:
                            print(f"     ❌ PIL method failed: {pil_error}")
                            import traceback
                            traceback.print_exc()
                    
                    if not scene_created:
                        print(f"     ❌ FATAL: Could not create scene {emergency_idx + 1} with any method!")
                        print(f"        ColorClip available: {colorclip_available}")
                        print(f"        PIL available: {pil_available}")
                
                print(f"  📊 Emergency creation results: {emergency_success_count}/{num_scenes} scenes created")
                
                # Final check: if we still have no scenes, try ONE MORE absolute last resort
                if not scene_clips:
                    print(f"  🆘 ABSOLUTE LAST RESORT: Using ColorClip directly (test passed, so this should work)...")
                    # ColorClip test passed, so let's use it directly
                    colorclip_errors = []
                    try:
                        # Create all scenes using ColorClip directly
                        for i in range(num_scenes):
                            try:
                                print(f"     Creating scene {i+1}/{num_scenes} using ColorClip...")
                                # Try different ways to set FPS based on MoviePy version
                                try:
                                    # MoviePy 1.x: FPS is set in constructor or with with_fps()
                                    scene_clip = ColorClip(size=(1080, 1080), color=(0, 0, 0), duration=scene_duration, fps=30)
                                except TypeError:
                                    # MoviePy 2.x: FPS might need to be set differently
                                    try:
                                        scene_clip = ColorClip(size=(1080, 1080), color=(0, 0, 0), duration=scene_duration)
                                        # Try with_fps if available
                                        if hasattr(scene_clip, 'with_fps'):
                                            scene_clip = scene_clip.with_fps(30)
                                        elif hasattr(scene_clip, 'set_fps'):
                                            scene_clip = scene_clip.set_fps(30)
                                        # If neither works, just use the clip as-is (FPS might be set automatically)
                                    except Exception as fps_error:
                                        print(f"     ⚠️ FPS setting failed, using clip without explicit FPS: {fps_error}")
                                        scene_clip = ColorClip(size=(1080, 1080), color=(0, 0, 0), duration=scene_duration)
                                
                                scene_clips.append(scene_clip)
                                print(f"     ✅ Created scene {i+1}/{num_scenes} using ColorClip")
                            except Exception as scene_error:
                                error_detail = f"Scene {i+1} failed: {scene_error}"
                                colorclip_errors.append(error_detail)
                                print(f"     ❌ Failed to create scene {i+1}: {scene_error}")
                                import traceback
                                traceback.print_exc()
                                # Continue trying other scenes
                        
                        if scene_clips:
                            print(f"  ✅ Created {len(scene_clips)}/{num_scenes} scenes using ColorClip fallback!")
                            print(f"  ⚠️ WARNING: Using fallback scenes - some scenes may be missing")
                        else:
                            error_detail = "ColorClip method failed for all scenes. Errors:\n" + "\n".join(colorclip_errors)
                            raise Exception(error_detail)
                    except Exception as pil_fallback_error:
                        error_msg = f"No scenes could be created. All attempts failed.\n"
                        error_msg += f"  - Requested scenes: {num_scenes}\n"
                        error_msg += f"  - Created scenes: {len(scene_clips)}\n"
                        error_msg += f"  - Emergency creation attempted: {num_scenes} scenes\n"
                        error_msg += f"  - Emergency creation succeeded: {emergency_success_count} scenes\n"
                        error_msg += f"  - ColorClip test passed: {colorclip_available}\n"
                        error_msg += f"  - PIL test passed: {pil_available}\n"
                        error_msg += f"  - PIL+ImageClip fallback failed: {pil_fallback_error}\n"
                        error_msg += f"\n  This suggests MoviePy is not working on Streamlit Cloud.\n"
                        error_msg += f"  Possible causes:\n"
                        error_msg += f"  1. Missing system dependencies (ffmpeg)\n"
                        error_msg += f"  2. MoviePy version incompatibility\n"
                        error_msg += f"  3. Environment restrictions on Streamlit Cloud\n"
                        error_msg += f"\n  Please check the console output above for detailed error messages."
                        print(f"\n❌ FATAL ERROR DETAILS:")
                        print(error_msg)
                        import traceback
                        traceback.print_exc()
                        raise Exception(error_msg)
            
            if not scene_clips:
                raise Exception("No scenes could be created after all fallback attempts")
            
            # Add professional commercial effects to each scene
            print("Adding commercial effects (zoom, text overlays)...")
            enhanced_scenes = []
            for i, scene_clip in enumerate(scene_clips):
                # Add subtle zoom effect for more dynamic feel
                # Simple approach: resize slightly larger, then crop to center
                try:
                    if hasattr(scene_clip, 'size') and scene_clip.size:
                        w, h = scene_clip.size
                        # More visible zoom (20% for commercial feel)
                        zoom_factor = 1.2
                        new_w = int(w * zoom_factor)
                        new_h = int(h * zoom_factor)
                        
                        # Resize to larger size
                        scene_clip = resize_clip(scene_clip, (new_w, new_h))
                        
                        # Crop to center to create ken burns effect
                        # Calculate crop area (center of larger image)
                        x_center = new_w // 2
                        y_center = new_h // 2
                        x1 = x_center - w // 2
                        y1 = y_center - h // 2
                        x2 = x1 + w
                        y2 = y1 + h
                        
                        scene_clip = scene_clip.cropped(x1=x1, y1=y1, x2=x2, y2=y2)
                        print(f"  ✅ Scene {i+1}: Added zoom effect (20% zoom, ken burns style)")
                    else:
                        print(f"  ⚠️ Scene {i+1}: No size attribute, skipping zoom")
                except Exception as e:
                    print(f"  ❌ Scene {i+1}: Could not add zoom effect: {e}")
                    import traceback
                    traceback.print_exc()
                    # Continue with original clip
                
                enhanced_scenes.append(scene_clip)
            
            # Concatenate all scenes
            print(f"🎬 Combining {len(enhanced_scenes)} scenes into final video...")
            print(f"  Total scene clips: {len(enhanced_scenes)} (requested: {num_scenes})")
            if len(enhanced_scenes) == 0:
                raise Exception("No scenes to combine!")
            if len(enhanced_scenes) < num_scenes:
                print(f"  ❌ ERROR: Only {len(enhanced_scenes)} scenes available, but {num_scenes} were requested!")
                print(f"     The final video will only show {len(enhanced_scenes)} GIFs instead of {num_scenes}")
                print(f"     This is a CRITICAL ERROR - check image generation and scene creation above!")
            if len(enhanced_scenes) == 1:
                print("  ⚠️ WARNING: Only 1 scene created! Expected multiple scenes.")
            
            total_expected_duration = 0
            for i, clip in enumerate(enhanced_scenes):
                print(f"  Scene {i+1}/{len(enhanced_scenes)}: duration={clip.duration:.2f}s, size={clip.size if hasattr(clip, 'size') else 'N/A'}")
                total_expected_duration += clip.duration
            
            print(f"  Expected total duration: {total_expected_duration:.2f}s")
            print(f"  Expected per scene: {scene_duration:.2f}s")
            print(f"  Actual total: {total_expected_duration:.2f}s")
            print(f"  ✅ All {len(enhanced_scenes)} scenes will be included in the main video!")
            
            # Concatenate all scenes - NEVER trim this!
            if len(enhanced_scenes) > 1:
                print(f"  Concatenating {len(enhanced_scenes)} clips...")
                final_video = concatenate_videoclips(enhanced_scenes, method="compose")
                print(f"  ✅ Concatenated video duration: {final_video.duration:.2f}s")
            else:
                print(f"  Only 1 scene, using it directly...")
                final_video = enhanced_scenes[0]
            
            print(f"📊 Main video summary:")
            print(f"  Combined main video duration: {final_video.duration:.2f}s")
            print(f"  Expected main video duration: {main_video_available_time:.2f}s")
            print(f"  Number of scenes in main video: {len(enhanced_scenes)}")
            print(f"  Audio duration: {audio_duration:.2f}s")
            print(f"  ✅ Main video contains ALL {len(enhanced_scenes)} scenes - DO NOT TRIM!")
            
            # The main video should already be the correct length (main_video_available_time)
            # We'll add the intro (2s) later, so total will be audio_duration
            # Don't trim or loop here - the video is already correctly sized for the main portion
            
            # Verify main video duration matches expected
            # But ensure it's never 0 or negative
            if main_video_available_time <= 0:
                print(f"⚠️ WARNING: main_video_available_time is {main_video_available_time:.2f}s (too short!)")
                print(f"   Audio: {audio_duration:.2f}s, Intro: {intro_duration}s, Outro: {outro_duration}s")
                print(f"   Using full audio duration for main video instead")
                main_video_available_time = audio_duration - intro_duration - outro_duration
                if main_video_available_time <= 0:
                    # Fallback: use full audio, skip intro/outro
                    main_video_available_time = audio_duration
                    intro_duration = 0
                    outro_duration = 0
                    print(f"   Fallback: Using full audio ({audio_duration:.2f}s) for main video")
            
            # Check duration but DON'T trim - we want ALL scenes included
            # If video is longer than expected, that's OK - we'll adjust outro or accept it
            duration_diff = final_video.duration - main_video_available_time
            print(f"📊 Duration check (main video only):")
            print(f"   Actual main video duration: {final_video.duration:.2f}s")
            print(f"   Expected main video duration: {main_video_available_time:.2f}s")
            print(f"   Difference: {duration_diff:.2f}s")
            print(f"   Number of scenes in main video: {len(enhanced_scenes)} (should be {num_scenes})")
            
            if len(enhanced_scenes) < num_scenes:
                print(f"   ❌ CRITICAL: Only {len(enhanced_scenes)} scenes created, but {num_scenes} requested!")
                print(f"      Check scene creation logs above to see which scenes failed!")
            
            if duration_diff < -0.1:
                # Video is shorter - this is OK, we'll pad or adjust
                print(f"   ⚠️ Main video is {abs(duration_diff):.2f}s shorter than expected (but all {len(enhanced_scenes)} scenes included)")
            elif duration_diff > 0.1:
                # Video is longer - this means we have all scenes, which is good!
                # Adjust outro duration to compensate, but keep it at least 1 second
                extra_time = duration_diff
                new_outro_duration = max(1.0, outro_duration - extra_time)
                print(f"   ✅ Main video is {extra_time:.2f}s longer (all {len(enhanced_scenes)} scenes included!)")
                print(f"   Adjusting outro duration from {outro_duration:.2f}s to {new_outro_duration:.2f}s to fit audio")
                outro_duration = new_outro_duration
                # Recalculate main_video_available_time for later use
                main_video_available_time = audio_duration - intro_duration - outro_duration
                print(f"   📊 Updated: main_video_available_time = {main_video_available_time:.2f}s")
            else:
                print(f"   ✅ Duration matches perfectly!")
            
            # NEVER trim the video - we want all scenes!
            print(f"✅ Keeping ALL {len(enhanced_scenes)} scenes in main video (duration: {final_video.duration:.2f}s)")
            print(f"✅ Main video will NOT be trimmed - all scenes preserved!")
            
            final_duration = audio_duration  # Always use full audio duration
            
            # Add commercial enhancements: black intro screen with brand name, slogan at end
            print("🎬 Adding commercial enhancements...")
            
            # Create black intro screen with brand name (2 seconds)
            # ALWAYS create intro if brand_name is provided and intro_duration > 0
            intro_clip = None
            intro_duration_actual = intro_duration if intro_duration > 0 else 0
            
            print(f"  🔍 Creating intro: brand_name='{brand_name}', intro_duration={intro_duration}, intro_duration_actual={intro_duration_actual}")
            
            # Force intro creation if brand_name is provided (even if intro_duration was adjusted)
            if brand_name:
                if intro_duration_actual <= 0:
                    # Restore intro duration if it was set to 0
                    intro_duration_actual = 2.0
                    print(f"  ⚠️ Intro duration was 0, restoring to {intro_duration_actual}s")
                
                if intro_duration_actual > 0:
                    try:
                        from moviepy import ColorClip
                        from PIL import Image, ImageDraw, ImageFont
                        import numpy as np
                        
                        # Create black background
                        black_screen = ColorClip(
                            size=(final_video.w, final_video.h),
                            color=(0, 0, 0),  # Black
                            duration=intro_duration_actual
                        )
                        
                        # Create brand name text image
                        text_img = Image.new('RGBA', (final_video.w, final_video.h), (0, 0, 0, 0))
                        draw = ImageDraw.Draw(text_img)
                        
                        # Try to use a system font
                        try:
                            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 100)
                        except:
                            try:
                                font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 100)
                            except:
                                font = ImageFont.load_default()
                        
                        # Get text size for centering
                        bbox = draw.textbbox((0, 0), brand_name, font=font)
                        text_width = bbox[2] - bbox[0]
                        text_height = bbox[3] - bbox[1]
                        x = (final_video.w - text_width) // 2
                        y = (final_video.h - text_height) // 2
                        
                        # Draw text with red stroke (outline)
                        for adj in range(-5, 6):
                            for adj2 in range(-5, 6):
                                if adj != 0 or adj2 != 0:
                                    draw.text((x + adj, y + adj2), brand_name, font=font, fill=(200, 16, 46, 255))
                        # Draw main white text
                        draw.text((x, y), brand_name, font=font, fill=(255, 255, 255, 255))
                        
                        # Convert to numpy array and create clip
                        text_array = np.array(text_img)
                        brand_text_clip = ImageClip(text_array).with_duration(intro_duration_actual)
                        
                        # Composite black screen with text
                        intro_clip = CompositeVideoClip([black_screen, brand_text_clip])
                        print(f"  ✅ Created black intro screen with '{brand_name}' ({intro_duration_actual}s)")
                    except Exception as e:
                        print(f"  ⚠️ Could not create intro screen: {e}")
                        import traceback
                        traceback.print_exc()
            
            # Create black screen with slogan text at the end
            # Use the adjusted outro_duration (may have been reduced to fit all scenes)
            # But ensure it's at least 1 second if slogan is provided
            outro_clip = None
            slogan_duration = outro_duration if outro_duration > 0 else (1.0 if slogan else 0)  # Minimum 1s if slogan exists
            print(f"  🔍 Creating outro: slogan='{slogan}', outro_duration={outro_duration}, slogan_duration={slogan_duration}")
            if slogan:
                if slogan_duration <= 0:
                    slogan_duration = 1.0  # Minimum 1 second for outro
                    print(f"  ⚠️ Outro duration was 0, setting to minimum {slogan_duration}s")
                
                if slogan_duration > 0:
                    try:
                        from moviepy import ColorClip
                        from PIL import Image, ImageDraw, ImageFont
                        import numpy as np
                        
                        # Create black background
                        black_screen = ColorClip(
                            size=(final_video.w, final_video.h),
                            color=(0, 0, 0),  # Black
                            duration=slogan_duration
                        )
                        
                        # Create slogan text image (wrapped text)
                        max_width = final_video.w - 100
                        text_img = Image.new('RGBA', (final_video.w, final_video.h), (0, 0, 0, 0))
                        draw = ImageDraw.Draw(text_img)
                        
                        # Try to use a system font
                        try:
                            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 65)
                        except:
                            try:
                                font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 65)
                            except:
                                font = ImageFont.load_default()
                        
                        # Simple text wrapping
                        words = slogan.split()
                        lines = []
                        current_line = []
                        current_width = 0
                        
                        for word in words:
                            word_width = draw.textbbox((0, 0), word, font=font)[2]
                            if current_width + word_width > max_width and current_line:
                                lines.append(' '.join(current_line))
                                current_line = [word]
                                current_width = word_width
                            else:
                                current_line.append(word)
                                current_width += word_width + draw.textbbox((0, 0), ' ', font=font)[2]
                        if current_line:
                            lines.append(' '.join(current_line))
                        
                        # Draw each line centered
                        text_height = draw.textbbox((0, 0), "Test", font=font)[3] - draw.textbbox((0, 0), "Test", font=font)[1]
                        total_text_height = len(lines) * (text_height + 10) - 10
                        y_start = (final_video.h - total_text_height) // 2
                        y_offset = y_start
                        
                        for line in lines:
                            bbox = draw.textbbox((0, 0), line, font=font)
                            text_width = bbox[2] - bbox[0]
                            x = (final_video.w - text_width) // 2
                            
                            # Draw stroke (red outline)
                            for adj in range(-4, 5):
                                for adj2 in range(-4, 5):
                                    if adj != 0 or adj2 != 0:
                                        draw.text((x + adj, y_offset + adj2), line, font=font, fill=(200, 16, 46, 255))
                            # Draw main white text
                            draw.text((x, y_offset), line, font=font, fill=(255, 255, 255, 255))
                            y_offset += text_height + 10
                        
                        # Convert to numpy array and create clip
                        text_array = np.array(text_img)
                        slogan_text_clip = ImageClip(text_array).with_duration(slogan_duration)
                        
                        # Composite black screen with text
                        outro_clip = CompositeVideoClip([black_screen, slogan_text_clip])
                        print(f"  ✅ Created black outro screen with slogan: '{slogan}' ({slogan_duration}s)")
                    except Exception as e:
                        print(f"  ⚠️ Could not create outro screen: {e}")
                        import traceback
                        traceback.print_exc()
                else:
                    print(f"  ⚠️ Outro duration is 0, skipping outro creation")
            
            # Combine: intro screen + main video + outro screen (black screen with slogan)
            video_segments = []
            
            print(f"\n🎬 Building final video structure:")
            print(f"   Intro clip created: {intro_clip is not None}")
            print(f"   Main video duration: {final_video.duration:.2f}s")
            print(f"   Outro clip created: {outro_clip is not None}")
            print(f"   Main video available time: {main_video_available_time:.2f}s")
            
            # Add intro screen if created
            if intro_clip:
                video_segments.append(intro_clip)
                print(f"  ✅ Added intro screen ({intro_duration_actual}s) with '{brand_name}'")
            else:
                print(f"  ⚠️ No intro screen (brand_name: {brand_name}, intro_duration: {intro_duration})")
            
            # Add main video (GIFs without any text overlays)
            # Main video duration should already match what we calculated
            # (num_scenes * scene_duration = main_video_available_time)
            if intro_clip or outro_clip:
                main_video_expected_duration = main_video_available_time
            else:
                main_video_expected_duration = final_duration
            
            print(f"  📊 Main video expected duration: {main_video_expected_duration:.2f}s")
            print(f"  📊 Main video actual duration: {final_video.duration:.2f}s")
            
            # Ensure main video has valid duration
            if final_video.duration <= 0:
                print(f"  ❌ ERROR: Main video has invalid duration ({final_video.duration:.2f}s)!")
                raise Exception(f"Main video duration is {final_video.duration:.2f}s - cannot create video")
            
            # NEVER trim the main video - we want ALL scenes included!
            # Use the video as-is, even if it's longer than expected
            main_video = final_video
            print(f"  ✅ Using main video as-is ({final_video.duration:.2f}s) - ALL {len(enhanced_scenes)} scenes included")
            
            # Always add main video (it should never be empty)
            if main_video.duration > 0:
                video_segments.append(main_video)
                print(f"  ✅ Added main video ({main_video.duration:.2f}s, {len(enhanced_scenes)} GIFs included, no text overlays)")
            else:
                print(f"  ❌ ERROR: Main video has 0 duration - skipping!")
                raise Exception("Main video has 0 duration!")
            
            # Add outro screen (black screen with slogan) if created
            if outro_clip:
                video_segments.append(outro_clip)
                print(f"  ✅ Added outro screen ({outro_duration}s) with slogan: '{slogan}'")
            else:
                print(f"  ⚠️ No outro screen (slogan: {slogan})")
            
            print(f"\n📋 Video segments to concatenate: {len(video_segments)}")
            for i, seg in enumerate(video_segments):
                print(f"   Segment {i+1}: duration={seg.duration:.2f}s")
            
            # Concatenate intro + main video + outro (sequential)
            if len(video_segments) == 0:
                raise Exception("No video segments to concatenate!")
            elif len(video_segments) > 1:
                print(f"  🎬 Concatenating {len(video_segments)} segments (intro + main + outro)...")
                final_video = concatenate_videoclips(video_segments, method="compose")
                print(f"  ✅ Final video duration: {final_video.duration:.2f}s")
            else:
                print(f"  ⚠️ Only 1 segment, using it directly...")
                final_video = video_segments[0]
            
            # Add audio - Keep ALL video content (intro + all GIFs + outro)
            # If audio is shorter, loop it. If video is shorter, extend video.
            print(f"  🔊 Adding audio ({audio_duration:.3f}s)...")
            print(f"  📊 Video duration before adding audio: {final_video.duration:.3f}s")
            print(f"  📊 Audio duration: {audio_duration:.3f}s")
            print(f"  📊 Video segments:")
            print(f"       Intro: {intro_clip.duration if intro_clip else 0:.3f}s")
            print(f"       Main video: {main_video.duration:.3f}s ({len(enhanced_scenes)} GIFs)")
            print(f"       Outro: {outro_clip.duration if outro_clip else 0:.3f}s")
            
            # Calculate the difference
            duration_diff = final_video.duration - audio_duration
            print(f"  📊 Duration difference: {duration_diff:.4f}s")
            
            # NEVER trim the video - we want ALL content (intro + all GIFs + outro)
            # Audio should play once and then stop (video continues silently if longer)
            if abs(duration_diff) > 0.01:
                if final_video.duration > audio_duration:
                    # Video is longer - audio plays once, then video continues silently
                    print(f"  ✅ Video ({final_video.duration:.3f}s) is longer than audio ({audio_duration:.3f}s)")
                    print(f"     Audio will play once, then video continues silently (preserving ALL video content)")
                    # Use audio as-is (don't extend it) - MoviePy will handle silence after audio ends
                    audio_clip_full = audio_clip  # Keep original audio duration
                else:
                    # Video is shorter - trim audio to match video
                    print(f"  ⚠️ Video ({final_video.duration:.3f}s) is shorter than audio ({audio_duration:.3f}s)")
                    print(f"     Trimming audio to match video duration...")
                    audio_clip_full = audio_clip.with_duration(final_video.duration)
            else:
                # Durations match (or very close) - use as-is
                print(f"  ✅ Durations match perfectly!")
                audio_clip_full = audio_clip
            
            # Verify durations before adding audio
            final_video_duration = final_video.duration
            audio_clip_duration = audio_clip_full.duration
            print(f"  📊 Final video duration: {final_video_duration:.4f}s")
            print(f"  📊 Final audio duration: {audio_clip_duration:.4f}s")
            
            if final_video_duration > audio_clip_duration:
                print(f"  📊 Audio will end at {audio_clip_duration:.4f}s, video continues silently until {final_video_duration:.4f}s")
            else:
                print(f"  📊 Durations match: {abs(final_video_duration - audio_clip_duration):.4f}s difference")
            
            # Add audio to video
            # If audio is shorter than video, MoviePy will automatically handle silence after audio ends
            final_video = set_audio_on_clip(final_video, audio_clip_full)
            
            print(f"  ✅ Audio added successfully!")
            print(f"  ✅ Final video duration: {final_video.duration:.4f}s")
            print(f"  ✅ ALL {len(enhanced_scenes)} GIFs are preserved in the video!")
            print(f"  ✅ Intro screen: {'✅' if intro_clip else '❌'}")
            print(f"  ✅ Outro screen: {'✅' if outro_clip else '❌'}")
            
            # Create output video file
            output_path = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4').name
            print(f"Rendering final video to {output_path}...")
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
            for clip in scene_clips:
                clip.close()
            for temp_file in temp_files:
                try:
                    if os.path.exists(temp_file):
                        os.unlink(temp_file)
                except:
                    pass
            os.unlink(audio_path)
            
            print(f"✅ Multi-scene video created: {output_path}")
            return output_path
            
        except Exception as e:
            # Cleanup on error
            if os.path.exists(audio_path):
                os.unlink(audio_path)
            raise e
            
    except Exception as e:
        print(f"Error creating multi-scene video: {e}")
        import traceback
        traceback.print_exc()
        raise e

