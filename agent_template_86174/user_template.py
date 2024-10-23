```python
from dotenv import load_dotenv
import os
from langchain_anthropic import ChatAnthropic
from langgraph.checkpoint.memory import MemorySaver
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent

# Load environment variables
load_dotenv()

# Initialize the model and memory
memory = MemorySaver()
model = ChatAnthropic(model="claude-3-sonnet-20240229")

# Initialize the tools
search = DuckDuckGoSearchRun()
tools = [search]

# Create the agent executor
agent_executor = create_react_agent(model, tools, checkpointer=memory)

# Define configuration
config = {"configurable": {"thread_id": "abc123"}}

# Use the agent
for chunk in agent_executor.stream(
    {"messages": [HumanMessage(content="hi im bob! and i live in olympia washington")]}, config
):
    print(chunk)
    print("----")

# Prompt for user input and process the input through the agent
prompt = input("Enter a prompt: ")
for chunk in agent_executor.stream(
    {"messages": [HumanMessage(content=prompt)]}, config
):
    print(chunk)
    print("----")
```