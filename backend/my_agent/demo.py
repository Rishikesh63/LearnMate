"""Demo: FastAPI application for the LangGraph agent."""

import os
from dotenv import load_dotenv
from fastapi import FastAPI
import uvicorn
from copilotkit.integrations.fastapi import add_fastapi_endpoint
from copilotkit import CopilotKitSDK, LangGraphAgent
from my_agent.agent import graph  # Import the graph from agent.py

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Root route to handle base URL requests
@app.get("/")
def root():
    """Root endpoint."""
    return {"message": "Welcome to the Study Plan Assistant API!"}

# Favicon route to suppress browser favicon.ico errors
@app.get("/favicon.ico")
async def favicon():
    """Handle favicon.ico requests."""
    return {"message": "No favicon available"}

# Status route
@app.get("/status")
def status():
    """Status endpoint."""
    return {"status": "OK"}

# Define the SDK and integrate the LangGraph agent
sdk = CopilotKitSDK(
    agents=[
        LangGraphAgent(
            name="study_plan_assistant",
            description=(
                "An assistant that helps users create, modify, and review study plans "
                "based on their preferences. It provides topic scheduling and feedback."
            ),
            graph=graph,  # Use the graph defined in agent.py
        )
    ]
)

# Add the SDK endpoint to the FastAPI app
add_fastapi_endpoint(app, sdk, "/copilotkit")

# Define the main function to run the server
def main():
    """Run the FastAPI server."""
    port = int(os.getenv("PORT", "8000"))  # Default to port 8000
    uvicorn.run("my_agent.demo:app", host="127.0.0.1", port=port, reload=True)  # Use localhost

# Run the server if executed directly
if __name__ == "__main__":
    main()
