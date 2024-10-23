```python
import os
from dotenv import load_dotenv

load_dotenv()

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from langchain_community.tools import DuckDuckGoSearchRun

# Initialize the memory saver and model
memory = MemorySaver()
model = ChatAnthropic(model="claude-3-sonnet-20240229")

# Initialize tools
search = DuckDuckGoSearchRun()
tools = [search]

# Create the agent
agent_executor = create_react_agent(model, tools, checkpointer=memory)

# Use the agent
config = {"configurable": {"thread_id": "abc123"}}
for chunk in agent_executor.stream(
    {"messages": [HumanMessage(content="hi im bob! and i live in olympia washington")]}, config
):
    print(chunk)
    print("----")

prompt = input("Enter a prompt: ")
for chunk in agent_executor.stream(
    {"messages": [HumanMessage(content=prompt)]}, config
):
    print(chunk)
    print("----")
```