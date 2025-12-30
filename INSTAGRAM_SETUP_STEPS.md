# 📱 Instagram Auto-Posting Setup - Step by Step

## Quick Overview

This guide will help you set up Instagram auto-posting for your CokeSense app. You'll need:
- An Instagram account (can be a throwaway for testing)
- A Meta Developer account (free)
- About 15-20 minutes

---

## Step 1: Convert Instagram Account to Business/Creator

**Why:** Instagram API only works with Business or Creator accounts, not personal accounts.

### Steps:
1. Open Instagram app on your phone
2. Go to your **Profile** (bottom right)
3. Tap the **☰ menu** (top right)
4. Go to **Settings** → **Account**
5. Scroll down and tap **Switch to Professional Account**
6. Choose **Business** or **Creator** (both work)
7. Follow the prompts to complete setup
8. **Optional:** Keep account **Private** for testing

✅ **Done when:** Your account shows "Business" or "Creator" in settings

---

## Step 2: Create Meta Developer Account

**Why:** You need this to create an app and get API access.

### Steps:
1. Go to [Meta for Developers](https://developers.facebook.com/)
2. Click **Get Started** (or **Log In** if you have a Facebook account)
3. Sign in with your Facebook account (or create one - it's free)
4. Complete the developer registration:
   - Accept terms
   - Verify your email
   - Add phone number (for security)

✅ **Done when:** You can access the Meta Developer dashboard

---

## Step 3: Create a Meta App

**Why:** You need an app to get Instagram API access.

### Steps:
1. In Meta Developer dashboard, click **My Apps** (top right)
2. Click **Create App**
3. Choose app type:
   - Select **Business** (recommended)
   - Click **Next**
4. Fill in app details:
   - **App Name:** `CokeSense` (or any name)
   - **App Contact Email:** Your email
   - **Business Account:** (optional, can skip)
   - Click **Create App**

✅ **Done when:** You see your app dashboard

---

## Step 4: Add Instagram Product

**Why:** This enables Instagram API features.

### Steps:
1. In your app dashboard, find **Add Products** section
2. Look for **Instagram** product
3. Click **Set Up** next to Instagram
4. You'll see Instagram Graph API options
5. **Note:** You may see a warning about app review - that's OK for testing

✅ **Done when:** Instagram appears in your app's product list

---

## Step 5: Get Instagram Access Token

**Why:** This token lets your app post to Instagram.

### Option A: Using Graph API Explorer (Easiest for Testing)

1. In your app dashboard, go to **Tools** → **Graph API Explorer**
2. At the top:
   - **User or Page:** Select your app
   - **Permissions:** Click **Get Token** → **Get User Access Token**
3. In the popup:
   - Check these permissions:
     - `instagram_basic`
     - `pages_show_list`
     - `instagram_content_publish`
   - Click **Generate Access Token**
4. **Important:** You'll need to:
   - Connect your Instagram Business account
   - Authorize the app
5. Copy the token that appears (starts with something like `IGQW...`)

### Option B: Using Instagram Basic Display API

1. In your app dashboard, go to **Products** → **Instagram** → **Basic Display**
2. Click **Create New App**
3. Add **Valid OAuth Redirect URIs:** `https://localhost:8501` (or your domain)
4. Add **Deauthorize Callback URL:** `https://localhost:8501`
5. Go to **Basic Display** → **User Token Generator**
6. Add yourself as a test user
7. Generate token

✅ **Done when:** You have a token (long string starting with `IGQW...` or similar)

---

## Step 6: Connect Token to CokeSense

**Why:** This links your Instagram account to the app.

### Steps:
1. **Start your Streamlit app:**
   ```bash
   python -m streamlit run streamlit_app.py
   ```

2. **Open the app** in your browser (usually `http://localhost:8501`)

3. **In the sidebar:**
   - Scroll to **📱 Instagram Posting** section
   - Paste your **Instagram Access Token** in the text field
   - The token will be saved automatically

4. **Verify:**
   - You should see "✅ Instagram token saved"

✅ **Done when:** Token is saved and shows success message

---

## Step 7: Test Posting

**Why:** Make sure everything works!

### Steps:
1. **Generate a campaign:**
   - Select a trend
   - Click **✨ Generate Coca-Cola Campaign**
   - Wait for campaign and image to generate

2. **Review the preview:**
   - Scroll to **📱 Post to Instagram** section
   - Click **📋 Preview Instagram Post** to see what will be posted
   - Check caption and image

3. **Post to Instagram:**
   - Click **🚀 Post to Instagram** button
   - Wait for confirmation
   - Check your Instagram account - post should appear!

✅ **Done when:** Post appears on your Instagram account

---

## Troubleshooting

### "Failed to get user info"
- **Check:** Token is valid and not expired
- **Fix:** Generate a new token
- **Check:** Account is Business/Creator type

### "Failed to create media container"
- **Check:** Image URL is publicly accessible
- **Check:** Token has `instagram_content_publish` permission
- **Fix:** Regenerate token with correct permissions

### "Failed to publish"
- **Check:** Rate limits (Instagram has daily limits)
- **Check:** Account status (not restricted)
- **Wait:** Try again in a few minutes

### Token Expired
- **Why:** Tokens expire (usually 60 days)
- **Fix:** Generate a new token and update in sidebar

### Can't Find Instagram Product
- **Check:** App type is "Business" (not "Consumer")
- **Fix:** Create a new Business app

---

## Important Notes

⚠️ **Rate Limits:**
- Instagram has daily posting limits
- Business accounts: ~25 posts/day
- Creator accounts: varies

⚠️ **Token Security:**
- Don't share your token
- Tokens expire (regenerate when needed)
- Use a throwaway account for testing

⚠️ **Account Requirements:**
- Must be Business or Creator account
- Personal accounts won't work
- Account can be private (for testing)

---

## Quick Reference

**Token Format:** Usually starts with `IGQW...` or `EAAB...`

**Required Permissions:**
- `instagram_basic`
- `pages_show_list`  
- `instagram_content_publish`

**Test Account Setup:**
1. Create throwaway Instagram account
2. Convert to Business (free)
3. Keep it private
4. Use for testing

---

## Need Help?

If you get stuck:
1. Check the error message in the app
2. Verify your account is Business/Creator type
3. Make sure token has all required permissions
4. Try generating a new token

**You're all set!** 🎉 Your CokeSense app can now auto-post to Instagram!

