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
            sql = """DROP TABLE IF EXISTS `usage`;
                  CREATE TABLE IF NOT EXISTS `usage` (
                    `year` INT(11) NOT NULL,
                    `month` INT(11) NOT NULL,
                    `format` VARCHAR(32) NOT NULL,
                    `elo` INT(11) NOT NULL,
                    `pokemon` VARCHAR(32) NOT NULL,
                    `usage_percent` FLOAT DEFAULT NULL,
                    `raw_usage` INT(11) DEFAULT NULL,
                    `raw_percent` FLOAT DEFAULT NULL,
                    `real_usage` INT(11) DEFAULT NULL,
                    `real_percent` FLOAT DEFAULT NULL,
                    UNIQUE KEY `usage_year_month_format_elo_pokemon_pk` (`year`,`month`,`format`,`elo`,`pokemon`)
                  ) ENGINE=MyISAM DEFAULT CHARSET=latin1;"""
            cursor.execute(sql)
        self.connection.commit()

    def fillUsage(self, usageFile):
        try:
            with self.connection.cursor() as cursor:
                data = [
                    [usageFile.year, usageFile.month, usageFile.meta, usageFile.elo, line[1], line[2], line[3], line[4],
                     line[5], line[6]] for line in usageFile.data]
                sql = "INSERT INTO `usage` (`year`, `month`, `format`, `elo`, `pokemon`, `usage_percent`, `raw_usage`, `raw_percent`, `real_usage`, `real_percent`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.executemany(sql, data)

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            self.connection.commit()
        finally:
            self.connection.close()