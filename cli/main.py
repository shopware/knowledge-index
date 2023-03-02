from typing import List, Union
from rich import print
from rich.console import Console
import typer
import os

# Disable tensorflow warn prompts
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

from web.ingest import ingest_url
from web.query import query, map_results

app = typer.Typer()


@app.command("ingest-url")
def cmd_ingest_url(url: str, collection: Union[str, None]):
    ingest_url(url, collection)


@app.command("query")
def cmd_query(search: str, collections: List[str] = typer.Option([])):
    console = Console()
    results = []
    with console.status("[bold green]Searching...", spinner="noise"):
        if len(collections) > 0:
            for collection in collections:
                results += map_results(query(search, collection))
        else:
            results = map_results(query(search, None))

    results.sort(key=lambda result: float(result["score"]))
    print(results)


def main():
    app()
