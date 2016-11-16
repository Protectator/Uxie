# ![Uxie](static/uxie_icon.png) Uxie [![Build Status](https://travis-ci.org/Protectator/Uxie.svg?branch=master)](https://travis-ci.org/Protectator/Uxie)

**Uxie** is a tool to build a database using Pokemon Showdown's usage stats.

## Installation

- Install [Python 2.7 or 3.5](https://www.python.org/)
- Install [pip](https://pip.pypa.io/en/stable/installing/)
- In the root directory of the project, run `pip install -r requirements.txt`

## Usage

Be sure you have an accessible instance of [MySQL](http://www.mysql.com/)

Run `uxie.py` with your preferred python version while providing necessary arguments, for example :

### Simple example

Connects via `mysql` to `localhost` with user `uxie` and password `secretpw` to database `uxiedb` :

`python uxie.py mysql localhost uxie secretpw uxiedb`

### Parameters

#### Database connexion

These parameters are required, and must be in this order :
`dbms host user password dbname`

| Name | Values | Description |
| --- | --- | --- |
| dbms | `mysql` | DataBase Management System. Currently only supports `mysql` |
| host | Domain or IP | The machine on which to build the database |
| user | string | The username used to connect to the database |
| password | string | The password corresponding to the username |
| dbname | string | The name of the database to use |

#### Information

| Flag | Description |
| --- |  --- |
| `-h` or `--help`| Show the help and exits without doing anything else |
| `-V` or `--version` | Show the version number and exits without doing anything else |
| `-v` or `--verbose` | Describe actions done |

#### Behaviour

| Flag | Argument | Description |
| --- | --- | --- |
| `-1` or `--skip-download` | - | Skip the download phase |
| `-2` or `--skip-parse` | - | Skip the parse and feed the DB phase |
| `-3` or `--skip-index` | - | Skip the indexing DB phase |
| `-d` or `--directory` | `DIRECTORY` | Save and load files from `DIRECTORY`. Default directory used is `stats` |

#### Filters

| Flag | Argument(s) | Values | Description | Example |
| --- | --- | --- | --- | --- |
| `-y` | `YEAR [YEAR ...]` | `int` >= `2014` | Only treat files from the years listed by `YEAR` | `-y 2014 2015` |
| `-m` | `MONTH [MONTH ...]` | `int` between `1` and `12` | Only treat files from the months listed by `MONTH` | `-m 1 2 3 10 11 12` |
| `-f` | `FORMAT [FORMAT ...]` | `string` | Only treat files of the formats listed by `FORMAT` | `-f ou gen5ubers vgc2016` |
| `-g` | `GXE [GXE ...]` | `int` |Only treat files of the minimal GXE of the values listed by `GXE` | `-g 0 1630` |
| `-t` | `TYPE [TYPE ...]` | `` | Only treat files of the types listed by `TYPE` | `-t chaos moveset` |

## License

Uxie is distributed under the terms of the [MIT License](LICENSE).
