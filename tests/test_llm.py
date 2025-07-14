import types
import sys
import robot.llm as llm


def test_long_session_truncated(monkeypatch):
    captured = {}

    class FakeMessage:
        def __init__(self, content):
            self.content = content

    class FakeChoice:
        def __init__(self, message):
            self.message = message

    class FakeChatCompletion:
        def create(self, *, model, messages):
            captured['model'] = model
            captured['messages'] = messages
            return types.SimpleNamespace(choices=[FakeChoice(FakeMessage("ok"))])

    monkeypatch.setenv("OPENAI_API_KEY", "x")
    fake_openai = types.SimpleNamespace(ChatCompletion=FakeChatCompletion())
    monkeypatch.setitem(sys.modules, 'openai', fake_openai)
    long_session = "a" * (llm.MAX_SESSION_CHARS + 10)
    llm.ask("q", long_session, provider="openai")
    sent = captured['messages'][1]['content']
    assert sent.startswith("Session:\n...")
    assert sent.endswith("\n\nQuestion:\nq")
    assert captured['model'] == "gpt-4.1-mini"
