# agente-eda-llm-memory

Course exercise from the I2A2 programme: a Streamlit app that loads a CSV, builds a compact description of it, and answers questions about it through one of three LLM providers, keeping what it has concluded so far in session memory.

Small on purpose. It exists to practise two things.

**Provider abstraction.** `llm.py` exposes a single `call_provider(provider, model, api_key, system, messages)` and keeps the OpenAI, Groq and Gemini differences behind it, including Gemini's separate `system_instruction` and flattened message parts. Swapping providers is a sidebar selection, not a code change.

**Context budget.** `eda.compact_overview` sends the model the schema, the row and column counts and a bounded sample rather than the dataframe, because the whole file does not fit and pretending otherwise produces answers that describe the sample. The local `insights` pass runs in pandas before the model is called at all.

`memory.AgentMemory` accumulates the dataset summary, the automatic insights and the recent Q&A, and renders them as the running conclusions of the session.

## Running it

```bash
uv sync
export GROQ_API_KEY=...   # or OPENAI_API_KEY / GEMINI_API_KEY
uv run streamlit run app.py
```

The key can also be pasted into the sidebar at runtime.

## Scope

Course scope, and it shows: insight generation reports the highest-variance numeric columns and little else, memory lives in the Streamlit session and disappears with it, and the optional "return pandas code" checkbox is an experiment, not a feature. Prompts, data and answers all go to a hosted provider.
