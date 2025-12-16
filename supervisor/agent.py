from langgraph_supervisor import create_supervisor
from langchain_openai import ChatOpenAI
from langgraph.pregel.remote import RemoteGraph
from langchain.messages import HumanMessage
from langchain.agents import create_agent
from langchain.tools import tool


subagent_graph = RemoteGraph(
    "agent",  # assistant_id as positional argument
    url="http://localhost:8000",
    distributed_tracing=True
)

@tool
def call_subagent(input: str) -> str:
    """Call the subagent to get the answer to the question."""
    result = subagent_graph.invoke({"messages": [HumanMessage(content=input)]})
    return result["messages"][-1]["content"] 

agent = create_agent(model="gpt-4o", tools=[call_subagent])