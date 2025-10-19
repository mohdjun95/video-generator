# 🚀 Streamlit Cloud Deployment Checklist

## ✅ Pre-Deployment Verification

### Files Ready for Deployment
- [x] `streamlit_app.py` - Main application (updated for st.secrets)
- [x] `main.py` - LangGraph workflow
- [x] `nodes.py` - Workflow nodes (updated for cloud env)
- [x] `state.py` - Pydantic state model
- [x] `requirements.txt` - All dependencies listed
- [x] `.streamlit/config.toml` - App configuration
- [x] `.streamlit/secrets.toml.template` - Secret template
- [x] `.gitignore` - Properly configured
- [x] `README.md` - Deployment documentation

### Files to EXCLUDE (in .gitignore)
- [x] `.env` - Local environment file
- [x] `__pycache__/` - Python cache
- [x] `uploads/` - Local uploads folder
- [x] `fal_results_cache.json` - Cache file
- [x] Dash apps and backup files - Removed

## 📋 Deployment Steps

### 1. GitHub Setup

```bash
# Initialize git repository (if not already done)
cd /Users/m.junaid/Desktop/Firoze/v3
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Production ready video generator"

# Create GitHub repository and push
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

### 2. Streamlit Cloud Deployment

1. **Login to Streamlit Cloud**
   - Go to: https://share.streamlit.io/
   - Sign in with GitHub

2. **Create New App**
   - Click "New app"
   - Select your repository
   - Branch: `main`
   - Main file: `streamlit_app.py`
   - App URL: Choose a custom URL (e.g., `your-app-name`)

3. **Configure Secrets**
   - Click on "Advanced settings" → "Secrets"
   - Copy content from `.streamlit/secrets.toml.template`
   - Replace placeholders with actual API keys:

```toml
FAL_KEY = "fal-xxxxxxxxxxxxxxxxxxxx"
CREATOMATE_API_KEY = "creatomate-xxxxxxxxxxxx"
LANGCHAIN_API_KEY = "lsv2_xxxxxxxxxxxx"
LANGCHAIN_PROJECT = "video-generator-prod"
LANGCHAIN_TRACING_V2 = "true"
```

4. **Deploy**
   - Click "Deploy!"
   - Wait 2-3 minutes for build
   - App will be live at: `https://your-app-name.streamlit.app`

## 🔑 API Keys Needed

### 1. fal.ai API Key
- Get from: https://fal.ai/dashboard
- Go to Settings → API Keys
- Create new key
- Copy and paste into Streamlit secrets

### 2. Creatomate API Key
- Get from: https://creatomate.com/dashboard
- Go to Settings → API Keys
- Copy existing key or create new one
- Paste into Streamlit secrets

### 3. LangSmith API Key (Optional but Recommended)
- Get from: https://smith.langchain.com/
- Go to Settings → API Keys
- Create new key
- Paste into Streamlit secrets
- Set project name in `LANGCHAIN_PROJECT`

## 🧪 Testing After Deployment

### Test Checklist

1. **App Loads**
   - [ ] App loads without errors
   - [ ] Sidebar appears with form
   - [ ] Main area shows upload section

2. **Image Upload**
   - [ ] Can upload 5 property images
   - [ ] Can upload agent picture
   - [ ] Image previews show correctly

3. **AI Processing**
   - [ ] Click "Start AI Processing" works
   - [ ] Images are processed by fal.ai
   - [ ] Agent picture uploads directly
   - [ ] Processed images appear for review

4. **HITL Approval**
   - [ ] Checkboxes appear for each image
   - [ ] Can reject and upload replacement
   - [ ] "Regenerate" button works
   - [ ] "Approve All" continues workflow

5. **Video Generation**
   - [ ] Video render starts
   - [ ] Status updates show progress
   - [ ] Final video displays in player
   - [ ] Download link works

6. **Error Handling**
   - [ ] Missing API keys show clear errors
   - [ ] Invalid images show warnings
   - [ ] Network errors are caught
   - [ ] Can reset with "Create Another Video"

## ⚙️ Configuration Options

### Streamlit Cloud Settings

**App Settings:**
- Python version: 3.9+
- Resource limits: Default (usually sufficient)
- Sleep mode: Enabled (app sleeps after inactivity)

**Advanced Settings:**
- Max upload size: 50MB (set in config.toml)
- CORS: Disabled (set in config.toml)
- XSRF Protection: Enabled (set in config.toml)

### Custom Domain (Optional)

Streamlit Cloud supports custom domains:
1. Go to App settings → Custom domain
2. Follow instructions to set up DNS
3. Typical setup time: 24-48 hours

## 🐛 Troubleshooting

### Common Deployment Issues

**Build fails with "Module not found":**
- Check `requirements.txt` has all dependencies
- Verify package names are correct (use exact names from pip)

**App crashes on startup:**
- Check secrets are configured correctly
- Verify no hardcoded API keys in code
- Check logs in Streamlit Cloud dashboard

**Images not uploading:**
- Verify file size < 50MB
- Check browser console for errors
- Try different image format (JPEG vs PNG)

**Video not generating:**
- Check Creatomate API key is valid
- Verify account has credits
- Check template ID exists in Creatomate account

## 📊 Monitoring

### Streamlit Cloud Dashboard
- View app logs
- Monitor resource usage
- Check crash reports
- Track app analytics

### LangSmith Dashboard
- View workflow traces
- Monitor API calls
- Debug failed workflows
- Analyze performance

## 🔄 Updating the App

```bash
# Make changes to code
git add .
git commit -m "Description of changes"
git push

# Streamlit Cloud auto-deploys on push to main branch
# Watch deployment progress in dashboard
```

## 📈 Scaling Considerations

**Current Setup:**
- Free tier: Limited to 1GB RAM, 1 CPU
- Concurrent users: ~10-20
- Video generation: Sequential (one at a time)

**If Scaling Needed:**
- Upgrade to Streamlit Cloud paid tier
- Consider moving to dedicated server
- Implement job queue for video generation
- Add database for persistent storage

## ✨ Production Best Practices

1. **Secrets Management**
   - Never commit API keys to git
   - Use different keys for dev/prod
   - Rotate keys periodically

2. **Error Handling**
   - All API calls wrapped in try/except
   - User-friendly error messages
   - Logging for debugging

3. **Performance**
   - Caching enabled for fal.ai results
   - Session state for workflow persistence
   - Efficient image handling with PIL

4. **User Experience**
   - Clear progress indicators
   - Visual feedback for all actions
   - Image previews throughout workflow

## 🎉 Launch!

Once all checks pass:
1. Share the app URL with users
2. Monitor initial usage
3. Collect feedback
4. Iterate and improve

**Your app URL:** `https://your-app-name.streamlit.app`

Good luck! 🚀
