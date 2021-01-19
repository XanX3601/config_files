import click

from .utils.print import print_msg_titled, print_stdoutputs
from .utils.git import clone_repository, update_repository, NotAGitRepo
from .utils.resources import repositories_path, console
from .utils.make import cmake
from .utils.files import LocationExists

from .cmake import install as cmake_install

ninja_name = "ninja"
ninja_homepage = "https://ninja-build.org/"
ninja_repo_link = "git://github.com/ninja-build/ninja.git"
ninja_repo_path = repositories_path.joinpath("ninja")


@click.group()
def ninja():
    """ninja commands group."""
    pass


@ninja.command()
def info():
    """print info on ninja."""
    print_msg_titled("{}".format(ninja_name), "home page: {}".format(ninja_homepage))


@ninja.command()
@click.option("--with-dependencies", is_flag=True, help="Install with dependencies")
@click.pass_context
def install(ctx, with_dependencies):
    """install ninja locally."""
    # handle dependencies
    if with_dependencies:
        ctx.invoke(cmake_install)

    # clone repository
    try:
        clone_repository(ninja_repo_link, ninja_repo_path, ninja_name)
    except LocationExists as exception:
        pass

    # update repository
    try:
        update_repository(ninja_repo_path, ninja_name)
    except NotAGitRepo as exception:
        print_msg_titled(
            "[bold red]Error while updating {} repository[/]".format(ninja_name),
            str(exception),
        )

    # build ninja using cmake
    returncode, stdout, stderr = cmake(
        ninja_repo_path, ["-Bbuild-cmake", "-H."], ninja_name
    )
    if returncode != 0:
        print_stdoutputs(
            "[bold red]Error while building {}[/]".format(ninja_name), stdout, stderr
        )
        exit(1)

    returncode, stdout, stderr = cmake(
        ninja_repo_path, ["--build", "build-cmake"], ninja_name
    )
    if returncode != 0:
        print_stdoutputs(
            "[bold red]Error while building {}[/]".format(ninja_name), stdout, stderr
        )
        exit(1)

    console.print(
        "[bold green]{} has been installed with success[/]".format(ninja_name)
    )
