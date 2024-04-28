import os.path
import re
from pathlib import Path

import serpapi
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
    imdb_title, imdb_key, imdb_link = imdb_search(search_title)
    if not imdb_key:
        rprint("[red]Could not find details of film")
        exit(1)

    rprint(f"[green]Found [cyan]{imdb_title}[/cyan], imdb reference [cyan]{imdb_key}[/cyan]")
    rprint(imdb_link)

    if edition:
        imdb_title = f"{imdb_title} {{edition-{edition}}}"
    imdb_title = imdb_title.replace(": ", " - ")
    imdb_title = imdb_title.replace("?", "")
    new_file_title = f"{imdb_title} {{imdb-{imdb_key}}}.mkv"
    new_file_path = os.path.join(path.parent, imdb_title, new_file_title)

    # Path(new_file_path).parent.mkdir(parents=True, exist_ok=True)
    rprint(new_file_title)
    rprint(new_file_path)


def imdb_search(name):
    # params = {
    #     "api_key": "8fa8cc8db2f79a57f0ff96afac7e9bc4251ee734447b67dbbec623975f570a99",
    #     "engine": "duckduckgo",
    #     "q": f"imdb: {name}",
    #     "kl": "us-en"
    # }
    #
    # search = serpapi.search(params)
    # search = {'organic_results': [{'link': 'https://www.imdb.com/title/tt1170358/',
    #                                'title': 'The Hobbit: The Desolation of Smaug (2013) - IMDb'}]}


    for result in search['organic_results']:
        rprint(result['link'])
        rprint(result['title'])
        imdb_link = re.match(r".*\Wimdb\.com/title/(tt\d+)", result['link'])
        imdb_title = re.match(r"(.*) - IMDb", result['title'])
        if imdb_link and imdb_title:
            imdb_key = imdb_link[1]
            imdb_title = imdb_title[1]
            return imdb_title, imdb_key, imdb_link[0]

    return None, None


import asyncio

from duckduckgo_search import AsyncDDGS

async def aget_results(word):
    results = await AsyncDDGS().text(word, max_results=1)
    return results

async def main():
    words = ["imdb: The Hobbit- The Desolation of Smaug (Extended)"]
    tasks = [aget_results(w) for w in words]
    results = await asyncio.gather(*tasks)
    return results

if __name__ == "__main__":
    results = asyncio.run(main())
    print(results)
