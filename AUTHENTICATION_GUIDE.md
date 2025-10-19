# 🔐 Authentication Guide

This guide explains how to secure your video generator app with username/password authentication.

---

## ✅ What Was Added

The app now has a **login system** that requires users to enter a username and password before accessing the video generator.

### Features:
- ✅ Username/Password login screen
- ✅ Multiple user support
- ✅ Logout button
- ✅ Session-based authentication
- ✅ Secure password handling (not stored in session)
- ✅ Cloud & local environment support

---

## 🚀 Quick Setup for Streamlit Cloud

### Step 1: Update Secrets in Streamlit Cloud

1. Go to your app dashboard: https://share.streamlit.io/
2. Click on your app: **video-generator**
3. Click **⚙️ Settings** (top right)
4. Select **Secrets** from the left menu
5. Add these lines to your existing secrets:

```toml
# Your existing secrets...
FAL_KEY = "your-fal-key"
CREATOMATE_API_KEY = "your-creatomate-key"
LANGCHAIN_API_KEY = "your-langsmith-key"
LANGCHAIN_PROJECT = "pr-enchanted-sticker-67"
LANGCHAIN_TRACING_V2 = "true"

# ADD THESE NEW LINES FOR AUTHENTICATION:
[auth]
admin = "YourSecurePassword123"
firoze = "AnotherSecurePassword456"
# Add more users as needed
```

6. Click **Save**
7. Your app will automatically restart with authentication enabled!

---

## 🏠 Local Development Setup

For local testing, you can either:

### Option A: Add to `.env` file
```bash
AUTH_USERNAME=admin
AUTH_PASSWORD=admin123
```

### Option B: Use `.streamlit/secrets.toml`
Create `.streamlit/secrets.toml` (not committed to git):
```toml
[auth]
admin = "admin123"
testuser = "testpass"
```

---

## 👥 Managing Users

### Add a New User
In Streamlit Cloud Secrets, just add a new line under `[auth]`:
```toml
[auth]
admin = "password1"
john = "password2"
sarah = "password3"  # <- NEW USER
```

### Remove a User
Delete their line or comment it out:
```toml
[auth]
admin = "password1"
# john = "password2"  <- DISABLED
```

### Change a Password
Just update the password value:
```toml
[auth]
admin = "NewPassword456"  # <- CHANGED
```

---

## 🔒 Security Best Practices

### ✅ DO:
- Use strong passwords (mix of letters, numbers, symbols)
- Change passwords regularly
- Use different passwords for each user
- Keep secrets.toml out of version control (already in .gitignore)

### ❌ DON'T:
- Don't use simple passwords like "password123"
- Don't share passwords in emails or chat
- Don't commit secrets.toml to git
- Don't reuse passwords from other systems

---

## 📱 How It Works

### Login Flow:
1. User visits your app
2. Login screen appears
3. User enters username and password
4. If correct: App loads normally
5. If incorrect: Error message shown
6. User can click "Logout" button to sign out

### Technical Details:
- Authentication is **session-based** (lasts until browser tab closes)
- Passwords are NOT stored in session state (security)
- Works with both Streamlit Cloud secrets and local .env
- Supports unlimited users
- No external database needed

---

## 🧪 Testing Authentication

### Test Locally:
1. Add credentials to `.env` or `.streamlit/secrets.toml`
2. Run: `streamlit run streamlit_app.py`
3. Try logging in with correct/incorrect credentials
4. Test the logout button

### Test on Streamlit Cloud:
1. Update secrets in Streamlit Cloud dashboard
2. Wait for app to restart (automatic)
3. Visit your app URL
4. Test login with your credentials

---

## 🔧 Troubleshooting

### Login Not Showing
- Check that `streamlit_app.py` has the authentication code
- Verify the `check_password()` function exists
- Clear browser cache and refresh

### Wrong Password Always
- Double-check username/password in secrets (case-sensitive!)
- Ensure secrets are saved in Streamlit Cloud
- Check for extra spaces in passwords
- Verify `[auth]` section exists in secrets

### Can't Logout
- Clear browser cookies
- Close and reopen browser tab
- Check that logout button calls `st.rerun()`

### Works Locally But Not in Cloud
- Verify secrets are added to Streamlit Cloud (not just locally)
- Check app logs in Streamlit Cloud dashboard
- Ensure `[auth]` section is properly formatted in cloud secrets

---

## 🎨 Customization

### Change Login Page Appearance
Edit the login UI in `streamlit_app.py` (around line 50):
```python
st.markdown("""
    <div style='text-align: center; padding: 2rem;'>
        <h1>🎬 Your Company Name</h1>
        <h3>Custom Login Message</h3>
    </div>
""", unsafe_allow_html=True)
```

### Add Password Strength Requirements
You can add validation in the `password_entered()` function to enforce password rules.

### Add Login Attempt Limits
Track failed attempts in `st.session_state` and block after X tries.

---

## 📊 User Activity (Future Enhancement)

Currently, the app tracks:
- `st.session_state.authenticated_user` - Who is logged in

You could extend this to:
- Log login times
- Track user actions
- Generate usage reports
- Send login notifications

---

## ❓ FAQ

**Q: Is this secure enough for production?**
A: This is basic authentication suitable for internal tools. For public-facing apps with sensitive data, consider enterprise solutions like Okta, Auth0, or AWS Cognito.

**Q: Can I integrate with Google/Microsoft login?**
A: Yes, but requires additional libraries like `streamlit-oauth` (not included by default).

**Q: Are passwords encrypted?**
A: Passwords are stored in Streamlit secrets (encrypted at rest on their servers). For enhanced security, use password hashing (bcrypt).

**Q: What if I forget my password?**
A: Since you control the secrets, you can reset any password in the Streamlit Cloud dashboard.

**Q: Can users change their own passwords?**
A: Not in the current implementation. You'd need to add a password change UI and update secrets programmatically (requires additional setup).

---

## 🚀 Next Steps

1. ✅ Make repository private (GitHub settings)
2. ✅ Add authentication credentials to Streamlit Cloud
3. ✅ Test login with your credentials
4. ✅ Share usernames/passwords with authorized users
5. ✅ Monitor app usage and adjust as needed

---

**Need Help?** Check the Streamlit docs: https://docs.streamlit.io/streamlit-community-cloud/get-started/deploy-an-app/connect-to-data-sources/secrets-management
