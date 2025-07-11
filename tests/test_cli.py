from typer.testing import CliRunner
from robot.cli import app

runner = CliRunner()

def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "activate" in result.stdout


def test_activate_invokes_pty(monkeypatch):
    called = []

    def fake_spawn(cmd):
        called.append(cmd)
        return 0

    monkeypatch.setattr("pty.spawn", fake_spawn)
    result = runner.invoke(app, ["activate"])
    assert result.exit_code == 0
    assert called
