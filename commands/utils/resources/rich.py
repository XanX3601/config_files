from rich.progress import BarColumn, Progress

from .console import console


def default_transient_progress():
    return Progress(
        "[progress.dexcription]{task.description}",
        BarColumn(),
        console=console,
        transient=True,
    )
