import os
import pytest
import click
from typer.testing import CliRunner
from robot.cli import app, main

runner = CliRunner()

def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "activate" in result.stdout
    assert "deactivate" in result.stdout


def test_activate_invokes_pty(monkeypatch):
    called = []

    def fake_spawn(cmd, **kwargs):
        called.append(kwargs)
        return 0

    monkeypatch.setattr("pty.spawn", fake_spawn)
    result = runner.invoke(app, ["activate"])
    assert result.exit_code == 0
    assert called
    assert "master_read" in called[0]
    assert "stdin_read" in called[0]
    log_path = result.stdout.split("Session log: ")[1].strip()
    assert os.path.exists(log_path)


def test_query_reads_log(tmp_path, monkeypatch, capsys):
    log_file = tmp_path / "session.log"
    log_file.write_text("command output")
    monkeypatch.setenv("ROBOT_SESSION_LOG", str(log_file))
    called = {}

    def fake_ask(question, session_data, provider=None, model=None):
        called["question"] = question
        called["session"] = session_data
        return "answer"

    monkeypatch.setattr("robot.cli.llm.ask", fake_ask)

    main(["what", "is", "going", "on?"])
    out = capsys.readouterr().out
    assert "Query:" not in out
    assert called["question"] == "what is going on?"
    assert called["session"] == "command output"
    assert out.strip().endswith("answer")


def test_query_missing_api_key(tmp_path, monkeypatch, capsys):
    """The CLI should print a helpful message when llm.ask fails."""
    log_file = tmp_path / "session.log"
    log_file.write_text("cmd")
    monkeypatch.setenv("ROBOT_SESSION_LOG", str(log_file))

    def fail(question, session_data, provider=None, model=None):
        raise RuntimeError("OPENAI_API_KEY not set")

    monkeypatch.setattr("robot.cli.llm.ask", fail)

    with pytest.raises(click.exceptions.Exit) as exc:
        main(["why?"])
    assert exc.value.exit_code == 1
    out = capsys.readouterr().out
    assert "OPENAI_API_KEY not set" in out
    assert "Traceback" not in out
