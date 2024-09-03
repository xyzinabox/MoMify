import typer
from typing_extensions import Annotated
from momify.loopback.record import record

def momify(
    name: Annotated[str, typer.Argument(help="The name of the process that you want recorded.")],
):
    path = record(name)
    print(path)
    
    #TO DO