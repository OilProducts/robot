import os
import pty
import sys
import tempfile

import typer

from . import llm
from rich.console import Console

app = typer.Typer(add_completion=False)


def main(args: list[str] | None = None) -> None:
    """Entry point for the ``robot`` command."""
    args = sys.argv[1:] if args is None else args
    if args and args[0] not in {"activate", "deactivate"} and not args[0].startswith("-"):
        query_command(" ".join(args))
    else:
        app()


@app.command()
def activate() -> None:
    """Start a monitored shell session."""
    shell = os.environ.get("SHELL", "/bin/bash")
    with tempfile.NamedTemporaryFile(prefix="robot-", suffix=".log", delete=False) as log_file:
        typer.echo(f"Session log: {log_file.name}")
        os.environ["ROBOT_SESSION_LOG"] = log_file.name

        def master_read(fd: int) -> bytes:
            data = os.read(fd, 1024)
            if data:
                log_file.write(data)
                log_file.flush()
            return data

        def stdin_read(fd: int) -> bytes:
            data = os.read(fd, 1024)
            if data:
                log_file.write(data)
                log_file.flush()
            return data

        pty.spawn(shell, master_read=master_read, stdin_read=stdin_read)


@app.command()
def deactivate() -> None:
    """End the current robot session."""
    log_path = os.environ.pop("ROBOT_SESSION_LOG", None)
    if log_path:
        typer.echo(f"Session ended. Log: {log_path}")
    else:
        typer.echo("No active robot session found.")


def query_command(question: str) -> None:
    """Ask a question about the current session."""
    log_path = os.environ.get("ROBOT_SESSION_LOG")
    if not log_path or not os.path.exists(log_path):
        typer.echo("No active session log found.")
        raise typer.Exit(1)

    with open(log_path, "r") as f:
        session_data = f.read()

    console = Console()
    with console.status("", spinner="dots"):
        response = llm.ask(question, session_data)

    console.print(response)


if __name__ == "__main__":
    app()
