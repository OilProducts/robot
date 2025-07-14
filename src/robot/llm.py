from __future__ import annotations

import os

MAX_SESSION_CHARS = 8000


def _build_messages(question: str, session_data: str) -> list[dict[str, str]]:
    """Prepare messages for the chat completion API.

    If the session data is very long, only the last portion is kept to stay
    within typical context window limits. See the OpenAI documentation for
    token limits on chat completions and the Google AI docs for Gemini models.
    """

    if len(session_data) > MAX_SESSION_CHARS:
        session_data = "..." + session_data[-MAX_SESSION_CHARS:]

    return [
        {
            "role": "system",
            "content": (
                "You are a helpful terminal assistant. Use the provided "
                "session transcript to answer the user's question."
            ),
        },
        {
            "role": "user",
            "content": f"Session:\n{session_data}\n\nQuestion:\n{question}",
        },
    ]


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
    model = model or "gpt-4.1-mini"
    messages = _build_messages(question, session_data)
    response = openai.ChatCompletion.create(model=model, messages=messages)
    return response.choices[0].message.content.strip()


def _ask_gemini(question: str, session_data: str, model: str | None = None) -> str:
    import google.generativeai as genai

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY not set")
    genai.configure(api_key=api_key)
    model = model or "models/gemini-2.5-flash"
    llm = genai.GenerativeModel(model)
    chat = llm.start_chat(history=[])
    messages = _build_messages(question, session_data)
    # Gemini expects a single string input rather than role-based messages.
    text = "\n\n".join(m["content"] for m in messages)
    response = chat.send_message(text)
    return response.text.strip()
