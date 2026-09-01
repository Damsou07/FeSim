import random
import math


STAT_KEYS = ["hp", "str", "mag", "skl", "spd", "lck", "defense", "res"]
TARGET_LEVEL = 20


class SimulationService:

    def simulate(self, character: dict, scenario_count: int) -> dict:
        start_level = character.get("level", 1)
        levels_to_simulate = TARGET_LEVEL - start_level
        if levels_to_simulate <= 0:
            return self._make_result(character, scenario_count, {})

        accumulators = {key: 0.0 for key in STAT_KEYS}
        squared_accumulators = {key: 0.0 for key in STAT_KEYS}
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
                squared_accumulators[key] += stats[key] ** 2
                min_stats[key] = min(min_stats[key], stats[key])
                max_stats[key] = max(max_stats[key], stats[key])

        avg_stats = {
            key: round(accumulators[key] / scenario_count, 1)
            for key in STAT_KEYS
        }
        variance_stats = {
            key: round(
                (squared_accumulators[key] / scenario_count) - (accumulators[key] / scenario_count) ** 2,
                1
            )
            for key in STAT_KEYS
        }

        return self._make_result(character, scenario_count, avg_stats, min_stats, max_stats, variance_stats)

    def simulate_post_promotion(
        self, character: dict, promotion_bonuses: dict, scenario_count: int
    ) -> dict:
        """Simulate stats at level 1 after promotion with bonuses applied."""
        # Start with current stats + promotion bonuses
        base_after_promo = {}
        for key in STAT_KEYS:
            base_after_promo[key] = character[key] + promotion_bonuses.get(key, 0)

        return {
            "character_name": character.get("name", "Inconnu"),
            "start_level": 1,
            "target_level": 1,
            "scenario_count": scenario_count,
            "base_stats": base_after_promo,
            "growth_rates": {key: character[f"{key}_growth"] for key in STAT_KEYS},
            "avg_stats": base_after_promo.copy(),
            "min_stats": base_after_promo.copy(),
            "max_stats": base_after_promo.copy(),
            "variance_stats": {key: 0.0 for key in STAT_KEYS},
        }

    @staticmethod
    def _make_result(
        character: dict,
        scenario_count: int,
        avg_stats: dict,
        min_stats: dict | None = None,
        max_stats: dict | None = None,
        variance_stats: dict | None = None,
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
            "variance_stats": variance_stats,
        }
