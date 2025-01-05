"""Demo: FastAPI application for the LangGraph agent."""

import os
from dotenv import load_dotenv
from fastapi import FastAPI
import uvicorn
from copilotkit.integrations.fastapi import add_fastapi_endpoint
from copilotkit import CopilotKitSDK, LangGraphAgent
from my_agent.agent import graph  

load_dotenv()

app = FastAPI()

@app.get("/")
def root():
    """Root endpoint."""
    return {"message": "Welcome to the Study Plan Assistant API!"}

@app.get("/favicon.ico")
async def favicon():
    """Handle favicon.ico requests."""
    return {"message": "No favicon available"}

@app.get("/status")
def status():
    """Status endpoint."""
    return {"status": "OK"}

sdk = CopilotKitSDK(
    agents=[
        LangGraphAgent(
            name="Study Plan Assistant",
            description=(
                "An assistant that helps users create, modify, and review study plans "
                "based on their preferences. It provides topic scheduling and feedback."
            ),
            graph=graph,  
        )
    ]
)

add_fastapi_endpoint(app, sdk, "/copilotkit")
@app.get("/api/copilotkit")
def read_copilotkit():
    return {"message": "This is the CopilotKit API"}
def main():
    """Run the FastAPI server."""
    port = int(os.getenv("PORT", "8000"))  
    uvicorn.run("my_agent.demo:app", host="localhost", port=port, reload=True)  # Use localhost


