import click
import git
import pathlib
import subprocess


@click.group()
def install():
    pass


@install.command()
def nvim():
    home_directory = pathlib.Path.home()
    nvim_repo_path = home_directory.joinpath('neovim')

    if nvim_repo_path.exists():
        try:
            nvim_repo = git.Repo(nvim_repo_path)
        except:
            click.secho('{} already exists and can not be opened'.format(
                nvim_repo_path),
                        fg='red',
                        err=True)
    else:
        nvim_repo = git.Repo.clone_from('https://github.com/neovim/neovim.git',
                                        nvim_repo_path)

    nvim_repo_build_path = nvim_repo_path.joinpath('build')

    if not nvim_repo_build_path.exists():
        nvim_repo_build_path.mkdir()

    args = [
        'cmake', '-S',
        str(nvim_repo_path), '-B',
        str(nvim_repo_build_path)
    ]
    subprocess.run(args)


@install.command()
def vifm():
    click.echo('installing vifm')


if __name__ == '__main__':
    install()
