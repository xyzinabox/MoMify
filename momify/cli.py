import typer

from momify.momify import momify #momify


app = typer.Typer()
app.command()(momify)


if __name__ == "__main__":
    app()