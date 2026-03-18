from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.7)

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are a Steelman Agent — an expert at constructing the strongest, 
most compelling argument IN FAVOR of any idea.

Your rules:
- Present the BEST possible version of the idea
- Use logical reasoning, not blind optimism  
- Highlight genuine strengths and real opportunities
- If a counter-argument exists in context, directly rebut it with facts
- Be concise: 3-4 punchy bullet points, then one strong closing statement
- Do NOT mention weaknesses — that is another agent's job"""
    ),
    (
        "human",
        """Idea to steelman: {idea}

Counter-argument to rebut (empty if first round): {devil_arg}

Build the strongest possible case FOR this idea."""
    )
])
    

chain = prompt | llm

def steelman_node(state: dict) -> dict:
    print("🛡️   Steelman agent is thinking...")  # helpful for debugging

    response = chain.invoke({
        "idea": state["idea"],
        # If devil hasn't argued yet, pass empty string — that's fine
        "devil_arg": state.get("devil_arg", "")
    })

    # response is an AIMessage object from LangChain
    # .content gives us the actual text string inside it
    return {"steelman_arg": response.content}


    # ── TEMP TEST (delete this block later) ───────────────────────────────────────
# if __name__ == "__main__":
#     # Simulate what LangGraph would pass as state
#     # print("hel.lo")
#     fake_state = {
#         "idea": "I should quit my job and build an AI startup",
#         "devil_arg": ""  # empty because it's the first round
#     }

#     result = steelman_node(fake_state)
#     print("\n=== STEELMAN ARGUMENT ===")
#     print(result["steelman_arg"])