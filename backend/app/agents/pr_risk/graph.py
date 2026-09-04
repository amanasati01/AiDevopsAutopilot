from langgraph.graph import StateGraph,START,END
from .state import PRRiskState
from .nodes import fetch_pr,fetch_pr_files
from .context import PRRiskContext
def build_pr_risk_graph():
    graph = StateGraph(PRRiskState,context_schema=PRRiskContext)
    graph.add_node("fetch_pr",fetch_pr)
    graph.add_node("fetch_pr_files",fetch_pr_files)
    graph.add_edge(START,"fetch_pr")
    graph.add_edge("fetch_pr","fetch_pr_files")
    graph.add_edge("fetch_pr_files",END)
    print("Graph.compie -> ",graph.compile)
    return graph.compile()