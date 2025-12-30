# 🚀 Groq AI Setup (Free!)

## How to Get Your Free Groq API Key

1. **Go to**: https://console.groq.com
2. **Sign up** with your email (or Google/GitHub)
3. **Navigate to**: API Keys section
4. **Click**: "Create API Key"
5. **Copy** your API key (starts with `gsk_...`)

## Add to Your .env File

Open your `.env` file and replace the placeholder:

```
GROQ_API_KEY=gsk_your_actual_key_here
```

## That's It! 🎉

Your app will now use **free AI generation** via Groq!

## How It Works

- **Priority 1**: OpenAI (if you have a key) - Best quality, costs money
- **Priority 2**: Groq (if you have a key) - Great quality, **FREE!**
- **Priority 3**: Demo mode - Template-based, no AI

## Benefits of Groq

✅ **100% Free** (generous rate limits)  
✅ **Super Fast** (faster than OpenAI)  
✅ **Great Quality** (uses Llama 3.1)  
✅ **No Credit Card Required**

## Test It

After adding your key, restart Streamlit:
```bash
python -m streamlit run streamlit_app.py
```

You should see "🤖 **AI Mode: Groq**" in the sidebar!

