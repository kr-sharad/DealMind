import streamlit as st
import os
import pandas as pd
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="DealMind",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

  html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; color: #1a1a2e; }

  [data-testid="stSidebar"] { background: #1a1a2e !important; border-right: 1px solid #2d2d4e; }
  [data-testid="stSidebar"] * { color: #e0e0f5 !important; }
  [data-testid="stSidebar"] .stMarkdown h1,
  [data-testid="stSidebar"] .stMarkdown h2,
  [data-testid="stSidebar"] .stMarkdown h3 { color: #ffffff !important; font-family: 'Syne', sans-serif; }

  .main .block-container { background: #ffffff; padding: 2rem 3rem; max-width: 960px; }

  .brand-header { display: flex; align-items: center; gap: 10px; padding: 1.2rem 1rem 0.5rem; margin-bottom: 0.5rem; }
  .brand-logo { width: 32px; height: 32px; background: linear-gradient(135deg, #6c63ff, #a78bfa); border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 18px; }
  .brand-name { font-family: 'Syne', sans-serif; font-weight: 800; font-size: 1.4rem; color: #ffffff !important; letter-spacing: -0.5px; }
  .brand-tag { font-size: 0.65rem; color: #6c63ff !important; font-weight: 600; letter-spacing: 1.5px; text-transform: uppercase; margin-left: 2px; }

  .prospect-card { background: rgba(108,99,255,0.08); border: 1px solid rgba(108,99,255,0.18); border-radius: 12px; padding: 14px 16px; margin: 8px 0; cursor: pointer; transition: all 0.2s ease; }
  .prospect-card:hover { background: rgba(108,99,255,0.18); border-color: rgba(108,99,255,0.45); transform: translateX(3px); }
  .prospect-card.selected { background: rgba(108,99,255,0.22); border-color: #6c63ff; box-shadow: 0 0 0 1px rgba(108,99,255,0.3); }
  .prospect-name { font-family: 'Syne', sans-serif; font-weight: 700; font-size: 0.95rem; color: #ffffff !important; margin-bottom: 3px; }
  .prospect-meta { font-size: 0.78rem; color: #a0a0c0 !important; margin-bottom: 6px; }

  .badge { display: inline-block; padding: 2px 10px; border-radius: 20px; font-size: 0.68rem; font-weight: 600; letter-spacing: 0.5px; text-transform: uppercase; }
  .badge-negotiation { background: rgba(108,99,255,0.25); color: #a78bfa !important; border: 1px solid rgba(108,99,255,0.4); }
  .badge-proposal { background: rgba(59,195,170,0.18); color: #3bc3aa !important; border: 1px solid rgba(59,195,170,0.35); }
  .badge-discovery { background: rgba(251,191,36,0.18); color: #fbbf24 !important; border: 1px solid rgba(251,191,36,0.35); }

  .section-label { font-size: 0.62rem; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; color: #5a5a8a !important; padding: 0.8rem 1rem 0.3rem; margin-top: 0.5rem; }

  .profile-card { background: linear-gradient(135deg, #f8f7ff 0%, #f0eeff 100%); border: 1px solid #e0d9ff; border-radius: 16px; padding: 28px 32px; margin-bottom: 28px; position: relative; overflow: hidden; }
  .profile-card::before { content: ''; position: absolute; top: 0; left: 0; width: 4px; height: 100%; background: linear-gradient(180deg, #6c63ff, #a78bfa); border-radius: 4px 0 0 4px; }
  .profile-card-header { display: flex; align-items: flex-start; gap: 18px; }
  .avatar-circle { width: 56px; height: 56px; border-radius: 14px; background: linear-gradient(135deg, #6c63ff, #a78bfa); display: flex; align-items: center; justify-content: center; font-family: 'Syne', sans-serif; font-weight: 800; font-size: 1.3rem; color: white; flex-shrink: 0; box-shadow: 0 4px 12px rgba(108,99,255,0.35); }
  .profile-name { font-family: 'Syne', sans-serif; font-weight: 800; font-size: 1.5rem; color: #1a1a2e; margin: 0 0 2px 0; line-height: 1.2; }
  .profile-company { font-size: 0.88rem; color: #6c63ff; font-weight: 600; margin-bottom: 6px; }
  .profile-stats { display: flex; gap: 24px; margin-top: 20px; flex-wrap: wrap; }
  .stat-item { display: flex; flex-direction: column; gap: 3px; }
  .stat-label { font-size: 0.68rem; font-weight: 700; letter-spacing: 1.2px; text-transform: uppercase; color: #9090b0; }
  .stat-value { font-family: 'Syne', sans-serif; font-weight: 700; font-size: 1.05rem; color: #1a1a2e; }
  .stat-value.deal-size { color: #6c63ff; }

  .chat-section-title { font-family: 'Syne', sans-serif; font-weight: 700; font-size: 1.05rem; color: #1a1a2e; margin-bottom: 16px; display: flex; align-items: center; gap: 8px; }
  .chat-bubble-user { background: #6c63ff; color: white; border-radius: 16px 16px 4px 16px; padding: 12px 18px; margin: 8px 0 8px auto; max-width: 75%; font-size: 0.88rem; line-height: 1.5; box-shadow: 0 2px 8px rgba(108,99,255,0.3); }
  .chat-bubble-ai { background: #f5f4ff; color: #1a1a2e; border: 1px solid #e5e2ff; border-radius: 16px 16px 16px 4px; padding: 14px 18px; margin: 8px auto 8px 0; max-width: 80%; font-size: 0.88rem; line-height: 1.6; }
  .ai-label { font-size: 0.68rem; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; color: #6c63ff; margin-bottom: 6px; }
  .user-label { font-size: 0.68rem; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; color: rgba(255,255,255,0.65); margin-bottom: 6px; text-align: right; }
  .chat-message-wrap { display: flex; flex-direction: column; margin-bottom: 4px; }
  .chat-message-wrap.user { align-items: flex-end; }
  .chat-message-wrap.ai { align-items: flex-start; }

  .stTextInput > div > div > input { border: 1.5px solid #e0d9ff !important; border-radius: 12px !important; font-family: 'DM Sans', sans-serif !important; font-size: 0.9rem !important; padding: 12px 16px !important; background: #fafafe !important; color: #1a1a2e !important; transition: border-color 0.2s; }
  .stTextInput > div > div > input:focus { border-color: #6c63ff !important; box-shadow: 0 0 0 3px rgba(108,99,255,0.12) !important; }

  .stButton > button { background: linear-gradient(135deg, #6c63ff, #8b84ff) !important; color: white !important; border: none !important; border-radius: 12px !important; font-family: 'Syne', sans-serif !important; font-weight: 700 !important; font-size: 0.88rem !important; padding: 12px 24px !important; transition: all 0.2s ease !important; box-shadow: 0 3px 12px rgba(108,99,255,0.35) !important; letter-spacing: 0.3px !important; }
  .stButton > button:hover { transform: translateY(-1px) !important; box-shadow: 0 5px 18px rgba(108,99,255,0.45) !important; background: linear-gradient(135deg, #7d75ff, #9d97ff) !important; }
  .stButton > button:active { transform: translateY(0) !important; }

  .custom-divider { height: 1px; background: linear-gradient(90deg, transparent, #e0d9ff, transparent); margin: 24px 0; }

  .empty-state { text-align: center; padding: 80px 40px; color: #9090b0; }
  .empty-state-icon { font-size: 3.5rem; margin-bottom: 16px; opacity: 0.5; }
  .empty-state h2 { font-family: 'Syne', sans-serif; font-size: 1.3rem; color: #3a3a6e; margin-bottom: 8px; }
  .empty-state p { font-size: 0.88rem; max-width: 320px; margin: 0 auto; line-height: 1.6; }

  .stSpinner > div { border-top-color: #6c63ff !important; }

  /* ── Cost Dashboard ── */
  .dash-section-title {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 1.1rem;
    color: #1a1a2e;
    margin: 28px 0 14px;
    padding-bottom: 8px;
    border-bottom: 2px solid #eeebff;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .routing-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.84rem;
    margin-top: 4px;
  }
  .routing-table thead tr {
    background: #1a1a2e;
    color: #ffffff;
  }
  .routing-table thead th {
    padding: 10px 14px;
    text-align: left;
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 0.72rem;
    letter-spacing: 0.8px;
    text-transform: uppercase;
  }
  .routing-table thead th:first-child { border-radius: 8px 0 0 0; }
  .routing-table thead th:last-child  { border-radius: 0 8px 0 0; }
  .routing-table tbody tr { border-bottom: 1px solid #f0eeff; transition: background 0.15s; }
  .routing-table tbody tr:hover { background: #faf8ff; }
  .routing-table tbody td { padding: 10px 14px; color: #2a2a4e; vertical-align: middle; }
  .routing-table tbody td:first-child { color: #9090b0; font-size: 0.75rem; font-weight: 600; }
  .model-chip {
    display: inline-block;
    padding: 2px 9px;
    border-radius: 20px;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.3px;
  }
  .chip-fast   { background: rgba(59,195,170,0.15); color: #1a9e86; border: 1px solid rgba(59,195,170,0.35); }
  .chip-mid    { background: rgba(251,191,36,0.15);  color: #b8870a; border: 1px solid rgba(251,191,36,0.35); }
  .chip-heavy  { background: rgba(108,99,255,0.15);  color: #5046d4; border: 1px solid rgba(108,99,255,0.3); }
  .cost-cell   { font-family: 'Syne', sans-serif; font-weight: 700; color: #6c63ff; }
  .dash-note {
    margin-top: 32px;
    text-align: center;
    font-size: 0.75rem;
    color: #b0a8d8;
    letter-spacing: 0.8px;
  }
  .dash-note span { color: #6c63ff; font-weight: 700; }

  /* Streamlit metric tweaks */
  [data-testid="stMetric"] {
    background: linear-gradient(135deg, #f8f7ff, #f2f0ff);
    border: 1px solid #e5e0ff;
    border-radius: 14px;
    padding: 18px 20px !important;
  }
  [data-testid="stMetricLabel"] { font-size: 0.72rem !important; font-weight: 700 !important; letter-spacing: 1px !important; text-transform: uppercase !important; color: #8080a8 !important; }
  [data-testid="stMetricValue"] { font-family: 'Syne', sans-serif !important; font-weight: 800 !important; font-size: 1.7rem !important; color: #1a1a2e !important; }
  [data-testid="stMetricDelta"] svg { display: none; }

  /* Tabs */
  .stTabs [data-baseweb="tab-list"] { gap: 4px; background: #f5f3ff; padding: 6px; border-radius: 12px; border: 1px solid #e5e0ff; }
  .stTabs [data-baseweb="tab"] { border-radius: 9px; font-family: 'Syne', sans-serif; font-weight: 700; font-size: 0.85rem; color: #7070a0; padding: 8px 22px; }
  .stTabs [aria-selected="true"] { background: #6c63ff !important; color: white !important; }

  #MainMenu, footer, header { visibility: hidden; }
  .stDeployButton { display: none; }
</style>
""", unsafe_allow_html=True)

# ── Constants: model routing tiers ────────────────────────────────────────────
ROUTING_TIERS = [
    {
        "model":      "gemma2-9b-it",
        "label":      "gemma2-9b",
        "chip_class": "chip-fast",
        "max_words":  40,
        "cost":       0.0001,
        "reason":     "Short query — lightweight model",
    },
    {
        "model":      "llama-3.1-8b-instant",
        "label":      "llama-3.1-8b",
        "chip_class": "chip-mid",
        "max_words":  120,
        "cost":       0.0004,
        "reason":     "Medium query — balanced model",
    },
    {
        "model":      "llama-3.3-70b-versatile",
        "label":      "llama-3.3-70b",
        "chip_class": "chip-heavy",
        "max_words":  float("inf"),
        "cost":       0.002,
        "reason":     "Complex query — full-power model",
    },
]
BASELINE_COST = 0.008   # always-premium baseline for savings calc

def route_query(text: str) -> dict:
    """Pick the cheapest model tier that fits the query length."""
    wc = len(text.split())
    for tier in ROUTING_TIERS:
        if wc <= tier["max_words"]:
            return {**tier, "words": wc}
    return {**ROUTING_TIERS[-1], "words": wc}

# ── Prospect data ──────────────────────────────────────────────────────────────
PROSPECTS = [
    {"id": "sarah_chen",  "name": "Sarah Chen",  "initials": "SC", "company": "Nexus Dynamics Corp",    "title": "VP of Engineering",    "deal_size": "$200,000", "deal_type": "Enterprise",  "stage": "Negotiation", "badge_class": "badge-negotiation", "last_contact": "May 18, 2026", "next_step": "Legal review call",          "notes": "Interested in multi-year contract. Budget approved. Legal team flagged 3 clauses."},
    {"id": "mark_wilson", "name": "Mark Wilson", "initials": "MW", "company": "Bright Leaf Solutions",  "title": "Head of Operations",   "deal_size": "$45,000",  "deal_type": "SMB",         "stage": "Proposal",    "badge_class": "badge-proposal",    "last_contact": "May 15, 2026", "next_step": "Follow-up on pricing deck",  "notes": "Comparing with two competitors. Price-sensitive. Likes automation features."},
    {"id": "priya_patel", "name": "Priya Patel", "initials": "PP", "company": "OrionEdge Technologies", "title": "Chief Product Officer", "deal_size": "$85,000",  "deal_type": "Mid-market",  "stage": "Discovery",   "badge_class": "badge-discovery",   "last_contact": "May 20, 2026", "next_step": "Technical demo scheduled",   "notes": "Early stage. Strong product-market fit. Expanding team in Q3."},
]

# ── Session state ──────────────────────────────────────────────────────────────
if "selected_prospect_id" not in st.session_state:
    st.session_state.selected_prospect_id = None
if "chat_histories" not in st.session_state:
    st.session_state.chat_histories = {}
if "query_log" not in st.session_state:
    st.session_state.query_log = []   # list of dicts: {num, words, model, label, chip_class, reason, cost}

def get_prospect(pid):
    return next((p for p in PROSPECTS if p["id"] == pid), None)

# ── Groq API call ──────────────────────────────────────────────────────────────
def call_groq(messages: list, model: str) -> str:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return "⚠️ GROQ_API_KEY not found. Please add it to your .env file."
    try:
        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=1024,
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Error calling Groq API: {str(e)}"

def build_system_prompt(prospect: dict) -> str:
    return f"""You are DealMind, an elite AI sales intelligence assistant embedded in a CRM.
You are currently helping a sales rep manage a deal with the following prospect:

PROSPECT PROFILE
────────────────
Name: {prospect['name']}
Title: {prospect['title']}
Company: {prospect['company']}
Deal Type: {prospect['deal_type']}
Deal Size: {prospect['deal_size']}
Current Stage: {prospect['stage']}
Last Contact: {prospect['last_contact']}
Next Step: {prospect['next_step']}
Notes: {prospect['notes']}

YOUR ROLE
─────────
- Provide sharp, actionable sales intelligence and coaching
- Suggest talking points, objection handling, and closing strategies
- Help draft emails, identify risks, and recommend next steps
- Be concise, confident, and commercially sharp — no fluff
- Reference the prospect's specific context in every response
- Use bullet points sparingly; prefer tight, direct prose
- Format key recommendations with a ▸ prefix for clarity

Always respond as a senior sales strategist who knows this deal inside-out."""

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="brand-header">
      <div class="brand-logo">⚡</div>
      <div>
        <div class="brand-name">DealMind</div>
        <div class="brand-tag">Sales Intelligence</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-label">Active Prospects</div>', unsafe_allow_html=True)

    for p in PROSPECTS:
        selected   = st.session_state.selected_prospect_id == p["id"]
        card_class = "prospect-card selected" if selected else "prospect-card"
        st.markdown(f"""
        <div class="{card_class}">
          <div class="prospect-name">{p['name']}</div>
          <div class="prospect-meta">{p['company']} · {p['deal_size']}</div>
          <span class="badge {p['badge_class']}">{p['stage']}</span>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"Open {p['name']}", key=f"btn_{p['id']}", use_container_width=True):
            st.session_state.selected_prospect_id = p["id"]
            if p["id"] not in st.session_state.chat_histories:
                st.session_state.chat_histories[p["id"]] = []
            st.rerun()

    st.markdown("---")
    st.markdown("""
    <div style="padding: 0 0.5rem; font-size: 0.72rem; color: #5a5a8a; line-height: 1.7;">
      <strong style="color: #8080b0 !important;">Routing:</strong> CascadeFlow<br>
      <strong style="color: #8080b0 !important;">Provider:</strong> Groq<br>
      <strong style="color: #8080b0 !important;">Context:</strong> Deal-aware
    </div>
    """, unsafe_allow_html=True)

# ── Main area ──────────────────────────────────────────────────────────────────
prospect_id = st.session_state.selected_prospect_id

if prospect_id is None:
    st.markdown("""
    <div class="empty-state">
      <div class="empty-state-icon">⚡</div>
      <h2>Select a prospect to begin</h2>
      <p>Choose a deal from the sidebar to open their profile and start a conversation with your AI sales coach.</p>
    </div>
    """, unsafe_allow_html=True)

else:
    prospect = get_prospect(prospect_id)
    if prospect_id not in st.session_state.chat_histories:
        st.session_state.chat_histories[prospect_id] = []
    chat_history = st.session_state.chat_histories[prospect_id]

    # ── Tabs ─────────────────────────────────────────────────────────────────
    tab_coach, tab_dash = st.tabs(["💬 Deal Coach", "📊 Cost Dashboard"])

    # ════════════════════════════════════════════════════════════════════════
    # TAB 1 — Deal Coach
    # ════════════════════════════════════════════════════════════════════════
    with tab_coach:
        # Profile card
        st.markdown(f"""
        <div class="profile-card">
          <div class="profile-card-header">
            <div class="avatar-circle">{prospect['initials']}</div>
            <div>
              <div class="profile-name">{prospect['name']}</div>
              <div class="profile-company">🏢 {prospect['company']} · {prospect['title']}</div>
              <span class="badge {prospect['badge_class']}">{prospect['stage']}</span>
            </div>
          </div>
          <div class="profile-stats">
            <div class="stat-item">
              <span class="stat-label">Deal Size</span>
              <span class="stat-value deal-size">{prospect['deal_size']}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Type</span>
              <span class="stat-value">{prospect['deal_type']}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Last Contact</span>
              <span class="stat-value">{prospect['last_contact']}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Next Step</span>
              <span class="stat-value">{prospect['next_step']}</span>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f'<div class="chat-section-title">💬 AI Deal Coach — {prospect["name"]}</div>', unsafe_allow_html=True)

        if not chat_history:
            st.markdown(f"""
            <div class="chat-message-wrap ai">
              <div class="ai-label">⚡ DealMind</div>
              <div class="chat-bubble-ai">
                I'm locked in on the <strong>{prospect['deal_size']} {prospect['deal_type']}</strong> deal with <strong>{prospect['name']}</strong> at {prospect['company']}.<br><br>
                They're in the <strong>{prospect['stage']}</strong> stage — next step: <em>{prospect['next_step']}</em>.<br><br>
                What would you like to work on — objection handling, a follow-up email, competitive positioning, or closing strategy?
              </div>
            </div>
            """, unsafe_allow_html=True)

        for msg in chat_history:
            if msg["role"] == "user":
                st.markdown(f"""
                <div class="chat-message-wrap user">
                  <div class="user-label">You</div>
                  <div class="chat-bubble-user">{msg['content']}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-message-wrap ai">
                  <div class="ai-label">⚡ DealMind</div>
                  <div class="chat-bubble-ai">{msg['content']}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

        col1, col2 = st.columns([5, 1])
        with col1:
            user_input = st.text_input(
                label="Message",
                placeholder=f"Ask about the {prospect['name']} deal…",
                label_visibility="collapsed",
                key=f"input_{prospect_id}",
            )
        with col2:
            send_clicked = st.button("Send ▸", use_container_width=True)

        def handle_send(text: str):
            tier = route_query(text)
            chat_history.append({"role": "user", "content": text})
            system_prompt = build_system_prompt(prospect)
            api_messages  = [{"role": "system", "content": system_prompt}] + chat_history
            with st.spinner("DealMind is thinking…"):
                ai_response = call_groq(api_messages, tier["model"])
            chat_history.append({"role": "assistant", "content": ai_response})
            st.session_state.chat_histories[prospect_id] = chat_history
            # Log the routing decision
            st.session_state.query_log.append({
                "num":        len(st.session_state.query_log) + 1,
                "words":      tier["words"],
                "model":      tier["label"],
                "chip_class": tier["chip_class"],
                "reason":     tier["reason"],
                "cost":       tier["cost"],
            })
            st.rerun()

        if send_clicked and user_input.strip():
            handle_send(user_input.strip())

        st.markdown("**Quick prompts:**")
        qcol1, qcol2, qcol3 = st.columns(3)
        quick_prompts = {
            "📧 Draft follow-up email": f"Draft a concise follow-up email to {prospect['name']} after our last contact on {prospect['last_contact']}. Reference the {prospect['stage']} stage and next step.",
            "🛡️ Handle objections":     f"What are the most likely objections {prospect['name']} might raise right now, and how should I handle them?",
            "🏁 Closing strategy":      f"Give me a sharp closing strategy to advance this {prospect['deal_size']} deal from {prospect['stage']} to closed-won.",
        }
        for i, (label, prompt) in enumerate(quick_prompts.items()):
            with [qcol1, qcol2, qcol3][i]:
                if st.button(label, key=f"quick_{prospect_id}_{i}", use_container_width=True):
                    handle_send(prompt)

    # ════════════════════════════════════════════════════════════════════════
    # TAB 2 — Cost Dashboard
    # ════════════════════════════════════════════════════════════════════════
    with tab_dash:
        log = st.session_state.query_log
        total_queries = len(log)
        total_cost    = sum(r["cost"] for r in log)
        avg_cost      = total_cost / total_queries if total_queries else 0.0
        est_no_route  = total_queries * BASELINE_COST
        money_saved   = est_no_route - total_cost
        pct_saved     = (money_saved / est_no_route * 100) if est_no_route > 0 else 0.0

        # ── 4 metric boxes ───────────────────────────────────────────────
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.metric("Total Queries", total_queries)
        with m2:
            st.metric("Avg Cost / Query", f"${avg_cost:.4f}")
        with m3:
            st.metric("Est. Without Routing", f"${est_no_route:.4f}")
        with m4:
            st.metric(
                "Money Saved",
                f"${money_saved:.4f}",
                delta=f"{pct_saved:.1f}% saved" if total_queries else "—",
            )

        # ── Routing Decisions table ───────────────────────────────────────
        st.markdown('<div class="dash-section-title">🔀 Routing Decisions</div>', unsafe_allow_html=True)

        if not log:
            st.markdown("""
            <div style="text-align:center; padding: 40px; color: #b0a8d8; font-size: 0.9rem;">
              No queries yet — send a message in the Deal Coach tab to see routing decisions here.
            </div>
            """, unsafe_allow_html=True)
        else:
            rows_html = ""
            for r in log:
                rows_html += f"""
                <tr>
                  <td>#{r['num']}</td>
                  <td>{r['words']}</td>
                  <td><span class="model-chip {r['chip_class']}">{r['model']}</span></td>
                  <td>{r['reason']}</td>
                  <td class="cost-cell">${r['cost']:.4f}</td>
                </tr>"""

            st.markdown(f"""
            <table class="routing-table">
              <thead>
                <tr>
                  <th>Query #</th>
                  <th>Words</th>
                  <th>Model Used</th>
                  <th>Reason</th>
                  <th>Cost</th>
                </tr>
              </thead>
              <tbody>{rows_html}</tbody>
            </table>
            """, unsafe_allow_html=True)

            # ── Bar chart: queries per model ──────────────────────────────
            st.markdown('<div class="dash-section-title">📊 Queries by Model</div>', unsafe_allow_html=True)

            model_counts = {}
            for r in log:
                model_counts[r["model"]] = model_counts.get(r["model"], 0) + 1

            chart_df = pd.DataFrame(
                {"Queries": model_counts},
            )
            st.bar_chart(chart_df, color="#6c63ff")

        # ── Footer note ───────────────────────────────────────────────────
        st.markdown("""
        <div class="dash-note">
          Powered by <span>CascadeFlow model routing</span> — automatically selecting the right model for every query.
        </div>
        """, unsafe_allow_html=True)
