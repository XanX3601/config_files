import click
import subprocess


@click.group()
def install():
    pass


@install.command()
def nvim():
    args = [
        'git', 'clone', 'https://github.com/neovim/neovim.git', '$HOME/neovim'
    ]
    subprocess.run(args, shell=True, check=True).args


@install.command()
def vifm():
    click.echo('installing vifm')


if __name__ == '__main__':
    install()
