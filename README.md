# 🎭 Devil's Advocate — AI-Powered Decision Coach

> Four specialized AI agents debate your ideas from every angle and deliver a structured verdict to help you make better decisions.

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![LangChain](https://img.shields.io/badge/LangChain-1.2+-green?style=flat-square)
![LangGraph](https://img.shields.io/badge/LangGraph-1.0+-orange?style=flat-square)
![Groq](https://img.shields.io/badge/Groq-LLaMA_3.3_70B-purple?style=flat-square)
![Gradio](https://img.shields.io/badge/Gradio-UI-yellow?style=flat-square)
![HuggingFace](https://img.shields.io/badge/HuggingFace-Spaces-orange?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-lightgrey?style=flat-square)

---

## 🔗 Live Demo

**[Try it on Hugging Face Spaces →](YOUR_HUGGING_FACE_URL)**

---

## 📌 What is this?

Most AI tools are built to agree with you. This one doesn't.

**Devil's Advocate** is a multi-agent AI system that stress-tests your ideas, plans, and decisions by running a structured debate across four specialized agents — before you commit to anything.

Submit any decision like *"Should I quit my job and start a startup?"* and watch four AI agents debate it from completely different perspectives, backed by real-world data.

---

## 🤖 How it works

```
User submits an idea
        ↓
┌─────────────────────────────────────────────┐
│              LangGraph StateGraph            │
│                                             │
│  🛡️ Steelman    → Best case FOR the idea    │
│       ↓                                     │
│  😈 Devil       → Worst case AGAINST        │
│       ↓                                     │
│  🔍 Researcher  → Real data from the web    │
│       ↓                                     │
│  ⚖️  Judge      → Structured final verdict  │
└─────────────────────────────────────────────┘
        ↓
  Decision Brief with confidence score
  + key risks + recommended first step
```

Each agent reads from and writes to a **shared TypedDict state** — passing context to the next agent in sequence. By the time the Judge runs, it has the full debate sitting in state to synthesize from.

---

## 🧠 The Four Agents

| Agent | Role | Temperature |
|-------|------|-------------|
| 🛡️ **Steelman** | Builds the strongest possible case *for* your idea using logical reasoning and genuine opportunities | 0.7 |
| 😈 **Devil's Advocate** | Attacks every assumption, hidden risk, and weakness — specifically dismantles the steelman's points | 0.85 |
| 🔍 **Researcher** | Searches the live web for real statistics, failure rates, market data, and expert opinions | 0.3 |
| ⚖️ **Judge** | Weighs all three perspectives and delivers a structured verdict: Proceed / Proceed with Caution / Do Not Proceed | 0.2 |

---

## 🏗️ Project Structure

```
devils-advocate/
│
├── .env                    # API keys (never commit this)
├── .gitignore
├── requirements.txt
│
├── agents/                 # Each agent's brain
│   ├── __init__.py
│   ├── steelman.py         # Argues FOR your idea
│   ├── devil.py            # Argues AGAINST your idea
│   ├── researcher.py       # Live web search for real facts
│   └── judge.py            # Synthesizes everything into a verdict
│
├── graph/                  # LangGraph orchestration
│   ├── __init__.py
│   ├── state.py            # Shared DebateState TypedDict
│   └── debate_graph.py     # StateGraph wiring all agents together
│
├── app.py                  # Gradio UI (Hugging Face deployment)
└── main.py                 # Local test runner
```

---

## ⚙️ Tech Stack

| Technology | Purpose |
|------------|---------|
| [LangChain](https://python.langchain.com/) | Agent chains, prompt templates, LCEL |
| [LangGraph](https://langchain-ai.github.io/langgraph/) | Multi-agent orchestration, StateGraph |
| [Groq API](https://console.groq.com/) | Fast free LLM inference (LLaMA 3.3 70B) |
| [Tavily](https://tavily.com/) | Real-time web search for the Researcher agent |
| [Gradio](https://gradio.app/) | Streaming web UI |
| [Hugging Face Spaces](https://huggingface.co/spaces) | Free deployment |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- A free [Groq API key](https://console.groq.com/)
- A free [Tavily API key](https://app.tavily.com/)

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/devils-advocate.git
cd devils-advocate
```

### 2. Create a virtual environment

```bash
python -m venv venv

# Mac/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

### 5. Run locally

**Terminal (no UI):**
```bash
python main.py
```

**With Gradio UI:**
```bash
python app.py
```

Then open `http://127.0.0.1:7860` in your browser.

---

## 🌐 Deploy to Hugging Face Spaces

1. Create a new Space at [huggingface.co/new-space](https://huggingface.co/new-space)
   - SDK: **Gradio**
   - Visibility: **Public**

2. Add your API keys under **Settings → Variables and Secrets**:
   ```
   GROQ_API_KEY    → your Groq key
   TAVILY_API_KEY  → your Tavily key
   ```

3. Push your code:
   ```bash
   git remote add origin https://huggingface.co/spaces/YOUR_USERNAME/devils-advocate
   git push origin main
   ```

Your app will be live in ~2 minutes at:
`https://huggingface.co/spaces/YOUR_USERNAME/devils-advocate`

---

## 💡 Example Usage

**Input:**
> "I should quit my job and build an AI startup"

**Output:**

```
🛡️ STEELMAN
The AI market is growing at 37% annually — timing couldn't be better.
Domain expertise gives you an unfair advantage over generic founders...

😈 DEVIL'S ADVOCATE
90% of AI startups fail within 2 years. Market growth attracts
better-funded competitors daily. Personal runway is your real constraint...

🔍 RESEARCH
- CB Insights 2024: 73% of AI startups fail due to premature scaling
- YC data: founders with 6+ months runway have 3x survival rate...

⚖️ VERDICT
## VERDICT
Proceed with Caution

## CONFIDENCE SCORE
7/10 — Strong market timing but execution risk is high

## RECOMMENDED FIRST STEP
Validate your core idea with 5 paying customers this week
before making any irreversible decisions...
```

---

## 🧩 Key Concepts Demonstrated

- **Multi-agent orchestration** with LangGraph `StateGraph`
- **Shared state management** using Python `TypedDict`
- **Tool-calling agents** with live web search (ReAct pattern)
- **LCEL chains** — `prompt | llm` composition
- **Streaming output** to Gradio UI using `graph.stream()`
- **Sequential agent dependencies** — each agent builds on the previous
- **Temperature tuning** per agent role

---

## 📁 Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GROQ_API_KEY` | ✅ Yes | From [console.groq.com](https://console.groq.com/) |
| `TAVILY_API_KEY` | ✅ Yes | From [app.tavily.com](https://app.tavily.com/) |

---

## 🤝 Contributing

Contributions are welcome! Some ideas for extensions:

- Add a **memory layer** so the agent remembers past debates
- Add a **follow-up round** where steelman and devil rebut each other
- Add **more agent roles** — e.g. a Financial Analyst or Devil's Psychologist
- Support **voice input/output** via Whisper + TTS
- Add **debate history** so users can revisit past decisions

To contribute:
```bash
git checkout -b feature/your-feature-name
# make your changes
git commit -m "Add: your feature description"
git push origin feature/your-feature-name
# open a Pull Request
```

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgements

- [LangChain](https://python.langchain.com/) for the agent building blocks
- [LangGraph](https://langchain-ai.github.io/langgraph/) for multi-agent orchestration
- [Groq](https://groq.com/) for blazing-fast free LLM inference
- [Tavily](https://tavily.com/) for real-time search
- [Hugging Face](https://huggingface.co/) for free deployment infrastructure

---

<p align="center">Built with LangChain · LangGraph · Groq · Gradio</p>