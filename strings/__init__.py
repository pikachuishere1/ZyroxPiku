import os
import logging
import sys
from typing import List
import yaml

# ─────────── LOGGER SETUP ─────────── #
LOGGER = logging.getLogger("TEAMZYRO")
LOGGER.setLevel(logging.INFO)

class ColorFormatter(logging.Formatter):
    COLORS = {
        "DEBUG": "\033[94m",
        "INFO": "\033[92m",
        "WARNING": "\033[93m",
        "ERROR": "\033[91m",
        "CRITICAL": "\033[95m",
    }
    RESET = "\033[0m"

    def format(self, record):
        log_color = self.COLORS.get(record.levelname, self.RESET)
        log_fmt = f"%(asctime)s | {log_color}%(levelname)s{self.RESET} | %(message)s"
        formatter = logging.Formatter(log_fmt, "%H:%M:%S")
        return formatter.format(record)

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(ColorFormatter())
if not LOGGER.handlers:
    LOGGER.addHandler(handler)
LOGGER.propagate = False

# ─────────── LANGUAGE LOADER ─────────── #
languages = {}
languages_present = {}

def get_string(lang: str):
    return languages[lang]

for filename in os.listdir(r"./strings/langs/"):
    if "en" not in languages:
        languages["en"] = yaml.safe_load(
            open(r"./strings/langs/en.yml", encoding="utf8")
        )
        languages_present["en"] = languages["en"]["name"]
    if filename.endswith(".yml"):
        language_name = filename[:-4]
        if language_name == "en":
            continue
        languages[language_name] = yaml.safe_load(
            open(r"./strings/langs/" + filename, encoding="utf8")
        )
        for item in languages["en"]:
            if item not in languages[language_name]:
                languages[language_name][item] = languages["en"][item]
    try:
        languages_present[language_name] = languages[language_name]["name"]
    except Exception as e:
        LOGGER.error(f"There is some issue with the language file: {e}")
        exit()
