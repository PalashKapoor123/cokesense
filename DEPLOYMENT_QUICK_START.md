# 🚀 Quick Deployment Guide - Get Your Shareable Link!

**Goal:** Deploy CokeSense so Pratik Thakar (or anyone) can test it via a link.

**Time:** 10 minutes | **Cost:** FREE

---

## Step 1: Create GitHub Repository (2 min)

1. Go to: https://github.com/new
2. Repository name: `cokesense`
3. Description: "AI-Powered Coca-Cola Marketing Campaign Generator"
4. Make it **Public** ✅ (required for free Streamlit Cloud)
5. **Don't** check "Add a README" (you already have one)
6. Click **"Create repository"**

---

## Step 2: Push Your Code to GitHub (3 min)

**Open terminal in your project folder** (`/Users/palashkapoor/Desktop/cokesense`) and run:

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: CokeSense AI Marketing Platform"

# Add your GitHub repository (REPLACE YOUR_USERNAME with your actual GitHub username!)
git remote add origin https://github.com/YOUR_USERNAME/cokesense.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**⚠️ Important:** Replace `YOUR_USERNAME` with your actual GitHub username!

---

## Step 3: Deploy to Streamlit Cloud (3 min)

1. Go to: https://share.streamlit.io/
2. Click **"Sign in"** → Sign in with **GitHub**
3. Click **"New app"**
4. Fill in:
   - **Repository**: Select `YOUR_USERNAME/cokesense`
   - **Branch**: `main`
   - **Main file path**: `streamlit_app.py`
   - **App URL**: `cokesense` (or your choice - this becomes part of your link)
5. Click **"Deploy"**

**Wait 2-3 minutes for deployment...**

---

## Step 4: Get Your Shareable Link! 🎉

Once deployed, you'll get a link like:
```
https://YOUR_USERNAME-cokesense.streamlit.app
```

**This is your shareable link!** Copy it and send it to Pratik Thakar.

---

## Step 5: Add API Keys (Optional - 2 min)

The app works without keys (uses free Pollinations.ai), but for full AI features:

1. In Streamlit Cloud, click on your app
2. Click **"⚙️ Settings"** (top right)
3. Click **"Secrets"** tab
4. Add this (replace with your actual keys):

```
OPENAI_API_KEY=your_openai_key_here
GROQ_API_KEY=your_groq_key_here
```

5. Click **"Save"**
6. App will automatically restart

---

## ✅ That's It!

Your app is now live at: `https://YOUR_USERNAME-cokesense.streamlit.app`

**Anyone with this link can:**
- Generate campaigns
- Create videos
- Use all features
- Test everything

**Perfect for your internship application! 🥤✨**

---

## 🐛 Troubleshooting

**"Repository not found"**
- Make sure repository is **public**
- Check you selected the right repository

**"App failed to deploy"**
- Check that `streamlit_app.py` is in the root folder
- Verify `requirements.txt` has all dependencies

**"Module not found error"**
- Check Streamlit Cloud logs (click on your app → "Manage app" → "Logs")

---

## 📧 Email Template for Pratik Thakar

```
Subject: CokeSense - AI Marketing Campaign Generator Demo

Hi Pratik,

I've built CokeSense, an AI-powered marketing campaign generator that creates 
complete Coca-Cola campaigns from real-time trends.

Live Demo: https://YOUR_USERNAME-cokesense.streamlit.app

The app generates:
- Hero concepts and slogans
- Social media posts
- AI-generated visuals
- Multi-scene commercial videos with audio
- Instagram posting with analytics

Feel free to test it out!

Best,
[Your Name]
```

