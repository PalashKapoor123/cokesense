# 🚀 Get Started - Make Your App 100% Functional

## ✅ Quick Setup Checklist

### Step 1: Get Your Free Groq API Key (5 minutes)

1. **Go to**: https://console.groq.com
2. **Sign up** (email, Google, or GitHub - all free)
3. **Click**: "API Keys" in the sidebar
4. **Click**: "Create API Key"
5. **Copy** your key (starts with `gsk_...`)

### Step 2: Add Key to .env File

Open `.env` file and update:

```
GROQ_API_KEY=gsk_your_actual_key_here
```

**Important**: Replace `gsk_your_actual_key_here` with your real key!

### Step 3: Restart Streamlit

If Streamlit is running:
1. Press `Ctrl+C` to stop it
2. Run: `python -m streamlit run streamlit_app.py`

### Step 4: Test Everything

1. **Open**: http://localhost:8501
2. **Check sidebar**: Should show "🤖 **AI Mode: Groq**"
3. **Select a trend**: e.g., "Christmas"
4. **Click**: "✨ Generate Coca-Cola Campaign"
5. **Verify**:
   - ✅ Text content appears (AI-generated, not templates)
   - ✅ Image appears (free Pollinations.ai)
   - ✅ All sections filled: Hero, Slogan, Social Post, Moodboard

## 🎯 What You'll Get

### With Groq API Key:
- ✅ **Free AI text generation** (14,400 requests/day)
- ✅ **Free AI image generation** (unlimited)
- ✅ **Real AI content** (not templates)
- ✅ **Full campaigns** (text + visuals)

### Without Groq Key (Demo Mode):
- ✅ **Template-based text** (still works)
- ✅ **Free AI images** (Pollinations.ai)
- ⚠️ **Limited variety** (same templates)

## 🔧 Troubleshooting

### "Demo Mode" still showing?
- Check `.env` file has correct key (no extra spaces)
- Restart Streamlit after adding key
- Key should start with `gsk_`

### Images not loading?
- Pollinations generates on-demand (10-30 seconds)
- Check internet connection
- Try refreshing the page

### No trends showing?
- Run: `python test_trends.py` to test trend fetching
- Check internet connection
- Trends update from real-time sources

## 📁 Project Structure

```
cokesense/
├── app/
│   ├── config.py          # API keys & clients
│   ├── trend_fetcher.py   # Gets trends (Google, X, Events)
│   ├── trend_classifier.py # Categorizes trends
│   ├── creative_engine.py # Generates text (Groq/OpenAI)
│   └── visual_engine.py   # Generates images (Pollinations/OpenAI)
├── data/
│   └── events.json        # Cultural events
├── streamlit_app.py       # Main UI
├── .env                   # Your API keys (keep secret!)
└── requirements.txt       # Dependencies
```

## 🎉 You're Done!

Once you add your Groq key, your app is **100% functional** with:
- ✅ Free AI text generation
- ✅ Free AI image generation  
- ✅ Real-time trend fetching
- ✅ Full campaign generation

**Enjoy your free AI-powered Coca-Cola campaign generator!** 🥤✨

