# 🆓 Free AI Setup Guide

## Complete Free AI Setup (Text + Images)

Your app now supports **100% free AI generation** for both text and images!

## What You Get

### ✅ Free Text Generation (Groq)
- Hero concepts
- Slogans  
- Social posts
- Moodboards

### ✅ Free Image Generation (Pollinations.ai)
- AI-generated visuals
- No API key needed
- High-quality images

## Setup Steps

### Step 1: Get Groq API Key (Free)

1. Go to: https://console.groq.com
2. Sign up (free, no credit card)
3. Create API key
4. Copy your key (starts with `gsk_...`)

### Step 2: Add to .env File

Open `.env` and add:

```
GROQ_API_KEY=gsk_your_actual_key_here
```

**Note:** You don't need an OpenAI key for images anymore - Pollinations.ai is free!

### Step 3: Restart Streamlit

```bash
python -m streamlit run streamlit_app.py
```

## How It Works

### Text Generation Priority:
1. **OpenAI** (if you have a key) - Paid, best quality
2. **Groq** (if you have a key) - **FREE**, great quality ⭐
3. **Demo Mode** - Templates, no AI

### Image Generation Priority:
1. **OpenAI DALL·E** (if you have a key) - Paid, best quality
2. **Pollinations.ai** - **FREE**, good quality ⭐

## What You'll See

- **With Groq key**: "🤖 **AI Mode: Groq**" + "✅ Free AI text generation ✅ Free AI image generation"
- **Without keys**: Demo mode (templates) + Free images still work!

## Benefits

✅ **100% Free** - No credit card needed  
✅ **Real AI** - Not templates  
✅ **Fast** - Groq is super fast  
✅ **Images Included** - Free image generation  

## Troubleshooting

**Images not loading?**
- Pollinations generates on-demand, may take 10-30 seconds
- Check your internet connection
- Try refreshing the page

**Text not generating?**
- Make sure Groq API key is in `.env`
- Restart Streamlit after adding key
- Check key starts with `gsk_`

Enjoy your free AI-powered Coca-Cola campaign generator! 🥤✨

