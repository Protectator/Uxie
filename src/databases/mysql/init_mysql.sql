DROP TABLE IF EXISTS `usage_pokemon`;
DROP TABLE IF EXISTS `usage`;
DROP TABLE IF EXISTS `leads_pokemon`;
DROP TABLE IF EXISTS `leads`;
DROP TABLE IF EXISTS `moveset_abilities`;
DROP TABLE IF EXISTS `moveset_items`;
DROP TABLE IF EXISTS `moveset_spreads`;
DROP TABLE IF EXISTS `moveset_moves`;
DROP TABLE IF EXISTS `moveset_teammates`;
DROP TABLE IF EXISTS `moveset_counters`;
DROP TABLE IF EXISTS `moveset_pokemon`;
DROP TABLE IF EXISTS `chaos_abilities`;
DROP TABLE IF EXISTS `chaos_items`;
DROP TABLE IF EXISTS `chaos_spreads`;
DROP TABLE IF EXISTS `chaos_moves`;
DROP TABLE IF EXISTS `chaos_teammates`;
DROP TABLE IF EXISTS `chaos_counters`;
DROP TABLE IF EXISTS `chaos_happiness`;
DROP TABLE IF EXISTS `chaos_pokemon`;
DROP TABLE IF EXISTS `chaos`;
DROP TABLE IF EXISTS `metagame_graphs`;
DROP TABLE IF EXISTS `metagame_usages`;

CREATE TABLE `usage` (
  `year` SMALLINT UNSIGNED NOT NULL,
  `month` TINYINT UNSIGNED NOT NULL,
  `format` VARCHAR(31) NOT NULL,
  `elo` SMALLINT UNSIGNED NOT NULL,
  `total_battles` INT(11) UNSIGNED NOT NULL,
  `avg_weight_per_team` DECIMAL(4,3) NOT NULL,
  PRIMARY KEY (`year`,`month`,`format`,`elo`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `usage_pokemon` (
  `year` SMALLINT UNSIGNED NOT NULL,
  `month` TINYINT UNSIGNED NOT NULL,
  `format` VARCHAR(31) NOT NULL,
  `elo` SMALLINT UNSIGNED NOT NULL,
  `pokemon` VARCHAR(31) NOT NULL,
  `usage_percent` DECIMAL(8,5) NOT NULL,
  `raw_usage` INT(11) UNSIGNED NOT NULL,
  `raw_percent` DECIMAL(6,3) NOT NULL,
  `real_usage` INT(11) UNSIGNED NOT NULL,
  `real_percent` DECIMAL(6,3) NOT NULL,
  PRIMARY KEY (`year`,`month`,`format`,`elo`,`pokemon`),
  FOREIGN KEY (`year`,`month`,`format`,`elo`)
  REFERENCES `usage`(`year`,`month`,`format`,`elo`)
    ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `leads` (
  `year` SMALLINT UNSIGNED NOT NULL,
  `month` TINYINT UNSIGNED NOT NULL,
  `format` VARCHAR(31) NOT NULL,
  `elo` SMALLINT UNSIGNED NOT NULL,
  `total_leads` INT(11) UNSIGNED NOT NULL,
  PRIMARY KEY (`year`,`month`,`format`,`elo`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `leads_pokemon` (
  `year` SMALLINT UNSIGNED NOT NULL,
  `month` TINYINT UNSIGNED NOT NULL,
  `format` VARCHAR(31) NOT NULL,
  `elo` SMALLINT UNSIGNED NOT NULL,
  `pokemon` VARCHAR(31) NOT NULL,
  `usage_percent` DECIMAL(8,5) NOT NULL,
  `raw_usage` INT(11) UNSIGNED NOT NULL,
  `raw_percent` DECIMAL(6,3) NOT NULL,
  PRIMARY KEY (`year`,`month`,`format`,`elo`,`pokemon`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `chaos` (
  `year` SMALLINT UNSIGNED NOT NULL,
  `month` TINYINT UNSIGNED NOT NULL,
  `format` VARCHAR(31) NOT NULL,
  `elo` SMALLINT UNSIGNED NOT NULL,
  `team_type` VARCHAR(31),
  `cutoff` FLOAT NOT NULL,
  `cutoff_deviation` FLOAT NOT NULL,
  `metagame` VARCHAR(31) NOT NULL,
  `number_battles` INT NOT NULL,
  PRIMARY KEY (`year`,`month`,`format`,`elo`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `chaos_pokemon` (
  `year` SMALLINT UNSIGNED NOT NULL,
  `month` TINYINT UNSIGNED NOT NULL,
  `format` VARCHAR(31) NOT NULL,
  `elo` SMALLINT UNSIGNED NOT NULL,
  `pokemon` VARCHAR(31) NOT NULL,
  `raw_count` INT UNSIGNED NOT NULL,
  `usage` FLOAT,
  `viability_ceiling1` SMALLINT UNSIGNED,
  `viability_ceiling2` SMALLINT UNSIGNED,
  `viability_ceiling3` SMALLINT UNSIGNED,
  `viability_ceiling4` SMALLINT UNSIGNED,
    PRIMARY KEY (`year`,`month`,`format`,`elo`, `pokemon`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `chaos_abilities` (
  `year` SMALLINT UNSIGNED NOT NULL,
  `month` TINYINT UNSIGNED NOT NULL,
  `format` VARCHAR(31) NOT NULL,
  `elo` SMALLINT UNSIGNED NOT NULL,
  `pokemon` VARCHAR(31) NOT NULL,
  `ability` VARCHAR(31) NOT NULL,
  `raw_count` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`year`,`month`,`format`,`elo`,`pokemon`, `ability`),
  FOREIGN KEY (`year`,`month`,`format`,`elo`,`pokemon`)
  REFERENCES chaos_pokemon(`year`,`month`,`format`,`elo`,`pokemon`)
    ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `chaos_items` (
  `year` SMALLINT UNSIGNED NOT NULL,
  `month` TINYINT UNSIGNED NOT NULL,
  `format` VARCHAR(31) NOT NULL,
  `elo` SMALLINT UNSIGNED NOT NULL,
  `pokemon` VARCHAR(31) NOT NULL,
  `item` VARCHAR(31) NOT NULL,
  `raw_count` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`year`,`month`,`format`,`elo`,`pokemon`, `item`),
  FOREIGN KEY (`year`,`month`,`format`,`elo`,`pokemon`)
  REFERENCES chaos_pokemon(`year`,`month`,`format`,`elo`,`pokemon`)
    ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `chaos_spreads` (
  `year` SMALLINT UNSIGNED NOT NULL,
  `month` TINYINT UNSIGNED NOT NULL,
  `format` VARCHAR(31) NOT NULL,
  `elo` SMALLINT UNSIGNED NOT NULL,
  `pokemon` VARCHAR(31) NOT NULL,
  `nature` VARCHAR(15) NOT NULL,
  `hp` TINYINT UNSIGNED NOT NULL,
  `atk` TINYINT UNSIGNED NOT NULL,
  `def` TINYINT UNSIGNED NOT NULL,
  `spa` TINYINT UNSIGNED NOT NULL,
  `spd` TINYINT UNSIGNED NOT NULL,
  `spe` TINYINT UNSIGNED NOT NULL,
  `raw_count` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`year`,`month`,`format`,`elo`,`pokemon`, `nature`, `hp`, `atk`, `def`, `spa`, `spd`, `spe`),
  FOREIGN KEY (`year`,`month`,`format`,`elo`,`pokemon`)
  REFERENCES chaos_pokemon(`year`,`month`,`format`,`elo`,`pokemon`)
    ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `chaos_moves` (
  `year` SMALLINT UNSIGNED NOT NULL,
  `month` TINYINT UNSIGNED NOT NULL,
  `format` VARCHAR(31) NOT NULL,
  `elo` SMALLINT UNSIGNED NOT NULL,
  `pokemon` VARCHAR(31) NOT NULL,
  `move` VARCHAR(31) NOT NULL,
  `raw_count` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`year`,`month`,`format`,`elo`,`pokemon`, `move`),
  FOREIGN KEY (`year`,`month`,`format`,`elo`,`pokemon`)
  REFERENCES chaos_pokemon(`year`,`month`,`format`,`elo`,`pokemon`)
    ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `chaos_teammates` (
  `year` SMALLINT UNSIGNED NOT NULL,
  `month` TINYINT UNSIGNED NOT NULL,
  `format` VARCHAR(31) NOT NULL,
  `elo` SMALLINT UNSIGNED NOT NULL,
  `pokemon` VARCHAR(31) NOT NULL,
  `teammate` VARCHAR(31) NOT NULL,
  `percentage` DECIMAL(6,3) NOT NULL,
  PRIMARY KEY (`year`,`month`,`format`,`elo`,`pokemon`, `teammate`),
  FOREIGN KEY (`year`,`month`,`format`,`elo`,`pokemon`)
  REFERENCES chaos_pokemon(`year`,`month`,`format`,`elo`,`pokemon`)
    ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `chaos_happiness` (
  `year` SMALLINT UNSIGNED NOT NULL,
  `month` TINYINT UNSIGNED NOT NULL,
  `format` VARCHAR(31) NOT NULL,
  `elo` SMALLINT UNSIGNED NOT NULL,
  `pokemon` VARCHAR(31) NOT NULL,
  `value` TINYINT UNSIGNED NOT NULL,
  `raw_count` INT UNSIGNED NOT NULL,
  KEY (`year`,`month`,`format`,`elo`,`pokemon`, `value`),
  FOREIGN KEY (`year`,`month`,`format`,`elo`,`pokemon`)
  REFERENCES chaos_pokemon(`year`,`month`,`format`,`elo`,`pokemon`)
    ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `chaos_counters` (
  `year` SMALLINT UNSIGNED NOT NULL,
  `month` TINYINT UNSIGNED NOT NULL,
  `format` VARCHAR(31) NOT NULL,
  `elo` SMALLINT UNSIGNED NOT NULL,
  `pokemon` VARCHAR(31) NOT NULL,
  `counter` VARCHAR(31) NOT NULL,
  `number1` DECIMAL(15,14) NOT NULL,
  `number2` DECIMAL(15,14) NOT NULL,
  `number3` DECIMAL(15,14) NOT NULL,
  PRIMARY KEY (`year`,`month`,`format`,`elo`,`pokemon`, `counter`),
  FOREIGN KEY (`year`,`month`,`format`,`elo`,`pokemon`)
  REFERENCES chaos_pokemon(`year`,`month`,`format`,`elo`,`pokemon`)
    ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `moveset_pokemon` (
  `year` SMALLINT UNSIGNED NOT NULL,
  `month` TINYINT UNSIGNED NOT NULL,
  `format` VARCHAR(31) NOT NULL,
  `elo` SMALLINT UNSIGNED NOT NULL,
  `pokemon` VARCHAR(31) NOT NULL,
  `raw_count` INT(11) UNSIGNED NOT NULL,
  `avg_weight` FLOAT,
  `viability_ceiling` SMALLINT UNSIGNED,
  PRIMARY KEY (`year`,`month`,`format`,`elo`,`pokemon`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `moveset_abilities` (
  `year` SMALLINT UNSIGNED NOT NULL,
  `month` TINYINT UNSIGNED NOT NULL,
  `format` VARCHAR(31) NOT NULL,
  `elo` SMALLINT UNSIGNED NOT NULL,
  `pokemon` VARCHAR(31) NOT NULL,
  `ability` VARCHAR(31) NOT NULL,
  `percentage` DECIMAL(6,3) NOT NULL,
  PRIMARY KEY (`year`,`month`,`format`,`elo`,`pokemon`, `ability`),
  FOREIGN KEY (`year`,`month`,`format`,`elo`,`pokemon`)
  REFERENCES moveset_pokemon(`year`,`month`,`format`,`elo`,`pokemon`)
    ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `moveset_items` (
  `year` SMALLINT UNSIGNED NOT NULL,
  `month` TINYINT UNSIGNED NOT NULL,
  `format` VARCHAR(31) NOT NULL,
  `elo` SMALLINT UNSIGNED NOT NULL,
  `pokemon` VARCHAR(31) NOT NULL,
  `item` VARCHAR(31) NOT NULL,
  `percentage` DECIMAL(6,3) NOT NULL,
  PRIMARY KEY (`year`,`month`,`format`,`elo`,`pokemon`, `item`),
  FOREIGN KEY (`year`,`month`,`format`,`elo`,`pokemon`)
  REFERENCES moveset_pokemon(`year`,`month`,`format`,`elo`,`pokemon`)
    ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `moveset_spreads` (
  `year` SMALLINT UNSIGNED NOT NULL,
  `month` TINYINT UNSIGNED NOT NULL,
  `format` VARCHAR(31) NOT NULL,
  `elo` SMALLINT UNSIGNED NOT NULL,
  `pokemon` VARCHAR(31) NOT NULL,
  `nature` VARCHAR(15) NOT NULL,
  `hp` TINYINT UNSIGNED NOT NULL,
  `atk` TINYINT UNSIGNED NOT NULL,
  `def` TINYINT UNSIGNED NOT NULL,
  `spa` TINYINT UNSIGNED NOT NULL,
  `spd` TINYINT UNSIGNED NOT NULL,
  `spe` TINYINT UNSIGNED NOT NULL,
  `percentage` DECIMAL(6,3) NOT NULL,
  PRIMARY KEY (`year`,`month`,`format`,`elo`,`pokemon`, `nature`, `hp`, `atk`, `def`, `spa`, `spd`, `spe`),
  FOREIGN KEY (`year`,`month`,`format`,`elo`,`pokemon`)
  REFERENCES moveset_pokemon(`year`,`month`,`format`,`elo`,`pokemon`)
    ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `moveset_moves` (
  `year` SMALLINT UNSIGNED NOT NULL,
  `month` TINYINT UNSIGNED NOT NULL,
  `format` VARCHAR(31) NOT NULL,
  `elo` SMALLINT UNSIGNED NOT NULL,
  `pokemon` VARCHAR(31) NOT NULL,
  `move` VARCHAR(31) NOT NULL,
  `percentage` DECIMAL(6,3) NOT NULL,
  PRIMARY KEY (`year`,`month`,`format`,`elo`,`pokemon`, `move`),
  FOREIGN KEY (`year`,`month`,`format`,`elo`,`pokemon`)
  REFERENCES moveset_pokemon(`year`,`month`,`format`,`elo`,`pokemon`)
    ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `moveset_teammates` (
  `year` SMALLINT UNSIGNED NOT NULL,
  `month` TINYINT UNSIGNED NOT NULL,
  `format` VARCHAR(31) NOT NULL,
  `elo` SMALLINT UNSIGNED NOT NULL,
  `pokemon` VARCHAR(31) NOT NULL,
  `teammate` VARCHAR(31) NOT NULL,
  `percentage` DECIMAL(6,3) NOT NULL,
  PRIMARY KEY (`year`,`month`,`format`,`elo`,`pokemon`, `teammate`),
  FOREIGN KEY (`year`,`month`,`format`,`elo`,`pokemon`)
  REFERENCES moveset_pokemon(`year`,`month`,`format`,`elo`,`pokemon`)
    ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `moveset_counters` (
  `year` SMALLINT UNSIGNED NOT NULL,
  `month` TINYINT UNSIGNED NOT NULL,
  `format` VARCHAR(31) NOT NULL,
  `elo` SMALLINT UNSIGNED NOT NULL,
  `pokemon` VARCHAR(31) NOT NULL,
  `counter` VARCHAR(31) NOT NULL,
  `percentage` DECIMAL(6,3) NOT NULL,
  `number2` DECIMAL(5,2) NOT NULL,
  `number3` DECIMAL(5,2) NOT NULL,
  `koed` DECIMAL(4,1) NOT NULL,
  `switched_out` DECIMAL(4,1) NOT NULL,
  PRIMARY KEY (`year`,`month`,`format`,`elo`,`pokemon`, `counter`),
  FOREIGN KEY (`year`,`month`,`format`,`elo`,`pokemon`)
  REFERENCES moveset_pokemon(`year`,`month`,`format`,`elo`,`pokemon`)
    ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS `metagame_usages` (
  `year` SMALLINT UNSIGNED NOT NULL,
  `month` TINYINT UNSIGNED NOT NULL,
  `format` VARCHAR(31) NOT NULL,
  `elo` SMALLINT UNSIGNED NOT NULL,
  `metagame` VARCHAR(31) NOT NULL,
  `percentage` DECIMAL(8,5) NOT NULL,
  PRIMARY KEY (`year`,`month`,`format`,`elo`,`metagame`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS `metagame_graphs` (
  `year` SMALLINT UNSIGNED NOT NULL,
  `month` TINYINT UNSIGNED NOT NULL,
  `format` VARCHAR(31) NOT NULL,
  `elo` SMALLINT UNSIGNED NOT NULL,
  `key` DECIMAL(6,3) NOT NULL,
  `value` DECIMAL(6,3) NOT NULL,
  PRIMARY KEY (`year`,`month`,`format`,`elo`,`key`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;