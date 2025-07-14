from __future__ import annotations

import os


def ask(question: str, session_data: str, provider: str | None = None, model: str | None = None) -> str:
    """Send a question and session transcript to an LLM and return the answer."""
    provider = provider or os.environ.get("ROBOT_PROVIDER", "openai")
    if provider == "openai":
        return _ask_openai(question, session_data, model=model)
    if provider == "gemini":
        return _ask_gemini(question, session_data, model=model)
    raise ValueError(f"Unknown provider: {provider}")


def _ask_openai(question: str, session_data: str, model: str | None = None) -> str:
    import openai

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set")
    openai.api_key = api_key
    model = model or "gpt-3.5-turbo"
    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful terminal assistant. "
                "Use the following session transcript to answer the user's question."
            ),
        },
        {
            "role": "user",
            "content": f"Session:\n{session_data}\n\nQuestion:\n{question}",
        },
    ]
    response = openai.ChatCompletion.create(model=model, messages=messages)
    return response.choices[0].message.content.strip()


def _ask_gemini(question: str, session_data: str, model: str | None = None) -> str:
    import google.generativeai as genai

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY not set")
    genai.configure(api_key=api_key)
    model = model or "models/gemini-pro"
    llm = genai.GenerativeModel(model)
    chat = llm.start_chat(history=[])
    response = chat.send_message(f"Session:\n{session_data}\n\nQuestion:\n{question}")
    return response.text.strip()
