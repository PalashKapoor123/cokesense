# 🚀 Deploy CokeSense to Streamlit Cloud

Make your app accessible via a shareable link in 10 minutes!

---

## Step 1: Push to GitHub

### 1.1 Create GitHub Repository
1. Go to https://github.com/new
2. Repository name: `cokesense` (or your choice)
3. Make it **Public** (required for free Streamlit Cloud)
4. Click "Create repository"

### 1.2 Push Your Code
```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: CokeSense AI Marketing Platform"

# Add remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/cokesense.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**Important**: Make sure `.env` is in `.gitignore` (it should be - we created it!)

---

## Step 2: Deploy to Streamlit Cloud

### 2.1 Sign Up / Sign In
1. Go to https://streamlit.io/cloud
2. Click "Sign up" or "Sign in"
3. Sign in with your GitHub account

### 2.2 Deploy Your App
1. Click "New app"
2. Select your repository: `YOUR_USERNAME/cokesense`
3. Branch: `main`
4. Main file path: `streamlit_app.py`
5. App URL: `cokesense` (or your choice - this becomes your link)
6. Click "Deploy"

### 2.3 Add Environment Variables (Optional)
1. Click on your deployed app
2. Click "Settings" (⚙️ icon)
3. Go to "Secrets"
4. Add your API keys:
   ```
   OPENAI_API_KEY=your_key_here
   GROQ_API_KEY=your_key_here
   ```
5. Click "Save"

**Note**: The app works without API keys (demo mode), but AI text generation needs at least one key.

---

## Step 3: Share Your Link!

Once deployed, you'll get a link like:
```
https://YOUR_USERNAME-cokesense.streamlit.app
```

**Share this link** - anyone can access your app!

---

## 🎯 Quick Deployment Checklist

- [ ] Code pushed to GitHub (public repository)
- [ ] Streamlit Cloud account created
- [ ] App deployed to Streamlit Cloud
- [ ] Environment variables added (optional)
- [ ] App tested via the public link
- [ ] Link shared in application materials

---

## 💡 Pro Tips

1. **Free Tier**: Streamlit Cloud free tier is perfect for demos
2. **Custom Domain**: You can add a custom domain later if needed
3. **Updates**: Every time you push to GitHub, Streamlit Cloud auto-updates
4. **Secrets**: Never commit API keys - use Streamlit Cloud's Secrets feature

---

## 🐛 Troubleshooting

**Issue**: "App failed to deploy"  
**Solution**: Check that `streamlit_app.py` is in the root directory

**Issue**: "Module not found"  
**Solution**: Ensure `requirements.txt` has all dependencies

**Issue**: "API keys not working"  
**Solution**: Add them in Streamlit Cloud Settings → Secrets

---

## 📧 Update Your Application

Once deployed, update your application materials:

**In your email/cover letter:**
"Live Demo: https://YOUR_USERNAME-cokesense.streamlit.app"

**In your resume:**
"Deployed at: [link]" or "Live demo available at: [link]"

---

**That's it! Your app is now accessible to anyone with the link! 🎉**
