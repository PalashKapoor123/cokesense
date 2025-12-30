# 📱 Instagram Auto-Posting Setup Guide

## Overview

CokeSense can automatically post your generated campaigns to Instagram, including:
- Hero concept
- Slogan
- Social post
- AI-generated image

## Requirements

1. **Instagram Business or Creator Account** (not personal account)
2. **Meta Developer Account** (free)
3. **Instagram Access Token**

## Setup Steps

### Step 1: Convert to Business/Creator Account

1. Open Instagram app
2. Go to Settings → Account → Switch to Professional Account
3. Choose "Business" or "Creator"
4. Complete the setup

### Step 2: Create Meta Developer App

1. Go to [Meta for Developers](https://developers.facebook.com/)
2. Click "My Apps" → "Create App"
3. Choose "Business" type
4. Fill in app details

### Step 3: Add Instagram Product

1. In your app dashboard, click "Add Product"
2. Find "Instagram" and click "Set Up"
3. Choose "Instagram Graph API" or "Instagram Basic Display API"

### Step 4: Get Access Token

**Option A: Instagram Graph API (Recommended)**
1. Go to Tools → Graph API Explorer
2. Select your app
3. Add permissions: `instagram_basic`, `pages_show_list`, `instagram_content_publish`
4. Generate token
5. Copy the token

**Option B: Instagram Basic Display API**
1. Go to Basic Display → Basic Display
2. Add test users
3. Generate token
4. Copy the token

### Step 5: Add Token to CokeSense

1. In Streamlit app sidebar
2. Paste your Instagram Access Token
3. Click outside the field to save

## Using Auto-Post

1. Generate a campaign as usual
2. Review the preview in "Preview Instagram Post"
3. Click "🚀 Post to Instagram"
4. Wait for confirmation

## Important Notes

⚠️ **Limitations:**
- Instagram API requires Business/Creator accounts
- Personal accounts cannot use the API
- Tokens expire (usually 60 days)
- Rate limits apply (varies by account type)

💡 **For Testing:**
- Use a throwaway Business account
- Keep account private for testing
- Tokens can be regenerated if expired

## Troubleshooting

**"Failed to get user info"**
- Check if token is valid
- Ensure account is Business/Creator type
- Verify token has correct permissions

**"Failed to create media container"**
- Image URL must be publicly accessible
- Check image URL is valid
- Ensure token has `instagram_content_publish` permission

**"Failed to publish"**
- Check rate limits
- Verify account status
- Ensure image meets Instagram requirements

## Alternative: Manual Posting

If API setup is too complex, you can:
1. Copy the caption from preview
2. Download the image
3. Post manually to Instagram

The preview shows exactly what will be posted!

