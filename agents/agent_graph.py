import os
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict, Annotated
from langchain.messages import AnyMessage, HumanMessage, SystemMessage
from langgraph.graph.message import add_messages
from langchain_aws import ChatBedrockConverse
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.runnables import RunnableConfig
from langchain_ollama.chat_models import ChatOllama
import asyncio

load_dotenv()

# Set API Key
os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY", "")

# Initiate LLM
# llm = ChatBedrockConverse(model='us.anthropic.claude-haiku-4-5-20251001-v1:0', region_name='us-west-2')
llm = ChatOllama(model="llama3.2:3b", temperature=0)


class AgentStates(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]


def agent(state: AgentStates):
    response = llm.invoke(state["messages"])
    return {"messages": [response]}


agent_graph = StateGraph(AgentStates)
agent_graph.add_node("agent", agent)

agent_graph.add_edge(START, 'agent')
agent_graph.add_edge('agent', END)

graph = agent_graph.compile(checkpointer=InMemorySaver())


# Show the agent
# from IPython.display import Image, display
# display(Image(agent.get_graph(xray=True).draw_mermaid_png()))
# print(graph.get_graph().draw_ascii())


async def on_message_events(input_message):
    final_state = None
    config: RunnableConfig = {"configurable": {"thread_id": "1"}}
    async for chunk in graph.astream(
            {"messages": [{"role": "user", "content": input_message}]},
            stream_mode=["messages", "values"],
            version="v2",
            config=config,
    ):
        if chunk["type"] == "messages":
            msg, metadata = chunk["data"]

            if msg.content:
                if isinstance(msg.content, str):
                    yield {"type": "token", "data": msg.content}
                elif isinstance(msg.content, list):
                    for part in msg.content:
                        if isinstance(part, dict) and part.get("text"):
                            yield {"type": "token", "data": part["text"]}

        elif chunk["type"] == "values":
            final_state = chunk["data"]

    yield {"type": "final_state", "data": final_state}
    yield {"type": "done"}


async def on_message_events(input_message):
    final_state = {}
    config_graph = {"configurable": {"thread_id": "1"}}

    # Use astream and async for to stay within the event loop
    async for chunk in graph.astream({"messages": [{"role": "user", "content": input_message}]},
                                     stream_mode=["messages", "values"], version='v2', config=config_graph):
        if chunk['type'] == "messages":
            if chunk['data']:
                yield {'type': 'token', 'data': chunk['data'][0].content}

        if chunk['type'] == "values":
            final_state = chunk['data']

    yield {'type': 'final_state', 'data': final_state}

# async def main():
#     async for event in on_message_events("Hi"):
#         print(event)
#
#
# asyncio.run(main())
