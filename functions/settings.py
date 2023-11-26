import json

DEBUG_MODE = False


def load_settings():
    global DEBUG_MODE

    try:
        with open("settings.json", "r") as settings_file:
            settings = json.load(settings_file)
            DEBUG_MODE = settings.get("debug", False)
    except FileNotFoundError:
        print("Settings file not found. Using default values.")


load_settings()
