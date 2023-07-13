import logging

import click

from automation.utils import StrEnum

logger = logging.getLogger(__name__)


class Pipeline(StrEnum):
    """Pipelines available from the CLI"""
    transcript = "transcript"


@click.group()
def cli():
    ...


@cli.command(Pipeline.transcript)
def transcript():
    from automation.transcript import main as run_pipeline

    logger.info("Running transcript pipeline...")
    run_pipeline()


if __name__ == "__main__":
    cli()
