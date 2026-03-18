from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.2
)

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are the Judge Agent — a wise, senior decision-making consultant 
with 20 years of experience evaluating ideas across business, tech, and life.

You have just witnessed a full debate. Your job is to synthesize everything 
into a clear, actionable decision brief.

Your output MUST follow this exact format:

## VERDICT
[One bold sentence: Proceed / Proceed with Caution / Do Not Proceed]

## CONFIDENCE SCORE
[X/10 — how confident you are in this verdict, with one line explanation]

## WHY THE STEELMAN WINS / LOSES
[2-3 sentences on which steelman points hold up under scrutiny]

## WHY THE DEVIL IS RIGHT / WRONG  
[2-3 sentences on which criticisms are legitimate vs overblown]

## WHAT THE DATA SAYS
[2-3 sentences synthesizing the research findings into the decision]

## KEY CONDITIONS
[3 bullet points — specific conditions under which this idea succeeds]

## BIGGEST SINGLE RISK
[One sentence — the single most important thing that could kill this idea]

## RECOMMENDED FIRST STEP
[One concrete, specific action the person should take THIS WEEK]

Be direct. Be honest. The person is counting on you for real guidance."""
    ),
    (
        "human",
        """Idea: {idea}

STEELMAN'S CASE:
{steelman_arg}

DEVIL'S CRITIQUE:
{devil_arg}

RESEARCH FINDINGS:
{research}

Deliver your verdict."""
    )
])

chain = prompt | llm

def judge_node(state: dict) -> dict:
    print("⚖️   Judge is deliberating...")

    response = chain.invoke({
        "idea": state["idea"],
        "steelman_arg": state.get("steelman_arg", ""),
        "devil_arg": state.get("devil_arg", ""),
        "research": state.get("research", "No research available.")
    })

    return {"verdict": response.content}

# ── TEMP TEST (delete this block later) ───────────────────────────────────────
# if __name__ == "__main__":
#     fake_state = {
#         "idea": "I should quit my job and build an AI startup",
#         "steelman_arg": """
#         - AI market growing at 37% annually — timing is perfect
#         - Domain expertise gives an unfair advantage over generic founders
#         - Lean startup methodology means minimal capital needed to validate
#         - Remote culture means access to global talent pool
#         """,
#         "devil_arg": """
#         - 90% of AI startups fail within 2 years
#         - Market growth attracts better-funded competitors daily
#         - Personal runway without salary is the real constraint
#         - Domain expertise rarely translates to business execution skills
#         """,
#         "research": """
#         - CB Insights 2024: 73% of AI startups fail due to premature scaling
#         - YC data shows founders with 6+ months runway have 3x survival rate
#         - AI SaaS companies reaching product-market fit average 18 months
#         - Domain expert founders outperform generalist founders by 40% in B2B
#         """
#     }

#     result = judge_node(fake_state)
#     print("\n=== JUDGE'S VERDICT ===")
#     print(result["verdict"])
