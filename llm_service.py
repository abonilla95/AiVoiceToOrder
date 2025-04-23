import os
import base64
from text_to_speech import text_to_speech
from typing import Annotated
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage

# Load environment variables from a .env file
load_dotenv()

# Retrieve the API key from the environment variables
api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    llm = ChatOpenAI(
        model="gpt-4o-mini-audio-preview",
        api_key=api_key,
        modalities=["text", "audio"],
        audio={"voice": "coral", "format": "mp3"},
    )
else:
    raise ValueError("OPENAI_API_KEY not found in environment variables.")


class State(TypedDict):
    """State of the LLM service."""

    messages: Annotated[list, add_messages] = [
        {
            "role": "system",
            "content": open("./prompts/restaurant_v2.txt", "r").read(),
        } # Can prepopulate with AI/User messages if needed to provide few-shot examples
    ]


def chatbot(state: State):
    return {"messages": [llm.invoke(state["messages"])]}


@tool
def add_to_order(item: str) -> str:
    """Add an item to the order."""
    with open("order.txt", "a+") as f:
        f.write(f"{item}\n")
    return f"Added {item} to the order."

@tool
def get_order() -> str:
    """Get the current order."""
    with open("order.txt", "r") as f:
        order = f.read()
    return f"Current order: {order}"

@tool
def clear_order() -> str:
    """Clear the current order."""
    with open("order.txt", "w") as f:
        f.write("")
    return "Order cleared."

@tool
def update_order(item: str) -> str:
    """Update the current order."""
    with open("order.txt", "w") as f:
        f.write(f"{item}\n")
    return f"Updated order to {item}."


tools = [ add_to_order, get_order, clear_order, update_order ]
llm = llm.bind_tools(tools)
graph_builder = StateGraph(State)
tool_node = ToolNode(tools=tools)
graph_builder.add_node("tools", tool_node)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge("chatbot", "tools")
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)
graph = graph_builder.compile()


def chatbot_service(user_input: str) -> str:
    """Chatbot service that uses the LangChain OpenAI LLM."""
    response = graph.invoke({"messages": [{"role": "user", "content": user_input}]})
    if type(response["messages"][-1]) == AIMessage:
        audio_response = response["messages"][-1].additional_kwargs["audio"]["data"]
            
        # Convert the audio response (base64 string) to bytes
        audio_response = base64.b64decode(audio_response)
        with open("response.mp3", "wb") as f:
            f.write(audio_response)
    elif type(response["messages"][-1]) == ToolMessage:
        tool_content = response["messages"][-1].content
        text_to_speech(tool_content)
    else:
        return None
