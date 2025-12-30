# 🚀 Deploy CokeSense - Get Your Shareable Link!

Deploy your app to Streamlit Cloud in 5 steps. **It's FREE and takes 10 minutes!**

---

## 🎯 What You'll Get

A link like: `https://yourname-cokesense.streamlit.app`

**Anyone can click this link and use your app!**

---

## Step 1: Create GitHub Repository (2 minutes)

1. Go to https://github.com/new
2. Repository name: `cokesense`
3. Description: "AI-Powered Coca-Cola Marketing Campaign Generator"
4. Make it **Public** (required for free Streamlit Cloud)
5. **Don't** initialize with README (you already have one)
6. Click "Create repository"

---

## Step 2: Push Code to GitHub (3 minutes)

Open terminal in your project folder and run:

```bash
# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: CokeSense AI Marketing Platform"

# Add your GitHub repository (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/cokesense.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**Replace `YOUR_USERNAME` with your actual GitHub username!**

---

## Step 3: Deploy to Streamlit Cloud (3 minutes)

1. Go to https://share.streamlit.io/
2. Click "Sign in" → Sign in with **GitHub**
3. Click "New app"
4. Fill in:
   - **Repository**: Select `YOUR_USERNAME/cokesense`
   - **Branch**: `main`
   - **Main file path**: `streamlit_app.py`
   - **App URL**: `cokesense` (or your choice)
5. Click "Deploy"

**Wait 2-3 minutes for deployment...**

---

## Step 4: Add API Keys (Optional - 2 minutes)

The app works without keys, but for full AI features:

1. In Streamlit Cloud, click on your app
2. Click "⚙️ Settings" (top right)
3. Click "Secrets" tab
4. Add this (replace with your actual keys):

```
OPENAI_API_KEY=your_openai_key_here
GROQ_API_KEY=your_groq_key_here
```

4. Click "Save"
5. App will automatically restart

---

## Step 5: Share Your Link! 🎉

You'll get a link like:
```
https://YOUR_USERNAME-cokesense.streamlit.app
```

**Copy and paste this link anywhere!**

---

## ✅ Quick Checklist

- [ ] GitHub repository created (public)
- [ ] Code pushed to GitHub
- [ ] Streamlit Cloud account created
- [ ] App deployed
- [ ] API keys added (optional)
- [ ] Link tested and working
- [ ] Link added to application materials

---

## 🎯 Update Your Application

**In your email to Pratik Thakar:**

> "Live Demo: https://YOUR_USERNAME-cokesense.streamlit.app"

**In your resume:**

> "Deployed at: [link]"

---

## 💡 Pro Tips

1. **Auto-Updates**: Every time you push to GitHub, Streamlit Cloud auto-updates your app
2. **Free Forever**: Streamlit Cloud free tier is perfect for demos
3. **No Credit Card**: Completely free, no payment needed
4. **Custom Domain**: Can add custom domain later if needed

---

## 🐛 Troubleshooting

**"Repository not found"**
- Make sure repository is **public**
- Check you selected the right repository

**"App failed to deploy"**
- Check that `streamlit_app.py` is in the root folder
- Verify `requirements.txt` has all dependencies

**"Module not found error"**
- Make sure all packages are in `requirements.txt`
- Check Streamlit Cloud logs for specific errors

---

## 🎬 That's It!

Your app is now live and shareable. Anyone with the link can:
- Generate campaigns
- Create videos
- See the analytics
- Use all features

**Perfect for your internship application! 🥤✨**

