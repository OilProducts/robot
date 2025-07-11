import typer

app = typer.Typer(add_completion=False)

@app.command()
def activate() -> None:
    """Start a monitored shell session (placeholder)."""
    typer.echo("Activating robot session (not yet implemented).")

@app.command(name="query")
def query_command(question: str) -> None:
    """Ask a question about the current session."""
    typer.echo(f"Query: {question} (not yet implemented).")

if __name__ == "__main__":
    app()
