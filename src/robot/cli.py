import os
import pty
import tempfile
import typer

app = typer.Typer(add_completion=False)

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

@app.command(name="query")
def query_command(question: str) -> None:
    """Ask a question about the current session."""
    typer.echo(f"Query: {question} (not yet implemented).")

if __name__ == "__main__":
    app()
