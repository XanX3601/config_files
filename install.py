import click

from commands import neovim, create_utils_dirs


@click.group()
def cli():
    pass


if __name__ == "__main__":
    create_utils_dirs()
    cli.add_command(neovim)
    cli()
