from langchain.agents import initialize_agent, create_structured_chat_agent
from langchain.tools import Tool
from langchain_openai import OpenAI  # Updated import for the LLM

# Define your search tool
def search_tool(query: str) -> str:
    # Replace with your search implementation
    return f"Results for: {query}"

search = Tool(
    name="search",
    func=search_tool,
    description="Useful for searching the web for information."
)

# Define your calculator tool
def calculator_tool(expression: str) -> str:
    # Replace with your calculator implementation
    result = eval(expression)  # Note: using eval is not safe for untrusted input.
    return str(result)

calculator = Tool(
    name="calculator",
    func=calculator_tool,
    description="Useful for performing arithmetic calculations."
)

# Initialize the LLM
llm = OpenAI(api_key="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")  # Replace with your actual API key

# Initialize the agent with the LLM
tools = [search, calculator]
agent = create_structured_chat_agent(tools, llm=llm)

# Now you can use the agent
query = "What's the capital of France?"
result = agent.invoke({"input": query})
print(result)
