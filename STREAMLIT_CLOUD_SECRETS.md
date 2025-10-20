# 🚀 Streamlit Cloud Secrets Setup

## Copy This Exact Configuration to Streamlit Cloud

### Steps:
1. Go to: **https://share.streamlit.io/**
2. Click on your app: **video-generator**
3. Click **⚙️ Settings** (top right corner)
4. Click **Secrets** in the left sidebar
5. **Copy and paste** the configuration below
6. **Replace passwords** with your own secure passwords
7. Click **Save**

---

## 📋 Complete Secrets Configuration

```toml
FAL_KEY = "your-fal-api-key-here"
CREATOMATE_API_KEY = "your-creatomate-api-key-here"
LANGCHAIN_API_KEY = "your-langsmith-api-key-here"
LANGCHAIN_PROJECT = "pr-enchanted-sticker-67"
LANGCHAIN_TRACING_V2 = "true"

# Simple Password Authentication - CHANGE THIS PASSWORD!
APP_PASSWORD = "YourSecurePassword123"
```

---

## ⚠️ IMPORTANT

### Before Saving:
1. ✅ Replace `"YourSecurePassword123"` with your actual password
2. ✅ Make password strong (letters + numbers + symbols)
3. ✅ Don't share password via email or chat

### After Saving:
- App will restart automatically (~30-60 seconds)
- Password screen will appear when you visit the app
- Enter the password you set to access the app

---

## 🔧 Troubleshooting

### "Login screen still not showing"
- Wait 1-2 minutes for app to fully restart
- Clear browser cache (Ctrl+Shift+R or Cmd+Shift+R)
- Check browser console for errors (F12)

### "Username/password not working"
- Check for typos in Streamlit Cloud secrets
- Password is case-sensitive!
- Make sure `APP_PASSWORD` is set
- Verify no extra spaces before/after password

### "App shows error page"
- Check app logs in Streamlit Cloud dashboard
- Verify all API keys are correct
- Make sure secrets format is exactly as shown above

---

## � Managing Access

### Change Password
In Streamlit Cloud Secrets, just update the password:
```toml

```

---

## 📝 Current Setup

After you save the secrets above, you'll have:

**Single password access** - One password protects the entire app

You can share this password with authorized users securely.

---

## ✅ Verification Steps

After updating secrets:

1. ✅ App restarts (check status in Streamlit Cloud)
2. ✅ Visit your app URL
3. ✅ See password entry screen
4. ✅ Enter the password
5. ✅ Successfully access the app

**If all steps pass, you're done!** 🎉

---

## 📞 Need Help?

Check these files:
- `AUTHENTICATION_GUIDE.md` - Detailed authentication documentation
- `SECURITY_SETUP.md` - Security checklist
- `README.md` - General setup guide

Or check Streamlit docs: https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/secrets-management
