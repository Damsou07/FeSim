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
        caps_phase1: dict | None = None,
        caps_phase2: dict | None = None,
    ) -> dict:
        """Simulate and return the full level-by-level stat matrix.

        For pre-promotion classes:
          - Phase 1: levels from start_level to 20 (uses caps_phase1)
          - Phase 2: apply promotion bonuses, then levels 1 to 20 (uses caps_phase2)

        For post-promotion classes:
          - levels from start_level to 20 (uses caps_phase1)

        Returns a dict with:
          - "columns": list of column labels
          - "matrix": { stat_key: [value_at_level1, value_at_level2, ...] }
        """
        start_level = character.get("level", 1)
        is_pre_promo = promotion_bonuses is not None

        # Default caps: no limit (999)
        if caps_phase1 is None:
            caps_phase1 = {key: 999 for key in STAT_KEYS}
        if caps_phase2 is None:
            caps_phase2 = {key: 999 for key in STAT_KEYS}

        # Build column headers
        if is_pre_promo:
            phase1_levels = list(range(start_level, TARGET_LEVEL + 1))
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
                            if stats[key] < caps_phase1[key]:
                                stats[key] += 1

            # Promotion column
            if is_pre_promo:
                for key in STAT_KEYS:
                    stats[key] += promotion_bonuses.get(key, 0)
                    # Clamp to phase2 cap after promotion bonus
                    if stats[key] > caps_phase2[key]:
                        stats[key] = caps_phase2[key]
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
                                if stats[key] < caps_phase2[key]:
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
