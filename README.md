# ![Uxie](static/uxie_icon.png) Uxie [![Build Status](https://travis-ci.org/Protectator/Uxie.svg?branch=master)](https://travis-ci.org/Protectator/Uxie)

Uxie is a tool to build a database using Pokemon Showdown's usage stats.

## Installation

- Install [Python 2.7 or 3.5](https://www.python.org/)
- Install [pip](https://pip.pypa.io/en/stable/installing/)
- In the root directory of the project, run `pip install -r requirements.txt`

## Usage

Be sure you have an accessible instance of [MySQL](http://www.mysql.com/)

Run `uxie.py`.

    usage: uxie.py [-h] [-v] [-V] [-1] [-2] [-3] [-y YEAR [YEAR ...]]
                   [-m MONTH [MONTH ...]] [-f FORMAT [FORMAT ...]]
                   [-g GXE [GXE ...]]
                   [-t {usage,chaos,leads,metagame,moveset} [{usage,chaos,leads,metagame,moveset} ...]]
                   [-d DIRECTORY]
                   {mysql} host user password dbname
    
    Download all Pokemon Showdown's stats files, and fill a database with its stats.
    
    positional arguments:
      {mysql}               Database Management System
      host                  Database address
      user                  Database user
      password              User password
      dbname                Database name
    
    optional arguments:
      -h, --help            show this help message and exit
      -v, --verbose         be verbose
      -V, --version         show the version number and exit
      -1, --skip-download   do not download any file from the internet and only use available local files to build the database
      -2, --skip-parse      do not parse and do not store any file in a database, and only download files from the internet
      -3, --skip-index      do not create index the recommended columns in the final database
      -y YEAR [YEAR ...], --year YEAR [YEAR ...]
                            Filter : Only treat files in use these years
      -m MONTH [MONTH ...], --month MONTH [MONTH ...]
                            Filter : Only treat files in these months
      -f FORMAT [FORMAT ...], --format FORMAT [FORMAT ...]
                            Filter : Only treat files of these formats
      -g GXE [GXE ...], --gxe GXE [GXE ...]
                            Filter : Only treat files at exactly these gxe limits
      -t {usage,chaos,leads,metagame,moveset} [{usage,chaos,leads,metagame,moveset} ...], --type {usage,chaos,leads,metagame,moveset} [{usage,chaos,leads,metagame,moveset} ...]
                            Filter : Only treat files of these types
      -d DIRECTORY, --directory DIRECTORY
                            directory to use to download files into, and to parse from

## License

Uxie is distributed under the terms of the [MIT License](LICENSE).
