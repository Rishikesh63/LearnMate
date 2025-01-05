from typing import Annotated
from langchain_openai import OpenAI
from langchain_anthropic import ChatAnthropic
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from pydantic import BaseModel
from typing_extensions import TypedDict
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
import os
from dotenv import load_dotenv
import logging

load_dotenv()
tavily_api_key = os.getenv("TAVILY_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")
copilot_api_key = os.getenv("COPILOT_CLOUD_PUBLIC_API_KEY")
langgraph_api_key = os.getenv("LANGGRAPH_API_KEY")

if not tavily_api_key:
    raise ValueError("Missing TAVILY_API_KEY in environment variables.")
if not openai_api_key:
    raise ValueError("Missing OPENAI_API_KEY in environment variables.")
if not copilot_api_key:
    raise ValueError("Missing COPILOT_CLOUD_PUBLIC_API_KEY in environment variables.")
if not langgraph_api_key:
    raise ValueError("Missing LANGGRAPH_API_KEY in environment variables.")

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class State(TypedDict):
    messages: list
    ask_human: bool
    user_preferences: dict
    study_plan: dict

class RequestAssistance(BaseModel):
    """Escalate the conversation to an expert."""
    request: str

tavily_tool = TavilySearchResults(max_results=2, tavily_api_key=tavily_api_key)
tools = [tavily_tool]

anthropic_llm = ChatAnthropic(model="claude-3-5-sonnet-20240620")
openai_llm = OpenAI(model="gpt-4o-mini", openai_api_key=openai_api_key)
llm_with_tools = anthropic_llm.bind_tools(tools + [RequestAssistance])

def validate_messages(messages):
    """
    Validate that all messages are in the correct format.
    Each message must be a dictionary with 'role' and 'content' keys.
    """
    for msg in messages:
        if not isinstance(msg, dict) or "role" not in msg or "content" not in msg:
            logger.error(f"Invalid message format: {msg}")
            raise ValueError(f"Invalid message format: {msg}")

def validate_and_convert_message(message):
    """
    Ensures the message is valid and converts it to a supported format.
    """
    if isinstance(message, str):
        return HumanMessage(content=message)
    elif isinstance(message, dict):
        role = message.get("role")
        content = message.get("content")
        if role == "user":
            return HumanMessage(content=content)
        elif role == "assistant":
            return AIMessage(content=content)
        elif role == "system":
            return SystemMessage(content=content)
        else:
            logger.error(f"Invalid role in message dict: {role}")
            raise ValueError(f"Invalid role in message dict: {role}")
    else:
        logger.error(f"Unsupported message format: {message}")
        raise ValueError(f"Unsupported message format: {message}")

def debug_state(state):
    """
    Log the entire state for debugging purposes.
    """
    logger.debug(f"State: {state}")

def generate_study_plan(user_preferences: dict):
    topics = user_preferences.get("topics", ["General Studies"])
    duration = user_preferences.get("duration", "1 week")
    difficulty = user_preferences.get("difficulty", "Intermediate")

    return {
        "topics": topics,
        "duration": duration,
        "difficulty": difficulty,
        "schedule": [
            {"day": i + 1, "topic": topic, "time": f"{2 * (i + 1)} hours"}
            for i, topic in enumerate(topics)
        ],
    }

def chatbot(state: State):
    try:
        messages = state["messages"]
        validate_messages(messages)

        user_message = messages[-1]["content"].lower()
        if "study plan" in user_message:
            return get_study_plan({"state": state})

        converted_messages = [validate_and_convert_message(msg) for msg in messages]
        debug_state(state)

        response = llm_with_tools.invoke(converted_messages)
        response_messages = [{"role": "assistant", "content": response["text"]}]

        ask_human = any(
            call["name"] == RequestAssistance.__name__ for call in response.tool_calls
        )

        return {"messages": state["messages"] + response_messages, "ask_human": ask_human}
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return {
            "messages": state["messages"] + [
                {"role": "assistant", "content": "An unexpected error occurred."}
            ],
            "ask_human": False,
        }

def human_node(state: State):
    return {"messages": state["messages"] + [{"role": "assistant", "content": "Awaiting human input..."}], "ask_human": False}

def get_study_plan(input_data: dict):
    logger.debug(f"Input data received: {input_data}")

    if "state" not in input_data:
        raise TypeError("Input must have a 'state' key.")

    state = input_data["state"]

    if not isinstance(state["messages"], list):
        raise TypeError(f"Expected 'state[\"messages\"]' to be a list, got {type(state['messages'])} instead.")

    user_preferences = state.get("user_preferences", {})
    study_plan = generate_study_plan(user_preferences)
    state["study_plan"] = study_plan

    response_message = {
        "role": "assistant",
        "content": f"Study plan created: {study_plan}",
    }
    state["messages"].append(response_message)

    return {"state": state}

def review_previous_plan(state: State):
    previous_plan = state.get("study_plan", "No previous plans available.")
    return {"messages": state["messages"] + [{"role": "assistant", "content": f"Here is your previous study plan: {previous_plan}"}]}

def human_feedback(state: State):
    return {"messages": state["messages"] + [{"role": "assistant", "content": "Would you like to approve or modify the study plan?"}], "ask_human": False}

def select_next_node(state: State):
    if state["ask_human"]:
        return "human"
    return tools_condition(state)

graph_builder = StateGraph(State)

# Add nodes to the graph
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("human", human_node)
graph_builder.add_node("get_study_plan", get_study_plan)
graph_builder.add_node("review_previous_plan", review_previous_plan)
graph_builder.add_node("human_feedback", human_feedback)
graph_builder.add_node("tools", ToolNode(tools=[tavily_tool]))

# Add conditional edges
graph_builder.add_conditional_edges(
    "chatbot", select_next_node, {"human": "human", "tools": "tools", END: END}
)
graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge("human", "chatbot")
graph_builder.add_edge("get_study_plan", "human_feedback")
graph_builder.add_edge("human_feedback", "chatbot")
graph_builder.add_edge(START, "get_study_plan")

graph_builder.add_edge("chatbot", "review_previous_plan")

# Compile the graph with checkpointing
memory = MemorySaver()
graph = graph_builder.compile(checkpointer=memory, interrupt_before=["human"])
