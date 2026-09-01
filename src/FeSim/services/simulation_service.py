import random


STAT_KEYS = ["hp", "str", "mag", "skl", "spd", "lck", "defense", "res"]
TARGET_LEVEL = 20


class SimulationService:

    def simulate(self, character: dict, scenario_count: int) -> dict:
        start_level = character.get("level", 1)
        levels_to_simulate = TARGET_LEVEL - start_level
        if levels_to_simulate <= 0:
            return self._make_result(character, scenario_count, {})

        accumulators = {key: 0.0 for key in STAT_KEYS}
        min_stats = {key: character[key] for key in STAT_KEYS}
        max_stats = {key: character[key] for key in STAT_KEYS}

        for _ in range(scenario_count):
            stats = {key: character[key] for key in STAT_KEYS}
            for _ in range(levels_to_simulate):
                for key in STAT_KEYS:
                    growth = character[f"{key}_growth"]
                    if random.randint(1, 100) <= growth:
                        stats[key] += 1
            for key in STAT_KEYS:
                accumulators[key] += stats[key]
                min_stats[key] = min(min_stats[key], stats[key])
                max_stats[key] = max(max_stats[key], stats[key])

        avg_stats = {
            key: round(accumulators[key] / scenario_count, 1)
            for key in STAT_KEYS
        }

        return self._make_result(character, scenario_count, avg_stats, min_stats, max_stats)

    @staticmethod
    def _make_result(
        character: dict,
        scenario_count: int,
        avg_stats: dict,
        min_stats: dict | None = None,
        max_stats: dict | None = None,
    ) -> dict:
        return {
            "character_name": character.get("name", "Inconnu"),
            "start_level": character.get("level", 1),
            "target_level": TARGET_LEVEL,
            "scenario_count": scenario_count,
            "base_stats": {key: character[key] for key in STAT_KEYS},
            "growth_rates": {key: character[f"{key}_growth"] for key in STAT_KEYS},
            "avg_stats": avg_stats,
            "min_stats": min_stats,
            "max_stats": max_stats,
        }
