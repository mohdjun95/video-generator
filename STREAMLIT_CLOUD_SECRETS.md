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
FAL_KEY = "0d6b11d4-8f1b-4c7d-8f45-3a0ed97489ae:15367343b681790d10b19d495c60579f"
CREATOMATE_API_KEY = "0392cdddcd264a4f8d0f8d0df5bc4afa0ff8743fbe7c463fed4103d871d5f82a77fff9af757bf4fa15bf9e984c0754a8"
LANGCHAIN_API_KEY = "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"
LANGCHAIN_PROJECT = "pr-enchanted-sticker-67"
LANGCHAIN_TRACING_V2 = "true"

# Authentication - CHANGE THESE PASSWORDS!
[auth]
admin = "ChangeMeToSecurePassword123"
firoze = "AnotherSecurePassword456"
```

---

## ⚠️ IMPORTANT

### Before Saving:
1. ✅ Replace `"ChangeMeToSecurePassword123"` with your actual password
2. ✅ Replace `"AnotherSecurePassword456"` with another password
3. ✅ Make passwords strong (letters + numbers + symbols)
4. ✅ Don't share passwords via email or chat

### After Saving:
- App will restart automatically (~30-60 seconds)
- Login screen will appear when you visit the app
- Use username: `admin` or `firoze` with the passwords you set

---

## 🔧 Troubleshooting

### "Login screen still not showing"
- Wait 1-2 minutes for app to fully restart
- Clear browser cache (Ctrl+Shift+R or Cmd+Shift+R)
- Check browser console for errors (F12)

### "Username/password not working"
- Check for typos in Streamlit Cloud secrets
- Passwords are case-sensitive!
- Make sure `[auth]` section is included
- Verify no extra spaces before/after passwords

### "App shows error page"
- Check app logs in Streamlit Cloud dashboard
- Verify all API keys are correct
- Make sure secrets format is exactly as shown above

---

## 📝 Current Users Configured

After you save the secrets above, you'll have:

| Username | Password | Notes |
|----------|----------|-------|
| `admin` | (You set this) | Main admin account |
| `firoze` | (You set this) | Secondary account |

You can add more users by adding more lines under `[auth]`:
```toml
[auth]
admin = "password1"
firoze = "password2"
colleague1 = "password3"
colleague2 = "password4"
```

---

## ✅ Verification Steps

After updating secrets:

1. ✅ App restarts (check status in Streamlit Cloud)
2. ✅ Visit your app URL
3. ✅ See login screen with username/password fields
4. ✅ Enter username and password
5. ✅ Successfully log in and see the app

**If all steps pass, you're done!** 🎉

---

## 📞 Need Help?

Check these files:
- `AUTHENTICATION_GUIDE.md` - Detailed authentication documentation
- `SECURITY_SETUP.md` - Security checklist
- `README.md` - General setup guide

Or check Streamlit docs: https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/secrets-management
