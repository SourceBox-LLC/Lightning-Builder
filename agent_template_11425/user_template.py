```python
import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent

# Load environment variables
load_dotenv()

# Define tools and model if necessary
# tools = [...]
# model = ...

# Create the agent executor
agent_executor = create_react_agent(model, tools, checkpointer=memory)

# Configuration for the agent
config = {"configurable": {"thread_id": "abc123"}}

# Use the agent with a predefined message
for chunk in agent_executor.stream(
    {"messages": [HumanMessage(content="hi im bob! and i live in olympia washington")]}, config
):
    print(chunk)
    print("----")

# Use the agent with a user-defined prompt
prompt = input("Enter a prompt: ")
for chunk in agent_executor.stream(
    {"messages": [HumanMessage(content=prompt)]}, config
):
    print(chunk)
    print("----")
```
