#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This file is part of Uxie.

Uxie - Pokemon Showdown's usage stats database builder
Copyright (C) 2016 Kewin Dousse (Protectator)

Licensed under the MIT License. See file LICENSE in the project root for license information.
"""
import pymysql.cursors

from src.databases.database import *


class MySQL(DataBase):
    def __init__(self):
        DataBase.__init__(self)
        self.connection = None

    def connect(self):
        self.connection = pymysql.connect(host='localhost',
                                          user='uxie',
                                          password='uxie',
                                          db='uxie',
                                          charset='utf8mb4',
                                          cursorclass=pymysql.cursors.DictCursor)

    def initialize(self):
        with self.connection.cursor() as cursor:
            with open("src/databases/init_mysql.sql", mode='r') as inputFile:
                sql = inputFile.read()
            cursor.execute(sql)
        self.connection.commit()

    def fillUsage(self, usageFile):
        try:
            with self.connection.cursor() as cursor:
                # Insert general values into `usage` table
                data = (usageFile.year, usageFile.month, usageFile.meta, usageFile.elo,
                        usageFile.data['total_battles'], usageFile.data['avg_weight'])
                sql = "INSERT INTO `usage`" \
                      "(`year`, `month`, `format`, `elo`, `total_battles`, `avg_weight_per_team`)" \
                      " VALUES " \
                      "(%s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, data)

                # Insert each value into `usage_pokemons` table
                data = [
                    [usageFile.year, usageFile.month, usageFile.meta, usageFile.elo, line['name'],
                     line['usage_percent'], line['raw_number'], line['raw_percent'],
                     line['real_number'], line['real_percent']] for line in usageFile.data['usage']]
                sql = "INSERT INTO `usage_pokemons`" \
                      "(`year`, `month`, `format`, `elo`, `pokemon`," \
                      " `usage_percent`, `raw_usage`, `raw_percent`," \
                      " `real_usage`, `real_percent`)" \
                      " VALUES " \
                      "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.executemany(sql, data)

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            self.connection.commit()
        finally:
            self.connection.close()


    def fillLeads(self, leadsFile):
        try:
            with self.connection.cursor() as cursor:
                # Insert general values into `leads` table
                data = (leadsFile.year, leadsFile.month, leadsFile.meta, leadsFile.elo,
                        leadsFile.data['total_leads'])
                sql = "INSERT INTO `leads`" \
                      "(`year`, `month`, `format`, `elo`, `total_leads`)" \
                      " VALUES " \
                      "(%s, %s, %s, %s, %s)"
                cursor.execute(sql, data)

                # Insert each value into `leads_pokemons` table
                data = [
                    [leadsFile.year, leadsFile.month, leadsFile.meta, leadsFile.elo, line['name'],
                     line['usage_percent'], line['raw_number'], line['raw_percent']
                     ] for line in leadsFile.data['usage']]
                sql = "INSERT INTO `leads_pokemons`" \
                      "(`year`, `month`, `format`, `elo`, `pokemon`," \
                      " `usage_percent`, `raw_usage`, `raw_percent`)" \
                      " VALUES " \
                      "(%s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.executemany(sql, data)

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            self.connection.commit()
        finally:
            self.connection.close()


    def fillMetagame(self, metagameFile):
        try:
            with self.connection.cursor() as cursor:
                # Insert each value into `metagame_usages` table
                data = [
                    [metagameFile.year, metagameFile.month, metagameFile.meta, metagameFile.elo,
                     line['type'], line['percentage']
                     ] for line in metagameFile.data['teams']]
                sql = "INSERT INTO `metagame_usages`" \
                      "(`year`, `month`, `format`, `elo`, `metagame`, `percentage`)" \
                      " VALUES " \
                      "(%s, %s, %s, %s, %s, %s)"
                cursor.executemany(sql, data)

                # Insert each value into `metagame_graphs` table
                lowest = metagameFile.data['graph']['lowest']
                increment = metagameFile.data['graph']['increment']
                characterValue = metagameFile.data['graph']['characterValue']
                i = 0
                data = []
                for line in metagameFile.data['graph']['bars']:
                    data.append([metagameFile.year, metagameFile.month, metagameFile.meta, metagameFile.elo,
                                 lowest + i*increment, line * characterValue])
                    i += 1
                sql = "INSERT INTO `metagame_graphs`" \
                      "(`year`, `month`, `format`, `elo`, `key`, `value`)" \
                      " VALUES " \
                      "(%s, %s, %s, %s, %s, %s)"
                cursor.executemany(sql, data)

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            self.connection.commit()
        finally:
            self.connection.close()


    def fillMoveset(self, movesetFile):
        try:
            with self.connection.cursor() as cursor: # For each Pokemon
                for pokemon in movesetFile.data:
                    # Insert general values into `moveset` table
                    data = (movesetFile.year, movesetFile.month, movesetFile.meta, movesetFile.elo,
                            pokemon['name'], pokemon['raw_count'], pokemon['avg_weight'], pokemon['viability_ceiling'])
                    sql = "INSERT INTO `moveset`" \
                          "(`year`, `month`, `format`, `elo`, `pokemon`, `raw_count`, `avg_weight`, `viability_ceiling`)" \
                          " VALUES " \
                          "(%s, %s, %s, %s, %s, %s, %s, %s)"
                    cursor.execute(sql, data)

                    # Insert each value into `moveset_abilities` table
                    data = [
                        [movesetFile.year, movesetFile.month, movesetFile.meta, movesetFile.elo, pokemon['name'],
                         ability['name'], ability['percentage']
                         ] for ability in pokemon['abilities']]
                    sql = "INSERT INTO `moveset_abilities`" \
                          "(`year`, `month`, `format`, `elo`, `pokemon`, `ability`, `percentage`)" \
                          " VALUES " \
                          "(%s, %s, %s, %s, %s, %s, %s)"
                    cursor.executemany(sql, data)

                    # Insert each value into `moveset_items` table
                    data = [
                        [movesetFile.year, movesetFile.month, movesetFile.meta, movesetFile.elo, pokemon['name'],
                         item['name'], item['percentage']
                         ] for item in pokemon['items'] if item['name'] != "Other"]
                    sql = "INSERT INTO `moveset_items`" \
                          "(`year`, `month`, `format`, `elo`, `pokemon`, `item`, `percentage`)" \
                          " VALUES " \
                          "(%s, %s, %s, %s, %s, %s, %s)"
                    cursor.executemany(sql, data)

                    # Insert each value into `moveset_spreads` table
                    data = [
                        [movesetFile.year, movesetFile.month, movesetFile.meta, movesetFile.elo, pokemon['name'],
                         spread['nature'], spread['hp'], spread['atk'], spread['def'],
                         spread['spa'], spread['spd'], spread['spe'], spread['percentage']
                         ] for spread in pokemon['spreads'] if spread['nature'] != "Other"]
                    sql = "INSERT INTO `moveset_spreads`" \
                          "(`year`, `month`, `format`, `elo`, `pokemon`, `nature`, " \
                          "`hp`, `atk`, `def`, `spa`, `spd`, `spe`, `percentage`)" \
                          " VALUES " \
                          "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    cursor.executemany(sql, data)

                    # Insert each value into `moveset_moves` table
                    data = [
                        [movesetFile.year, movesetFile.month, movesetFile.meta, movesetFile.elo, pokemon['name'],
                         move['name'], move['percentage']
                         ] for move in pokemon['moves'] if move['name'] != "Other"]
                    sql = "INSERT INTO `moveset_moves`" \
                          "(`year`, `month`, `format`, `elo`, `pokemon`, `move`, `percentage`)" \
                          " VALUES " \
                          "(%s, %s, %s, %s, %s, %s, %s)"
                    cursor.executemany(sql, data)

                    # Insert each value into `moveset_teammates` table
                    data = [
                        [movesetFile.year, movesetFile.month, movesetFile.meta, movesetFile.elo, pokemon['name'],
                         teammate['name'], teammate['percentage']
                         ] for teammate in pokemon['teammates'] if teammate['name'] != "Other"]
                    sql = "INSERT INTO `moveset_teammates`" \
                          "(`year`, `month`, `format`, `elo`, `pokemon`, `teammate`, `percentage`)" \
                          " VALUES " \
                          "(%s, %s, %s, %s, %s, %s, %s)"
                    cursor.executemany(sql, data)

                    # Insert each value into `moveset_counters` table
                    data = [
                        [movesetFile.year, movesetFile.month, movesetFile.meta, movesetFile.elo, pokemon['name'],
                         counter['name'], counter['number1'], counter['number2'], counter['number3'], counter['koed'], counter['switched_out']
                         ] for counter in pokemon['counters']]
                    sql = "INSERT INTO `moveset_counters`" \
                          "(`year`, `month`, `format`, `elo`, `pokemon`, `counter`, `percentage`, " \
                          "`number2`, `number3`, `koed`, `switched_out`)" \
                          " VALUES " \
                          "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    cursor.executemany(sql, data)

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            self.connection.commit()
        finally:
            self.connection.close()