# 🚀 Quick Start Guide

Get CokeSense running in 5 minutes!

## Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

## Step 2: Set Up API Keys (Optional)
1. Copy `.env.example` to `.env`
2. Add your Groq API key (free): https://console.groq.com/keys
   - Or use OpenAI API key (paid): https://platform.openai.com/api-keys
3. **Note**: App works in demo mode without keys!

## Step 3: Run the App
```bash
streamlit run streamlit_app.py
```

## Step 4: Open in Browser
Navigate to: `http://localhost:8501`

## That's It! 🎉

The app will:
- ✅ Work in demo mode (no API keys needed)
- ✅ Generate campaigns from trends
- ✅ Create images (free via Pollinations.ai)
- ✅ Generate videos and audio

**For full AI text generation**, add a Groq API key (free tier available).

---

## Troubleshooting

**Issue**: "Module not found"  
**Solution**: `pip install -r requirements.txt`

**Issue**: Images not generating  
**Solution**: Check internet connection, Pollinations.ai may be slow

**Issue**: Video creation fails  
**Solution**: Ensure MoviePy is installed: `pip install moviepy`

---

## Next Steps

- Read `README.md` for full documentation
- Check `DEMO_GUIDE.md` for demo script
- See `PROJECT_SUMMARY.md` for project overview

**Happy campaigning! 🥤**

