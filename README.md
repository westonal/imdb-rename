# IMDB rename

This script uses [DuckDuckGo](https://duckduckgo.com/) to search IMDB for the correct title, year and imdb key for a movie.

It then suggests a [Plex suitable file name](https://support.plex.tv/articles/naming-and-organizing-your-movie-media-files/).

## Setup

This uses Poetry for Python virtual environment management, please refer to [Installation docs](https://python-poetry.org/docs/). 

## Running

Pass the script the path of the file output from MakeMKV:

```shell
poetry run python imdb_rename.py "E:\TempRip\Back to the Future Part II-SEG_MainFeature_t00.mkv"
```

It will take the file name and do a search on IMDB via DuckDuckGo.

If it finds a single result it will suggest a renaming:

```
Do you want to rename:
  The Hobbit- The Battle of the Five Armies_t00.mkv
to:
  The Hobbit - The Battle of the Five Armies (2014)\The Hobbit - The Battle of the Five Armies (2014)
{imdb-tt2310332}.mkv
? [y/N]:
```

If it finds multiple then it lets you rerun specifying the IMDB key:

```
Searching for Oceans 11
                                              Multiple IMDB Results
┏━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ IMDB Key  ┃ Title          ┃ Year ┃ Overview                                                                  ┃
┡━━━━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ tt0240772 │ Ocean's Eleven │ 2001 │ Directed by Steven Soderbergh. With George Clooney, Cecelia Ann Birt,     │
│           │                │      │ Paul L. Nolan, Carol Florence. Danny Ocean and his ten accomplices plan   │
│           │                │      │ to rob three Las Vegas casinos simultaneously.                            │
├───────────┼────────────────┼──────┼───────────────────────────────────────────────────────────────────────────┤
│ tt0054135 │ Ocean's Eleven │ 1960 │ Directed by Lewis Milestone. With Frank Sinatra, Dean Martin, Sammy Davis │
│           │                │      │ Jr., Peter Lawford. Danny Ocean gathers a group of his World War II       │
│           │                │      │ compatriots to pull off the ultimate Las Vegas heist. Together the eleven │
│           │                │      │ friends plan to rob five Las Vegas casinos in one night.                  │
└───────────┴────────────────┴──────┴───────────────────────────────────────────────────────────────────────────┘
Run again with --imdb-key <key prefix> or just -<key prefix> for your chosen title. e.g. -tt0240772
```

You can also supply a title to search for as alternative for the file name:

```shell
 poetry run python imdb_rename.py "E:\TempRip\Back to the Future Part II-SEG_MainFeature_t00.mkv" -s"The Terminata"
```

As it uses a search engine, it's resilient to bad spelling!

```
                                              Multiple IMDB Results
┏━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ IMDB Key  ┃ Title                      ┃ Year ┃ Overview                                                      ┃
┡━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ tt0088247 │ The Terminator             │ 1984 │ Directed by James Cameron. With Arnold Schwarzenegger,        │
│           │                            │      │ Michael Biehn, Linda Hamilton, Paul Winfield. A human soldier │
│           │                            │      │ is sent from 2029 to 1984 to stop an almost indestructible    │
│           │                            │      │ cyborg killing machine, sent from the same year, which has    │
│           │                            │      │ been programmed to execute a young woman whose unborn son is  │
│           │                            │      │ the key to humanity's future salvation.                       │
├───────────┼────────────────────────────┼──────┼───────────────────────────────────────────────────────────────┤
│ tt0362227 │ The Terminal               │ 2004 │ Directed by Steven Spielberg. With Tom Hanks, Catherine       │
│           │                            │      │ Zeta-Jones, Stanley Tucci, Chi McBride. An Eastern European   │
│           │                            │      │ tourist unexpectedly finds himself stranded in JFK airport,   │
│           │                            │      │ and must take up temporary residence there.                   │
├───────────┼────────────────────────────┼──────┼───────────────────────────────────────────────────────────────┤
│ tt0103064 │ Terminator 2: Judgment Day │ 1991 │ Directed by James Cameron. With Arnold Schwarzenegger, Linda  │
│           │                            │      │ Hamilton, Edward Furlong, Robert Patrick. A cyborg, identical │
│           │                            │      │ to the one who failed to kill Sarah Connor, must now protect  │
│           │                            │      │ her ten year old son John from an even more advanced and      │
│           │                            │      │ powerful cyborg.                                              │
└───────────┴────────────────────────────┴──────┴───────────────────────────────────────────────────────────────┘
Run again with --imdb-key <key prefix> or just -<key prefix> for your chosen title. e.g. -tt0088247
```

### Feeling lucky?

Pass the `-l` parameter to just take the first result:

```shell
poetry run python imdb_rename.py "E:\TempRip\Back to the Future Part II-SEG_MainFeature_t00.mkv" -l
```

```
Searching for Back to the Future Part II-SEG_MainFeature_t00
                                                   IMDB Result
┏━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ IMDB Key  ┃ Title                      ┃ Year ┃ Overview                                                      ┃
┡━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ tt0096874 │ Back to the Future Part II │ 1989 │ Directed by Robert Zemeckis. With Michael J. Fox, Christopher │
│           │                            │      │ Lloyd, Lea Thompson, Tom Wilson. After visiting 2015, Marty   │
│           │                            │      │ McFly must repeat his visit to 1955 to prevent disastrous     │
│           │                            │      │ changes to 1985...without interfering with his first trip.    │
└───────────┴────────────────────────────┴──────┴───────────────────────────────────────────────────────────────┘
Do you want to rename:
  Back to the Future Part II-SEG_MainFeature_t00.mkv
to:
  Back to the Future Part II (1989)\Back to the Future Part II (1989) {imdb-tt0096874}.mkv
? [y/N]:
```

### Editions

It can detect some common editions by name in the file name and you can also pass the edition using the `-e` option:

```shell
poetry run python imdb_rename.py "E:\TempRip\Back to the Future Part II-SEG_MainFeature_t00.mkv" -e"Extended" -l
```

```
Do you want to rename:
  Back to the Future Part II-SEG_MainFeature_t00.mkv
to:
  Back to the Future Part II (1989) {edition-Extended}\Back to the Future Part II (1989) {edition-Extended}
{imdb-tt0096874}.mkv
? [y/N]:
```
