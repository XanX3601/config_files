import click

from .utils.files import download_archive, extract_tarfile, move, remove
from .utils.make import configure, make, make_install
from .utils.print import print_msg_titled, print_stdoutputs
from .utils.resources import console, local_path, packages_path, temp_path

llvm_name = "llvm"
llvm_version = "11.0.0"
llvm_homepage = "https://llvm.org/"
llvm_archive_link = "https://github.com/llvm/llvm-project/releases/download/llvmorg-11.0.0/clang+llvm-11.0.0-x86_64-linux-gnu-ubuntu-20.04.tar.xz"
llvm_archive_top_directory_name = "clang+llvm-11.0.0-x86_64-linux-gnu-ubuntu-20.04"
llvm_archive_path = temp_path.joinpath("llvm.tar.xz")
llvm_install_path = local_path


@click.group()
def llvm():
    """llvm commands group."""
    pass


@llvm.command()
def info():
    """print info on llvm."""
    print_msg_titled(
        "{} - {}".format(llvm_name, llvm_version),
        "home page: {}".format(llvm_homepage),
    )


@llvm.command()
def install():
    """install llvm locally."""
    # download archive
    download_archive(llvm_archive_link, llvm_archive_path, llvm_name)

    # extract archive
    llvm_tmp_path = temp_path.joinpath(llvm_archive_top_directory_name)

    if llvm_tmp_path.exists():
        remove(llvm_tmp_path, "{}".format(llvm_tmp_path))

    extract_tarfile(llvm_archive_path, temp_path, llvm_name)

    # move temp directory to install path
    target = llvm_install_path
    source = llvm_tmp_path
    move(source, target, llvm_name, True)

    console.print("[bold green]{} has been installed with success[/]".format(llvm_name))
