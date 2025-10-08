from typing import List, Dict

def call_openai(model: str, api_key: str, system: str, messages: List[Dict]) -> str:
    from openai import OpenAI
    client = OpenAI(api_key=api_key) if api_key else OpenAI()
    resp = client.chat.completions.create(model=model, messages=[{"role":"system","content":system}] + messages)
    return resp.choices[0].message.content

def call_groq(model: str, api_key: str, system: str, messages: List[Dict]) -> str:
    from groq import Groq
    client = Groq(api_key=api_key)
    resp = client.chat.completions.create(model=model, messages=[{"role":"system","content":system}] + messages)
    return resp.choices[0].message.content

def call_gemini(model: str, api_key: str, system: str, messages: List[Dict]) -> str:
    import google.generativeai as genai
    genai.configure(api_key=api_key)
    m = genai.GenerativeModel(model_name=model, system_instruction=system)
    parts = []
    for msg in messages:
        parts.append(f"[{msg.get('role','user').upper()}] {msg.get('content','')}")
    resp = m.generate_content(parts)
    return resp.text

def call_provider(provider: str, model: str, api_key: str, system: str, messages: List[Dict]) -> str:
    if provider == "openai":
        return call_openai(model, api_key, system, messages)
    elif provider == "groq":
        return call_groq(model, api_key, system, messages)
    elif provider == "gemini":
        return call_gemini(model, api_key, system, messages)
    else:
        raise ValueError("Provider não suportado")
