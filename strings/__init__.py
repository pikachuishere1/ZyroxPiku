import os
import yaml
import logging
from typing import Dict

# ---------------- LOGGER SETUP ----------------
LOGGER = logging.getLogger("LanguageLoader")
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# ---------------- GLOBALS ----------------
languages: Dict[str, dict] = {}
languages_present: Dict[str, str] = {}


# ---------------- FUNCTIONS ----------------
def get_string(lang: str) -> dict:
    """
    Return language strings for the given code.
    Fallbacks to English if not available.
    """
    return languages.get(lang, languages.get("en", {}))


def load_languages() -> None:
    """
    Load all language .yml files from ./strings/langs/
    Merges each language with English as fallback.
    """
    base_path = "./strings/langs/"

    if not os.path.exists(base_path):
        os.makedirs(base_path)
        LOGGER.warning("⚠️  Created missing folder: ./strings/langs/")

    # Ensure English file exists
    en_path = os.path.join(base_path, "en.yml")
    if not os.path.exists(en_path):
        with open(en_path, "w", encoding="utf8") as f:
            f.write("name: English\nhello: 'Hello!'\nbye: 'Goodbye!'\n")
        LOGGER.info("🆕 Created default English language file (en.yml)")

    for filename in os.listdir(base_path):
        if not filename.endswith(".yml"):
            continue

        lang_code = filename[:-4]  # Remove ".yml"
        filepath = os.path.join(base_path, filename)

        try:
            with open(filepath, "r", encoding="utf8") as f:
                data = yaml.safe_load(f) or {}

            if lang_code == "en":
                languages["en"] = data
                languages_present["en"] = data.get("name", "English")
                continue

            # Merge with English fallback
            merged = {**languages["en"], **data}
            languages[lang_code] = merged
            languages_present[lang_code] = merged.get("name", lang_code)

        except Exception as e:
            LOGGER.error(f"❌ Error loading {filename}: {e}")
            return

    LOGGER.info(f"✅ Loaded {len(languages_present)} languages: {', '.join(languages_present.keys())}")


# ---------------- MAIN ----------------
if __name__ == "__main__":
    load_languages()

    # Example usage
    print(get_string("en").get("hello"))
    print(get_string("hi").get("hello", "Fallback to English"))