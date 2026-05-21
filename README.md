# DealMind 🤝
### AI-Powered Sales Deal Intelligence Platform

DealMind gives sales reps an AI assistant that remembers every prospect interaction and gets smarter with every conversation — turning scattered call notes into personalized, deal-closing intelligence.

## The Problem
Sales reps lose deals because they forget. Prospects re-explain context. Follow-ups are generic. Institutional knowledge leaves when reps leave.

## The Solution
DealMind uses persistent AI memory to build a comprehensive understanding of every prospect over time — and routes AI queries intelligently to minimize cost without sacrificing quality.

## Key Features
- 🧠 **Persistent Memory**: Powered by Hindsight — AI remembers every call, concern, and commitment across sessions
- 🔀 **Smart Model Routing**: Powered by CascadeFlow — routes queries to the optimal model, reducing AI costs by 75%
- 📊 **Cost Dashboard**: Real-time visibility into AI usage, routing decisions, and savings
- 🎯 **Deal Intelligence**: Context-aware responses that reference specific past interactions

## Tech Stack
- **Frontend**: Streamlit
- **Memory**: Hindsight (Vectorize)
- **Model Routing**: CascadeFlow
- **AI Models**: Groq (llama-3.3-70b, llama-3.1-405b)
- **Language**: Python

## Live Demo
🔗 [Try DealMind Live](https://your-app-url.streamlit.app)

## Getting Started
```bash
git clone https://github.com/yourusername/dealmind
cd dealmind
pip install -r requirements.txt
# Add your API keys to .env
streamlit run app.py
```

## How It Works
1. Sales rep selects a prospect
2. Hindsight retrieves all past interaction memories
3. Rep asks a question or requests a follow-up draft
4. CascadeFlow routes to optimal AI model based on query complexity
5. AI responds with full context from memory
6. New insights are stored back in Hindsight for next session

## The Memory Effect
| Session | Without DealMind | With DealMind |
|---------|-----------------|---------------|
| Call 1 | "Thanks for your interest!" | Personalized to their context |
| Call 5 | Still generic | References specific objections from Call 2 |
| Call 10 | Rep forgets details | AI recalls everything precisely |

## Built With
- [Hindsight](https://hindsight.vectorize.io/) — Persistent AI memory system
- [CascadeFlow](https://docs.cascadeflow.ai/) — Runtime intelligence and model routing
- [Groq](https://groq.com/) — High-performance inference
