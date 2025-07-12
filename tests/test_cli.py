import os
from typer.testing import CliRunner
from robot.cli import app

runner = CliRunner()

def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "activate" in result.stdout


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
