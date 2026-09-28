from pynput import keyboard, mouse
import time

# Activity counters for the current measurement window
key_count = 0
backspace_count = 0
mouse_clicks = 0
mouse_movements = 0

# Overall session start time
start_time = time.time()

# Start of the current measurement window
window_start_time = time.time()


def on_key_press(key):
    global key_count, backspace_count

    key_count += 1

    if key == keyboard.Key.backspace:
        backspace_count += 1


def on_click(x, y, button, pressed):
    global mouse_clicks

    if pressed:
        mouse_clicks += 1


def on_move(x, y):
    global mouse_movements

    mouse_movements += 1


keyboard_listener = keyboard.Listener(on_press=on_key_press)

mouse_listener = mouse.Listener(
    on_click=on_click,
    on_move=on_move
)

keyboard_listener.start()
mouse_listener.start()


def get_current_metrics():
    global key_count
    global backspace_count
    global mouse_clicks
    global mouse_movements
    global window_start_time

    current_time = time.time()

    window_minutes = (current_time - window_start_time) / 60

    if window_minutes > 0:
        wpm = (key_count / 5) / window_minutes
    else:
        wpm = 0

    correction_rate = (
        (backspace_count / key_count) * 100
        if key_count > 0
        else 0
    )

    work_minutes = (current_time - start_time) / 60

    metrics = {
        "wpm": wpm,
        "correction_rate": correction_rate,
        "mouse_clicks": mouse_clicks,
        "mouse_movements": mouse_movements,
        "work_minutes": work_minutes
    }

    # Reset the current measurement window
    key_count = 0
    backspace_count = 0
    mouse_clicks = 0
    mouse_movements = 0
    window_start_time = current_time

    return metrics


if __name__ == "__main__":
    print("WorkSync tracker started.")
    print("Tracking activity only — typed content is NOT stored.")
    print("Press Ctrl+C to stop.")

    try:
        while True:
            time.sleep(5)

            metrics = get_current_metrics()

            print(
                f"WPM: {metrics['wpm']:.1f} | "
                f"Corrections: {metrics['correction_rate']:.1f}% | "
                f"Mouse clicks: {metrics['mouse_clicks']} | "
                f"Mouse movements: {metrics['mouse_movements']} | "
                f"Work time: {metrics['work_minutes']:.1f} min"
            )

    except KeyboardInterrupt:
        keyboard_listener.stop()
        mouse_listener.stop()
        print("\nWorkSync tracker stopped.")