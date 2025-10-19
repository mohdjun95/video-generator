import streamlit as st
import os
from datetime import datetime
from main import VideoGenerationWorkflow
from state import GraphState
from langgraph.checkpoint.memory import MemorySaver
from PIL import Image
import time

# Configure environment variables for cloud deployment
# Streamlit Cloud uses st.secrets, local development uses .env
try:
    # Try to use Streamlit secrets (cloud deployment)
    os.environ["FAL_KEY"] = st.secrets.get("FAL_KEY", os.getenv("FAL_KEY", ""))
    os.environ["CREATOMATE_API_KEY"] = st.secrets.get("CREATOMATE_API_KEY", os.getenv("CREATOMATE_API_KEY", ""))
    os.environ["LANGCHAIN_API_KEY"] = st.secrets.get("LANGCHAIN_API_KEY", os.getenv("LANGCHAIN_API_KEY", ""))
    os.environ["LANGCHAIN_PROJECT"] = st.secrets.get("LANGCHAIN_PROJECT", os.getenv("LANGCHAIN_PROJECT", "video-generation"))
    os.environ["LANGCHAIN_TRACING_V2"] = st.secrets.get("LANGCHAIN_TRACING_V2", os.getenv("LANGCHAIN_TRACING_V2", "false"))
except Exception:
    # Fallback to .env file for local development
    from dotenv import load_dotenv
    load_dotenv()

# Page config
st.set_page_config(
    page_title="Real Estate Video Generator",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .success-box {
        padding: 1rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 0.5rem;
        color: #155724;
        margin: 1rem 0;
    }
    .info-box {
        padding: 1rem;
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 0.5rem;
        color: #0c5460;
        margin: 1rem 0;
    }
    .stButton>button {
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'workflow_started' not in st.session_state:
    st.session_state.workflow_started = False
if 'checkpointer' not in st.session_state:
    st.session_state.checkpointer = MemorySaver()
if 'thread_id' not in st.session_state:
    st.session_state.thread_id = None
if 'app_graph' not in st.session_state:
    st.session_state.app_graph = None
if 'current_state' not in st.session_state:
    st.session_state.current_state = None
if 'session_dir' not in st.session_state:
    session_id = datetime.now().strftime('%Y%m%d_%H%M%S')
    st.session_state.session_dir = f"/Users/m.junaid/Desktop/Firoze/v2/uploads/{session_id}"
    os.makedirs(st.session_state.session_dir, exist_ok=True)

# Header
st.markdown('<div class="main-header">🎬 Real Estate Video Generator</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">AI-Powered Video Creation with Human-in-the-Loop Control</div>', unsafe_allow_html=True)

# Progress bar
progress_value = 0
if st.session_state.workflow_started:
    if st.session_state.current_state:
        if st.session_state.current_state.get('final_video_url'):
            progress_value = 100
        elif st.session_state.current_state.get('render_id'):
            progress_value = 85
        elif st.session_state.current_state.get('awaiting_approval'):
            progress_value = 60
        elif st.session_state.current_state.get('processed_image_urls'):
            progress_value = 50
        else:
            progress_value = 20

st.progress(progress_value / 100)
st.markdown(f"**Progress: {progress_value}%**")

# Sidebar for template parameters
with st.sidebar:
    st.header("📝 Property Details")
    
    address = st.text_area(
        "Property Address",
        value="Los Angeles,\nCA 90045",
        height=80
    )
    
    details_1 = st.text_input(
        "Property Details (Line 1)",
        value="2,500 sqft\n4 Bedrooms\n3 Bathrooms"
    )
    
    details_2 = st.text_input(
        "Property Details (Line 2)",
        value="Built in 1995\n2 Garage Spaces\n$1,595,000"
    )
    
    st.divider()
    
    st.header("👤 Agent Information")
    
    agent_name = st.text_input("Agent Name", value="Elisabeth Parker")
    brand_name = st.text_input("Brand/Company Name", value="Build Masters Constructions")
    email = st.text_input("Contact Email", value="elisabeth@mybrand.com")
    phone = st.text_input("Contact Phone", value="(123) 555-1234")
    
    st.divider()
    
    st.header("🖼️ Agent/Brand Picture")
    agent_picture = st.file_uploader(
        "Upload Agent Picture",
        type=['jpg', 'jpeg', 'png'],
        help="Upload your headshot or company logo"
    )
    
    if agent_picture:
        st.success("✓ Picture uploaded!")
        # Show preview
        agent_img = Image.open(agent_picture)
        st.image(agent_img, caption="Agent Picture Preview", width=200)

# Main content area
st.header("📸 Step 1: Upload Property Images")
st.markdown("Upload 5 property images that will be AI-enhanced for your video")

# Image upload
uploaded_files = st.file_uploader(
    "Choose 5 property images",
    type=['jpg', 'jpeg', 'png'],
    accept_multiple_files=True,
    key="property_images"
)

# Display uploaded images with previews
if uploaded_files:
    st.markdown(f"### ✓ {len(uploaded_files)} images uploaded")
    
    if len(uploaded_files) == 5:
        st.success("Perfect! All 5 images uploaded.")
    elif len(uploaded_files) < 5:
        st.warning(f"Please upload {5 - len(uploaded_files)} more image(s)")
    else:
        st.error(f"Too many images! Please upload only 5 (you have {len(uploaded_files)})")
    
    # Show image previews in a grid
    cols = st.columns(5)
    for idx, uploaded_file in enumerate(uploaded_files[:5]):
        with cols[idx]:
            img = Image.open(uploaded_file)
            st.image(img, caption=f"Photo-{idx+1}", use_column_width=True)
            st.markdown(f"**{uploaded_file.name}**")

# Start processing button
st.divider()

if len(uploaded_files) == 5 and not st.session_state.workflow_started:
    if st.button("🚀 Start AI Processing", type="primary", use_container_width=True):
        with st.spinner("Saving images and starting workflow..."):
            # Save property images
            input_images = {}
            for idx, uploaded_file in enumerate(uploaded_files, 1):
                filepath = os.path.join(st.session_state.session_dir, uploaded_file.name)
                with open(filepath, 'wb') as f:
                    f.write(uploaded_file.getbuffer())
                input_images[f"Photo-{idx}"] = filepath
            
            # Save agent picture
            agent_picture_path = None
            if agent_picture:
                agent_filepath = os.path.join(st.session_state.session_dir, f"agent_{agent_picture.name}")
                with open(agent_filepath, 'wb') as f:
                    f.write(agent_picture.getbuffer())
                agent_picture_path = agent_filepath
            
            # Create initial state
            initial_state = GraphState(
                template_id="6821de4e-c173-4a8f-9c8e-d8f0e3c292ed",
                input_images=input_images,
                address=address,
                details_1=details_1,
                details_2=details_2,
                agent_picture_path=agent_picture_path,
                agent_name=agent_name,
                brand_name=brand_name,
                email=email,
                phone_number=phone
            )
            
            # Create workflow
            st.session_state.thread_id = f"thread_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            workflow = VideoGenerationWorkflow(checkpointer=st.session_state.checkpointer)
            st.session_state.app_graph = workflow.compile()
            
            # Start workflow (will pause at wait_approval)
            config = {"configurable": {"thread_id": st.session_state.thread_id}}
            
            try:
                # Start workflow - it will pause at wait_approval
                event_count = 0
                for event in st.session_state.app_graph.stream(initial_state.model_dump(), config):
                    event_count += 1
                    node_name = list(event.keys())[0] if event else "unknown"
                    st.write(f"✓ Step {event_count}: {node_name}")
                
                st.write(f"Processed {event_count} workflow steps")
                
                # Get current state
                state = st.session_state.app_graph.get_state(config)
                st.session_state.current_state = state.values
                st.session_state.workflow_started = True
                
                st.write(f"Current state keys: {list(state.values.keys())}")
                st.write(f"Awaiting approval: {state.values.get('awaiting_approval')}")
                st.write(f"Processed URLs count: {len(state.values.get('processed_image_urls', {}))}")
                
                st.success("✓ AI processing complete! Please review images below.")
                st.rerun()
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
                import traceback
                st.code(traceback.format_exc())

# Show processed images for approval
if st.session_state.workflow_started and st.session_state.current_state:
    current_state = st.session_state.current_state
    
    if current_state.get('processed_image_urls') and current_state.get('awaiting_approval'):
        st.header("🌟 Step 2: Review AI-Processed Images")
        st.markdown("These are your property images after AI enhancement. Approve or reject each one:")
        
        processed_urls = current_state['processed_image_urls']
        
        # Create approval interface
        approved_images = []
        rejected_images = []
        replacement_images = {}
        
        cols = st.columns(5)
        for idx, (placeholder, url) in enumerate(processed_urls.items()):
            with cols[idx % 5]:
                st.image(url, caption=placeholder, use_column_width=True)
                
                approve = st.checkbox(f"✓ Approve {placeholder}", value=True, key=f"approve_{placeholder}")
                
                if not approve:
                    rejected_images.append(placeholder)
                    
                    # Option to replace
                    replace_file = st.file_uploader(
                        f"Replace {placeholder}",
                        type=['jpg', 'jpeg', 'png'],
                        key=f"replace_{placeholder}"
                    )
                    
                    if replace_file:
                        replace_path = os.path.join(st.session_state.session_dir, f"replacement_{placeholder}_{replace_file.name}")
                        with open(replace_path, 'wb') as f:
                            f.write(replace_file.getbuffer())
                        replacement_images[placeholder] = replace_path
                        st.success(f"✓ Replacement uploaded")
                else:
                    approved_images.append(placeholder)
        
        st.divider()
        
        # Action buttons
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("✅ Approve All & Continue to Video", type="primary", use_container_width=True):
                if rejected_images:
                    st.error(f"⚠️ Please approve all images or regenerate the {len(rejected_images)} rejected image(s)")
                else:
                    with st.spinner("Creating video..."):
                        config = {"configurable": {"thread_id": st.session_state.thread_id}}
                        
                        # Update state
                        update = {
                            "approved_images": approved_images,
                            "rejected_images": [],
                            "replacement_images": {},
                            "human_approval_received": True
                        }
                        
                        st.write(f"Updating state with: {update}")
                        st.session_state.app_graph.update_state(config, update)
                        
                        # Verify state was updated
                        current = st.session_state.app_graph.get_state(config)
                        st.write(f"State after update - human_approval_received: {current.values.get('human_approval_received')}")
                        
                        # Resume workflow - continue until completion
                        try:
                            st.write("Resuming workflow...")
                            event_count = 0
                            for event in st.session_state.app_graph.stream(None, config):
                                event_count += 1
                                node_name = list(event.keys())[0] if event else "unknown"
                                st.write(f"✓ Step {event_count}: {node_name}")
                            
                            st.write(f"Completed {event_count} workflow steps")
                        except Exception as e:
                            st.error(f"Error during workflow: {e}")
                            import traceback
                            st.code(traceback.format_exc())
                        
                        # Update state
                        state = st.session_state.app_graph.get_state(config)
                        st.session_state.current_state = state.values
                        
                        st.write(f"Final state - render_id: {state.values.get('render_id')}")
                        st.write(f"Final state - render_status: {state.values.get('render_status')}")
                        st.write(f"Final state - final_video_url: {state.values.get('final_video_url')}")
                        
                        st.success("✓ Video creation started!")
                        st.rerun()
        
        with col2:
            if rejected_images and st.button("↻ Regenerate Rejected Images", use_container_width=True):
                with st.spinner(f"Regenerating {len(rejected_images)} image(s)..."):
                    config = {"configurable": {"thread_id": st.session_state.thread_id}}
                    
                    # Update state
                    update = {
                        "approved_images": approved_images,
                        "rejected_images": rejected_images,
                        "replacement_images": replacement_images,
                        "human_approval_received": False
                    }
                    st.session_state.app_graph.update_state(config, update)
                    
                    # Resume workflow
                    for event in st.session_state.app_graph.stream(None, config):
                        st.write(f"Processing: {list(event.keys())}")
                    
                    # Update state
                    state = st.session_state.app_graph.get_state(config)
                    st.session_state.current_state = state.values
                    
                    st.success("✓ Images regenerated! Please review again.")
                    st.rerun()
    
    # Show video status
    if current_state.get('render_id') and not current_state.get('final_video_url'):
        st.header("🎬 Step 3: Video Generation")
        
        render_status = current_state.get('render_status', 'planned')
        
        if render_status == 'rendering' or render_status == 'planned':
            st.info(f"⏳ Your video is being created... Status: {render_status}")
            
            # Auto-refresh every 3 seconds
            status_placeholder = st.empty()
            with status_placeholder:
                with st.spinner("Rendering video... Please wait."):
                    time.sleep(3)
            
            # Poll for status
            config = {"configurable": {"thread_id": st.session_state.thread_id}}
            
            # Resume to check status
            try:
                for event in st.session_state.app_graph.stream(None, config):
                    st.write(f"Status check: {list(event.keys())}")
            except Exception as e:
                st.error(f"Error checking status: {e}")
            
            # Update state
            state = st.session_state.app_graph.get_state(config)
            st.session_state.current_state = state.values
            
            st.rerun()
        elif render_status == 'failed':
            st.error("❌ Video rendering failed. Please try again.")
        else:
            st.warning(f"⚠️ Unknown status: {render_status}")
    
    # Show final video
    if current_state.get('final_video_url'):
        st.header("🎉 Step 4: Video Complete!")
        st.balloons()
        
        video_url = current_state['final_video_url']
        
        st.success("✅ Your video has been generated successfully!")
        
        # Display video
        st.video(video_url)
        
        # Download button
        st.markdown(f"### [⬇️ Download Video]({video_url})")
        
        # Create another button
        if st.button("🔄 Create Another Video", use_container_width=True):
            # Reset session state
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

# Footer
st.divider()
st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem;">
        <p>🎬 Real Estate Video Generator v2.0 | Powered by LangGraph, fal.ai & Creatomate</p>
    </div>
""", unsafe_allow_html=True)
