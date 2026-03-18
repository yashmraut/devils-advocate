from langchain_groq import ChatGroq
from langchain_tavily import TavilySearch
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.3,
    max_tokens=500
)

search_tool = TavilySearch(
    max_results=2
)

tools = [search_tool]

system_prompt = """You are a Research Agent — a rigorous fact-finder who only 
deals in verified, real-world data. You have access to live web search.

Your rules:
- Search for SPECIFIC facts relevant to this debate: market data, failure rates,
  statistics, expert opinions, recent news
- Search at least 2 different angles (pro AND con evidence)
- Only report what the search results actually say — no hallucination
- Clearly label where facts support or challenge the idea
- Format: bullet points of key findings, each with a source reference
- End with: one-line summary of what the data says overall"""

research_agent = create_react_agent(
    model=llm,
    tools=tools,
    prompt=system_prompt
)

def researcher_node(state: dict) -> dict:
    print("🔍  Researcher is searching the web...")

    # Build the human message combining all debate context
    steelman_short = state.get("steelman_arg", "")[:300]
    devil_short = state.get("devil_arg", "")[:300]

    human_message = f"""Idea: {state["idea"]}

                Key arguments for: {steelman_short}
                Key arguments against: {devil_short}

                Search for 2-3 key facts and statistics relevant to this idea."""

    # create_react_agent uses the messages format
    result = research_agent.invoke({
        "messages": [("human", human_message)]
    })

    # The final response is the last message in the messages list
    # result["messages"][-1] is the final AIMessage after all tool calls
    final_message = result["messages"][-1]
    return {"research": final_message.content}

# ── TEMP TEST (delete this block later) ───────────────────────────────────────
# if __name__ == "__main__":
#     fake_state = {
#         "idea": "I should quit my job and build an AI startup",
#         "steelman_arg": """
#         - AI market growing at 37% annually
#         - Your domain expertise gives unfair advantage
#         - Lean startup means you need minimal capital
#         """,
#         "devil_arg": """
#         - 90% of startups fail within the first year
#         - AI space is dominated by well-funded giants
#         - Without salary, personal runway is your real constraint
#         """
#     }

#     result = researcher_node(fake_state)
#     print("\n=== RESEARCH FINDINGS ===")
#     print(result["research"])
