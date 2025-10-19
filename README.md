# 🎬 AI Video Generation Tool - Production Version# Video Generation Platform v2 - Production Ready with HITL



A production-ready video generation tool built with LangGraph, fal.ai, and Creatomate. Features Human-in-the-Loop (HITL) approval workflow with Streamlit interface.## Overview

This is a production-ready video generation platform built with:

## 🌟 Features- **LangGraph**: Workflow orchestration with checkpointing and interrupts

- **Plotly Dash**: Interactive web interface

- **AI Image Enhancement**: Automatically enhances property images using fal.ai- **fal.ai**: AI-powered image processing and enhancement

- **Human-in-the-Loop**: Review and approve AI-processed images before video creation- **Creatomate**: Professional video template rendering

- **Image Replacement**: Upload replacement images or regenerate rejected ones- **Human-in-the-Loop (HITL)**: Manual approval and regeneration controls

- **Smart Caching**: Caches processed images to avoid redundant API calls

- **Template-Based**: Customizable video templates via Creatomate## Features

- **Professional UI**: Clean Streamlit interface with image previews and progress tracking

### ✅ Core Functionality

## 🚀 Deployment to Streamlit Cloud- Upload multiple images through web interface

- AI processing with fal.ai (9:16 aspect ratio optimization)

### Prerequisites- Human approval workflow with visual preview

- Selective image regeneration

1. **API Keys Required**:- Automated video creation with Creatomate

   - [fal.ai API Key](https://fal.ai/) - For AI image processing- Real-time status monitoring

   - [Creatomate API Key](https://creatomate.com/) - For video rendering

   - [LangSmith API Key](https://smith.langchain.com/) - For workflow tracking (optional)### ✅ HITL Controls

- **Review & Approve**: Preview all processed images before video creation

### Step-by-Step Deployment- **Regenerate**: Reject and regenerate specific images you're not happy with

- **Full Control**: Workflow pauses until you approve, ensuring quality

#### 1. Fork/Upload to GitHub

### ✅ Production Features

1. Create a new GitHub repository- Persistent workflow state with checkpointing

2. Upload all files from the `v3` folder to your repository- Session management for multiple concurrent users

3. Make sure `.env` is NOT uploaded (it's in `.gitignore`)- Error handling and recovery

- Caching to save API credits

#### 2. Deploy to Streamlit Cloud- Clean Bootstrap UI with responsive design



1. Go to [share.streamlit.io](https://share.streamlit.io/)## Architecture

2. Click "New app"

3. Select your GitHub repository### LangGraph Workflow

4. Set the following:```

   - **Main file path**: `streamlit_app.py`process_images → wait_approval → [regenerate] → prepare_payload → create_render → check_status

   - **Python version**: 3.9 or higher                      ↑               ↓

                      └───────────────┘

#### 3. Configure Secrets                    (rejection loop)

```

In Streamlit Cloud dashboard:

### Files Structure

1. Go to your app settings → **Secrets**- `state.py`: Pydantic GraphState model with HITL fields

2. Add the following secrets:- `nodes.py`: All workflow nodes (process, approval, regenerate, render)

- `main.py`: LangGraph workflow definition with conditional edges

```toml- `dash_app.py`: Plotly Dash web interface

FAL_KEY = "your-fal-api-key-here"- `.env`: API credentials (FAL_KEY, CREATOMATE_API_KEY, LANGSMITH)

CREATOMATE_API_KEY = "your-creatomate-api-key-here"

LANGCHAIN_API_KEY = "your-langsmith-api-key-here"## Setup & Installation

LANGCHAIN_PROJECT = "your-project-name"

LANGCHAIN_TRACING_V2 = "true"### 1. Install Dependencies

``````bash

cd /Users/m.junaid/Desktop/Firoze/v2

3. Click "Save"source ../.venv/bin/activate

pip install dash dash-bootstrap-components langgraph fal-client requests python-dotenv pydantic

#### 4. Deploy!```



Click "Deploy" and wait for your app to build (usually 2-3 minutes)### 2. Configure Environment

Ensure `.env` file has:

## 💻 Local Development```

FAL_KEY=your_fal_api_key

### InstallationCREATOMATE_API_KEY=your_creatomate_api_key

LANGSMITH_TRACING=true

```bashLANGSMITH_API_KEY=your_langsmith_key

# Clone the repositoryLANGSMITH_PROJECT=your_project_name

git clone <your-repo-url>```

cd v3

### 3. Run the Application

# Create virtual environment```bash

python3 -m venv venvpython dash_app.py

source venv/bin/activate  # On Windows: venv\Scripts\activate```



# Install dependenciesThen open: http://127.0.0.1:8050

pip install -r requirements.txt

## Usage Guide

# Create .env file

cp .streamlit/secrets.toml.template .env### Step 1: Upload Images

# Edit .env and add your API keys1. Drag & drop or select 5 images (Photo-1 through Photo-5)

```2. Images will be automatically mapped to template placeholders

3. Click "Start Processing" to begin

### Run Locally

### Step 2: Review & Approve

```bash1. Wait for fal.ai to process your images (~30-60 seconds)

streamlit run streamlit_app.py2. Review the processed images in the preview grid

```3. **Approve All**: Check all images and click "Approve Selected & Continue"

4. **Regenerate Some**: Leave problematic images unchecked, click "Regenerate Rejected"

Visit `http://localhost:8501` in your browser.

### Step 3: Video Generation

## 📁 Project Structure1. Once approved, video rendering begins automatically

2. Status updates every 3 seconds

```3. Download link appears when video is ready (~30-60 seconds)

v3/

├── streamlit_app.py          # Main Streamlit application## Technical Details

├── main.py                   # LangGraph workflow definition

├── nodes.py                  # Workflow node functions### Checkpointing & Interrupts

├── state.py                  # Pydantic state model- Uses `MemorySaver` for in-memory checkpointing

├── requirements.txt          # Python dependencies- `interrupt_before=["wait_approval"]` pauses workflow at approval node

├── .streamlit/- `update_state()` injects human decisions back into workflow

│   ├── config.toml          # Streamlit configuration- Thread-based session management for concurrent users

│   └── secrets.toml.template # Template for secrets

├── .gitignore               # Git ignore rules### HITL Implementation

└── README.md                # This file- **Approval Node**: Pauses workflow, displays images in Dash

```- **Regeneration Node**: Reprocesses rejected images only

- **Conditional Routing**: Automatically loops back for regeneration or proceeds to video creation

## 🎯 How It Works

### Error Handling

### Workflow Steps- Try-catch blocks in all API calls

- Graceful fallbacks for missing files

1. **Upload Images**: User uploads 5 property images and 1 agent picture- State validation with Pydantic

2. **Fill Template**: Enter property details, agent info, and contact details- LangSmith tracing for debugging

3. **AI Processing**: Property images are enhanced with fal.ai (agent picture uploaded directly)

4. **Human Review**: Review AI-processed images with preview## Customization

5. **Approve/Regenerate**: Approve all or regenerate/replace specific images

6. **Video Creation**: Approved images sent to Creatomate for video rendering### Modify Template Fields

7. **Download**: Final video is ready to downloadEdit `nodes.py` → `prepare_creatomate_payload()`:

```python

### LangGraph Workflowmodifications.update({

    "Address.text": "Your Address",

```    "Details-1.text": "Your Details",

process_images → wait_approval → [regenerate ↩] → prepare_payload → create_render → check_status → END    # ... etc

```})

```

- **Checkpointing**: State is persisted using MemorySaver

- **HITL**: Workflow pauses after `wait_approval` for human input### Change Template

- **Conditional Routing**: Rejected images trigger regeneration loopUpdate `TEMPLATE_ID` in `dash_app.py`:

```python

## 🔧 ConfigurationTEMPLATE_ID = "your-template-id-here"

```

### Creatomate Template

### Adjust fal.ai Prompt

Default template ID: `6821de4e-c173-4a8f-9c8e-d8f0e3c292ed`Edit `nodes.py` → `regenerate_images()` or `process_images_with_fal()`:

```python

Template placeholders:"prompt": "Your custom prompt here",

- `Photo-1` to `Photo-5`: Property images"aspect_ratio": "16:9",  # or other ratios

- `Address`: Property address```

- `Details-1`, `Details-2`: Property details

- `Picture`: Agent/brand picture## Monitoring & Debugging

- `Name`: Agent name

- `Brand-Name`: Company name### LangSmith Tracing

- `Email`, `Phone-Number`: Contact infoAll workflow executions are traced in LangSmith for observability:

- View node execution times

### fal.ai Model- Inspect state at each step

- Debug approval/rejection flows

Model: `fal-ai/nano-banana/edit`

- Aspect ratio: 9:16 (vertical video)### Console Logs

- Output format: JPEGThe application prints detailed logs:

- Caching enabled for efficiency- Image processing status

- Approval decisions

## 🐛 Troubleshooting- Regeneration attempts

- Video render status

### Common Issues

### Cache Files

**Images not processing:**- `fal_results_cache.json`: Stores processed image URLs

- Check FAL_KEY is set correctly in secrets- Prevents reprocessing identical images

- Verify images are JPEG/PNG format- Saves API credits and time

- Check file size (max 50MB per Streamlit Cloud)

## API Credits Management

**Video not rendering:**

- Verify CREATOMATE_API_KEY is correct### Caching Strategy

- Check Creatomate account has sufficient credits- First run: Processes all images, saves to cache

- Ensure template ID exists in your account- Subsequent runs: Loads from cache if images unchanged

- Regeneration: Only processes rejected images

**Workflow stuck:**

- Refresh the page to reset session### Cost Optimization

- Check LangSmith traces for errors- **fal.ai**: ~$0.01-0.05 per image

- Clear cache by clicking "Create Another Video"- **Creatomate**: Video render costs per template

- Caching reduces costs by ~80% for repeated workflows

## 📊 Monitoring

## Troubleshooting

LangSmith integration provides:

- Workflow execution traces### Images Not Appearing

- Node-by-node performance metrics- Check console for fal.ai errors

- Error tracking and debugging- Verify FAL_KEY in .env

- State snapshots at each step- Ensure images are under 10MB



Access at: [smith.langchain.com](https://smith.langchain.com/)### Workflow Stuck

- Check LangSmith traces

## 📝 License- Verify checkpointer is working

- Restart Dash app

Proprietary - Build Masters Constructions

### Video Rendering Fails

## 👥 Support- Check CREATOMATE_API_KEY

- Verify all template fields are provided

For issues or questions:- Check Creatomate API status

- Email: firoze@bmcons.com

- Project: Build Masters Constructions Video Generator## Future Enhancements

- [ ] Multi-template support
- [ ] Batch processing
- [ ] Video preview before final render
- [ ] Custom prompt input per image
- [ ] Database persistence instead of memory
- [ ] User authentication
- [ ] Cloud deployment (AWS/GCP)

## License
Internal use only - Proprietary

## Support
For issues or questions, contact: m.junaid@company.com
