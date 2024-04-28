import os.path
import re
from pathlib import Path

import duckduckgo_search
import asyncio

from rich import print as rprint

import click


@click.command()
@click.argument("file")
@click.option("--edition", "-e", help='Edition of the file')
@click.option("--title", "-t", help='Basic title of film, if missing will get from file name')
def cli(file, edition, title):
    if not file:
        rprint("No file specified")
        exit(1)
    path = Path(file)
    if not path.exists():
        rprint(f"File [cyan]{file}[/] not found")
        exit(1)

    match = re.match(r"(.*)_t\d+.mkv", path.name)

    if not match:
        rprint("[red]Not an expected mkv name")
        exit(1)

    search_title = title or match[1]
    rprint(f"Searching for [cyan]{search_title}")
    imdb_results = imdb_search(search_title)

    if not imdb_results:
        rprint("[red]Could not find details of film")
        exit(1)

    if len(imdb_results) > 1:
        rprint("Multiple results")
        rprint(imdb_results)
        #exit(1)

    imdb_title, imdb_key, imdb_link, imdb_body = imdb_results[0]

    rprint(f"[green]Found [cyan]{imdb_title}[/], imdb reference [cyan]{imdb_key}[/]")
    rprint(imdb_link)
    rprint(f"[cyan]{imdb_body}[/]")

    if edition:
        imdb_title = f"{imdb_title} {{edition-{edition}}}"
    imdb_title = imdb_title.replace(": ", " - ")
    imdb_title = imdb_title.replace("?", "")
    new_file_title = f"{imdb_title} {{imdb-{imdb_key}}}.mkv"
    new_file_path = os.path.join(path.parent, imdb_title, new_file_title)

    Path(new_file_path).parent.mkdir(parents=True, exist_ok=True)
    rprint(new_file_title)
    rprint(new_file_path)

    path.rename(new_file_path)


def imdb_search(title):
    results = []

    for result in ddg_imdb_search(f"imdb: {title}"):
        imdb_link = re.match(r".*\Wimdb\.com/title/(tt\d+)", result['href'])
        imdb_title = re.match(r"(.*) - IMDb", result['title'])
        if imdb_link and imdb_title:
            imdb_key = imdb_link[1]
            imdb_title = imdb_title[1]
            results += [(imdb_title, imdb_key, imdb_link[0], result['body'])]

    return results


async def ddg_imdb_search_async(search_term):
    return await duckduckgo_search.AsyncDDGS().text(search_term, max_results=10)


def ddg_imdb_search(title):
    return asyncio.run(ddg_imdb_search_async(title))


if __name__ == "__main__":
    cli()
