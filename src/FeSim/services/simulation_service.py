import random


STAT_KEYS = ["hp", "str", "mag", "skl", "spd", "lck", "defense", "res"]
STAT_LABELS = ["HP", "STR", "MAG", "SKL", "SPD", "LCK", "DEF", "RES"]

# Poids
STAT_WEIGHTS = {
    "hp": 0.6,
    "str": 1.25,
    "mag": 1.25,
    "skl": 0.75,
    "spd": 1.50,
    "lck": 0.35,
    "defense": 1.25,
    "res": 1.00,
}

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
        start_level = character.get("level", 1)
        is_pre_promo = promotion_bonuses is not None

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

        # Accumulators for average
        accumulators = {key: [0.0] * total_cols for key in STAT_KEYS}

        # Track best and worst scenarios
        best_total = -1
        worst_total = float("inf")
        best_snapshot = None
        worst_snapshot = None

        # Accumulate final scores
        total_score_sum = 0

        # Définis si l'unité est une unité magique ou physique
        ismagic = character.get("mag", 0) >= character.get("str", 0)
        excluded_stat = "str" if ismagic else "mag"

        # diviseur pour calcul score
        total_weight = sum(
            STAT_WEIGHTS[key]
            for key in STAT_KEYS
            if key != excluded_stat
        )
        
        for _ in range(scenario_count):
            stats = {key: character[key] for key in STAT_KEYS}
            # Store full path for this scenario
            snapshot = {key: [0] * total_cols for key in STAT_KEYS}
            col = 0

            # Phase 1
            for lv in phase1_levels:
                for key in STAT_KEYS:
                    accumulators[key][col] += stats[key]
                    snapshot[key][col] = stats[key]
                col += 1
                if lv < TARGET_LEVEL:
                    for key in STAT_KEYS:
                        growth = character[f"{key}_growth"]
                        if stats[key] < caps_phase1[key]:
                            if random.randint(1, 100) <= growth:
                                stats[key] += 1

            # Promotion column
            if is_pre_promo:
                for key in STAT_KEYS:
                    stats[key] += promotion_bonuses.get(key, 0)
                    if stats[key] > caps_phase2[key]:
                        stats[key] = caps_phase2[key]
                    accumulators[key][col] += stats[key]
                    snapshot[key][col] = stats[key]
                col += 1

                # Phase 2
                for lv in phase2_levels:
                    for key in STAT_KEYS:
                        accumulators[key][col] += stats[key]
                        snapshot[key][col] = stats[key]
                    col += 1
                    if lv < TARGET_LEVEL:
                        for key in STAT_KEYS:
                            growth = character[f"{key}_growth"]
                            if stats[key] < caps_phase2[key]:
                                if random.randint(1, 100) <= growth:
                                    stats[key] += 1

            # définis le pire et meilleure scénario, pour une unité physique la mag est retiré du calcul
            # pour une unité magique la force est retiré du calcul
            final_col = total_cols - 1

            total = sum(
                snapshot[key][final_col] * STAT_WEIGHTS[key]
                for key in STAT_KEYS
                if key != excluded_stat
            )

            # calcule le score moyen de tous les scénarios
            total_score_sum += total
           
            if total > best_total:
                best_total = total
                best_snapshot = snapshot

            if total < worst_total:
                worst_total = total
                worst_snapshot = snapshot

        # Build average matrix
        avg_matrix = {}
        for key in STAT_KEYS:
            avg_matrix[key] = [round(v / scenario_count, 1) for v in accumulators[key]]

        # Build best/worst matrices (convert to float for consistency)
        best_matrix = {}
        worst_matrix = {}
        for key in STAT_KEYS:
            best_matrix[key] = [float(v) for v in best_snapshot[key]]
            worst_matrix[key] = [float(v) for v in worst_snapshot[key]]

        # Scores finaux
        score_average = total_score_sum / scenario_count / total_weight
        score_best = best_total / total_weight
        score_worst = worst_total / total_weight

        return {
            "columns": columns,
            "avg_matrix": avg_matrix,
            "best_matrix": best_matrix,
            "worst_matrix": worst_matrix,
            "score_average": score_average,
            "score_best": score_best,
            "score_worst": score_worst,
            "start_level": start_level,
            "target_level": TARGET_LEVEL,
            "scenario_count": scenario_count,
            "character_name": character.get("name", "Inconnu"),
            "is_pre_promo": is_pre_promo,
        }
