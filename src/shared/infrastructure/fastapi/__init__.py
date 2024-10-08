from pathlib import Path

from dotenv import load_dotenv

# Load environnement variables.
load_dotenv(
    dotenv_path=(Path(".env.dev") if Path(".env.dev").exists() else Path(".env"))
)
