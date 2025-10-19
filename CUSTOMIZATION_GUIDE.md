# 🎨 Customization Guide - Change Default Values

This guide shows you exactly where to change default values in your app.

## 📍 Files to Edit

### 1. **streamlit_app.py** - Default Form Values

#### Location: Lines ~107-127 (Sidebar form section)

**What to change:** Default values in the form fields

```python
# FIND THIS SECTION (around line 107):

with st.sidebar:
    st.header("📝 Property Details")
    
    address = st.text_area(
        "Property Address",
        value="Los Angeles,\nCA 90045",          # ← CHANGE THIS
        height=80
    )
    
    details_1 = st.text_input(
        "Property Details (Line 1)",
        value="2,500 sqft\n4 Bedrooms\n3 Bathrooms"  # ← CHANGE THIS
    )
    
    details_2 = st.text_input(
        "Property Details (Line 2)",
        value="Built in 1995\n2 Garage Spaces\n$1,595,000"  # ← CHANGE THIS
    )
    
    st.divider()
    
    st.header("👤 Agent Information")
    
    agent_name = st.text_input("Agent Name", value="Elisabeth Parker")  # ← CHANGE THIS
    brand_name = st.text_input("Brand/Company Name", value="Build Masters Constructions")  # ← CHANGE THIS
    email = st.text_input("Contact Email", value="elisabeth@mybrand.com")  # ← CHANGE THIS
    phone = st.text_input("Contact Phone", value="(123) 555-1234")  # ← CHANGE THIS
```

**Example Changes:**
```python
# Your desired defaults might be:
address = st.text_area(
    "Property Address",
    value="Whitefield,\nBengaluru 560066",  # Your default
    height=80
)

details_1 = st.text_input(
    "Property Details (Line 1)",
    value="1,200 sqft\n2 Bedrooms\n2 Bathrooms"  # Your default
)

details_2 = st.text_input(
    "Property Details (Line 2)",
    value="Built with premium materials\n2 Parking Spaces\n₹85 Lakhs"  # Your default
)

agent_name = st.text_input("Agent Name", value="Firoze Pasha")  # Your name
brand_name = st.text_input("Brand/Company Name", value="Build Masters Constructions")  # Already correct
email = st.text_input("Contact Email", value="firoze@bmcons.com")  # Your email
phone = st.text_input("Contact Phone", value="+91 90364 95343")  # Your phone
```

---

### 2. **main.py** - Template ID (If you have a different template)

#### Location: Lines ~115-120 (Main execution section)

**What to change:** Creatomate template ID if you're using a different template

```python
# FIND THIS SECTION (around line 115):

if __name__ == "__main__":
    # --- Configuration ---
    # Specify the Creatomate template ID we want to use
    TEMPLATE_ID = "6821de4e-c173-4a8f-9c8e-d8f0e3c292ed"  # ← CHANGE THIS if using different template
```

**To find your template ID:**
1. Go to https://creatomate.com/
2. Click on your template
3. The URL will show: `https://creatomate.com/templates/YOUR-TEMPLATE-ID`
4. Copy that ID

---

### 3. **state.py** - Default State Values (Optional)

#### Location: Lines ~8-30 (GraphState class)

**What to change:** Default values for template fields

```python
# FIND THIS SECTION (around line 8):

class GraphState(BaseModel):
    """State for the video generation workflow with template fields"""
    
    # Template configuration
    template_id: str
    
    # Template fields - property information
    address: str = "Los Angeles, CA"  # ← CHANGE THIS
    details_1: str = "2,500 sqft, 4 Bedrooms, 3 Bathrooms"  # ← CHANGE THIS
    details_2: str = "Built in 1995, 2 Garage Spaces, $1,595,000"  # ← CHANGE THIS
    
    # Template fields - agent/brand information  
    agent_name: str = "Elisabeth Parker"  # ← CHANGE THIS
    brand_name: str = "Build Masters Constructions"  # Already correct
    email: str = "elisabeth@mybrand.com"  # ← CHANGE THIS
    phone_number: str = "(123) 555-1234"  # ← CHANGE THIS
```

**Note:** These are fallback defaults. The streamlit_app.py values take priority.

---

## 🎬 Creatomate Template Changes

### Option A: Modify Existing Template

1. Go to https://creatomate.com/templates
2. Find template: `6821de4e-c173-4a8f-9c8e-d8f0e3c292ed`
3. Click "Edit"
4. Make your changes:
   - Text styles (fonts, colors, sizes)
   - Animations and transitions
   - Background music
   - Video duration
   - Layout and positioning

5. **Important:** Keep the same placeholder names:
   - `Photo-1`, `Photo-2`, `Photo-3`, `Photo-4`, `Photo-5`
   - `Address`
   - `Details-1`, `Details-2`
   - `Picture` (agent picture)
   - `Name`, `Brand-Name`, `Email`, `Phone-Number`

6. Click "Save"
7. No code changes needed if placeholder names stay the same!

### Option B: Use Different Template

If you create a NEW template:

1. Create your template in Creatomate
2. Make sure it has these placeholders:
   - 5 image placeholders: `Photo-1` through `Photo-5`
   - Text placeholders: `Address`, `Details-1`, `Details-2`, `Name`, `Brand-Name`, `Email`, `Phone-Number`
   - 1 image placeholder: `Picture` (for agent)

3. Copy the new template ID
4. Update `main.py` line ~118 with new template ID
5. Update `streamlit_app.py` line ~226 (inside GraphState initialization):
   ```python
   initial_state = GraphState(
       template_id="YOUR-NEW-TEMPLATE-ID-HERE",  # ← CHANGE THIS
       input_images=input_images,
       # ... rest of the fields
   )
   ```

---

## 📝 Step-by-Step Change Process

### **Step 1: Edit streamlit_app.py**

```bash
# Open the file
open -a "Visual Studio Code" /Users/m.junaid/Desktop/Firoze/v3/streamlit_app.py
# Or use any text editor you prefer
```

1. Scroll to line ~107 (search for `"Property Address"`)
2. Change the `value=` parameters for each field
3. Save the file

### **Step 2: Edit state.py (Optional)**

```bash
open -a "Visual Studio Code" /Users/m.junaid/Desktop/Firoze/v3/state.py
```

1. Scroll to line ~8 (search for `class GraphState`)
2. Change the default values
3. Save the file

### **Step 3: Edit main.py (Only if changing template ID)**

```bash
open -a "Visual Studio Code" /Users/m.junaid/Desktop/Firoze/v3/main.py
```

1. Scroll to line ~118 (search for `TEMPLATE_ID`)
2. Change the template ID
3. Save the file

### **Step 4: Test Locally**

```bash
cd /Users/m.junaid/Desktop/Firoze/v3
/Users/m.junaid/Desktop/Firoze/.venv/bin/streamlit run streamlit_app.py
```

Test that:
- ✅ Form shows your new default values
- ✅ You can still change the values
- ✅ Video generation works with new defaults

### **Step 5: Commit and Push**

```bash
cd /Users/m.junaid/Desktop/Firoze/v3

# Check what changed
git status
git diff

# Add all changes
git add streamlit_app.py state.py main.py

# Commit with descriptive message
git commit -m "Update default values: phone, email, agent name, property details"

# Push to GitHub
git push

# Streamlit Cloud will auto-redeploy in 1-2 minutes!
```

---

## 🎯 Quick Reference: What to Change

**Common Changes:**

| What | File | Search For | Example |
|------|------|-----------|---------|
| Default Phone | `streamlit_app.py` | `"Contact Phone"` | `+91 90364 95343` |
| Default Email | `streamlit_app.py` | `"Contact Email"` | `firoze@bmcons.com` |
| Default Agent Name | `streamlit_app.py` | `"Agent Name"` | `Firoze Pasha` |
| Default Address | `streamlit_app.py` | `"Property Address"` | `Whitefield, Bengaluru` |
| Default Property Details | `streamlit_app.py` | `"Property Details"` | Your property info |
| Template ID | `main.py` | `TEMPLATE_ID` | Your Creatomate template |

---

## ⚠️ Important Notes

1. **Don't change placeholder names** in code unless you also change them in Creatomate template
2. **Keep the format** of text_input and text_area (don't remove quotes or commas)
3. **Test locally first** before pushing to GitHub
4. **Phone number format:** Can be any format (`(123) 456-7890` or `+91 12345 67890` or `123-456-7890`)
5. **Multi-line text:** Use `\n` for line breaks in address and details

---

## 🔄 After Making Changes

1. Save all files
2. Test locally to verify
3. Commit and push to GitHub
4. Streamlit Cloud will auto-redeploy
5. Test the live app

---

## 📞 Need Help?

If you're unsure about any change:
1. Make a backup first: `cp streamlit_app.py streamlit_app.py.backup`
2. Make one change at a time
3. Test after each change
4. If something breaks, restore from backup

---

**Ready to make changes?** Open the files and update the values! Let me know if you need clarification on any section.
