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

# Initialize memory for checkpoints
memory = MemorySaver()

# Initialize the language model
model = ChatAnthropic(model="claude-3-sonnet-20240229")

# Initialize search tools
search = DuckDuckGoSearchRun()
tools = [search]

# Create the agent with the model and tools
agent_executor = create_react_agent(model, tools, checkpointer=memory)

# Configuration for streaming
config = {"configurable": {"thread_id": "abc123"}}

# Use the agent with an initial prompt
initial_message = HumanMessage(content="hi im bob! and i live in olympia washington")
for chunk in agent_executor.stream({"messages": [initial_message]}, config):
    print(chunk)
    print("----")

# Allow user to enter a custom prompt
prompt = input("Enter a prompt: ")
for chunk in agent_executor.stream(
    {"messages": [HumanMessage(content=prompt)]}, config
):
    print(chunk)
    print("----")
```