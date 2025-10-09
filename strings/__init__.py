import os
import yaml
from typing import Dict
from strings.init import LOGGER

languages: Dict[str, dict] = {}
languages_present: Dict[str, str] = {}


def get_string(lang: str):
    return languages.get(lang, languages["en"])


# Load all language files
for filename in os.listdir("./strings/langs/"):
    if filename.endswith(".yml"):
        language_name = filename[:-4]

        try:
            with open(f"./strings/langs/{filename}", encoding="utf8") as f:
                data = yaml.safe_load(f)

            if language_name == "en":
                languages["en"] = data
                languages_present["en"] = data.get("name", "English")
                continue

            # fallback merge with English
            merged = languages["en"].copy()
            merged.update(data)
            languages[language_name] = merged
            languages_present[language_name] = merged.get("name", language_name)

        except Exception as e:
            LOGGER.error(f"❌ Error loading language file {filename}: {e}")
            exit()

LOGGER.info(f"✅ Loaded {len(languages_present)} languages: {', '.join(languages_present.keys())}")