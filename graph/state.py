from typing import TypedDict

class DebateState(TypedDict):
    idea: str           # The original idea being debated
    steelman_arg: str   # Best case argument FOR the idea
    devil_arg: str      # Worst case argument AGAINST the idea
    research: str       # Real world facts from web search
    verdict: str        # Final structured decision brief


    