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
            with open("src/databases/init_mysql.sql", mode='r') as file:
                sql = file.read()
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
