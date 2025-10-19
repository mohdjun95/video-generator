# ✏️ Quick Edit Checklist

Use this as a quick reference while editing. Open `CUSTOMIZATION_GUIDE.md` for detailed instructions.

## 🎯 Changes to Make in streamlit_app.py (Lines 114-137)

Current values → Change to your values:

```python
# Line 114-117: Property Address
value="Los Angeles,\nCA 90045"
# → Change to: "Whitefield,\nBengaluru 560066"  (or your address)

# Line 121: Property Details Line 1  
value="2,500 sqft\n4 Bedrooms\n3 Bathrooms"
# → Change to: "1,200 sqft\n2 Bedrooms\n2 Bathrooms"  (or your details)

# Line 126: Property Details Line 2
value="Built in 1995\n2 Garage Spaces\n$1,595,000"
# → Change to: "Premium materials\n2 Parking\n₹85 Lakhs"  (or your details)

# Line 134: Agent Name
value="Elisabeth Parker"
# → Change to: "Firoze Pasha"  (or your name)

# Line 135: Brand Name
value="Build Masters Constructions"
# → Keep as is OR change to your company name

# Line 136: Email
value="elisabeth@mybrand.com"
# → Change to: "firoze@bmcons.com"  (or your email)

# Line 137: Phone
value="(123) 555-1234"
# → Change to: "+91 90364 95343"  (or your phone)
```

## 📝 How to Edit

1. **Open the file:**
   ```bash
   open /Users/m.junaid/Desktop/Firoze/v3/streamlit_app.py
   ```

2. **Use Find (Cmd+F):**
   - Search for: `"Contact Phone"`
   - This will take you to line 137
   - Scroll up a bit to see all the form fields

3. **Edit carefully:**
   - Only change the text inside the quotes after `value=`
   - Don't remove quotes or commas
   - Keep the `\n` for line breaks

4. **Save:** Cmd+S

## ✅ After Editing - Deploy to Cloud

```bash
cd /Users/m.junaid/Desktop/Firoze/v3

# Test locally first (optional)
/Users/m.junaid/Desktop/Firoze/.venv/bin/streamlit run streamlit_app.py

# If it works, push to GitHub
git add streamlit_app.py
git commit -m "Update default form values"
git push

# Streamlit Cloud will auto-redeploy in 1-2 minutes
```

## 🎬 Template ID (Optional)

**Only change if using a different Creatomate template**

File: `main.py`, Line ~118
```python
TEMPLATE_ID = "6821de4e-c173-4a8f-9c8e-d8f0e3c292ed"
# → Change to your new template ID from Creatomate
```

---

**That's it!** Just edit those values in `streamlit_app.py`, save, and push to GitHub.

See `CUSTOMIZATION_GUIDE.md` for detailed explanations.
