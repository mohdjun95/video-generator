import os
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from state import GraphState
from nodes import (
    process_images_with_fal, 
    prepare_creatomate_payload, 
    create_video_render, 
    check_video_status,
    wait_for_approval,
    regenerate_images
)

# --- Graph Definition ---

class VideoGenerationWorkflow:
    def __init__(self, checkpointer=None):
        self.workflow = StateGraph(GraphState)
        self.checkpointer = checkpointer or MemorySaver()
        self._define_graph()

    def _define_graph(self):
        """
        Defines the nodes and edges of the LangGraph workflow with HITL approval.
        """
        # Add all nodes to the workflow
        self.workflow.add_node("process_images", process_images_with_fal)
        self.workflow.add_node("wait_approval", wait_for_approval)
        self.workflow.add_node("regenerate", regenerate_images)
        self.workflow.add_node("prepare_payload", prepare_creatomate_payload)
        self.workflow.add_node("create_render", create_video_render)
        self.workflow.add_node("check_status", check_video_status)

        # Set the entry point
        self.workflow.set_entry_point("process_images")

        # Define the sequence: process → wait for approval
        self.workflow.add_edge("process_images", "wait_approval")
        
        # After approval, decide whether to regenerate or proceed
        self.workflow.add_conditional_edges(
            "wait_approval",
            self.check_approval,
            {
                "regenerate": "regenerate",
                "proceed": "prepare_payload",
            }
        )
        
        # After regeneration, go back to approval
        self.workflow.add_edge("regenerate", "wait_approval")
        
        # Continue with video creation flow
        self.workflow.add_edge("prepare_payload", "create_render")
        
        # Add conditional edges for polling
        self.workflow.add_conditional_edges(
            "create_render",
            self.should_continue_render,
            {
                "continue": "check_status",
                "finish": END,
                "error": END,
            }
        )
        self.workflow.add_conditional_edges(
            "check_status",
            self.should_continue_render,
            {
                "continue": "check_status",
                "finish": END,
                "error": END,
            }
        )

    def check_approval(self, state: GraphState) -> str:
        """
        Determines whether to regenerate images or proceed based on approval.
        """
        # If there are rejected images, regenerate them
        if state.rejected_images and len(state.rejected_images) > 0:
            return "regenerate"
        
        # If all images are approved, proceed to video creation
        if state.human_approval_received:
            return "proceed"
        
        # Default: wait for approval (shouldn't reach here normally)
        return "proceed"

    def should_continue_render(self, state: GraphState) -> str:
        """
        Determines the next step based on the render status.
        """
        render_status = state.render_status
        
        # If no status yet (just created render), continue to check
        if render_status is None:
            return "continue"
        
        if render_status == "succeeded":
            return "finish"
        elif render_status == "failed" or render_status == "error":
            return "error"
        else:
            # Still processing (planned, rendering, etc.)
            return "continue"

    def compile(self):
        """
        Compiles the workflow into a runnable graph with checkpointing.
        """
        return self.workflow.compile(checkpointer=self.checkpointer, interrupt_after=["wait_approval"])

# --- Main Execution ---

if __name__ == "__main__":
    # --- Configuration ---
    # Specify the Creatomate template ID we want to use
    TEMPLATE_ID = "6821de4e-c173-4a8f-9c8e-d8f0e3c292ed" # Real Estate Ad with 5 photos

    # Provide the local paths to the images you want to use.
    # The keys should match the placeholder names in your Creatomate template.
    INPUT_IMAGES = {
        "Photo-1": "WhatsApp Image 2025-10-05 at 10.33.35.jpeg",
        "Photo-2": "WhatsApp Image 2025-10-05 at 10.33.36 (1).jpeg",
        "Photo-3": "WhatsApp Image 2025-10-05 at 10.33.36.jpeg",
        "Photo-4": "WhatsApp Image 2025-10-05 at 10.33.37.jpeg",
        "Photo-5": "WhatsApp Image 2025-10-05 at 10.33.38.jpeg",
    }

    # --- Graph Invocation ---
    
    # Initial state for the graph
    initial_state = {
        "template_id": TEMPLATE_ID,
        "input_images": INPUT_IMAGES,
        "processed_image_urls": {},
        "modifications": {},
        "render_id": None,
        "final_video_url": None,
    }

    # Instantiate and compile the workflow
    graph_builder = VideoGenerationWorkflow()
    app = graph_builder.compile()

    print("--- Invoking Graph ---")
    # Run the graph and stream the results
    for output in app.stream(initial_state):
        # The key is the name of the node that just ran
        for key, value in output.items():
            print(f"Output from node '{key}':")
            print("---")
            print(value)
    print("--- Graph Finished ---")

    # To see the final state, you can invoke the graph like this:
    # final_state = app.invoke(initial_state)
    # print("\n--- Final State ---")
    # print(final_state)
