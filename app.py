# # app.py
# 
# import gradio as gr
# from graph.debate_graph import debate_graph
# 
# 
# # ── The core function Gradio will call ────────────────────────────────────────
# # Gradio works by connecting UI components to Python functions.
# # Whatever this function returns gets displayed in the UI.
# #
# # We use a GENERATOR function (yield instead of return) for streaming —
# # this lets us show each agent's output AS IT HAPPENS instead of waiting
# # for all 4 agents to finish before showing anything.
# # That's a much better user experience for something that takes 20-30 seconds.
# 
# def run_debate_streaming(idea: str):
# 
#     # Input validation — don't waste API calls on empty input
#     if not idea.strip():
#         yield "", "", "", "", "⚠️ Please enter an idea first!"
#         return
# 
#     # Show the user something is happening immediately
#     yield (
#         "🛡️ Steelman is building the best case...",
#         "",
#         "",
#         "",
#         ""
#     )
# 
#     try:
#         # .stream() is LangGraph's streaming method
#         # Instead of waiting for the full result, it yields state
#         # updates one node at a time as each agent finishes.
#         #
#         # Each chunk is a dict like:
#         #   {"steelman": {"steelman_arg": "..."}}  ← after steelman runs
#         #   {"devil": {"devil_arg": "..."}}         ← after devil runs
#         #   etc.
# 
#         steelman_out = ""
#         devil_out = ""
#         research_out = ""
#         verdict_out = ""
# 
#         for chunk in debate_graph.stream({
#             "idea": idea,
#             "steelman_arg": "",
#             "devil_arg": "",
#             "research": "",
#             "verdict": ""
#         }):
#             # chunk is a dict where key = node name that just finished
#             # We check which node finished and update the right output
# 
#             if "steelman" in chunk:
#                 steelman_out = chunk["steelman"]["steelman_arg"]
#                 yield (
#                     steelman_out,
#                     "😈 Devil's Advocate is attacking...",
#                     "",
#                     "",
#                     ""
#                 )
# 
#             elif "devil" in chunk:
#                 devil_out = chunk["devil"]["devil_arg"]
#                 yield (
#                     steelman_out,
#                     devil_out,
#                     "🔍 Researcher is searching the web...",
#                     "",
#                     ""
#                 )
# 
#             elif "researcher" in chunk:
#                 research_out = chunk["researcher"]["research"]
#                 yield (
#                     steelman_out,
#                     devil_out,
#                     research_out,
#                     "⚖️ Judge is deliberating...",
#                     ""
#                 )
# 
#             elif "judge" in chunk:
#                 verdict_out = str(chunk["judge"]["verdict"]).strip()
#                 yield (
#                     steelman_out,
#                     devil_out,
#                     research_out,
#                     verdict_out,
#                     "✅ Debate complete!"
#                 )
# 
#     except Exception as e:
#         yield "", "", "", "", f"❌ Error: {str(e)}"
# 
# 
# # ── Build the Gradio UI ───────────────────────────────────────────────────────
# # gr.Blocks() gives us full layout control — we can arrange components
# # exactly how we want using rows and columns.
# # Much more flexible than gr.Interface() which is just input → output.
# 
# with gr.Blocks(
#     title="Devil's Advocate — AI Decision Coach",
#     theme=gr.themes.Soft(),         # clean, modern look
#     css="""
#         .verdict-box textarea { 
#             font-size: 15px !important; 
#             line-height: 1.7 !important;
#         }
#         .title-text {
#             text-align: center;
#             margin-bottom: 8px;
#         }
#     """
# ) as demo:
# 
#     # ── Header ────────────────────────────────────────────────────────────
#     gr.Markdown("""
#     # 🎭 Devil's Advocate
#     ### AI-powered decision coach that stress-tests your ideas
#     
#     Enter any idea, plan, or decision. Four specialized AI agents will debate 
#     it from every angle and deliver a structured verdict to help you decide.
#     """, elem_classes=["title-text"])
# 
#     # ── Input Section ─────────────────────────────────────────────────────
#     with gr.Row():
#         with gr.Column(scale=4):
#             idea_input = gr.Textbox(
#                 placeholder="e.g. I should quit my job and build an AI startup...",
#                 label="💡 Your Idea or Decision",
#                 lines=3
#             )
#         with gr.Column(scale=1):
#             submit_btn = gr.Button(
#                 "⚔️ Start Debate",
#                 variant="primary",
#                 size="lg"
#             )
# 
#     # ── Example ideas to try ──────────────────────────────────────────────
#     gr.Examples(
#         examples=[
#             ["I should quit my job and build an AI startup"],
#             ["I should move to a new city for a job opportunity"],
#             ["I should invest my savings in index funds instead of real estate"],
#             ["I should learn web development to switch careers"],
#         ],
#         inputs=idea_input,
#         label="💡 Try these examples"
#     )
# 
#     # ── Status bar ────────────────────────────────────────────────────────
#     status = gr.Textbox(
#         label="Status",
#         interactive=False,
#         max_lines=1
#     )
# 
#     # ── Agent outputs — 2x2 grid ──────────────────────────────────────────
#     gr.Markdown("## 🤖 Agent Debate")
# 
#     with gr.Row():
#         with gr.Column():
#             steelman_out = gr.Textbox(
#                 label="🛡️ Steelman — Best case FOR your idea",
#                 lines=10,
#                 interactive=False
#             )
#         with gr.Column():
#             devil_out = gr.Textbox(
#                 label="😈 Devil's Advocate — Worst case AGAINST",
#                 lines=10,
#                 interactive=False
#             )
# 
#     with gr.Row():
#         with gr.Column():
#             research_out = gr.Textbox(
#                 label="🔍 Researcher — Real world facts",
#                 lines=10,
#                 interactive=False
#             )
#         with gr.Column():
#             verdict_out = gr.Textbox(
#                 label="⚖️ Judge — Final verdict",
#                 lines=10,
#                 interactive=False,
#                 elem_classes=["verdict-box"]
#             )
# 
#     # ── Wire the button to the function ───────────────────────────────────
#     # inputs  → list of components whose values get passed to the function
#     # outputs → list of components the function yields values into
#     # The order of outputs must match the order you yield values in the function
# 
#     submit_btn.click(
#         fn=run_debate_streaming,
#         inputs=[idea_input],
#         outputs=[steelman_out, devil_out, research_out, verdict_out, status]
#     )
# 
# # ── Launch ────────────────────────────────────────────────────────────────────
# if __name__ == "__main__":
#     demo.launch()
# 
# app.py
# 
# import gradio as gr
# from graph.debate_graph import debate_graph
# 
# def run_debate_streaming(idea: str):
#     if not idea.strip():
#         yield "", "", "", "", "⚠️ Please enter an idea first."
#         return
# 
#     yield (
#         "*Steelman is building the strongest case for your idea...*",
#         "",
#         "",
#         "",
#         "ANALYZING"
#     )
# 
#     try:
#         steelman_out = ""
#         devil_out = ""
#         research_out = ""
#         verdict_out = ""
# 
#         for chunk in debate_graph.stream({
#             "idea": idea,
#             "steelman_arg": "",
#             "devil_arg": "",
#             "research": "",
#             "verdict": ""
#         }):
#             if "steelman" in chunk:
#                 steelman_out = chunk["steelman"]["steelman_arg"]
#                 yield (
#                     steelman_out,
#                     "*Devil's Advocate is sharpening its attack...*",
#                     "",
#                     "",
#                     "DEBATING"
#                 )
#             elif "devil" in chunk:
#                 devil_out = chunk["devil"]["devil_arg"]
#                 yield (
#                     steelman_out,
#                     devil_out,
#                     "*Researcher is searching the web for real data...*",
#                     "",
#                     "RESEARCHING"
#                 )
#             elif "researcher" in chunk:
#                 research_out = chunk["researcher"]["research"]
#                 yield (
#                     steelman_out,
#                     devil_out,
#                     research_out,
#                     "*Judge is deliberating on the full debate...*",
#                     "DELIBERATING"
#                 )
#             elif "judge" in chunk:
#                 verdict_out = str(chunk["judge"]["verdict"]).strip()
#                 yield (
#                     steelman_out,
#                     devil_out,
#                     research_out,
#                     verdict_out,
#                     "COMPLETE"
#                 )
# 
#     except Exception as e:
#         yield "", "", "", "", f"ERROR: {str(e)}"
# 
# 
# ── Custom CSS — Dark Luxury Editorial ────────────────────────────────────────
# custom_css = """
# @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600&family=DM+Sans:wght@300;400;500&family=DM+Mono:wght@400&display=swap');
# 
# /* ── Reset & Base ── */
# *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
# 
# body, .gradio-container {
#     background: #0a0a0a !important;
#     font-family: 'DM Sans', sans-serif !important;
#     color: #e8e4dc !important;
#     min-height: 100vh;
# }
# 
# .gradio-container {
#     max-width: 1200px !important;
#     margin: 0 auto !important;
#     padding: 0 24px !important;
# }
# 
# /* ── Remove Gradio default chrome ── */
# .gr-panel, .gr-box, footer { display: none !important; }
# .gap, .contain { gap: 0 !important; }
# 
# /* ── Header ── */
# .header-wrap {
#     padding: 64px 0 48px;
#     border-bottom: 1px solid #1e1e1e;
#     margin-bottom: 48px;
#     position: relative;
# }
# 
# .header-wrap::before {
#     content: '';
#     position: absolute;
#     top: 0; left: -24px; right: -24px;
#     height: 1px;
#     background: linear-gradient(90deg, transparent, #c9a84c, transparent);
# }
# 
# .site-label {
#     font-family: 'DM Mono', monospace;
#     font-size: 10px;
#     letter-spacing: 0.3em;
#     color: #c9a84c;
#     text-transform: uppercase;
#     margin-bottom: 20px;
# }
# 
# .main-title {
#     font-family: 'Playfair Display', serif !important;
#     font-size: clamp(36px, 5vw, 64px) !important;
#     font-weight: 500 !important;
#     color: #f0ece4 !important;
#     line-height: 1.1 !important;
#     letter-spacing: -0.02em !important;
#     margin-bottom: 16px !important;
# }
# 
# .subtitle {
#     font-size: 15px !important;
#     color: #6b6760 !important;
#     font-weight: 300 !important;
#     max-width: 520px !important;
#     line-height: 1.6 !important;
# }
# 
# /* ── Input area ── */
# .input-section {
#     margin-bottom: 40px;
# }
# 
# .input-section label {
#     font-family: 'DM Mono', monospace !important;
#     font-size: 10px !important;
#     letter-spacing: 0.25em !important;
#     color: #4a4744 !important;
#     text-transform: uppercase !important;
#     margin-bottom: 10px !important;
#     display: block;
# }
# 
# .input-section textarea {
#     background: #111111 !important;
#     border: 1px solid #1e1e1e !important;
#     border-radius: 4px !important;
#     color: #e8e4dc !important;
#     font-family: 'DM Sans', sans-serif !important;
#     font-size: 16px !important;
#     font-weight: 300 !important;
#     padding: 20px 24px !important;
#     resize: none !important;
#     transition: border-color 0.2s ease !important;
#     line-height: 1.6 !important;
# }
# 
# .input-section textarea:focus {
#     border-color: #c9a84c !important;
#     outline: none !important;
#     box-shadow: 0 0 0 1px #c9a84c22 !important;
# }
# 
# .input-section textarea::placeholder {
#     color: #2e2c2a !important;
# }
# 
# /* ── Submit button ── */
# .submit-btn {
#     background: #c9a84c !important;
#     color: #0a0a0a !important;
#     border: none !important;
#     border-radius: 4px !important;
#     font-family: 'DM Mono', monospace !important;
#     font-size: 11px !important;
#     letter-spacing: 0.2em !important;
#     text-transform: uppercase !important;
#     font-weight: 400 !important;
#     padding: 14px 32px !important;
#     cursor: pointer !important;
#     transition: all 0.2s ease !important;
#     width: 100% !important;
#     margin-top: 12px !important;
# }
# 
# .submit-btn:hover {
#     background: #d4b660 !important;
#     transform: translateY(-1px) !important;
# }
# 
# .submit-btn:active {
#     transform: translateY(0) !important;
# }
# 
# /* ── Status pill ── */
# .status-wrap {
#     margin-bottom: 40px;
# }
# 
# .status-wrap label { display: none !important; }
# 
# .status-wrap textarea,
# .status-wrap input {
#     background: transparent !important;
#     border: none !important;
#     border-top: 1px solid #1a1a1a !important;
#     border-radius: 0 !important;
#     color: #c9a84c !important;
#     font-family: 'DM Mono', monospace !important;
#     font-size: 10px !important;
#     letter-spacing: 0.3em !important;
#     padding: 12px 0 !important;
#     text-transform: uppercase !important;
#     box-shadow: none !important;
# }
# 
# /* ── Section divider ── */
# .section-label {
#     font-family: 'DM Mono', monospace !important;
#     font-size: 10px !important;
#     letter-spacing: 0.3em !important;
#     color: #2e2c2a !important;
#     text-transform: uppercase !important;
#     margin-bottom: 24px !important;
#     padding-bottom: 12px !important;
#     border-bottom: 1px solid #161616 !important;
# }
# 
# /* ── Agent cards ── */
# .agent-card {
#     background: #0e0e0e !important;
#     border: 1px solid #191919 !important;
#     border-radius: 4px !important;
#     margin-bottom: 2px !important;
#     transition: border-color 0.3s ease !important;
# }
# 
# .agent-card:hover {
#     border-color: #242424 !important;
# }
# 
# .agent-card label {
#     font-family: 'DM Mono', monospace !important;
#     font-size: 10px !important;
#     letter-spacing: 0.2em !important;
#     color: #3a3835 !important;
#     text-transform: uppercase !important;
#     padding: 16px 20px 0 !important;
#     display: block !important;
# }
# 
# .agent-card textarea {
#     background: transparent !important;
#     border: none !important;
#     color: #c4bfb6 !important;
#     font-family: 'DM Sans', sans-serif !important;
#     font-size: 14px !important;
#     font-weight: 300 !important;
#     line-height: 1.8 !important;
#     padding: 12px 20px 20px !important;
#     resize: none !important;
#     box-shadow: none !important;
# }
# 
# /* ── Verdict card — special gold treatment ── */
# .verdict-card {
#     background: #0e0e0e !important;
#     border: 1px solid #c9a84c33 !important;
#     border-radius: 4px !important;
#     margin-bottom: 2px !important;
#     position: relative !important;
# }
# 
# .verdict-card::before {
#     content: '';
#     position: absolute;
#     top: 0; left: 0; right: 0;
#     height: 1px;
#     background: linear-gradient(90deg, transparent, #c9a84c66, transparent);
# }
# 
# .verdict-card label {
#     font-family: 'DM Mono', monospace !important;
#     font-size: 10px !important;
#     letter-spacing: 0.2em !important;
#     color: #c9a84c88 !important;
#     text-transform: uppercase !important;
#     padding: 16px 20px 0 !important;
#     display: block !important;
# }
# 
# .verdict-card textarea {
#     background: transparent !important;
#     border: none !important;
#     color: #d4cfc6 !important;
#     font-family: 'DM Sans', sans-serif !important;
#     font-size: 14px !important;
#     font-weight: 300 !important;
#     line-height: 1.9 !important;
#     padding: 12px 20px 20px !important;
#     resize: none !important;
#     box-shadow: none !important;
# }
# 
# /* ── Examples ── */
# .examples-wrap .label-wrap { display: none !important; }
# .examples-wrap table { 
#     background: transparent !important; 
#     border: none !important;
# }
# .examples-wrap td {
#     background: #111 !important;
#     border: 1px solid #1a1a1a !important;
#     border-radius: 3px !important;
#     color: #4a4744 !important;
#     font-family: 'DM Sans', sans-serif !important;
#     font-size: 13px !important;
#     padding: 8px 14px !important;
#     cursor: pointer !important;
#     transition: all 0.15s ease !important;
# }
# .examples-wrap td:hover {
#     border-color: #c9a84c44 !important;
#     color: #c9a84c !important;
# }
# 
# /* ── Grid layout ── */
# .agents-grid {
#     display: grid !important;
#     grid-template-columns: 1fr 1fr !important;
#     gap: 2px !important;
#     margin-bottom: 2px !important;
# }
# 
# /* ── Scrollbar ── */
# ::-webkit-scrollbar { width: 4px; }
# ::-webkit-scrollbar-track { background: #0a0a0a; }
# ::-webkit-scrollbar-thumb { background: #1e1e1e; border-radius: 2px; }
# ::-webkit-scrollbar-thumb:hover { background: #2a2a2a; }
# """
# 
# ── Build the UI ───────────────────────────────────────────────────────────────
# with gr.Blocks(
#     title="Devil's Advocate",
#     css=custom_css,
#     theme=gr.themes.Base(
#         primary_hue=gr.themes.colors.stone,
#         neutral_hue=gr.themes.colors.stone,
#         font=gr.themes.GoogleFont("DM Sans"),
#     )
# ) as demo:
# 
#     # ── Header ────────────────────────────────────────────────────────────
#     with gr.Column(elem_classes=["header-wrap"]):
#         gr.Markdown("DECISION INTELLIGENCE SYSTEM", elem_classes=["site-label"])
#         gr.Markdown("Devil's\nAdvocate", elem_classes=["main-title"])
#         gr.Markdown(
#             "Four specialized AI agents debate your idea from every angle — "
#             "steelman, critique, research, verdict.",
#             elem_classes=["subtitle"]
#         )
# 
#     # ── Input ─────────────────────────────────────────────────────────────
#     with gr.Column(elem_classes=["input-section"]):
#         idea_input = gr.Textbox(
#             placeholder="Describe your idea, plan, or decision...",
#             label="Your idea",
#             lines=3,
#             max_lines=6,
#         )
# 
#         gr.Examples(
#             examples=[
#                 ["I should quit my job and build an AI startup"],
#                 ["I should move to a new city for a better job opportunity"],
#                 ["I should invest my savings in index funds over real estate"],
#                 ["I should learn web development to switch careers"],
#             ],
#             inputs=idea_input
#             # elem_classes=["examples-wrap"]
#         )
# 
#         submit_btn = gr.Button(
#             "RUN DEBATE",
#             variant="primary",
#             elem_classes=["submit-btn"]
#         )
# 
#     # ── Status ────────────────────────────────────────────────────────────
#     with gr.Column(elem_classes=["status-wrap"]):
#         status = gr.Textbox(
#             value="STANDBY",
#             interactive=False,
#             max_lines=1,
#             show_label=False
#         )
# 
#     # ── Agent outputs ─────────────────────────────────────────────────────
#     gr.Markdown("THE DEBATE", elem_classes=["section-label"])
# 
#     with gr.Row(elem_classes=["agents-grid"]):
#         steelman_out = gr.Textbox(
#             label="01 — Steelman",
#             lines=12,
#             interactive=False,
#             elem_classes=["agent-card"]
#         )
#         devil_out = gr.Textbox(
#             label="02 — Devil's Advocate",
#             lines=12,
#             interactive=False,
#             elem_classes=["agent-card"]
#         )
# 
#     with gr.Row(elem_classes=["agents-grid"]):
#         research_out = gr.Textbox(
#             label="03 — Research",
#             lines=12,
#             interactive=False,
#             elem_classes=["agent-card"]
#         )
#         verdict_out = gr.Textbox(
#             label="04 — Verdict",
#             lines=12,
#             interactive=False,
#             elem_classes=["verdict-card"]
#         )
# 
#     # ── Wire up ───────────────────────────────────────────────────────────
#     submit_btn.click(
#         fn=run_debate_streaming,
#         inputs=[idea_input],
#         outputs=[steelman_out, devil_out, research_out, verdict_out, status]
#     )
# 
# if __name__ == "__main__":
#     demo.launch()


import gradio as gr
from graph.debate_graph import debate_graph

def run_debate_streaming(idea: str):
    if not idea.strip():
        yield "", "", "", "", "⚠️ Please enter an idea first."
        return

    yield (
        "Constructing the best possible case...",
        "",
        "",
        "",
        "ANALYZING"
    )

    try:
        steelman_out = ""
        devil_out = ""
        research_out = ""
        verdict_out = ""

        # LangGraph streaming
        for chunk in debate_graph.stream({
            "idea": idea,
            "steelman_arg": "",
            "devil_arg": "",
            "research": "",
            "verdict": ""
        }):
            if "steelman" in chunk:
                steelman_out = chunk["steelman"]["steelman_arg"]
                yield (
                    steelman_out,
                    "Preparing counter-arguments...",
                    "",
                    "",
                    "DEBATING"
                )
            elif "devil" in chunk:
                devil_out = chunk["devil"]["devil_arg"]
                yield (
                    steelman_out,
                    devil_out,
                    "Gathering real-world facts...",
                    "",
                    "RESEARCHING"
                )
            elif "researcher" in chunk:
                research_out = chunk["researcher"]["research"]
                yield (
                    steelman_out,
                    devil_out,
                    research_out,
                    "Weighing all sides...",
                    "DELIBERATING"
                )
            elif "judge" in chunk:
                verdict_out = str(chunk["judge"]["verdict"]).strip()
                yield (
                    steelman_out,
                    devil_out,
                    research_out,
                    verdict_out,
                    "COMPLETE"
                )

    except Exception as e:
        yield "", "", "", "", f"ERROR: {str(e)}"

custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600&display=swap');

:root {
    --bg-gradient: linear-gradient(135deg, #09090b 0%, #18181b 100%);
    --card-bg: rgba(24, 24, 27, 0.65);
    --card-border: rgba(255, 255, 255, 0.08);
    --glass-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.36);
    --accent-red: #f43f5e;
    --accent-blue: #3b82f6;
    --accent-green: #10b981;
    --accent-purple: #8b5cf6;
    --text-primary: #f8fafc;
    --text-secondary: #94a3b8;
}

body, .gradio-container {
    background: var(--bg-gradient) !important;
    background-attachment: fixed !important;
    font-family: 'Inter', sans-serif !important;
    color: var(--text-primary) !important;
    min-height: 100vh;
}

.gradio-container {
    max-width: 1400px !important;
    margin: 0 auto !important;
    padding: 40px 24px !important;
}

/* Hide default gradio stuff */
footer { display: none !important; }
.gr-panel, .gr-box { background: transparent !important; border: none !important; }
.gr-padded { padding: 0 !important; }

/* ── Typography & Header ── */
.app-header {
    text-align: center;
    margin-bottom: 3rem;
    animation: fadeInDown 0.8s ease-out;
}

.title-text {
    font-family: 'Outfit', sans-serif !important;
    font-size: clamp(5rem, 10vw, 8rem) !important;
    font-weight: 800 !important;
    color: #ffffff !important;
    margin-bottom: 0.5rem !important;
    letter-spacing: -0.02em !important;
    line-height: 1.1 !important;
}

.subtitle-text {
    font-family: 'Inter', sans-serif !important;
    font-size: 1.25rem !important;
    color: var(--text-secondary) !important;
    font-weight: 300 !important;
    max-width: 600px;
    margin: 0 auto !important;
}

/* ── Input Section ── */
.input-container {
    background: var(--card-bg) !important;
    backdrop-filter: blur(16px) !important;
    -webkit-backdrop-filter: blur(16px) !important;
    border: 1px solid var(--card-border) !important;
    border-radius: 24px !important;
    padding: 32px !important;
    box-shadow: var(--glass-shadow) !important;
    margin-bottom: 40px !important;
    animation: fadeInUp 0.8s ease-out 0.2s both;
}

.input-container textarea {
    background: rgba(0,0,0,0.2) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 16px !important;
    color: white !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 1.1rem !important;
    padding: 24px !important;
    transition: all 0.3s ease !important;
}

.input-container textarea:focus {
    border-color: var(--accent-purple) !important;
    box-shadow: 0 0 0 2px rgba(139, 92, 246, 0.2) !important;
    outline: none !important;
}

.submit-btn {
    background: linear-gradient(135deg, #f43f5e 0%, #8b5cf6 100%) !important;
    border: none !important;
    border-radius: 12px !important;
    color: white !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 600 !important;
    font-size: 1.1rem !important;
    padding: 16px 32px !important;
    margin-top: 16px !important;
    cursor: pointer !important;
    transition: transform 0.2s ease, box-shadow 0.2s ease !important;
    box-shadow: 0 4px 14px 0 rgba(244, 63, 94, 0.39) !important;
}

.submit-btn:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px 0 rgba(244, 63, 94, 0.5) !important;
}

/* ── Status Indicator ── */
.status-pill {
    background: rgba(0,0,0,0.3) !important;
    border-radius: 999px !important;
    padding: 8px 16px !important;
    border: 1px solid rgba(255,255,255,0.05) !important;
    text-align: center !important;
    margin: 0 auto 32px !important;
    max-width: 200px !important;
}

.status-pill input {
    background: transparent !important;
    border: none !important;
    color: var(--accent-blue) !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: 0.1em !important;
    text-align: center !important;
    font-size: 0.9rem !important;
    box-shadow: none !important;
}

/* ── Agent Cards Glassmorphism ── */
.agent-card {
    background: var(--card-bg) !important;
    backdrop-filter: blur(16px) !important;
    -webkit-backdrop-filter: blur(16px) !important;
    border: 1px solid var(--card-border) !important;
    border-radius: 24px !important;
    padding: 32px !important;
    transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease !important;
    position: relative !important;
    overflow: hidden !important;
    animation: fadeInUp 0.8s ease-out 0.4s both;
    margin-bottom: 0px !important;
}

/* Grids for better alignment */
.row-gap { gap: 24px !important; margin-bottom: 24px !important; }

.agent-card:hover {
    transform: translateY(-5px) !important;
    box-shadow: 0 12px 40px rgba(0,0,0,0.4) !important;
    border-color: rgba(255, 255, 255, 0.2) !important;
}

.agent-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 4px;
}

.card-steelman::before { background: linear-gradient(90deg, transparent, var(--accent-blue), transparent); }
.card-devil::before { background: linear-gradient(90deg, transparent, var(--accent-red), transparent); }
.card-research::before { background: linear-gradient(90deg, transparent, var(--accent-green), transparent); }
.card-verdict::before { background: linear-gradient(90deg, #f43f5e, #8b5cf6, #3b82f6); }

.card-verdict {
    border: 1px solid rgba(139, 92, 246, 0.3) !important;
    box-shadow: 0 4px 30px rgba(139, 92, 246, 0.1) !important;
}

.card-verdict label {
    font-size: 1.5rem !important;
    text-align: center !important;
    color: #f8fafc !important;
    background: transparent !important;
}

.card-verdict textarea {
    font-size: 1.15rem !important;
    color: #ffffff !important;
    opacity: 1 !important;
    visibility: visible !important;
}

.agent-card label {
    font-family: 'Outfit', sans-serif !important;
    font-size: 1.25rem !important;
    font-weight: 600 !important;
    color: white !important;
    margin-bottom: 16px !important;
    display: block !important;
    background: transparent !important;
    border: none !important;
}

.agent-card textarea {
    background: transparent !important;
    border: none !important;
    color: var(--text-secondary) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 1rem !important;
    line-height: 1.7 !important;
    padding: 0 !important;
    resize: none !important;
    box-shadow: none !important;
}

/* Custom Scrollbar for textareas */
.agent-card textarea::-webkit-scrollbar { width: 6px; }
.agent-card textarea::-webkit-scrollbar-track { background: transparent; }
.agent-card textarea::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 3px; }
.agent-card textarea::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.2); }

/* Suggestion Chips */
.examples-wrap { margin-top: 16px !important; }
.examples-wrap .label-wrap { display: none !important; }
.examples-wrap table { background: transparent !important; border: none !important; }
.examples-wrap td {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 99px !important;
    color: var(--text-secondary) !important;
    padding: 8px 16px !important;
    transition: all 0.2s ease !important;
    cursor: pointer !important;
    display: inline-block !important;
    margin: 4px !important;
}
.examples-wrap td:hover {
    background: rgba(255,255,255,0.1) !important;
    color: white !important;
    transform: scale(1.02) !important;
}

/* ── Animations ── */
@keyframes fadeInDown {
    from { opacity: 0; transform: translateY(-20px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}
"""

with gr.Blocks(
    title="Devil's Advocate"
) as demo:
    
    with gr.Column(elem_classes=["app-header"]):
        gr.Markdown("# Devil's Advocate", elem_classes=["title-text"])
        gr.Markdown("Stress-test your ideas with four specialized AI agents debating from every angle.", elem_classes=["subtitle-text"])

    with gr.Column(elem_classes=["input-container"]):
        idea_input = gr.Textbox(
            placeholder="Type your startup idea, life decision, or master plan here...",
            label="What's on your mind?",
            lines=3,
        )
        
        gr.Examples(
            examples=[
                ["I should quit my job and build an AI startup"],
                ["I should move to a new city for a better job opportunity"],
                ["I should invest my savings in index funds over real estate"],
            ],
            inputs=idea_input
        )

        submit_btn = gr.Button("IGNITE DEBATE", elem_classes=["submit-btn"])

    with gr.Column(elem_classes=["status-pill"]):
        status = gr.Textbox(
            value="READY",
            interactive=False,
            show_label=False
        )

    with gr.Row(elem_classes=["row-gap"]):
        steelman_out = gr.Textbox(
            label="🛡️ Steelman",
            lines=8,
            interactive=False,
            elem_classes=["agent-card", "card-steelman"]
        )
        devil_out = gr.Textbox(
            label="😈 Devil's Advocate",
            lines=8,
            interactive=False,
            elem_classes=["agent-card", "card-devil"]
        )

    with gr.Row(elem_classes=["row-gap"]):
        research_out = gr.Textbox(
            label="🔍 Researcher",
            lines=8,
            interactive=False,
            elem_classes=["agent-card", "card-research"]
        )

    with gr.Row(elem_classes=["row-gap"]):
        verdict_out = gr.Textbox(
            label="⚖️ Judge's Verdict",
            lines=10,
            interactive=False,
            elem_classes=["agent-card", "card-verdict"]
        )

    submit_btn.click(
        fn=run_debate_streaming,
        inputs=[idea_input],
        outputs=[steelman_out, devil_out, research_out, verdict_out, status]
    )

if __name__ == "__main__":
    demo.launch(css=custom_css, theme=gr.themes.Base())
