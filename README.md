# Uxie [![Build Status](https://travis-ci.org/Protectator/Uxie.svg?branch=master)](https://travis-ci.org/Protectator/Uxie)

Uxie is a tool to build a database using Pokemon Showdown's usage stats.

## Installation

- Install [Python 2.7](https://www.python.org/)
- Install [pip](https://pip.pypa.io/en/stable/installing/)
- In the root directory of the project, run `pip install -r requirements.txt`

## Usage

Be sure you have an accessible instance of [MySQL](http://www.mysql.com/)

Run `main.py`.

    usage: main.py [-h] [-p] [-F FOLDER] [-f FILE] [-v] {mysql} host user password dbname
    
    positional arguments:
      {mysql}               Database Management System
      host                  Database address
      user                  Database user
      password              User password
      dbname                Database name

    optional arguments:
      -h, --help            show this help message and exit
      -p, --only-parse, --skip-download
                            do not download any file from the internet and only
                            use available local files to build the database
      -F FOLDER, --folder FOLDER
                            folder to use to download files into, and to parse
                            from
      -f FILE, --file FILE  only process a single specific file
      -v, --verbose         be verbose


## License

Uxie is distributed under the terms of the [MIT License](LICENSE).
