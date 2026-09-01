import random


STAT_KEYS = ["hp", "str", "mag", "skl", "spd", "lck", "defense", "res"]
STAT_LABELS = ["HP", "STR", "MAG", "SKL", "SPD", "LCK", "DEF", "RES"]
TARGET_LEVEL = 20


class SimulationService:

    def simulate_matrix(
        self,
        character: dict,
        scenario_count: int,
        promotion_bonuses: dict | None = None,
    ) -> dict:
        """Simulate and return the full level-by-level stat matrix.

        For pre-promotion classes:
          - Phase 1: levels from start_level to 20
          - Phase 2: apply promotion bonuses, then levels 1 to 20

        For post-promotion classes:
          - levels from start_level to 20

        Returns a dict with:
          - "columns": list of column labels (e.g. ["1", "2", ..., "20", "↑", "1", "2", ..., "20"])
          - "matrix": { stat_key: [value_at_level1, value_at_level2, ...] }
        """
        start_level = character.get("level", 1)
        is_pre_promo = promotion_bonuses is not None

        # Build column headers and compute average stats at each level
        if is_pre_promo:
            # Phase 1: start_level -> 20
            phase1_levels = list(range(start_level, TARGET_LEVEL + 1))
            # Phase 2: after promotion, levels 1 -> 20
            phase2_levels = list(range(1, TARGET_LEVEL + 1))
            columns = [str(lv) for lv in phase1_levels] + ["↑"] + [str(lv) for lv in phase2_levels]
            total_cols = len(phase1_levels) + 1 + len(phase2_levels)
        else:
            phase1_levels = list(range(start_level, TARGET_LEVEL + 1))
            phase2_levels = []
            columns = [str(lv) for lv in phase1_levels]
            total_cols = len(phase1_levels)

        # Accumulators for average at each column
        accumulators = {key: [0.0] * total_cols for key in STAT_KEYS}

        for _ in range(scenario_count):
            stats = {key: character[key] for key in STAT_KEYS}
            col = 0

            # Phase 1: level up to 20
            for lv in phase1_levels:
                for key in STAT_KEYS:
                    accumulators[key][col] += stats[key]
                col += 1
                if lv < TARGET_LEVEL:
                    for key in STAT_KEYS:
                        growth = character[f"{key}_growth"]
                        if random.randint(1, 100) <= growth:
                            stats[key] += 1

            # Promotion column
            if is_pre_promo:
                for key in STAT_KEYS:
                    stats[key] += promotion_bonuses.get(key, 0)
                    accumulators[key][col] += stats[key]
                col += 1

                # Phase 2: level 1 -> 20 after promotion
                for lv in phase2_levels:
                    for key in STAT_KEYS:
                        accumulators[key][col] += stats[key]
                    col += 1
                    if lv < TARGET_LEVEL:
                        for key in STAT_KEYS:
                            growth = character[f"{key}_growth"]
                            if random.randint(1, 100) <= growth:
                                stats[key] += 1

        # Average
        matrix = {}
        for key in STAT_KEYS:
            matrix[key] = [round(v / scenario_count, 1) for v in accumulators[key]]

        return {
            "columns": columns,
            "matrix": matrix,
            "start_level": start_level,
            "target_level": TARGET_LEVEL,
            "scenario_count": scenario_count,
            "character_name": character.get("name", "Inconnu"),
            "is_pre_promo": is_pre_promo,
        }
