def calculate_fatigue_score(current, baseline, recent_samples=None):
    score = 0

    # -----------------------------
    # 1. Sustained WPM decline
    # -----------------------------

    if baseline["wpm"] > 0 and recent_samples:
        slow_samples = 0

        for sample in recent_samples:
            wpm_change = (
                (baseline["wpm"] - sample["wpm"])
                / baseline["wpm"]
            ) * 100

            if wpm_change > 10:
                slow_samples += 1

        # Require repeated deviation instead of one slow sample
        if slow_samples >= 3:
            score += 30
        elif slow_samples >= 2:
            score += 15

    # -----------------------------
    # 2. Increased correction rate
    # -----------------------------

    if current["correction_rate"] > baseline["correction_rate"] * 1.5:
        score += 20

    elif current["correction_rate"] > baseline["correction_rate"] * 1.2:
        score += 10

    # -----------------------------
    # 3. Reduced mouse activity
    # -----------------------------

    if baseline["mouse_movements"] > 0:

        activity_change = (
            (baseline["mouse_movements"] - current["mouse_movements"])
            / baseline["mouse_movements"]
        ) * 100

        if activity_change > 30:
            score += 20

        elif activity_change > 15:
            score += 10

    # -----------------------------
    # 4. Long continuous work
    # -----------------------------

    if current["work_minutes"] > 60:
        score += 30

    elif current["work_minutes"] > 45:
        score += 20

    elif current["work_minutes"] > 30:
        score += 10

    return min(score, 100)


def get_fatigue_level(score):

    if score < 30:
        return "Normal"

    elif score < 60:
        return "Mild"

    elif score < 80:
        return "Elevated"

    else:
        return "High"