from .console import console
from rich.progress import Progress, BarColumn

def default_transient_progress():
    return Progress(
        "[progress.dexcription]{task.description}",
        BarColumn(),
        console=console,
        transient=True,
    )
