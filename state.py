from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class GraphState(BaseModel):
    """
    Represents the state of our graph using Pydantic for validation.

    Attributes:
        template_id: The ID of the Creatomate template.
        input_images: A dictionary mapping template placeholders to local file paths.
        processed_image_urls: A dictionary mapping placeholders to the new URLs
                              after processing and uploading.
        modifications: The final JSON payload for the Creatomate API.
        render_id: The ID of the video render job.
        render_status: The status of the video render (planned, rendering, succeeded, failed).
        final_video_url: The URL of the final rendered video.
        
        # Template-specific fields
        address: Property address
        details_1: First detail line (sqft, bedrooms, bathrooms)
        details_2: Second detail line (built year, garage, price)
        picture_source: Agent/brand picture URL
        email: Contact email
        phone_number: Contact phone
        brand_name: Company/brand name
        agent_name: Agent name
        
        # HITL (Human-in-the-Loop) fields
        awaiting_approval: Whether the workflow is waiting for human approval.
        approved_images: List of placeholder names that have been approved.
        rejected_images: List of placeholder names that need regeneration.
        replacement_images: Dict mapping placeholder to new uploaded image path
        human_approval_received: Whether human has provided approval decision.
        regeneration_count: Number of times images have been regenerated.
    """
    template_id: str
    input_images: Dict[str, str]
    processed_image_urls: Dict[str, str] = {}
    modifications: Dict[str, Any] = {}
    render_id: Optional[str] = None
    render_status: Optional[str] = None
    final_video_url: Optional[str] = None
    
    # Template fields
    address: str = "Los Angeles,\nCA 90045"
    details_1: str = "2,500 sqft\n4 Bedrooms\n3 Bathrooms"
    details_2: str = "Built in 1995\n2 Garage Spaces\n$1,595,000"
    agent_picture_path: Optional[str] = None  # Path to uploaded agent/brand picture
    picture_source: str = ""  # Will be set after processing agent picture
    email: str = "elisabeth@mybrand.com"
    phone_number: str = "(123) 555-1234"
    brand_name: str = "Build Masters Constructions"
    agent_name: str = "Elisabeth Parker"
    
    # HITL fields
    awaiting_approval: bool = False
    approved_images: List[str] = []
    rejected_images: List[str] = []
    replacement_images: Dict[str, str] = {}
    human_approval_received: bool = False
    regeneration_count: int = 0
