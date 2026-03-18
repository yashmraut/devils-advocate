from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.85)

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are the Devil's Advocate Agent — a razor-sharp critical thinker 
whose sole job is to find every flaw, risk, and weakness in an idea.

Your rules:
- Be brutally honest, not mean — there's a difference
- Attack the IDEA, never the person
- If a steelman argument exists, systematically dismantle its key points
- Focus on: hidden risks, faulty assumptions, market realities, execution problems
- Use real-world examples of similar ideas that failed when possible
- Be concise: 3-4 devastating bullet points, then one sharp closing statement
- Do NOT suggest improvements — that is not your job
- Do NOT mention positives — the steelman handles that"""
    ),
    (
        "human",
        """Idea being evaluated: {idea}

Steelman's best case (attack this directly): {steelman_arg}

Identify every critical flaw and risk. Be ruthless but fair."""
    )
])


chain = prompt | llm

def devil_node(state: dict) -> dict:
    print("😈  Devil's Advocate is sharpening its attack...")

    response = chain.invoke({
        "idea": state["idea"],
        # steelman always runs before devil in our graph
        # so steelman_arg will always exist here — no .get() needed
        # but we use .get() anyway as safe habit
        "steelman_arg": state.get("steelman_arg", "")
    })

    return {"devil_arg": response.content}


# ── TEMP TEST (delete this block later) ───────────────────────────────────────
# if __name__ == "__main__":
#     # print("hello")
#     # We simulate a full state — as if steelman already ran
#     fake_state = {
#         "idea": "I should quit my job and build an AI startup",
#         "steelman_arg": """
#         - The AI mark-et is growing at 37% annually — timing could not be better
#         - Your domain expertise gives you an unfair advantage over generic founders
#         - Remote work culture means you can hire top talent without relocation costs
#         - Lean startup methodology lets you validate with minimal capital
        
#         The window for AI opportunities is open RIGHT NOW — waiting means 
#         letting better-positioned competitors claim the space you could own.
#         """
#     }

#     result = devil_node(fake_state)
#     print("\n=== DEVIL'S ARGUMENT ===")
#     print(result["devil_arg"])