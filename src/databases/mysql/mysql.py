#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This file is part of Uxie.

Uxie - Pokemon Showdown's usage stats database builder
Copyright (C) 2016-2017 Kewin Dousse (Protectator)

Licensed under the MIT License. See file LICENSE in the project root for license information.
"""
import pymysql.cursors

from src.databases.database import *


class MySQL(DataBase):
    def __init__(self):
        DataBase.__init__(self)
        self.connection = None

    def connect(self, host, user, password, db):
        self.connection = pymysql.connect(host=host,
                                          user=user,
                                          password=password,
                                          db=db,
                                          charset='utf8mb4',
                                          cursorclass=pymysql.cursors.DictCursor)

    def initialize(self):
        with self.connection.cursor() as cursor:
            with open("src/databases/mysql/init_mysql.sql", mode='r') as inputFile:
                sql = inputFile.read()
            cursor.execute(sql)
        self.connection.commit()

    def postInsert(self):
        with self.connection.cursor() as cursor:
            with open("src/databases/mysql/end_mysql.sql", mode='r') as inputFile:
                sql = inputFile.read()
            cursor.execute(sql)
        self.connection.commit()

    """
    # I tried. It doesn't work of course, but might be useful once later.
    def prepareInsert(self, table, columns):
        sql = "INSERT IGNORE INTO `" + table + "` ("
        values = " VALUES ("
        array = []
        first = True
        for key in columns:
            sql += ("`" + key + "`" if first else ", `" + key + "`")
            values += ("%s" if first else ", %s")
            array.append(columns[key])
            first = False
        sql = sql + ")" + values + ")"
        return sql, array"""

    def fillUsage(self, usageFile):
        with self.connection.cursor() as cursor:
            # Insert general values into `usage` table
            data = (usageFile.year, usageFile.month, usageFile.meta, usageFile.elo,
                    usageFile.data['total_battles'], usageFile.data['avg_weight'])
            sql = "INSERT INTO `usage`" \
                  "(`year`, `month`, `format`, `elo`, `total_battles`, `avg_weight_per_team`)" \
                  " VALUES " \
                  "(%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, data)

            # Insert each value into `usage_pokemon` table
            data = [
                [usageFile.year, usageFile.month, usageFile.meta, usageFile.elo, line['name'],
                 line['usage_percent'], line['raw_number'], line['raw_percent'],
                 line['real_number'], line['real_percent']] for line in usageFile.data['usage']]
            sql = "INSERT INTO `usage_pokemon`" \
                  "(`year`, `month`, `format`, `elo`, `pokemon`," \
                  " `usage_percent`, `raw_usage`, `raw_percent`," \
                  " `real_usage`, `real_percent`)" \
                  " VALUES " \
                  "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.executemany(sql, data)

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        self.connection.commit()


    def fillLeads(self, leadsFile):
        with self.connection.cursor() as cursor:
            # Insert general values into `leads` table
            data = (leadsFile.year, leadsFile.month, leadsFile.meta, leadsFile.elo,
                    leadsFile.data['total_leads'])
            sql = "INSERT INTO `leads`" \
                  "(`year`, `month`, `format`, `elo`, `total_leads`)" \
                  " VALUES " \
                  "(%s, %s, %s, %s, %s)"
            cursor.execute(sql, data)

            # Insert each value into `leads_pokemon` table
            data = [
                [leadsFile.year, leadsFile.month, leadsFile.meta, leadsFile.elo, line['name'],
                 line['usage_percent'], line['raw_number'], line['raw_percent']
                 ] for line in leadsFile.data['usage']]
            sql = "INSERT INTO `leads_pokemon`" \
                  "(`year`, `month`, `format`, `elo`, `pokemon`," \
                  " `usage_percent`, `raw_usage`, `raw_percent`)" \
                  " VALUES " \
                  "(%s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.executemany(sql, data)
            # connection is not autocommit by default. So you must commit to save
            # your changes.
            self.connection.commit()


    def fillMetagame(self, metagameFile):
        with self.connection.cursor() as cursor:
            if 'teams' in metagameFile.data:
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

            if 'graph' in metagameFile.data:
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


    def fillMoveset(self, movesetFile):
        with self.connection.cursor() as cursor: # For each Pokemon
            for pokemon in movesetFile.data:
                # Insert general values into `moveset_pokemon` table
                data = [movesetFile.year, movesetFile.month, movesetFile.meta, movesetFile.elo, pokemon['name']]
                sql = "INSERT IGNORE INTO `moveset_pokemon`" \
                      "(`year`, `month`, `format`, `elo`, `pokemon`, `raw_count`, `avg_weight`, `viability_ceiling`)" \
                      " VALUES " \
                      "(%s, %s, %s, %s, %s"
                if 'raw_count' in pokemon:
                    data.append(pokemon['raw_count'])
                    sql += ", %s"
                else:
                    sql += ", NULL"
                if 'avg_weight' in pokemon:
                    data.append(pokemon['avg_weight'])
                    sql += ", %s"
                else:
                    sql += ", NULL"
                if 'viability_ceiling' in pokemon:
                    data.append(pokemon['viability_ceiling'])
                    sql += ", %s"
                else:
                    sql += ", NULL"
                sql += ")"
                cursor.execute(sql, data)

                # Insert each value into `moveset_abilities` table
                data = [
                    [movesetFile.year, movesetFile.month, movesetFile.meta, movesetFile.elo, pokemon['name'],
                     ability['name'], ability['percentage']
                     ] for ability in pokemon['abilities']]
                sql = "INSERT IGNORE INTO `moveset_abilities`" \
                      "(`year`, `month`, `format`, `elo`, `pokemon`, `ability`, `percentage`)" \
                      " VALUES " \
                      "(%s, %s, %s, %s, %s, %s, %s)"
                cursor.executemany(sql, data)

                # Insert each value into `moveset_items` table
                data = [
                    [movesetFile.year, movesetFile.month, movesetFile.meta, movesetFile.elo, pokemon['name'],
                     item['name'], item['percentage']
                     ] for item in pokemon['items'] if item['name'] != "Other"]
                sql = "INSERT IGNORE INTO `moveset_items`" \
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
                sql = "INSERT IGNORE INTO `moveset_spreads`" \
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
                sql = "INSERT IGNORE INTO `moveset_moves`" \
                      "(`year`, `month`, `format`, `elo`, `pokemon`, `move`, `percentage`)" \
                      " VALUES " \
                      "(%s, %s, %s, %s, %s, %s, %s)"
                cursor.executemany(sql, data)

                # Insert each value into `moveset_teammates` table
                data = [
                    [movesetFile.year, movesetFile.month, movesetFile.meta, movesetFile.elo, pokemon['name'],
                     teammate['name'], teammate['percentage']
                     ] for teammate in pokemon['teammates'] if teammate['name'] != "Other"]
                sql = "INSERT IGNORE INTO `moveset_teammates`" \
                      "(`year`, `month`, `format`, `elo`, `pokemon`, `teammate`, `percentage`)" \
                      " VALUES " \
                      "(%s, %s, %s, %s, %s, %s, %s)"
                cursor.executemany(sql, data)

                # Insert each value into `moveset_counters` table
                data = [
                    [movesetFile.year, movesetFile.month, movesetFile.meta, movesetFile.elo, pokemon['name'],
                     counter['name'], counter['number1'], counter['number2'], counter['number3'], counter['koed'], counter['switched_out']
                     ] for counter in pokemon['counters']]
                sql = "INSERT IGNORE INTO `moveset_counters`" \
                      "(`year`, `month`, `format`, `elo`, `pokemon`, `counter`, `percentage`, " \
                      "`number2`, `number3`, `koed`, `switched_out`)" \
                      " VALUES " \
                      "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.executemany(sql, data)

        self.connection.commit()

    def fillChaos(self, chaosFile):
        with self.connection.cursor() as cursor:
            info = chaosFile.data['info']
            data = chaosFile.data['data']

            # Table `chaos`
            array = [chaosFile.year, chaosFile.month, chaosFile.meta, chaosFile.elo, info['cutoff'],
                    info['cutoff deviation'], info['metagame'], info['number of battles']]
            sql = "INSERT IGNORE INTO `chaos`" \
                  "(`year`, `month`, `format`, `elo`, `cutoff`, `cutoff_deviation`, `metagame`, `number_battles`)" \
                  " VALUES " \
                  "(%s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, array)

            # Table `chaos_pokemon`
            array = [
                [chaosFile.year, chaosFile.month, chaosFile.meta, chaosFile.elo, pokemon, data[pokemon]['Raw count'],
                 data[pokemon]['usage'] if 'usage' in data[pokemon] else None,
                 data[pokemon]['Viability Ceiling'][0] if 'Viability Ceiling' in data[pokemon] else None,
                 data[pokemon]['Viability Ceiling'][1] if 'Viability Ceiling' in data[pokemon] else None,
                 data[pokemon]['Viability Ceiling'][2] if 'Viability Ceiling' in data[pokemon] else None,
                 data[pokemon]['Viability Ceiling'][3] if 'Viability Ceiling' in data[pokemon] else None
                 ] for pokemon in data]
            sql = "INSERT IGNORE INTO `chaos_pokemon`" \
                  "(`year`, `month`, `format`, `elo`, `pokemon`, `raw_count`, " \
                  "`usage`, `viability_ceiling_total_players`, `viability_ceiling_top_gxe`, `viability_ceiling_gxe_99perc`, `viability_ceiling_gxe_95perc`)" \
                  " VALUES " \
                  "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.executemany(sql, array)

            # Table `chaos_ablities`
            for pokemon in data:
                array = [
                    [chaosFile.year, chaosFile.month, chaosFile.meta, chaosFile.elo, pokemon, ability,
                     data[pokemon]['Abilities'][ability]
                     ] for ability in data[pokemon]['Abilities']]
                sql = "INSERT IGNORE INTO `chaos_abilities`" \
                      "(`year`, `month`, `format`, `elo`, `pokemon`, `ability`, `raw_count`)" \
                      " VALUES " \
                      "(%s, %s, %s, %s, %s, %s, %s)"
                cursor.executemany(sql, array)

            # Table `chaos_counters`
            for pokemon in data:
                array = [
                    [chaosFile.year, chaosFile.month, chaosFile.meta, chaosFile.elo, pokemon, counter,
                     data[pokemon]['Checks and Counters'][counter][0],
                     data[pokemon]['Checks and Counters'][counter][1],
                     data[pokemon]['Checks and Counters'][counter][2],
                     ] for counter in data[pokemon]['Checks and Counters']]
                sql = "INSERT IGNORE INTO `chaos_counters`" \
                      "(`year`, `month`, `format`, `elo`, `pokemon`, `counter`, `occurences`, `koorswitch`, `standarddev`)" \
                      " VALUES " \
                      "(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.executemany(sql, array)

            # Table `chaos_happiness`
            for pokemon in data:
                if 'Happiness' in data[pokemon]:
                    array = [
                        [chaosFile.year, chaosFile.month, chaosFile.meta, chaosFile.elo, pokemon,
                         value if 'Happiness' in data[pokemon] else None,
                         data[pokemon]['Happiness'][value] if 'Happiness' in data[pokemon] else None
                         ] for value in data[pokemon]['Happiness']]
                    sql = "INSERT IGNORE INTO `chaos_happiness`" \
                          "(`year`, `month`, `format`, `elo`, `pokemon`, `value`, `raw_count`)" \
                          " VALUES " \
                          "(%s, %s, %s, %s, %s, %s, %s)"
                    cursor.executemany(sql, array)

            # Table `chaos_items`
            for pokemon in data:
                array = [
                    [chaosFile.year, chaosFile.month, chaosFile.meta, chaosFile.elo, pokemon, item,
                     data[pokemon]['Items'][item]
                     ] for item in data[pokemon]['Items']]
                sql = "INSERT IGNORE INTO `chaos_items`" \
                      "(`year`, `month`, `format`, `elo`, `pokemon`, `item`, `raw_count`)" \
                      " VALUES " \
                      "(%s, %s, %s, %s, %s, %s, %s)"
                cursor.executemany(sql, array)

            # Table `chaos_moves`
            for pokemon in data:
                array = [
                    [chaosFile.year, chaosFile.month, chaosFile.meta, chaosFile.elo, pokemon, move,
                     data[pokemon]['Moves'][move]
                     ] for move in data[pokemon]['Moves']]
                sql = "INSERT IGNORE INTO `chaos_moves`" \
                      "(`year`, `month`, `format`, `elo`, `pokemon`, `move`, `raw_count`)" \
                      " VALUES " \
                      "(%s, %s, %s, %s, %s, %s, %s)"
                cursor.executemany(sql, array)

            # Table `chaos_spreads`
            for pokemon in data:
                final_array = []
                for spread in data[pokemon]['Spreads']:
                    raw_count = data[pokemon]['Spreads'][spread]
                    parts = spread.split(':')
                    evs = parts[1].split('/')
                    array = [chaosFile.year, chaosFile.month, chaosFile.meta, chaosFile.elo, pokemon, parts[0], evs[0],
                             evs[1], evs[2], evs[3], evs[4], evs[5], raw_count]
                    final_array.append(array)
                sql = "INSERT IGNORE INTO `chaos_spreads`" \
                      "(`year`, `month`, `format`, `elo`, `pokemon`, `nature`, `hp`, `atk`, `def`, `spa`, `spd`," \
                      "`spe`,`raw_count`)" \
                      " VALUES " \
                      "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.executemany(sql, final_array)

        self.connection.commit()
