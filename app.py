import os, json, re, streamlit as st, pandas as pd, numpy as np
from agente_eda.loader import load_csv
from agente_eda.eda import compact_overview
from agente_eda.insights import generate_insights
from agente_eda.llm import call_provider
from agente_eda.memory import AgentMemory

st.set_page_config(page_title="Agente EDA (LLM + Memória)", layout="wide")
if "memory" not in st.session_state: st.session_state.memory = AgentMemory()

st.title("Agente EDA (LLM + Memória)")
st.caption("Envie um CSV, escolha o provedor (OpenAI/Groq/Gemini) e faça perguntas. O agente guarda memória e expõe conclusões.")

# Provider/model/api key
st.sidebar.header("LLM")
provider = st.sidebar.selectbox("Provedor", ["openai","groq","gemini"])
defaults = {"openai":"gpt-4o-mini", "groq":"llama-3.3-70b-versatile", "gemini":"gemini-1.5-flash"}
model = st.sidebar.text_input("Modelo", value=defaults[provider])
env_map = {"openai":"OPENAI_API_KEY","groq":"GROQ_API_KEY","gemini":"GEMINI_API_KEY"}
env_key = env_map[provider]
api_key_input = st.sidebar.text_input(f"{env_key} (opcional, senão usa env)", type="password")
api_key = api_key_input or os.getenv(env_key, "")
if not api_key:
    st.sidebar.warning(f"Defina {env_key} ou preencha o campo acima.")

# CSV upload
uploaded = st.file_uploader("CSV", type=["csv"])
if not uploaded:
    st.info("Envie um CSV para começar.")
    st.stop()

df = load_csv(uploaded)
st.success(f"CSV carregado: {len(df):,} linhas x {len(df.columns):,} colunas")
st.dataframe(df.head(), use_container_width=True)

# Context + memory
with st.expander("Contexto compacto enviado à LLM"):
    rows = st.slider("Amostra de linhas", 3, 50, 10)
    ctx = compact_overview(df, sample_rows=rows)
    st.json(ctx)
    st.session_state.memory.store_dataset_summary(ctx)

with st.expander("Insights automáticos (locais)"):
    ins = generate_insights(df)
    st.write(ins)
    if ins: st.session_state.memory.add_insight(ins)

# Ask
st.header("Perguntar à LLM")
q = st.text_input("Sua pergunta")
allow_code = st.checkbox("Permitir retorno de código pandas (experimental)", value=False)
if st.button("Perguntar") and q:
    if not api_key:
        st.error("Informe a API key.")
    else:
        SYSTEM = "Você é um analista de dados. Responda SOMENTE com base no contexto do dataset; se faltar algo, diga o que falta. Responda em português."
        payload = {"question": q, "context": ctx, "memory_hint": {"recent_qas": st.session_state.memory.qa_history[-3:]}, "mode": "code" if allow_code else "text"}
        try:
            ans = call_provider(provider, model, api_key, SYSTEM, [{"role":"user","content": json.dumps(payload)[:120000]}])
            if allow_code and "```" in ans:
                m = re.search(r"```python(.*?)```", ans, re.S)
                if m:
                    code = m.group(1)
                    st.code(code, language="python")
                    ns = {"df": df, "pd": pd, "np": np}
                    try:
                        exec(code, ns, ns)
                        st.success("Código executado.")
                    except Exception as ex:
                        st.error(f"Falha ao executar o código: {ex}")
                else:
                    st.write(ans)
            else:
                st.write(ans)
            st.session_state.memory.add_qa(q, ans)
        except Exception as e:
            st.error(f"Erro ao consultar a LLM: {e}")

# Conclusions
st.header("Conclusões do agente (memória)")
if st.button("Mostrar conclusões"):
    st.markdown(st.session_state.memory.conclusions_text())
