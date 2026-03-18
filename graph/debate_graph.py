from langgraph.graph import StateGraph, START, END
from graph.state import DebateState
from agents.steelman import steelman_node
from agents.devil import devil_node
from agents.researcher import researcher_node
from agents.judge import judge_node

def build_debate_graph():
    graph = StateGraph(DebateState)

    graph.add_node("steelman", steelman_node)
    graph.add_node("devil", devil_node)
    graph.add_node("researcher", researcher_node)
    graph.add_node("judge", judge_node)

    graph.add_edge(START, "steelman")
    graph.add_edge("steelman", "devil")
    graph.add_edge("devil", "researcher")
    graph.add_edge("researcher", "judge")
    graph.add_edge("judge", END)

    return graph.compile()

debate_graph = build_debate_graph()
