from graph.debate_graph import debate_graph

def run_debate(idea: str) -> dict:
    print(f"\n{'='*60}")
    print(f"💡 IDEA: {idea}")
    print(f"{'='*60}\n")

    final_state = debate_graph.invoke({
        "idea": idea,
        "steelman_arg": "",
        "devil_arg": "",
        "research": "",
        "verdict": ""
    })

    return final_state

if __name__ == "__main__":
    idea = "I should quit my job and build an AI startup"
    result = run_debate(idea)

    print("\n" + "="*60)
    print("🛡️  STEELMAN:")
    print(result["steelman_arg"])

    print("\n" + "="*60)
    print("😈  DEVIL:")
    print(result["devil_arg"])

    print("\n" + "="*60)
    print("🔍  RESEARCH:")
    print(result["research"])

    print("\n" + "="*60)
    print("⚖️   VERDICT:")
    print(result["verdict"])

