# IronGate Cortex AI Workforce Copilot — Executive Experience POC 

An offline, synthetic, presentation-oriented demonstration of **three distinct Snowflake Cortex AI value propositions** for healthcare staffing operations.

## Run on Windows in VS Code

Open the `irongate_amn_poc` folder (the folder containing `app.py` and `requirements.txt`) in VS Code, then in its terminal:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

If the `.venv` folder doesn't exist yet, create it using your installed Python 3.12 executable:

```powershell
& "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe" -m venv .venv
```

Alternatively, if your virtual environment is already activated: `python -m streamlit run app.py`.

## Demonstration flow

1. **Cortex Analyst:** ask business questions and show governed SQL *concept* and cited structured results.
2. **Cortex Search:** present a readable, evidence-grounded answer with source IDs and expandable fictional passages (offline rule-based RAG simulation).
3. **Cortex Agents:** show an executive-ready agent briefing with findings, priority, recommended actions, source evidence, and human approval gates.
4. **Production blueprint:** explain the architecture and what is required to connect to real Snowflake services.

## Scope and truthfulness

- **All data and documents are fictional.** None originate from AMN Healthcare.
- **No live Snowflake connection, Cortex Analyst, Cortex Search, Cortex Agents, LLM, or external API is used.**
- Analyst is deterministic pandas logic; Search is transparent keyword matching; Agent is scripted orchestration. They are *experience simulations*, not production-grade implementations.
- No candidate outreach, employment decisions, credentialing determinations, or writes occur.
- The app is a discussion starter for a potential read-only pilot using customer-approved data.
