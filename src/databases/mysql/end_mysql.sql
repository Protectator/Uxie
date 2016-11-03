CREATE INDEX `usage_pokemon_year_index` ON `usage_pokemon`(`year`) USING BTREE;
CREATE INDEX `usage_year_index` ON `usage`(`year`) USING BTREE;
CREATE INDEX `leads_pokemon_year_index` ON `leads_pokemon`(`year`) USING BTREE;
CREATE INDEX `leads_year_index` ON `leads`(`year`) USING BTREE;
CREATE INDEX `moveset_abilities_year_index` ON `moveset_abilities`(`year`) USING BTREE;
CREATE INDEX `moveset_items_year_index` ON `moveset_items`(`year`) USING BTREE;
CREATE INDEX `moveset_spreads_year_index` ON `moveset_spreads`(`year`) USING BTREE;
CREATE INDEX `moveset_moves_year_index` ON `moveset_moves`(`year`) USING BTREE;
CREATE INDEX `moveset_teammates_year_index` ON `moveset_teammates`(`year`) USING BTREE;
CREATE INDEX `moveset_counters_year_index` ON `moveset_counters`(`year`) USING BTREE;
CREATE INDEX `moveset_year_index` ON `moveset_pokemon`(`year`) USING BTREE;
CREATE INDEX `chaos_abilities_year_index` ON `chaos_abilities`(`year`) USING BTREE;
CREATE INDEX `chaos_items_year_index` ON `chaos_items`(`year`) USING BTREE;
CREATE INDEX `chaos_spreads_year_index` ON `chaos_spreads`(`year`) USING BTREE;
CREATE INDEX `chaos_moves_year_index` ON `chaos_moves`(`year`) USING BTREE;
CREATE INDEX `chaos_teammates_year_index` ON `chaos_teammates`(`year`) USING BTREE;
CREATE INDEX `chaos_counters_year_index` ON `chaos_counters`(`year`) USING BTREE;
CREATE INDEX `chaos_happiness_year_index` ON `chaos_happiness`(`year`) USING BTREE;
CREATE INDEX `chaos_pokemon_year_index` ON `chaos_pokemon`(`year`) USING BTREE;
CREATE INDEX `chaos_year_index` ON `chaos`(`year`) USING BTREE;
CREATE INDEX `metagame_graphs_year_index` ON `metagame_graphs`(`year`) USING BTREE;
CREATE INDEX `metagame_usages_year_index` ON `metagame_usages`(`year`) USING BTREE;

CREATE INDEX `usage_pokemon_month_index` ON `usage_pokemon`(`month`) USING BTREE;
CREATE INDEX `usage_month_index` ON `usage`(`month`) USING BTREE;
CREATE INDEX `leads_pokemon_month_index` ON `leads_pokemon`(`month`) USING BTREE;
CREATE INDEX `leads_month_index` ON `leads`(`month`) USING BTREE;
CREATE INDEX `moveset_abilities_month_index` ON `moveset_abilities`(`month`) USING BTREE;
CREATE INDEX `moveset_items_month_index` ON `moveset_items`(`month`) USING BTREE;
CREATE INDEX `moveset_spreads_month_index` ON `moveset_spreads`(`month`) USING BTREE;
CREATE INDEX `moveset_moves_month_index` ON `moveset_moves`(`month`) USING BTREE;
CREATE INDEX `moveset_teammates_month_index` ON `moveset_teammates`(`month`) USING BTREE;
CREATE INDEX `moveset_counters_month_index` ON `moveset_counters`(`month`) USING BTREE;
CREATE INDEX `moveset_month_index` ON `moveset_pokemon`(`month`) USING BTREE;
CREATE INDEX `chaos_abilities_month_index` ON `chaos_abilities`(`month`) USING BTREE;
CREATE INDEX `chaos_items_month_index` ON `chaos_items`(`month`) USING BTREE;
CREATE INDEX `chaos_spreads_month_index` ON `chaos_spreads`(`month`) USING BTREE;
CREATE INDEX `chaos_moves_month_index` ON `chaos_moves`(`month`) USING BTREE;
CREATE INDEX `chaos_teammates_month_index` ON `chaos_teammates`(`month`) USING BTREE;
CREATE INDEX `chaos_counters_month_index` ON `chaos_counters`(`month`) USING BTREE;
CREATE INDEX `chaos_happiness_month_index` ON `chaos_happiness`(`month`) USING BTREE;
CREATE INDEX `chaos_pokemon_month_index` ON `chaos_pokemon`(`month`) USING BTREE;
CREATE INDEX `chaos_month_index` ON `chaos`(`month`) USING BTREE;
CREATE INDEX `metagame_graphs_month_index` ON `metagame_graphs`(`month`) USING BTREE;
CREATE INDEX `metagame_usages_month_index` ON `metagame_usages`(`month`) USING BTREE;

CREATE INDEX `usage_pokemon_format_index` ON `usage_pokemon`(`format`) USING HASH;
CREATE INDEX `usage_format_index` ON `usage`(`format`) USING HASH;
CREATE INDEX `leads_pokemon_format_index` ON `leads_pokemon`(`format`) USING HASH;
CREATE INDEX `leads_format_index` ON `leads`(`format`) USING HASH;
CREATE INDEX `moveset_abilities_format_index` ON `moveset_abilities`(`format`) USING HASH;
CREATE INDEX `moveset_items_format_index` ON `moveset_items`(`format`) USING HASH;
CREATE INDEX `moveset_spreads_format_index` ON `moveset_spreads`(`format`) USING HASH;
CREATE INDEX `moveset_moves_format_index` ON `moveset_moves`(`format`) USING HASH;
CREATE INDEX `moveset_teammates_format_index` ON `moveset_teammates`(`format`) USING HASH;
CREATE INDEX `moveset_counters_format_index` ON `moveset_counters`(`format`) USING HASH;
CREATE INDEX `moveset_format_index` ON `moveset_pokemon`(`format`) USING HASH;
CREATE INDEX `chaos_abilities_format_index` ON `chaos_abilities`(`format`) USING HASH;
CREATE INDEX `chaos_items_format_index` ON `chaos_items`(`format`) USING HASH;
CREATE INDEX `chaos_spreads_format_index` ON `chaos_spreads`(`format`) USING HASH;
CREATE INDEX `chaos_moves_format_index` ON `chaos_moves`(`format`) USING HASH;
CREATE INDEX `chaos_teammates_format_index` ON `chaos_teammates`(`format`) USING HASH;
CREATE INDEX `chaos_counters_format_index` ON `chaos_counters`(`format`) USING HASH;
CREATE INDEX `chaos_happiness_format_index` ON `chaos_happiness`(`format`) USING HASH;
CREATE INDEX `chaos_pokemon_format_index` ON `chaos_pokemon`(`format`) USING HASH;
CREATE INDEX `chaos_format_index` ON `chaos`(`format`) USING HASH;
CREATE INDEX `metagame_graphs_format_index` ON `metagame_graphs`(`format`) USING HASH;
CREATE INDEX `metagame_usages_format_index` ON `metagame_usages`(`format`) USING HASH;

CREATE INDEX `usage_pokemon_elo_index` ON `usage_pokemon`(`elo`) USING HASH;
CREATE INDEX `usage_elo_index` ON `usage`(`elo`) USING HASH;
CREATE INDEX `leads_pokemon_elo_index` ON `leads_pokemon`(`elo`) USING HASH;
CREATE INDEX `leads_elo_index` ON `leads`(`elo`) USING HASH;
CREATE INDEX `moveset_abilities_elo_index` ON `moveset_abilities`(`elo`) USING HASH;
CREATE INDEX `moveset_items_elo_index` ON `moveset_items`(`elo`) USING HASH;
CREATE INDEX `moveset_spreads_elo_index` ON `moveset_spreads`(`elo`) USING HASH;
CREATE INDEX `moveset_moves_elo_index` ON `moveset_moves`(`elo`) USING HASH;
CREATE INDEX `moveset_teammates_elo_index` ON `moveset_teammates`(`elo`) USING HASH;
CREATE INDEX `moveset_counters_elo_index` ON `moveset_counters`(`elo`) USING HASH;
CREATE INDEX `moveset_elo_index` ON `moveset_pokemon`(`elo`) USING HASH;
CREATE INDEX `chaos_abilities_elo_index` ON `chaos_abilities`(`elo`) USING HASH;
CREATE INDEX `chaos_items_elo_index` ON `chaos_items`(`elo`) USING HASH;
CREATE INDEX `chaos_spreads_elo_index` ON `chaos_spreads`(`elo`) USING HASH;
CREATE INDEX `chaos_moves_elo_index` ON `chaos_moves`(`elo`) USING HASH;
CREATE INDEX `chaos_teammates_elo_index` ON `chaos_teammates`(`elo`) USING HASH;
CREATE INDEX `chaos_counters_elo_index` ON `chaos_counters`(`elo`) USING HASH;
CREATE INDEX `chaos_happiness_elo_index` ON `chaos_happiness`(`elo`) USING HASH;
CREATE INDEX `chaos_pokemon_elo_index` ON `chaos_pokemon`(`elo`) USING HASH;
CREATE INDEX `chaos_elo_index` ON `chaos`(`elo`) USING HASH;
CREATE INDEX `metagame_graphs_elo_index` ON `metagame_graphs`(`elo`) USING HASH;
CREATE INDEX `metagame_usages_elo_index` ON `metagame_usages`(`elo`) USING HASH;

CREATE INDEX `usage_pokemon_pokemon_index` ON `usage_pokemon`(`pokemon`) USING HASH;
CREATE INDEX `leads_pokemon_pokemon_index` ON `leads_pokemon`(`pokemon`) USING HASH;
CREATE INDEX `chaos_pokemon_pokemon_index` ON `chaos_pokemon`(`pokemon`) USING HASH;
CREATE INDEX `chaos_abilities_pokemon_index` ON `chaos_abilities`(`pokemon`) USING HASH;
CREATE INDEX `chaos_items_pokemon_index` ON `chaos_items`(`pokemon`) USING HASH;
CREATE INDEX `chaos_spreads_pokemon_index` ON `chaos_spreads`(`pokemon`) USING HASH;
CREATE INDEX `chaos_moves_pokemon_index` ON `chaos_moves`(`pokemon`) USING HASH;
CREATE INDEX `chaos_teammates_pokemon_index` ON `chaos_teammates`(`pokemon`) USING HASH;
CREATE INDEX `chaos_happiness_pokemon_index` ON `chaos_happiness`(`pokemon`) USING HASH;
CREATE INDEX `chaos_counters_pokemon_index` ON `chaos_counters`(`pokemon`) USING HASH;
CREATE INDEX `moveset_pokemon_index` ON `moveset_pokemon`(`pokemon`) USING HASH;
CREATE INDEX `moveset_abilities_pokemon_index` ON `moveset_abilities`(`pokemon`) USING HASH;
CREATE INDEX `moveset_items_pokemon_index` ON `moveset_items`(`pokemon`) USING HASH;
CREATE INDEX `moveset_spreads_pokemon_index` ON `moveset_spreads`(`pokemon`) USING HASH;
CREATE INDEX `moveset_moves_pokemon_index` ON `moveset_moves`(`pokemon`) USING HASH;
CREATE INDEX `moveset_teammates_pokemon_index` ON `moveset_teammates`(`pokemon`) USING HASH;
CREATE INDEX `moveset_counters_pokemon_index` ON `moveset_counters`(`pokemon`) USING HASH;