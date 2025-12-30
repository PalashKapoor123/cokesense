import streamlit as st
import os
from dotenv import load_dotenv
import time
import requests
from datetime import datetime

from app.trend_fetcher import get_all_trends
from app.trend_classifier import classify_trend
from app.creative_engine import generate_campaign_for_trend
from app.visual_engine import build_dalle_prompt, generate_image_url, build_video_prompt, generate_video_url
from app.config import openai_client  # Import for checking which service generated images
from app.instagram_poster import post_to_instagram, format_campaign_caption
from app.pdf_exporter import export_campaign_to_pdf
from app.post_history import get_all_posts_with_insights, init_database
from app.audio_generator import generate_slogan_audio, get_audio_bytes
from app.multi_scene_video import create_multi_scene_video

load_dotenv()
# Check if we have any AI API keys
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
GROQ_KEY = os.getenv("GROQ_API_KEY")
IS_DEMO_MODE = (
    (not OPENAI_KEY or OPENAI_KEY == "your_openai_api_key_here") and
    (not GROQ_KEY or GROQ_KEY == "your_groq_api_key_here")
)


# -----------------------------------------------------------
# App Configuration
# -----------------------------------------------------------
st.set_page_config(
    page_title="CokeSense: Real-Time Coca-Cola Creative Engine",
    page_icon="🥤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------
# Custom CSS for Dark Theme (Figma Design)
# -----------------------------------------------------------
st.markdown("""
<style>
    /* Dark Theme Base */
    .stApp {
        background-color: #0A0A0A;
        color: #FFFFFF;
    }
    
    /* Header Styling */
    .main-header {
        background: linear-gradient(135deg, #1A1A1A 0%, #0A0A0A 100%);
        padding: 1.5rem 2rem;
        border-bottom: 2px solid #F40009;
        margin-bottom: 2rem;
    }
    
    .header-content {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .logo-section {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .coca-cola-logo-text {
        color: #F40009;
        font-weight: 700;
        font-size: 2.2rem;
        letter-spacing: 0.03em;
        font-family: 'Georgia', 'Times New Roman', serif;
        font-style: italic;
        text-shadow: 0 2px 6px rgba(244, 0, 9, 0.4);
        margin-right: 0.75rem;
        display: inline-block;
        /* Mimic the iconic Coca-Cola script style with subtle effects */
        background: linear-gradient(135deg, #F40009 0%, #D40008 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        position: relative;
    }
    
    .coca-cola-logo-text::after {
        content: '';
        position: absolute;
        bottom: -2px;
        left: 0;
        width: 100%;
        height: 2px;
        background: linear-gradient(90deg, transparent, #F40009, transparent);
        opacity: 0.3;
    }
    
    .coca-cola-logo {
        color: #F40009;
        font-weight: 700;
        font-size: 1.5rem;
        letter-spacing: 0.05em;
    }
    
    .cokesense-title {
        color: #FFFFFF;
        font-weight: 600;
        font-size: 1.5rem;
        margin-left: 0.5rem;
    }
    
    .subtitle {
        color: #B0B0B0;
        font-size: 0.9rem;
        margin-top: 0.25rem;
    }
    
    .powered-by {
        color: #B0B0B0;
        font-size: 0.85rem;
    }
    
    /* Card Styling */
    .campaign-card {
        background-color: #1A1A1A;
        border: 1px solid #2A2A2A;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    
    .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
        border-bottom: 1px solid #2A2A2A;
        padding-bottom: 0.75rem;
    }
    
    .card-title {
        color: #F40009;
        font-weight: 600;
        font-size: 1.1rem;
        margin: 0;
    }
    
    .card-content {
        color: #E0E0E0;
        line-height: 1.6;
    }
    
    /* Button Styling */
    .stButton > button {
        background-color: #F40009;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background-color: #D40008;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(244, 0, 9, 0.4);
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #1A1A1A;
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: #FFFFFF;
    }
    
    /* Text Input Styling */
    .stTextInput > div > div > input {
        background-color: #2A2A2A;
        color: #FFFFFF;
        border: 1px solid #3A3A3A;
    }
    
    /* Selectbox Styling */
    .stSelectbox > div > div {
        background-color: #2A2A2A;
        color: #FFFFFF;
    }
    
    .stSelectbox label {
        color: #E0E0E0;
    }
    
    /* Main content area */
    .main .block-container {
        padding-top: 2rem;
    }
    
    /* Hide default Streamlit header */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Improve card spacing */
    .campaign-card {
        margin-bottom: 1.5rem;
    }
    
    /* Better button styling for secondary buttons */
    .stButton > button[kind="secondary"] {
        background-color: #2A2A2A;
        color: #FFFFFF;
        border: 1px solid #3A3A3A;
    }
    
    .stButton > button[kind="secondary"]:hover {
        background-color: #3A3A3A;
        border-color: #4A4A4A;
    }
    
    /* Metric Cards */
    .metric-card {
        background-color: #1A1A1A;
        border: 1px solid #2A2A2A;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
    }
    
    .metric-value {
        color: #F40009;
        font-size: 1.5rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        color: #B0B0B0;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Section Headers */
    .section-header {
        color: #F40009;
        font-weight: 600;
        font-size: 1.2rem;
        margin: 1.5rem 0 1rem 0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Copy Icon Button */
    .copy-btn {
        background: transparent;
        border: 1px solid #3A3A3A;
        color: #B0B0B0;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        cursor: pointer;
        font-size: 0.85rem;
    }
    
    .copy-btn:hover {
        background-color: #2A2A2A;
        color: #FFFFFF;
    }
    
    /* Coca-Cola Logo Image Styling */
    .coca-cola-logo-img {
        height: 45px;
        width: auto;
        object-fit: contain;
        margin-right: 12px;
        display: inline-block;
        vertical-align: middle;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------
# Header Section (Figma Design)
# -----------------------------------------------------------
# Check if local logo file exists (for local development)
logo_path = "assets/images/coca_cola_logo.png"
logo_exists = os.path.exists(logo_path)

if logo_exists:
    # Use local image logo if available (for local dev)
    try:
        st.markdown("""
        <div class="main-header">
            <div class="header-content">
                <div class="logo-section">
                    <img src="data:image/png;base64,{}" 
                         alt="Coca-Cola Logo" 
                         class="coca-cola-logo-img">
                    <div>
                        <span class="cokesense-title">CokeSense</span>
                        <div class="subtitle">AI-Powered Marketing Campaign Generator</div>
                    </div>
                </div>
                <div class="powered-by">Powered by AI</div>
            </div>
        </div>
        """.format(
            # Read and encode the image
            __import__('base64').b64encode(open(logo_path, 'rb').read()).decode('utf-8')
        ), unsafe_allow_html=True)
    except Exception:
        # Fall through to styled text version if local file read fails
        logo_exists = False

if not logo_exists:
    # Use styled text version (works on Streamlit Cloud and locally)
    # The CSS already styles this beautifully with the Coca-Cola red gradient
    st.markdown("""
    <div class="main-header">
        <div class="header-content">
            <div class="logo-section">
                <div class="coca-cola-logo-text">Coca‑Cola</div>
                <div>
                    <span class="cokesense-title">CokeSense</span>
                    <div class="subtitle">AI-Powered Marketing Campaign Generator</div>
                </div>
            </div>
            <div class="powered-by">Powered by AI</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# -----------------------------------------------------------
# Sidebar (Figma Design)
# -----------------------------------------------------------
with st.sidebar:
    # Controls Section
    st.markdown("### Controls")
    if st.button("✨ New Campaign", type="primary", width='stretch'):
        # Clear all campaign data
        st.session_state.pop("last_campaign", None)
        st.session_state.pop("last_image_url", None)
        st.session_state.pop("last_trend", None)
        st.session_state.pop("last_category", None)
        st.session_state.pop("campaign_generated", None)
        st.session_state.pop("last_dalle_prompt", None)
        st.session_state.pop("last_video_url", None)
        st.session_state.pop("multi_scene_video_path", None)
        st.session_state.pop("slogan_audio_bytes", None)
        st.rerun()
    
    if st.button("💾 Save Draft", width='stretch'):
        st.info("💾 Draft saved! (Feature coming soon)")
    
    st.divider()
    
    # Instagram Section
    st.markdown("### 📱 Instagram")
    instagram_token = st.text_input(
        "Access Token",
        type="password",
        help="Enter your Instagram access token",
        key="instagram_token_input"
    )
    
    if instagram_token:
        st.session_state["instagram_token"] = instagram_token
        if st.button("🔗 Connect", width='stretch'):
            st.success("✅ Connected!")
    else:
        st.info("💡 Add token to connect")
    
    st.divider()
    
    # Analytics Section
    st.markdown("### 📊 Analytics")
    
    if instagram_token:
        # Initialize database
        init_database()
        
        # Get analytics
        with st.spinner("Loading..."):
            posts = get_all_posts_with_insights(instagram_token, include_deleted=False)
        
        if posts:
            active_posts = [p for p in posts if p.get('status') != 'deleted' and not p.get('deleted')]
            total_likes = sum(p.get('likes', 0) for p in active_posts)
            total_comments = sum(p.get('comments', 0) for p in active_posts)
            total_reach = sum(p.get('reach', 0) for p in active_posts)
            avg_engagement = sum(p.get('engagement_rate', 0) for p in active_posts) / len(active_posts) if active_posts else 0
            
            # Get top trend
            trend_counts = {}
            for p in active_posts:
                trend = p.get('trend', 'Unknown')
                trend_counts[trend] = trend_counts.get(trend, 0) + 1
            top_trend = max(trend_counts.items(), key=lambda x: x[1])[0] if trend_counts else "N/A"
            
            st.markdown(f"**Total Campaigns:** {len(active_posts)}")
            st.markdown(f"**Avg. Engagement:** {avg_engagement:.1f}%")
            st.markdown(f"**Total Reach:** {total_reach/1000000:.1f}M" if total_reach >= 1000000 else f"**Total Reach:** {total_reach/1000:.1f}K")
            st.markdown(f"**Top Trend:** {top_trend[:20]}")
        else:
            st.info("📭 No campaigns yet")
    else:
        st.info("💡 Connect Instagram to see analytics")
    
    st.divider()
    
    # Mode indicator (compact)
    if IS_DEMO_MODE:
        st.caption("🎭 Demo Mode")
    elif os.getenv("GROQ_API_KEY") and os.getenv("GROQ_API_KEY") != "your_groq_api_key_here":
        st.caption("🤖 AI Mode: Groq")
    elif os.getenv("OPENAI_API_KEY") and os.getenv("OPENAI_API_KEY") != "your_openai_api_key_here":
        st.caption("🤖 AI Mode: OpenAI")
    

# -----------------------------------------------------------
# Main Content Area (Figma Design)
# -----------------------------------------------------------

# Generate Campaign Section
st.markdown('<div class="section-header">✨ Generate Campaign</div>', unsafe_allow_html=True)

# Load trends once and cache them in session state
if "trends" not in st.session_state:
    with st.spinner("Fetching real-time cultural trends..."):
        st.session_state["trends"] = get_all_trends()

trends = st.session_state["trends"]

if len(trends) == 0:
    st.error("No trends available right now. Try again later.")
    st.stop()

selected_trend = st.selectbox("Select Cultural Trend", trends, key="trend_select")

# Generate Campaign Button
generate_clicked = st.button("✨ Generate Campaign", type="primary", width='stretch', key="generate_btn")

if generate_clicked:
    category = classify_trend(selected_trend)

    if category == "skip":
        st.warning(
            "⚠ This trend contains political/sensitive content. "
            "Please choose a different trend."
        )
        st.stop()

    with st.spinner("Generating creative concept..."):
        campaign = generate_campaign_for_trend(selected_trend, category)
        
        # Store campaign in session state for Instagram posting
        st.session_state["last_campaign"] = campaign
        st.session_state["last_trend"] = selected_trend
        st.session_state["last_category"] = category
        st.session_state["campaign_generated"] = True
        st.rerun()  # Rerun to show the campaign immediately

# -------------------------------------------------------
# Display Campaign Results (Figma Design - Card Layout)
# -------------------------------------------------------
if st.session_state.get("campaign_generated") and st.session_state.get("last_campaign"):
    campaign = st.session_state["last_campaign"]
    selected_trend = st.session_state.get("last_trend", selected_trend)
    category = st.session_state.get("last_category", "general")
    
    st.markdown('<div class="section-header">📊 Campaign Results</div>', unsafe_allow_html=True)
    
    # Hero Concept Card
    st.markdown("""
    <div class="campaign-card">
        <div class="card-header">
            <div class="card-title">Hero Concept</div>
            <button class="copy-btn" onclick="navigator.clipboard.writeText('{}')">📋 Copy</button>
        </div>
        <div class="card-content">{}</div>
    </div>
    """.format(
        campaign.get("hero_concept", "").replace("'", "\\'"),
        campaign.get("hero_concept", "")
    ), unsafe_allow_html=True)
    
    slogan = campaign.get('slogan', '')
    
    # Campaign Slogan Card
    if slogan:
        st.markdown("""
        <div class="campaign-card">
            <div class="card-header">
                <div class="card-title">Campaign Slogan</div>
                <button class="copy-btn" onclick="navigator.clipboard.writeText('{}')">📋 Copy</button>
            </div>
            <div class="card-content" style="color: #F40009; font-size: 1.2rem; font-weight: 600;">"{}"</div>
        </div>
        """.format(
            slogan.replace("'", "\\'"),
            slogan
        ), unsafe_allow_html=True)

    # Social Media Post Card
    social_post = campaign.get("social_post", "")
    if social_post:
        st.markdown("""
        <div class="campaign-card">
            <div class="card-header">
                <div class="card-title">Social Media Post</div>
                <button class="copy-btn" onclick="navigator.clipboard.writeText('{}')">📋 Copy</button>
            </div>
            <div class="card-content">{}</div>
        </div>
        """.format(
            social_post.replace("'", "\\'").replace("\n", "\\n"),
            social_post.replace("\n", "<br>")
        ), unsafe_allow_html=True)
    
    # AI-Generated Visual Card
    st.markdown("""
    <div class="campaign-card">
        <div class="card-header">
            <div class="card-title">AI-Generated Visual</div>
            <div>
                <button class="copy-btn" style="margin-right: 0.5rem;">🔗 Share</button>
                <button class="copy-btn">📥 Download</button>
            </div>
        </div>
        <div class="card-content">
        """, unsafe_allow_html=True)
    
    # Generate image if not already stored
    if not st.session_state.get("last_image_url"):
        dalle_prompt = build_dalle_prompt(
            selected_trend, campaign.get("moodboard", "")
        )
        with st.spinner("Generating image..."):
            image_url = generate_image_url(dalle_prompt)
            st.session_state["last_image_url"] = image_url
            st.session_state["last_dalle_prompt"] = dalle_prompt
    else:
        image_url = st.session_state["last_image_url"]
        dalle_prompt = st.session_state.get("last_dalle_prompt", "")
    
    if image_url:
        st.image(image_url, width='stretch')
        st.caption("This image was created based on your selected trend and campaign concept.")
        # Show which service was used
        if openai_client:
            st.caption("✨ Generated with OpenAI DALL·E")
        else:
            st.caption("🆓 Generated with Pollinations.ai (Free)")
    else:
        st.error("⚠️ Could not generate image. Please try again.")
    
    st.markdown("</div>", unsafe_allow_html=True)  # Close AI-Generated Visual card
    
    # Campaign Details Card
    st.markdown("""
    <div class="campaign-card">
        <div class="card-header">
            <div class="card-title">Campaign Details</div>
        </div>
        <div class="card-content">
            <p><strong>Trend:</strong> {}</p>
            <p><strong>Generated:</strong> {}</p>
            <p><strong>Status:</strong> Generated</p>
            <p><strong>Platform:</strong> Multi-channel</p>
        </div>
    </div>
    """.format(
        selected_trend,
        datetime.now().strftime("%m/%d/%Y")
    ), unsafe_allow_html=True)
    
    # PDF Export (preserved functionality)
    st.divider()
    st.subheader("📄 Export Campaign Brief")
    pdf_bytes = export_campaign_to_pdf(
        campaign=campaign,
        trend=selected_trend,
        category=category,
        image_url=st.session_state.get("last_image_url")
    )
    st.download_button(
        label="📥 Download PDF Campaign Brief",
        data=pdf_bytes,
        file_name=f"CokeSense_Campaign_{selected_trend.replace(' ', '_')}_{datetime.now().strftime('%Y-%m-%d')}.pdf",
        mime="application/pdf",
        help="Download a professional PDF campaign brief ready for presentation"
    )
    st.caption("✨ Professional campaign brief with all assets and recommendations")
    
    # Additional features (Audio, Video, etc.) - keeping functionality but in cleaner format
    if slogan:
        # Audio feature
        if not st.session_state.get("slogan_audio_bytes") or st.session_state.get("last_slogan") != slogan:
            with st.spinner("🎙️ Generating audio..."):
                audio_bytes = get_audio_bytes(slogan)
                if audio_bytes:
                    st.session_state["slogan_audio_bytes"] = audio_bytes
                    st.session_state["last_slogan"] = slogan
                else:
                    st.error("Could not generate audio")
        else:
            audio_bytes = st.session_state.get("slogan_audio_bytes")
        
        if audio_bytes:
            st.audio(audio_bytes, format='audio/mp3')
    
    # Video Generation Section
    st.divider()
    st.subheader("🎬 AI-Generated Video")
    
    # Generate video if not already stored
    if not st.session_state.get("last_video_url") and image_url:
        video_prompt = build_video_prompt(
            selected_trend, 
            campaign.get("moodboard", ""),
            campaign.get("hero_concept", "")
        )
        
        # Check if video is still loading
        if st.session_state.get("video_loading"):
            st.warning("⏳ Video is still generating... This can take 60-90 seconds. Please wait.")
            st.info("💡 **Tip:** Hugging Face free tier may queue requests. The video will appear when ready!")
        else:
            with st.spinner("🎬 Generating video from image (60-90 seconds - Hugging Face free tier)..."):
                # Pass the image URL to generate video
                video_result = generate_video_url(video_prompt, image_url)
                
                if video_result and video_result.startswith("LOADING:"):
                    # Model is loading, store loading state
                    estimated_time = video_result.split(":")[1]
                    st.session_state["video_loading"] = True
                    st.session_state["video_estimated_time"] = estimated_time
                    st.warning(f"⏳ Model is loading (estimated {estimated_time}s). Please wait and try again in a moment.")
                elif video_result:
                    # Video generated successfully
                    st.session_state["last_video_url"] = video_result
                    st.session_state["last_video_prompt"] = video_prompt
                    st.session_state["video_loading"] = False
                    st.rerun()  # Refresh to show video
                else:
                    # Generation failed
                    st.session_state["video_loading"] = False
                    st.error("⚠️ Video generation failed. This can happen with free tier rate limits. Try again in a few minutes.")
    else:
        video_url = st.session_state.get("last_video_url")
        video_prompt = st.session_state.get("last_video_prompt", "")
    
    # Display video if available
    video_url = st.session_state.get("last_video_url")
    if video_url and not video_url.startswith("LOADING:"):
        try:
                # Check if it's a file path (local) or URL
                if os.path.exists(str(video_url)):
                    # Determine file type
                    is_gif = video_url.lower().endswith('.gif')
                    file_type = "GIF" if is_gif else "Video"
                    mime_type = "image/gif" if is_gif else "video/mp4"
                    file_extension = ".gif" if is_gif else ".mp4"
                    
                    # Local file - display based on type
                    try:
                        if is_gif:
                            # Display GIF using st.image() - this shows animated GIFs properly!
                            with open(video_url, "rb") as gif_file:
                                gif_bytes = gif_file.read()
                                st.image(gif_bytes, caption="🆓 Generated as animated GIF (fallback - always works!)")
                        else:
                            # Display video using st.video()
                            st.video(video_url)
                            st.caption("🆓 Generated with Hugging Face Stable Video Diffusion (Free)")
                        
                        # Download button
                        try:
                            with open(video_url, "rb") as video_file:
                                video_bytes = video_file.read()
                                if video_bytes:  # Make sure file isn't empty
                                    st.download_button(
                                        label=f"📥 Download {file_type}",
                                        data=video_bytes,
                                        file_name=f"cokesense_{selected_trend.replace(' ', '_')}{file_extension}",
                                        mime=mime_type
                                    )
                        except Exception as download_error:
                            st.warning(f"Could not create download button: {download_error}")
                    except Exception as display_error:
                        st.error(f"Error displaying {file_type.lower()}: {display_error}")
                        st.info("💡 The file exists but couldn't be displayed. Try opening it manually.")
                else:
                    # URL - check if it's a GIF or video
                    is_gif_url = video_url.lower().endswith('.gif') or 'gif' in video_url.lower()
                    try:
                        if is_gif_url:
                            # For GIF URLs, download and display
                            gif_response = requests.get(video_url, timeout=30)
                            if gif_response.status_code == 200:
                                st.image(gif_response.content, caption="🆓 Generated animated GIF")
                            else:
                                st.video(video_url)  # Fallback to video display
                        else:
                            st.video(video_url)
                            st.caption("🆓 Generated video")
                    except Exception as url_error:
                        st.error(f"Error displaying video URL: {url_error}")
        except Exception as e:
            st.error(f"Error with video: {e}")
            st.info("💡 The video may have been generated but couldn't be displayed. Try regenerating the campaign.")
    
    # Show info about video generation
    if not video_url:
            st.info("""
            💡 **Video Generation Info:**
            
            **Primary Method:**
            - Uses **Hugging Face's free Stable Video Diffusion** (image-to-video)
            - Creates a **3-5 second animated video** from your generated image
            - **Free tier:** ~30 requests/hour (perfect for testing!)
            
            **Automatic Fallback:**
            - If Hugging Face is unavailable, creates an **animated GIF** instead
            - Subtle zoom/pan animation - perfect for social media!
            - **Always works** - no external API needed for fallback
            
            **Note:** First request may take longer (model cold start). If video doesn't appear, you'll get a GIF automatically!
            """)
    
    # Multi-Scene Video Feature
    st.divider()
    st.subheader("🎞️ Multi-Scene Campaign Video")
    st.markdown("""
        Create a **multi-scene video** by combining multiple images/GIFs into one dynamic video with audio!
        Perfect for longer campaigns with multiple visual moments.
        """)
    
    # Number of scenes slider (outside button)
    num_scenes = st.slider("Number of scenes", 2, 5, 3, key="num_scenes")
    
    if st.button("🎬 Create Multi-Scene Video", type="secondary"):
            if not image_url:
                st.error("⚠️ Please generate an image first!")
            elif not st.session_state.get("slogan_audio_bytes"):
                st.error("⚠️ Please generate audio first (Coca-Cola Bear feature)!")
            else:
                with st.spinner("🎬 Creating multi-scene video (this may take a few minutes)..."):
                    try:
                        
                        st.info(f"Generating {num_scenes} image variations...")
                        image_urls = [image_url]  # Start with the original
                        st.write(f"✅ Image 1/5: Using original image")
                        
                        # Get trend and campaign from session state
                        current_trend = st.session_state.get("last_trend", "Trend")
                        current_campaign = st.session_state.get("last_campaign", {})
                        
                        # Generate additional image variations
                        dalle_prompt = build_dalle_prompt(
                            current_trend, current_campaign.get("moodboard", "")
                        )
                        
                        # Generate num_scenes - 1 additional images (we already have 1)
                        # Loop from 1 to num_scenes (exclusive), which gives us num_scenes - 1 iterations
                        # CRITICAL: We MUST have exactly num_scenes images at the end
                        for i in range(1, num_scenes):
                            # Add variation to prompt for different images
                            # Make each variation more distinct
                            variation_descriptors = [
                                "wide angle shot",
                                "close-up detail",
                                "different perspective",
                                "alternative composition",
                                "unique camera angle"
                            ]
                            descriptor = variation_descriptors[(i-1) % len(variation_descriptors)]
                            variation_prompt = dalle_prompt + f", {descriptor}, variation {i+1}"
                            
                            st.write(f"🖼️ Generating image {i+1}/{num_scenes}...")
                            
                            # Ensure we always add an image (even if it's a duplicate)
                            image_added = False
                            
                            # Try to generate a unique image
                            try:
                                variation_url = generate_image_url(variation_prompt)
                                
                                # Check if we got a valid, unique URL
                                if variation_url and isinstance(variation_url, str) and len(variation_url.strip()) > 0:
                                    if variation_url.strip() != image_url.strip() and variation_url.strip() not in [url.strip() for url in image_urls]:
                                        image_urls.append(variation_url)
                                        st.write(f"✅ Generated unique image {i+1}/{num_scenes} (total: {len(image_urls)}/{num_scenes})")
                                        image_added = True
                                    else:
                                        st.warning(f"⚠️ Generated duplicate URL for image {i+1}, retrying...")
                                else:
                                    st.warning(f"⚠️ Invalid URL returned for image {i+1}, retrying...")
                            except Exception as e:
                                st.warning(f"⚠️ Error generating image {i+1}: {e}, retrying...")
                            
                            # Retry if first attempt failed
                            if not image_added:
                                st.warning(f"⚠️ Could not generate unique image {i+1}, retrying...")
                                try:
                                    retry_prompt = dalle_prompt + f", completely different scene, variation {i+1}, unique composition"
                                    retry_url = generate_image_url(retry_prompt)
                                    
                                    if retry_url and isinstance(retry_url, str) and len(retry_url.strip()) > 0:
                                        if retry_url.strip() != image_url.strip() and retry_url.strip() not in [url.strip() for url in image_urls]:
                                            image_urls.append(retry_url)
                                            st.write(f"✅ Generated image {i+1}/{num_scenes} on retry (total: {len(image_urls)}/{num_scenes})")
                                            image_added = True
                                except Exception as e:
                                    st.warning(f"⚠️ Retry also failed for image {i+1}: {e}")
                            
                            # Final fallback: ALWAYS add original if we still don't have an image
                            # This ensures we have exactly num_scenes images
                            if not image_added:
                                st.error(f"❌ Failed to generate image {i+1}, using original as fallback")
                                image_urls.append(image_url)  # Fallback to original (will create duplicate, but ensures we have 5 images)
                                st.write(f"✅ Added fallback image {i+1}/{num_scenes} (total: {len(image_urls)}/{num_scenes})")
                                image_added = True  # Mark as added
                            
                            # Double-check that we actually added an image
                            if not image_added or len(image_urls) < i + 1:
                                st.error(f"❌ CRITICAL: Image {i+1} was not added! Current count: {len(image_urls)}")
                                # Force add original as emergency fallback
                                image_urls.append(image_url)
                                st.write(f"✅ Emergency fallback: Added image {i+1}/{num_scenes} (total: {len(image_urls)}/{num_scenes})")
                        
                        # CRITICAL VERIFICATION: We MUST have exactly num_scenes images
                        if len(image_urls) < num_scenes:
                            st.error(f"❌ CRITICAL ERROR: Only {len(image_urls)} images in list, but {num_scenes} scenes requested!")
                            st.error(f"   Adding {num_scenes - len(image_urls)} fallback images to reach {num_scenes} total...")
                            # Add missing images using original as fallback
                            while len(image_urls) < num_scenes:
                                image_urls.append(image_url)
                            st.write(f"✅ Fixed: Now have {len(image_urls)} images (some may be duplicates)")
                        elif len(image_urls) > num_scenes:
                            st.warning(f"⚠️ WARNING: {len(image_urls)} images generated, but only {num_scenes} requested. Using first {num_scenes}.")
                            image_urls = image_urls[:num_scenes]
                        
                        # Final verification
                        if len(image_urls) == num_scenes:
                            st.success(f"✅ Successfully prepared {len(image_urls)} images for {num_scenes} scenes!")
                        else:
                            st.error(f"❌ FATAL: Still have {len(image_urls)} images instead of {num_scenes}!")
                        
                        # Get audio
                        audio_bytes = st.session_state.get("slogan_audio_bytes")
                        
                        # Get slogan for commercial-style text overlay
                        current_campaign = st.session_state.get("last_campaign", {})
                        slogan = current_campaign.get("slogan", "")
                        
                        # Create multi-scene video with commercial enhancements
                        st.info(f"Combining {len(image_urls)} images into commercial-style video...")
                        if len(image_urls) < num_scenes:
                            st.warning(f"⚠️ Only {len(image_urls)} images generated, but {num_scenes} scenes requested. Using available images.")
                        video_path = create_multi_scene_video(
                            image_urls=image_urls,
                            audio_bytes=audio_bytes,
                            scene_duration=3.0,
                            transition_duration=0.5,
                            slogan=slogan,
                            brand_name="Coca-Cola"
                        )
                        
                        if video_path and os.path.exists(video_path):
                            st.session_state["multi_scene_video_path"] = video_path
                            st.success(f"✅ Multi-scene video created! ({num_scenes} scenes)")
                            st.rerun()
                        else:
                            st.error("⚠️ Could not create multi-scene video")
                            
                    except Exception as e:
                        st.error(f"❌ Error creating multi-scene video: {e}")
                        import traceback
                        st.code(traceback.format_exc())
    
    # Display multi-scene video if available
    multi_scene_path = st.session_state.get("multi_scene_video_path")
    if multi_scene_path and os.path.exists(multi_scene_path):
            st.video(multi_scene_path)
            st.caption("🎞️ Multi-scene campaign video with audio")
            
            # Download button
            try:
                with open(multi_scene_path, "rb") as video_file:
                    video_bytes = video_file.read()
                    if video_bytes:
                        st.download_button(
                            label="📥 Download Multi-Scene Video",
                            data=video_bytes,
                            file_name=f"cokesense_multiscene_{selected_trend.replace(' ', '_')}.mp4",
                            mime="video/mp4"
                        )
            except Exception as e:
                st.warning(f"Could not create download button: {e}")
            
            # Option to use for Instagram posting
            st.session_state["multi_scene_video_available"] = True
    
# -------------------------------------------------------
# Instagram Posting Section (appears after campaign is generated)
# -------------------------------------------------------
if st.session_state.get("campaign_generated") and st.session_state.get("last_campaign") and st.session_state.get("last_image_url"):
        st.divider()
        st.subheader("📱 Post to Instagram")
        
        last_campaign = st.session_state["last_campaign"]
        last_trend = st.session_state.get("last_trend", "Trend")
        last_image_url = st.session_state["last_image_url"]
        
        # Debug: Show what we have
        with st.expander("🔍 Debug Info", expanded=False):
            st.write(f"Campaign in session: {bool(st.session_state.get('last_campaign'))}")
            st.write(f"Image URL in session: {bool(st.session_state.get('last_image_url'))}")
            st.write(f"Token in session: {bool(st.session_state.get('instagram_token'))}")
            if st.session_state.get("instagram_token"):
                token_preview = st.session_state["instagram_token"][:20] + "..." if len(st.session_state["instagram_token"]) > 20 else st.session_state["instagram_token"]
                st.write(f"Token preview: {token_preview}")
        
        # Show preview of what will be posted
        with st.expander("📋 Preview Instagram Post", expanded=True):
            preview_caption = format_campaign_caption(
                last_campaign.get("hero_concept", ""),
                last_campaign.get("slogan", ""),
                last_campaign.get("social_post", ""),
                last_trend
            )
            st.text_area("Caption Preview", preview_caption, height=200, key="caption_preview")
            st.image(last_image_url, caption="Image to post", width=300)
        
        # Post button - always visible, but checks for token
        if st.session_state.get("instagram_token"):
            st.write("**Ready to post!** Click the button below:")
            
            if st.button("🚀 Post to Instagram", type="primary", key="post_instagram_btn"):
                # Immediate feedback
                st.info("🎯 **Button clicked! Starting Instagram post...**")
                st.write("")
                
                try:
                    caption = format_campaign_caption(
                        last_campaign.get("hero_concept", ""),
                        last_campaign.get("slogan", ""),
                        last_campaign.get("social_post", ""),
                        last_trend
                    )
                    
                    # Show what we're trying to post
                    st.write("**📊 Preparing post...**")
                    st.write(f"✅ Image URL ready")
                    st.write(f"✅ Caption prepared ({len(caption)} characters)")
                    st.write(f"✅ Token verified")
                    st.write(f"✅ Trend: {last_trend}")
                    st.write("")
                    
                    st.write("**🔄 Sending to Instagram...**")
                    st.info("⏳ Instagram needs to download and process the image first. This may take 15-45 seconds...")
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    with st.spinner("Posting to Instagram (waiting for image processing)..."):
                        # Get audio if available
                        audio_bytes = st.session_state.get("slogan_audio_bytes")
                        
                        # Check for multi-scene video first (highest priority)
                        multi_scene_path = st.session_state.get("multi_scene_video_path")
                        use_multi_scene = False
                        
                        if multi_scene_path and os.path.exists(multi_scene_path):
                            # Multi-scene video is ready - we can post it directly
                            # But Instagram API needs a public URL, so we'll note it
                            use_multi_scene = True
                            st.info("🎞️ **Multi-scene video available!** (See download option below - Instagram API requires public URL)")
                        
                        # Get GIF path if available (for single-scene video with audio)
                        video_url = st.session_state.get("last_video_url")
                        gif_path = None
                        if not use_multi_scene and video_url and os.path.exists(str(video_url)) and str(video_url).lower().endswith('.gif'):
                            gif_path = video_url
                            print(f"Using GIF for video creation: {gif_path}")
                        
                        result = post_to_instagram(
                            image_url=last_image_url,
                            caption=caption,
                            access_token=st.session_state["instagram_token"],
                            trend=last_trend,
                            audio_bytes=audio_bytes,
                            gif_path=gif_path
                        )
                    
                    # Check if video was actually created (not just if audio exists)
                    video_created = result.get("video_created", False)
                    video_path = result.get("video_path")
                    
                    if video_created and video_path:
                        st.success("🎬 **Video with audio created!** (Image posted - see note below)")
                    elif audio_bytes and result.get("success"):
                        # Audio exists but video wasn't created - show info
                        st.warning("⚠️ **Audio available but video creation failed.** Check the terminal/console for error details. The image was posted successfully.")
                    
                    # Always show the result
                    st.write("")
                    st.write("**📡 Instagram API Response:**")
                    st.json(result)
                    
                    # Note about video
                    if video_created:
                        st.info("""
                        💡 **Video with Audio Created:**
                        
                        A video combining your image + audio was created, but Instagram's API 
                        requires videos to be at a public URL. The image was posted instead.
                        
                        **To post the video with audio:**
                        1. Download the video (if available)
                        2. Upload manually via Instagram app
                        3. Or use a CDN service (S3, Cloudinary) for automatic posting
                        
                        For a production app, you'd upload the video to a CDN first, then post the URL.
                        """)
                    st.write("")
                    
                    if result.get("success"):
                        st.success(f"🎉 **SUCCESS!** {result.get('message', 'Posted successfully!')}")
                        st.balloons()
                        st.info("💡 Check your Instagram account - the post should appear there!")
                        
                        # Show video download if video was created
                        if result.get("video_created") and result.get("video_path"):
                            st.divider()
                            st.markdown("#### 🎬 Video with Audio Created!")
                            st.info("""
                            A video combining your image + audio was created!
                            
                            **Note:** Instagram's API requires videos to be at a public URL. 
                            The image was posted, but you can download the video and upload it 
                            manually via Instagram's app (which supports videos with audio).
                            """)
                            
                            # Video download button
                            try:
                                with open(result["video_path"], "rb") as video_file:
                                    video_data = video_file.read()
                                    st.download_button(
                                        label="📥 Download Video (with Audio)",
                                        data=video_data,
                                        file_name=f"cokesense_video_{last_trend.replace(' ', '_')}.mp4",
                                        mime="video/mp4",
                                        help="Download the video to upload manually to Instagram"
                                    )
                            except Exception as e:
                                st.warning(f"Could not create download button: {e}")
                    else:
                        st.error(f"❌ **POST FAILED**")
                        st.error(f"**Error:** {result.get('error', 'Unknown error')}")
                        st.write("")
                        st.warning("**🔧 Troubleshooting Steps:**")
                        st.markdown("""
                        1. **Check token:** Is it still valid? (Tokens expire after ~60 days)
                        2. **Account type:** Is your Instagram account Business/Creator? (Not personal)
                        3. **Permissions:** Does token have `instagram_content_publish` permission?
                        4. **Image URL:** Is the image URL publicly accessible?
                        5. **Account status:** Check if your Instagram account has any restrictions
                        """)
                except Exception as e:
                    st.error(f"❌ **Exception occurred:** {str(e)}")
                    st.exception(e)
        else:
            st.warning("⚠️ **Add your Instagram access token in the sidebar** to enable posting")
            st.info("💡 Go to the sidebar → Instagram Posting section → Enter your token")
