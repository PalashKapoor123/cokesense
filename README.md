# 🥤 CokeSense: Real-Time Coca-Cola Creative Engine

> **AI-Powered Marketing Campaign Generator** | Transform real-time cultural trends into personalized Coca-Cola marketing campaigns with multi-modal AI content generation.

---

## 🎯 Overview

CokeSense is an end-to-end AI marketing automation platform that generates complete Coca-Cola campaigns from real-time trends. It creates hero concepts, slogans, social posts, AI-generated visuals, multi-scene commercial videos with audio, and automatically posts to Instagram with analytics tracking.

### Key Features

- **🎨 Multi-Modal AI Content Generation**
  - Text generation using OpenAI GPT-4o-mini or Groq Llama 3.3
  - Image generation via DALL-E 3 or free Pollinations.ai
  - Video generation with animated GIFs
  - Text-to-speech audio for slogans

- **📊 Real-Time Trend Analysis**
  - Google Trends integration
  - X (Twitter) trending topics
  - Cultural events calendar
  - Automatic trend classification

- **🎬 Commercial Video Creation**
  - Multi-scene video generation (2-5 scenes)
  - Brand intro/outro screens
  - Audio synchronization
  - Zoom/ken burns effects
  - Instagram-optimized format (1080x1080)

- **📱 Social Media Integration**
  - Direct Instagram posting via Graph API
  - Automated caption formatting
  - Post history tracking
  - Real-time analytics (likes, comments, reach, engagement)

- **📄 Professional Export**
  - PDF campaign briefs
  - Branded document templates
  - Executive summaries
  - Asset recommendations

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Instagram Business/Creator account (for posting)
- API keys (optional - free tier available):
  - Groq API key (free) - for AI text generation
  - OpenAI API key (paid) - for premium text/image generation

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd cokesense
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys (optional)
   ```

4. **Run the application**
   ```bash
   streamlit run streamlit_app.py
   ```

5. **Access the app**
   - Open your browser to `http://localhost:8501`

---

## 📋 Features in Detail

### 1. Campaign Generation
- Select from real-time trends or cultural events
- Generate personalized campaigns with:
  - Hero creative concept
  - Catchy slogan
  - Social media post copy
  - Visual moodboard description
  - AI-generated images

### 2. Multi-Scene Video Creation
- Generate 2-5 unique image variations
- Create animated GIFs from images
- Combine into commercial-style video with:
  - Brand intro screen (Coca-Cola logo)
  - Multiple scene transitions
  - Zoom/ken burns effects
  - Slogan outro screen
  - Synchronized audio

### 3. Instagram Automation
- One-click posting to Instagram
- Automatic caption formatting
- Video/image optimization
- Post history database
- Real-time analytics dashboard

### 4. Analytics & Tracking
- Track all posted campaigns
- View engagement metrics:
  - Likes, comments, reach
  - Engagement rate
  - Post performance trends
- Filter deleted posts
- Export analytics data

### 5. Professional Export
- Generate PDF campaign briefs
- Branded document templates
- Executive summaries
- Asset recommendations
- Ready for client presentation

---

## 🛠 Technical Architecture

### Tech Stack
- **Frontend**: Streamlit (Python web framework)
- **AI/ML**: 
  - OpenAI GPT-4o-mini, DALL-E 3
  - Groq Llama 3.3 (free alternative)
  - Google Text-to-Speech (gTTS)
- **APIs**: 
  - Instagram Graph API
  - Google Trends API
  - Pollinations.ai (free image generation)
- **Data**: SQLite (local post history)
- **Media Processing**: 
  - MoviePy (video editing)
  - Pillow (image/GIF generation)
  - ReportLab (PDF generation)

### Project Structure
```
cokesense/
├── app/
│   ├── config.py              # API configuration
│   ├── trend_fetcher.py       # Trend data collection
│   ├── trend_classifier.py    # Trend categorization
│   ├── creative_engine.py     # AI text generation
│   ├── visual_engine.py       # Image/video generation
│   ├── instagram_poster.py    # Social media posting
│   ├── post_history.py        # Analytics & tracking
│   ├── pdf_exporter.py        # PDF generation
│   ├── audio_generator.py     # Text-to-speech
│   ├── video_creator.py       # Single video creation
│   └── multi_scene_video.py   # Commercial video creation
├── data/
│   └── events.json            # Cultural events database
├── streamlit_app.py           # Main application
├── requirements.txt           # Dependencies
└── README.md                  # This file
```

### Key Design Decisions

1. **Multi-Provider AI Support**: Prioritizes free options (Groq) with fallback to paid (OpenAI) and demo mode
2. **Robust Error Handling**: Comprehensive fallbacks for API failures, timeouts, and edge cases
3. **Session State Management**: Persistent campaign data across page interactions
4. **Modular Architecture**: Separated concerns for easy maintenance and extension

---

## 💼 Business Value

### For Coca-Cola Marketing Teams

1. **Rapid Prototyping**: Generate 10-20 campaign concepts in minutes
2. **Local Market Personalization**: Create region-specific campaigns at scale
3. **Trend Responsiveness**: Capitalize on viral trends within hours
4. **A/B Testing**: Generate multiple variations for performance testing
5. **Cost Efficiency**: Reduce agency costs for smaller campaigns
6. **Content Pipeline**: Maintain consistent social media presence

### Use Cases

- **Event-Driven Campaigns**: Automatically generate campaigns for sports events, holidays, cultural moments
- **Multi-Market Launch**: Create personalized campaigns for 50+ markets simultaneously
- **Rapid Iteration**: Test multiple concepts before agency involvement
- **Social Media Management**: Maintain daily/weekly posting schedule with personalized content

---

## 🎓 Learning Outcomes

This project demonstrates:

- **Full-Stack AI Integration**: Orchestrating multiple AI models and APIs
- **Real-World API Integration**: Instagram Graph API, error handling, retry logic
- **Media Processing**: Video creation, audio synchronization, image manipulation
- **Database Design**: SQLite for local data persistence
- **Production Engineering**: Error handling, fallbacks, user experience optimization
- **Business Acumen**: Understanding marketing workflows and campaign creation

---

## 📸 Screenshots

*Add screenshots of your app here:*
- Main dashboard
- Campaign generation
- Video creation
- Analytics dashboard
- PDF export

---

## 🔮 Future Enhancements

- [ ] Multi-brand support (Sprite, Fanta, etc.)
- [ ] Brand guideline enforcement (colors, fonts, tone)
- [ ] Approval workflow (manager review before posting)
- [ ] Performance prediction (which campaigns might perform best)
- [ ] Multi-platform posting (TikTok, Twitter, Facebook)
- [ ] A/B testing framework
- [ ] Voice cloning for authentic Coca-Cola bear voice
- [ ] Real-time collaboration features

---

## 📝 License

This project is a portfolio piece for educational purposes.

---

## 👤 Author

**Palash Kapoor**
- Built for Coca-Cola Generative AI Internship Application
- Demonstrating end-to-end AI marketing automation capabilities

---

## 🙏 Acknowledgments

- Coca-Cola for brand inspiration
- OpenAI, Groq, and Pollinations.ai for AI services
- Streamlit for the amazing framework
- Meta for Instagram Graph API

---

## 📧 Contact

For questions or feedback, please reach out via [your contact method].

---

**Built with ❤️ for Coca-Cola's Real Magic**
