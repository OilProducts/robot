from typer.testing import CliRunner
from robot.cli import app

runner = CliRunner()

def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "activate" in result.stdout
