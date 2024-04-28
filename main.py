import os.path
import re
from functools import cached_property
from pathlib import Path

import duckduckgo_search
import asyncio

from rich import print as rprint

import click
from rich.markup import escape
from rich.table import Table


@click.command()
@click.argument("file")
@click.option("--edition", "-e", help='Edition of the file')
@click.option("--search", "-s", "search_title",
              help='Basic title of film to search for, if missing will get from file name')
@click.option("--imdb-key", "-t", help='Filter search results to this key')
def cli(file, edition, search_title, imdb_key):
    if not file:
        rprint("No file specified")
        exit(1)
    path = Path(file)
    if not path.exists():
        rprint(f"[red]File [cyan]{file}[/] not found")
        exit(1)

    if not search_title:
        match = re.match(r"(.*)(?:_t\d+)?.mkv", path.name)

        if imdb_key:
            # ensure starts with tt
            if not imdb_key.startswith("t"):
                imdb_key = f"t{imdb_key}"
            if not imdb_key.startswith("tt"):
                imdb_key = f"t{imdb_key}"

        if not match:
            rprint("[red]Not an expected mkv name")
            exit(1)

        search_title = match[1]

    if search_title == "title":
        rprint("[red]The file name is not specific enough")
        rprint('[yellow]Specify a search title using [cyan]--search "<title>"[/] or [cyan]-s"<title>"[/]')
        exit(1)

    rprint(f"Searching for [cyan]{search_title}[/]")
    imdb_results = imdb_search(search_title)

    if imdb_key:
        imdb_results = [r for r in imdb_results if r.key.startswith(imdb_key)]

    if not imdb_results:
        rprint(f'[red]Could not find any IMDB search results for the film "[cyan]{search_title}[/]"')
        if search_title:
            rprint('[yellow]Try specifying a different search title')
        else:
            rprint('[yellow]Try specifying the search title using [cyan]--search "<title>"[/] or [cyan]-s"<title>"[/]')
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
            f"[cyan]-<key prefix>[/] for your chosen title. e.g. [cyan]-{imdb_results[0].key}[/]"
        )
        exit(1)

    imdb_result = imdb_results[0]

    imdb_title = imdb_result.title_and_year

    if not edition:
        for e in ["Extended", "Theatrical", "Director's Cut"]:
            if f"({e})" in path.name:
                if confirm(f'[yellow]Do you want to use the edition "[cyan]{e}[/]" detected in file name?',
                           default=True):
                    edition = e
                    break

    if edition:
        imdb_title = f"{imdb_title} {{edition-{edition}}}"
    imdb_title = imdb_title.replace(": ", " - ")
    imdb_title = imdb_title.replace("?", "")
    new_file_title = f"{imdb_title} {{imdb-{imdb_result.key}}}.mkv"
    new_file_path = os.path.join(path.parent, imdb_title, new_file_title)

    if confirm(
            f"[yellow]Do you want to rename:\n"
            f"  [cyan]{path.name}[/]\n"
            f"to:\n"
            f"  [cyan]{Path(new_file_path).relative_to(path.parent)}[/]"
            f"\n?", default=False):
        Path(new_file_path).parent.mkdir(parents=True, exist_ok=True)
        path.rename(new_file_path)
        rprint("[green]Renamed")


def confirm(message, default=False):
    rprint(message, end="")
    if default:
        hint = '[Y/n]'
    else:
        hint = '[y/N]'
    rprint(f"[reset] {escape(hint)}", end="")
    return click.prompt("", default='y' if default else 'n', show_default=False) in ['y', 'Y']


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

    @cached_property
    def title_and_year(self):
        return f"{self.title} ({self.year})"


async def ddg_imdb_search_async(search_term):
    return await duckduckgo_search.AsyncDDGS().text(search_term, max_results=10)


def ddg_imdb_search(title):
    return asyncio.run(ddg_imdb_search_async(title))


if __name__ == "__main__":
    cli()
