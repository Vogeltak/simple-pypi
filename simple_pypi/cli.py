from pathlib import Path

import click

from simple_pypi import core


@click.group()
@click.version_option()
def cli():
    "Create and manage Python package indexes conforming to the Simple Repository API (PEP 503)."


@cli.command()
@click.argument("repo")
@click.argument("packages", nargs=-1)
@click.option(
    "-r",
    "--requirements",
    type=click.Path(exists=True),
    help="Requirements.txt file"
)
def install(repo, requirements, packages):
    """
    Pull requirements from PyPI into the target repository
    
    The repository path can either be local or remote. When the path contains ':',
    it is considered a remote path, and Simple PyPI will push to it using rsync.
    """
    repo = Path(repo)
    repo.mkdir(mode=0o755, exist_ok=True)
    core.download_packages(repo, Path(requirements), packages)
    core.update_simple_repository(repo)

@cli.command()
@click.argument("repo")
def info(repo):
    "Show detailed information about a Python repository"
    repo = Path(repo)
    package_count = core.get_index_info(repo)

    if package_count:
        click.echo(f"{repo.name} lists {package_count} packages")
    else:
        click.secho(f"Couldn't find a repository at {repo.absolute()}", fg="red")
