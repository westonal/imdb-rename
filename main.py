import os.path
import re
from pathlib import Path

import duckduckgo_search
import asyncio

from rich import print as rprint

import click
from rich.table import Table


@click.command()
@click.argument("file")
@click.option("--edition", "-e", help='Edition of the file')
@click.option("--title", "-t", help='Basic title of film to search for, if missing will get from file name')
@click.option("--rename", "-r", is_flag=True, help='Rename the file')
@click.option("--imdb-key", "-k", help='Filter search results to this key')
def cli(file, edition, title, rename, imdb_key):
    if not file:
        rprint("No file specified")
        exit(1)
    path = Path(file)
    if not path.exists():
        rprint(f"[red]File [cyan]{file}[/] not found")
        exit(1)

    match = re.match(r"(.*)_t\d+.mkv", path.name)

    if not match:
        rprint("[red]Not an expected mkv name")
        exit(1)

    search_title = title or match[1]
    rprint(f"Searching for [cyan]{search_title}")
    imdb_results = imdb_search(search_title)

    if imdb_key:
        imdb_results = [r for r in imdb_results if r.key.startswith(imdb_key)]

    if not imdb_results:
        rprint("[red]Could not find details of film")
        exit(1)

    multiple_results = len(imdb_results) > 1
    if multiple_results:
        table = Table(title="[red]Multiple IMDB Results")
    else:
        table = Table(title="[green]IMDB Result")
    table.add_column("IMDB Key")
    table.add_column("Title")
    table.add_column("Year")
    table.add_column("Overview")
    for r in imdb_results:
        table.add_row(f"[link={r.url}]{r.key}[/link]", r.title, r.year, r.overview)
        table.add_section()
    rprint(table)
    if multiple_results:
        rprint(
            "[yellow]Run again with [cyan]--imdb-key <key prefix>[/] or just "
            "[cyan]-k<key prefix>[/] for your chosen title"
        )
        exit(1)

    imdb_result = imdb_results[0]

    imdb_title = f"{imdb_result.title} ({imdb_result.year})"
    if edition:
        imdb_title = f"{imdb_title} {{edition-{edition}}}"
    imdb_title = imdb_title.replace(": ", " - ")
    imdb_title = imdb_title.replace("?", "")
    new_file_title = f"{imdb_title} {{imdb-{imdb_result.key}}}.mkv"
    new_file_path = os.path.join(path.parent, imdb_title, new_file_title)

    if rename:
        rprint(
            f"[yellow]Rename:\n"
            f"  [cyan]{path.name}[/]\n"
            f"to:\n"
            f"  [cyan]{Path(new_file_path).relative_to(path.parent)}[/]"
            f"\n? (y/N)",
            end="")
        if click.prompt("", default="n", show_default=False) == 'y':
            rprint("Rename")
            Path(new_file_path).parent.mkdir(parents=True, exist_ok=True)
            path.rename(new_file_path)


def imdb_search(title):
    results = []
    result_keys = set()

    for result in ddg_imdb_search(f"site:imdb.com {title}"):
        imdb_link = re.match(r".*\Wimdb\.com/title/(tt\d+)", result['href'])
        imdb_title = re.match(r"(.*) \((\d{4})\) - IMDb", result['title'])
        if imdb_link and imdb_title:
            key = imdb_link[1]
            title = imdb_title[1]
            if (key, title) in result_keys:
                continue
            result_keys.add((key, title))
            results.append(
                ImdbEntry(
                    key=key,
                    title=title,
                    year=imdb_title[2],
                    url=imdb_link[0],
                    overview=re.sub(rf"^{re.escape(title)}: ", "", result['body'])
                )
            )

    return results


class ImdbEntry:
    def __init__(self, key, title, year, url, overview):
        self.key = key
        self.title = title
        self.year = year
        self.url = url
        self.overview = overview


async def ddg_imdb_search_async(search_term):
    return await duckduckgo_search.AsyncDDGS().text(search_term, max_results=10)


def ddg_imdb_search(title):
    return asyncio.run(ddg_imdb_search_async(title))


if __name__ == "__main__":
    cli()
