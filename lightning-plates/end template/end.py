from langchain.agents import AgentExecutor

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

agent_executor.invoke({"input": "hi!"})

agent_executor.invoke({"input": "how can langsmith help with testing?"})