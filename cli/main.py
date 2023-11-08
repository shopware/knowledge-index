from typing import List, Union
from rich import print
from rich.console import Console
from rich.markdown import Markdown
import typer
import os

# Disable tensorflow warn prompts
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

from web.ingest import ingest_url, ingest
from web.query import query, map_results
from .answering import text_gen

app = typer.Typer()


@app.command("ingest-url")
def cmd_ingest_url(url: str, collection: Union[str, None] = typer.Option(None)):
    ingest_url(url, collection)


@app.command("ingest")
def cmd_ingest_(collection: Union[str, None] = typer.Option(None)):
    ingest(collection)


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


@app.command("question")
def cmd_generate_text(plain: bool = typer.Option(False)):
    person_name = typer.prompt("What is your question?")
    answer = text_gen(person_name)
    # text = ''.join([par["text"] for par in paragraphs])
    if plain:
        print(text)
    else:
        print("")
        # print(Markdown(text))
        print(answer)


def main():
    app()
