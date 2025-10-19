# 🔄 Cache Management Guide

## Understanding the Cache

The app caches fal.ai processed images to:
- ✅ **Save API costs** - Avoid reprocessing the same images
- ✅ **Speed up testing** - Instant results for repeated tests
- ✅ **Reduce API calls** - Fewer calls to fal.ai

Cache file: `fal_results_cache.json`

---

## 🎯 Three Ways to Handle Cache

### **Option 1: Disable Cache Temporarily (Recommended for Testing)**

Add this to your Streamlit Cloud secrets:

```toml
DISABLE_CACHE = "true"
```

**Steps:**
1. Go to Streamlit Cloud app settings
2. Click "Secrets"
3. Add the line above
4. Click "Save"
5. App will restart and process ALL images fresh

**When to use:** Testing new images, verifying AI processing works

**To re-enable caching later:**
- Remove the `DISABLE_CACHE` line from secrets
- Or change to `DISABLE_CACHE = "false"`

---

### **Option 2: Delete Cache File on Cloud**

The cache file on Streamlit Cloud persists between runs. To clear it:

**Unfortunately**, Streamlit Cloud doesn't provide direct file system access, so you can't manually delete files. 

**Workaround:** Use Option 1 (disable cache) or Option 3 (delete locally)

---

### **Option 3: Clear Local Cache (For Local Testing)**

If testing locally:

```bash
cd /Users/m.junaid/Desktop/Firoze/v3
rm fal_results_cache.json
/Users/m.junaid/Desktop/Firoze/.venv/bin/streamlit run streamlit_app.py
```

**Note:** This only affects your local machine, not Streamlit Cloud.

---

## 🚀 Recommended Setup

### For Production (Normal Users):
```toml
# Don't add DISABLE_CACHE
# Let caching work normally to save costs
```

### For Testing/Development:
```toml
# In Streamlit Cloud secrets, add:
DISABLE_CACHE = "true"
```

---

## 📊 How Cache Works

### With Cache Enabled (Default):
```
1. User uploads 5 images → Check cache
2. Image 1-5 found in cache → Use cached URLs ✅ (instant, free)
3. No API calls to fal.ai
4. Continue to video generation
```

### With Cache Disabled:
```
1. User uploads 5 images → Skip cache check
2. Process all images with fal.ai → 5 API calls 💰
3. Save to cache for next time
4. Continue to video generation
```

### Smart Cache (Mixed):
```
1. User uploads 5 images → Check cache
2. Image 1-3 found in cache → Use cached ✅
3. Image 4-5 not in cache → Process with fal.ai 💰
4. Add Image 4-5 to cache
5. Continue to video generation
```

---

## ⚙️ Current Implementation

**Cache Location:** Same directory as the app (Streamlit Cloud temp storage)

**Cache Key:** Placeholder name (Photo-1, Photo-2, etc.)

**Note:** Cache is based on placeholder name, NOT image content. So:
- Same placeholder name = Uses cached result
- Different images but same placeholder = Still uses cache

This is why you're seeing cached images even with new uploads!

---

## 🔧 To Deploy Cache Control

```bash
cd /Users/m.junaid/Desktop/Firoze/v3

# Commit the cache control feature
git add nodes.py
git commit -m "Add cache control via DISABLE_CACHE environment variable"
git push

# Then in Streamlit Cloud:
# 1. Go to app settings
# 2. Add DISABLE_CACHE = "true" to secrets
# 3. Save and restart
```

---

## 🎯 Quick Actions

**Want fresh processing every time?**
→ Add `DISABLE_CACHE = "true"` to Streamlit secrets

**Want to save API costs?**
→ Keep cache enabled (default, don't add DISABLE_CACHE)

**Testing with same images repeatedly?**
→ Keep cache enabled (faster, cheaper)

**Testing with different images?**
→ Disable cache (ensures real AI processing)

---

## 💡 Best Practice

**For your production app:**
1. Keep cache enabled (save costs)
2. Cache is based on placeholder names (Photo-1, Photo-2, etc.)
3. Each user session gets fresh processing (different temp directories)
4. Cache only helps within same session or repeated tests

**The cache is actually GOOD** for:
- Development/testing (faster iterations)
- Demonstrations (consistent results)
- Cost savings (avoid redundant API calls)

---

**Ready to disable cache for testing?** Let me know and I'll help you add it to Streamlit Cloud secrets!
