import typer

from momify.summarize import momify


app = typer.Typer()
app.command()(momify)


if __name__ == "__main__":
    app()