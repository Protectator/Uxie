#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This file is part of Uxie.

Uxie - Pokemon Showdown's usage stats database builder
Copyright (C) 2016 Kewin Dousse (Protectator)

Licensed under the MIT License. See file LICENSE in the project root for license information.
"""
import re


def filter(file, filters):
    if (filters['year'] and (file.year not in filters['year'])):
        return False
    if (filters['month']and (file.month not in filters['month'])):
        return False
    if (filters['gxe'] and (file.elo not in filters['gxe'])):
        return False
    if (filters['format'] and (file.meta not in filters['format'])):
        return False
    if (filters['type']):
        type = typeoffolder(file.folders)
        return type in filters['type']
    return True

def filterFolder(folder, filters):
    matchs = re.search('^/?(\d+)-(\d+)', folder)
    year = int(matchs.groups()[0])
    month = int(matchs.groups()[1])
    if (filters['year'] and (year not in filters['year'])):
        return False
    if (filters['month']and (month not in filters['month'])):
        return False
    return True

def typeoffolder(folders):
    if folders is None:
        return "usage"
    elif "leads" in folders:
        return "leads"
    elif "metagame" in folders:
        return "metagame"
    elif "moveset" in folders:
        return "moveset"
    elif "chaos" in folders:
        return "chaos"
    return "usage"