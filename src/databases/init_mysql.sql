DROP TABLE IF EXISTS `usage_pokemons`;
DROP TABLE IF EXISTS `usage`;
DROP TABLE IF EXISTS `leads`;
DROP TABLE IF EXISTS `moveset_abilities`;
DROP TABLE IF EXISTS `moveset_items`;
DROP TABLE IF EXISTS `moveset_spreads`;
DROP TABLE IF EXISTS `moveset_moves`;
DROP TABLE IF EXISTS `moveset_teammates`;
DROP TABLE IF EXISTS `moveset_counters`;
DROP TABLE IF EXISTS `moveset`;
DROP TABLE IF EXISTS `metagame_graphs`;
DROP TABLE IF EXISTS `metagame_usages`;

CREATE TABLE IF NOT EXISTS `usage` (
  `year` INT(11) NOT NULL,
  `month` INT(11) NOT NULL,
  `format` VARCHAR(32) NOT NULL,
  `elo` INT(11) NOT NULL,
  `total_battles` INT(11) NOT NULL,
  `avg_weight_per_team` FLOAT NOT NULL,
  PRIMARY KEY (`year`,`month`,`format`,`elo`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS `usage_pokemons` (
  `year` INT(11) NOT NULL,
  `month` INT(11) NOT NULL,
  `format` VARCHAR(32) NOT NULL,
  `elo` INT(11) NOT NULL,
  `pokemon` VARCHAR(32) NOT NULL,
  `usage_percent` FLOAT NOT NULL,
  `raw_usage` INT(11) NOT NULL,
  `raw_percent` FLOAT NOT NULL,
  `real_usage` INT(11) NOT NULL,
  `real_percent` FLOAT NOT NULL,
  PRIMARY KEY (`year`,`month`,`format`,`elo`,`pokemon`),
  FOREIGN KEY (`year`,`month`,`format`,`elo`)
  REFERENCES `usage`(`year`,`month`,`format`,`elo`)
    ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS `leads` (
  `year` INT(11) NOT NULL,
  `month` INT(11) NOT NULL,
  `format` VARCHAR(32) NOT NULL,
  `elo` INT(11) NOT NULL,
  `total_leads` INT(11) NOT NULL,
  PRIMARY KEY (`year`,`month`,`format`,`elo`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS `leads_pokemons` (
  `year` INT(11) NOT NULL,
  `month` INT(11) NOT NULL,
  `format` VARCHAR(32) NOT NULL,
  `elo` INT(11) NOT NULL,
  `pokemon` VARCHAR(32) NOT NULL,
  `usage_percent` FLOAT NOT NULL,
  `raw_usage` INT(11) NOT NULL,
  `raw_percent` FLOAT NOT NULL,
  PRIMARY KEY (`year`,`month`,`format`,`elo`,`pokemon`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `moveset` (
  `year` int(11) NOT NULL,
  `month` int(11) NOT NULL,
  `format` varchar(32) NOT NULL,
  `elo` int(11) NOT NULL,
  `pokemon` varchar(32) NOT NULL,
  `raw_count` int(11) NOT NULL,
  `avg_weight` float NOT NULL,
  `viability_ceiling` int(11) NOT NULL,
  PRIMARY KEY (`year`,`month`,`format`,`elo`,`pokemon`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `moveset_abilities` (
  `year` int(11) NOT NULL,
  `month` int(11) NOT NULL,
  `format` varchar(32) NOT NULL,
  `elo` int(11) NOT NULL,
  `pokemon` varchar(32) NOT NULL,
  `ability` varchar(32) NOT NULL,
  `percentage` float NOT NULL,
  PRIMARY KEY (`year`,`month`,`format`,`elo`,`pokemon`, `ability`),
  FOREIGN KEY (`year`,`month`,`format`,`elo`,`pokemon`)
  REFERENCES moveset(`year`,`month`,`format`,`elo`,`pokemon`)
    ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `moveset_items` (
  `year` int(11) NOT NULL,
  `month` int(11) NOT NULL,
  `format` varchar(32) NOT NULL,
  `elo` int(11) NOT NULL,
  `pokemon` varchar(32) NOT NULL,
  `item` varchar(32) NOT NULL,
  `percentage` float NOT NULL,
  PRIMARY KEY (`year`,`month`,`format`,`elo`,`pokemon`, `item`),
  FOREIGN KEY (`year`,`month`,`format`,`elo`,`pokemon`)
  REFERENCES moveset(`year`,`month`,`format`,`elo`,`pokemon`)
    ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `moveset_spreads` (
  `year` int(11) NOT NULL,
  `month` int(11) NOT NULL,
  `format` varchar(32) NOT NULL,
  `elo` int(11) NOT NULL,
  `pokemon` varchar(32) NOT NULL,
  `nature` varchar(32) NOT NULL,
  `hp` tinyint unsigned NOT NULL,
  `atk` tinyint unsigned NOT NULL,
  `def` tinyint unsigned NOT NULL,
  `spa` tinyint unsigned NOT NULL,
  `spd` tinyint unsigned NOT NULL,
  `spe` tinyint unsigned NOT NULL,
  `percentage` float NOT NULL,
  PRIMARY KEY (`year`,`month`,`format`,`elo`,`pokemon`, `nature`, `hp`, `atk`, `def`, `spa`, `spd`, `spe`),
  FOREIGN KEY (`year`,`month`,`format`,`elo`,`pokemon`)
  REFERENCES moveset(`year`,`month`,`format`,`elo`,`pokemon`)
    ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `moveset_moves` (
  `year` int(11) NOT NULL,
  `month` int(11) NOT NULL,
  `format` varchar(32) NOT NULL,
  `elo` int(11) NOT NULL,
  `pokemon` varchar(32) NOT NULL,
  `move` varchar(32) NOT NULL,
  `percentage` float NOT NULL,
  PRIMARY KEY (`year`,`month`,`format`,`elo`,`pokemon`, `move`),
  FOREIGN KEY (`year`,`month`,`format`,`elo`,`pokemon`)
  REFERENCES moveset(`year`,`month`,`format`,`elo`,`pokemon`)
    ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `moveset_teammates` (
  `year` int(11) NOT NULL,
  `month` int(11) NOT NULL,
  `format` varchar(32) NOT NULL,
  `elo` int(11) NOT NULL,
  `pokemon` varchar(32) NOT NULL,
  `teammate` varchar(32) NOT NULL,
  `percentage` float NOT NULL,
  PRIMARY KEY (`year`,`month`,`format`,`elo`,`pokemon`, `teammate`),
  FOREIGN KEY (`year`,`month`,`format`,`elo`,`pokemon`)
  REFERENCES moveset(`year`,`month`,`format`,`elo`,`pokemon`)
    ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `moveset_counters` (
  `year` int(11) NOT NULL,
  `month` int(11) NOT NULL,
  `format` varchar(32) NOT NULL,
  `elo` int(11) NOT NULL,
  `pokemon` varchar(32) NOT NULL,
  `counter` varchar(32) NOT NULL,
  `percentage` float NOT NULL,
  `number2` float NOT NULL,
  `number3` float NOT NULL,
  `koed` float NOT NULL,
  `switched_out` float NOT NULL,
  PRIMARY KEY (`year`,`month`,`format`,`elo`,`pokemon`, `counter`),
  FOREIGN KEY (`year`,`month`,`format`,`elo`,`pokemon`)
  REFERENCES moveset(`year`,`month`,`format`,`elo`,`pokemon`)
    ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS `metagame_usages` (
  `year` INT(11) NOT NULL,
  `month` INT(11) NOT NULL,
  `format` VARCHAR(32) NOT NULL,
  `elo` INT(11) NOT NULL,
  `metagame` VARCHAR(32) NOT NULL,
  `percentage` FLOAT NOT NULL,
  PRIMARY KEY (`year`,`month`,`format`,`elo`,`metagame`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS `metagame_graphs` (
  `year` INT(11) NOT NULL,
  `month` INT(11) NOT NULL,
  `format` VARCHAR(32) NOT NULL,
  `elo` INT(11) NOT NULL,
  `key` FLOAT NOT NULL,
  `value` FLOAT NOT NULL,
  PRIMARY KEY (`year`,`month`,`format`,`elo`,`key`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;