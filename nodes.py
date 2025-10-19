import os
import fal_client
from typing import Dict
from state import GraphState
import time
import requests
import json

# Load environment variables - works for both local (.env) and cloud (already set by streamlit_app.py)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not needed in cloud deployment

# --- Get API Keys ---
FAL_KEY = os.getenv("FAL_KEY")
if not FAL_KEY:
    print("Warning: FAL_KEY not found in environment. Image processing will be skipped.")

CREATOMATE_API_KEY = os.getenv("CREATOMATE_API_KEY")

# The specific fal.ai model for image editing
FAL_MODEL_URL = "fal-ai/nano-banana/edit"

def on_queue_update(update):
    """Callback function to print logs from the fal.ai queue."""
    if isinstance(update, fal_client.InProgress):
        for log in update.logs:
            print(log["message"])


def process_images_with_fal(state: GraphState) -> dict:
    """
    Uploads local property images, submits jobs to fal-ai/nano-banana/edit,
    polls for the result, and returns the new image URLs.
    Agent picture is uploaded directly without AI processing.
    Uses caching to avoid reprocessing the same images.
    """
    CACHE_FILE = "fal_results_cache.json"
    
    # Try to load cached results first
    if os.path.exists(CACHE_FILE):
        print("--- Loading cached fal.ai results ---")
        with open(CACHE_FILE, "r") as f:
            cached_data = json.load(f)
        
        # Check if all required images are in cache
        input_images = state.input_images
        all_cached = all(placeholder in cached_data for placeholder in input_images.keys())
        
        if all_cached:
            print("All images found in cache. Skipping fal.ai processing.")
            processed_urls = {k: cached_data[k] for k in input_images.keys()}
            
            current_state = state.model_dump()
            current_state["processed_image_urls"] = processed_urls
            
            # Upload agent picture directly (no AI processing)
            if state.agent_picture_path and os.path.exists(state.agent_picture_path):
                print("Uploading agent picture directly (no AI processing)...")
                try:
                    with open(state.agent_picture_path, "rb") as f:
                        image_bytes = f.read()
                    agent_url = fal_client.upload(image_bytes, content_type="image/jpeg")
                    current_state["picture_source"] = agent_url
                    print(f"Agent picture uploaded: {agent_url}")
                except Exception as e:
                    print(f"Error uploading agent picture: {e}")
            
            return current_state
        else:
            print("Some images not in cache. Processing missing images...")
            processed_urls = cached_data.copy()
    else:
        print("No cache found. Processing all images...")
        processed_urls = {}
    
    if not FAL_KEY:
        print("Warning: FAL_KEY not found. Skipping image processing.")
        return {**state.model_dump(), "processed_image_urls": {}}

    input_images = state.input_images

    print("--- Starting Image Processing with fal-client ---")

    for placeholder, file_path in input_images.items():
        # Skip if already in cache
        if placeholder in processed_urls:
            print(f"Skipping '{placeholder}' (already cached)")
            continue
            
        if not os.path.exists(file_path):
            print(f"Warning: Image file not found at {file_path}. Skipping.")
            continue

        print(f"\nProcessing image for '{placeholder}' from {file_path}...")

        try:
            # 1. Read the image file as bytes and upload it
            print("Uploading file...")
            with open(file_path, "rb") as f:
                image_bytes = f.read()
            
            # Add the required content_type argument
            uploaded_url = fal_client.upload(image_bytes, content_type="image/jpeg")
            print(f"File uploaded to temporary URL: {uploaded_url}")

            # 2. Submit the job to fal.ai using subscribe (blocking call with logs)
            print("Submitting job to fal.ai...")
            result = fal_client.subscribe(
                FAL_MODEL_URL,
                arguments={
                    "prompt": "A high-quality, clear photograph, vibrant and professional, with the best part of the image in focus with no zooming",
                    "image_urls": [uploaded_url],
                    "num_images": 1,
                    "output_format": "jpeg",
                    "aspect_ratio": "9:16"
                },
                with_logs=True,
                on_queue_update=on_queue_update,
            )
            
            # 3. Extract the processed image URL from the result
            if result and "images" in result and len(result["images"]) > 0:
                processed_image_url = result["images"][0]["url"]
                processed_urls[placeholder] = processed_image_url
                print(f"Successfully processed '{placeholder}'. New URL: {processed_image_url}")
            else:
                print(f"Warning: No image URL returned for '{placeholder}'")

        except Exception as e:
            print(f"An error occurred while processing image {file_path} with fal.ai: {e}")

    print("\n--- Finished Image Processing ---")
    
    # Save results to cache
    with open(CACHE_FILE, "w") as f:
        json.dump(processed_urls, f, indent=2)
    print(f"Results saved to cache: {CACHE_FILE}")
    
    current_state = state.model_dump()
    current_state["processed_image_urls"] = processed_urls
    
    # Upload agent picture directly (no AI processing needed)
    if state.agent_picture_path and os.path.exists(state.agent_picture_path):
        print(f"\nUploading agent/brand picture from {state.agent_picture_path}...")
        print("(Agent picture is uploaded directly, no AI processing)")
        
        try:
            with open(state.agent_picture_path, "rb") as f:
                image_bytes = f.read()
            
            agent_picture_url = fal_client.upload(image_bytes, content_type="image/jpeg")
            current_state["picture_source"] = agent_picture_url
            print(f"Agent picture uploaded successfully: {agent_picture_url}")
        
        except Exception as e:
            print(f"Error uploading agent picture: {e}")
            # Use default if upload fails
            current_state["picture_source"] = "https://creatomate.com/files/assets/08322d05-9717-402a-b267-5f49fb511f95"
    
    return current_state


def prepare_creatomate_payload(state: GraphState) -> dict:
    """
    Prepares the JSON payload for the Creatomate API using template fields from state.
    """
    print("--- Preparing Creatomate Payload ---")
    
    modifications = {}
    
    # Add processed image URLs to the payload
    processed_urls = state.processed_image_urls
    for placeholder, url in processed_urls.items():
        modifications[f"{placeholder}.source"] = url
        print(f"Adding '{placeholder}' with URL to payload.")

    # Add template fields from state
    modifications.update({
        "Address.text": state.address,
        "Details-1.text": state.details_1,
        "Details-2.text": state.details_2,
        "Picture.source": state.picture_source,
        "Email.text": state.email,
        "Phone-Number.text": state.phone_number,
        "Brand-Name.text": state.brand_name,
        "Name.text": state.agent_name
    })

    print("--- Payload Prepared ---")
    
    current_state = state.model_dump()
    current_state["modifications"] = modifications
    return current_state


def create_video_render(state: GraphState) -> dict:
    """
    Sends the request to the Creatomate API to start a new video render.
    """
    if not CREATOMATE_API_KEY:
        print("Error: CREATOMATE_API_KEY not found in .env file.")
        return state.model_dump()

    print("--- Starting Video Render ---")

    headers = {
        "Authorization": f"Bearer {CREATOMATE_API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "template_id": state.template_id,
        "modifications": state.modifications,
    }

    try:
        response = requests.post("https://api.creatomate.com/v2/renders", json=data, headers=headers)
        response.raise_for_status()
        
        render_data = response.json()
        print(f"Creatomate response: {render_data}")
        
        # Handle both single object and array responses
        if isinstance(render_data, list):
            render_id = render_data[0]["id"]
        else:
            render_id = render_data["id"]
        
        print(f"Successfully started render. Render ID: {render_id}")
        
        current_state = state.model_dump()
        current_state["render_id"] = render_id
        return current_state

    except requests.exceptions.RequestException as e:
        print(f"Error calling Creatomate API: {e}")
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_body = e.response.json()
                print(f"Response body: {error_body}")
            except:
                print(f"Response text: {e.response.text}")
        return state.model_dump()


def check_video_status(state: GraphState) -> dict:
    """
    Checks the status of the video render and updates the state.
    """
    render_id = state.render_id
    if not render_id:
        print("Error: Render ID not found in state.")
        current_state = state.model_dump()
        current_state["render_status"] = "error"
        return current_state

    print(f"--- Checking Status for Render ID: {render_id} ---")

    headers = {
        "Authorization": f"Bearer {CREATOMATE_API_KEY}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.get(f"https://api.creatomate.com/v2/renders/{render_id}", headers=headers)
        response.raise_for_status()
        
        render_data = response.json()
        status = render_data.get("status")
        
        print(f"Current render status: '{status}'")
        
        current_state = state.model_dump()
        current_state["render_status"] = status

        if status == "succeeded":
            final_url = render_data.get("url")
            print(f"Render successful! Final video URL: {final_url}")
            current_state["final_video_url"] = final_url
        elif status == "failed":
            print("Error: Video rendering failed.")
        else:
            time.sleep(10)

        return current_state

    except requests.exceptions.RequestException as e:
        print(f"Error checking status: {e}")
        current_state = state.model_dump()
        current_state["render_status"] = "error"
        return current_state


def wait_for_approval(state: GraphState) -> dict:
    """
    HITL node: Pauses execution and waits for human approval of processed images.
    Uses LangGraph's interrupt mechanism to pause the workflow.
    """
    print("\n--- Waiting for Human Approval ---")
    print("Processed images are ready for review.")
    print(f"Images to review: {list(state.processed_image_urls.keys())}")
    
    current_state = state.model_dump()
    current_state["awaiting_approval"] = True
    
    # Return state - the interrupt_before in compile() will pause here
    # The Dash app will update the state with approval decisions
    return current_state


def regenerate_images(state: GraphState) -> dict:
    """
    Regenerates images that were rejected by the human reviewer.
    Can either regenerate with AI or use a replacement image uploaded by user.
    Only processes the rejected images, keeping approved ones unchanged.
    """
    print("\n--- Regenerating Rejected Images ---")
    
    rejected = state.rejected_images
    if not rejected:
        print("No images to regenerate.")
        return state.model_dump()
    
    print(f"Images to regenerate: {rejected}")
    
    current_state = state.model_dump()
    current_state["regeneration_count"] += 1
    
    if not FAL_KEY:
        print("Warning: FAL_KEY not found. Cannot regenerate images.")
        return current_state
    
    # Process each rejected image
    for placeholder in rejected:
        # Check if user provided a replacement image
        if placeholder in state.replacement_images:
            # Use the replacement image path
            file_path = state.replacement_images[placeholder]
            print(f"\nUsing replacement image for '{placeholder}' from {file_path}...")
        else:
            # Use original image for regeneration
            file_path = state.input_images.get(placeholder)
            print(f"\nRegenerating image for '{placeholder}' from {file_path}...")
        
        if not file_path or not os.path.exists(file_path):
            print(f"Warning: Image file not found for {placeholder}. Skipping.")
            continue
        
        try:
            # Upload the image
            with open(file_path, "rb") as f:
                image_bytes = f.read()
            
            uploaded_url = fal_client.upload(image_bytes, content_type="image/jpeg")
            print(f"File uploaded to temporary URL: {uploaded_url}")
            
            # Use a slightly modified prompt for regeneration
            regeneration_prompt = f"A high-quality, clear photograph, vibrant and professional, well-composed with excellent lighting and focus. Attempt {current_state['regeneration_count']}"
            
            # Submit to fal.ai
            result = fal_client.subscribe(
                FAL_MODEL_URL,
                arguments={
                    "prompt": regeneration_prompt,
                    "image_urls": [uploaded_url],
                    "num_images": 1,
                    "output_format": "jpeg",
                    "aspect_ratio": "9:16"
                },
                with_logs=True,
                on_queue_update=on_queue_update,
            )
            
            # Extract the new processed image URL
            if result and "images" in result and len(result["images"]) > 0:
                new_url = result["images"][0]["url"]
                current_state["processed_image_urls"][placeholder] = new_url
                print(f"Successfully regenerated '{placeholder}'. New URL: {new_url}")
            else:
                print(f"Warning: No image URL returned for '{placeholder}'")
        
        except Exception as e:
            print(f"Error regenerating image {file_path}: {e}")
    
    print("\n--- Finished Regenerating Images ---")
    
    # Clear rejected list and reset approval flags for new review
    current_state["rejected_images"] = []
    current_state["approved_images"] = []
    current_state["replacement_images"] = {}
    current_state["human_approval_received"] = False
    
    return current_state
