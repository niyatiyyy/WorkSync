from flask import Flask, jsonify, render_template,session
import tracker
import detector
import database
from datetime import datetime
import time


app = Flask(__name__)
app.secret_key = "worksync-secret-key"


# Create database when WorkSync starts
database.create_database()
last_metric_sample_time = 0
cached_metrics = None


@app.route("/")
def home():
    return render_template("dashboard.html")


@app.route("/break")
def break_page():
    current = tracker.get_current_metrics()

    session["before_wpm"] = round(current["wpm"], 1)
    session["before_correction"] = round(current["correction_rate"], 1)

    return render_template("break.html")
@app.route("/recovery")
def recovery_page():

    before_wpm = session.get("before_wpm", 0)
    before_correction = session.get("before_correction", 0)

    current = tracker.get_current_metrics()

    baseline = database.get_baseline()

    if baseline is None:
        baseline_wpm = 0
    else:
        baseline_wpm = round(baseline["wpm"], 1)

    return render_template(
        "recovery.html",
        before_wpm=before_wpm,
        after_wpm=round(current["wpm"], 1),
        baseline_wpm=baseline_wpm
    )
@app.route("/history")
def history_page():

    history = database.get_activity_history(50)

    if history:
        avg_wpm = sum(item["wpm"] for item in history) / len(history)

        avg_correction = (
            sum(item["correction_rate"] for item in history)
            / len(history)
        )

    else:
        avg_wpm = 0
        avg_correction = 0

    peak_fatigue = 0

    return render_template(
        "history.html",
        history=history,
        avg_wpm=round(avg_wpm, 1),
        avg_correction=round(avg_correction, 1),
        peak_fatigue=peak_fatigue
    )
@app.route("/api/metrics")
def metrics():
    global last_metric_sample_time
    global cached_metrics

    current_time = time.time()

    # Only collect a new activity sample every 5 seconds.
    if cached_metrics is not None and current_time - last_metric_sample_time < 5:
        return jsonify(cached_metrics)

    current = tracker.get_current_metrics()
    timestamp = datetime.now().isoformat()

    database.save_activity(
        timestamp,
        current["wpm"],
        current["correction_rate"],
        current["mouse_clicks"],
        current["mouse_movements"],
        current["work_minutes"]
    )

    last_metric_sample_time = current_time

    sample_count = database.get_activity_count()

    if sample_count < 12:
        cached_metrics = {
            "wpm": round(current["wpm"], 1),
            "correction_rate": round(current["correction_rate"], 1),
            "mouse_clicks": current["mouse_clicks"],
            "mouse_movements": current["mouse_movements"],
            "work_minutes": round(current["work_minutes"], 1),
            "fatigue_score": 0,
            "fatigue_level": "Calibrating",
            "baseline_ready": False,
            "samples": sample_count,
            "samples_needed": 12
        }

        return jsonify(cached_metrics)

    baseline = database.get_baseline()

    if baseline is None:
        baseline = database.create_baseline()

    recent_samples = database.get_recent_activity(3)

    score = detector.calculate_fatigue_score(
        current,
        {
            "wpm": baseline["wpm"],
            "correction_rate": baseline["correction_rate"],
            "mouse_movements": baseline["mouse_movements"],
            "work_minutes": 20
        },
        recent_samples
    )

    level = detector.get_fatigue_level(score)

    cached_metrics = {
        "wpm": round(current["wpm"], 1),
        "correction_rate": round(current["correction_rate"], 1),
        "mouse_clicks": current["mouse_clicks"],
        "mouse_movements": current["mouse_movements"],
        "work_minutes": round(current["work_minutes"], 1),
        "fatigue_score": score,
        "fatigue_level": level,
        "baseline_ready": True,
        "samples": sample_count,
        "samples_needed": 12,
        "baseline_wpm": round(baseline["wpm"], 1),
        "baseline_correction_rate": round(baseline["correction_rate"], 1),
        "baseline_mouse_movements": round(baseline["mouse_movements"], 1)
    }

    return jsonify(cached_metrics)

if __name__ == "__main__":
    app.run(debug=True)
