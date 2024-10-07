import os.path
from pathlib import Path
from dotenv import load_dotenv  # Import dotenv to load environment variables
from split_settings.tools import include, optional  # type: ignore

# Load environment variables from .env file
load_dotenv()  # Ensure this is at the top

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

# namespacing our custom environment variables
ENVAR_SETTINGS_PREFIX = 'CORESETTINGS_'

ENV_SETTINGS_PATH = os.getenv(f'{ENVAR_SETTINGS_PREFIX}Local_SETTINGS_PATH')
LOCAL_SETTINGS_PATH = f'{BASE_DIR}{ENV_SETTINGS_PATH}' if ENV_SETTINGS_PATH else None

if not LOCAL_SETTINGS_PATH:
    LOCAL_SETTINGS_PATH = 'local/settings.dev.py'

if not os.path.isabs(LOCAL_SETTINGS_PATH):
    LOCAL_SETTINGS_PATH = str(BASE_DIR / LOCAL_SETTINGS_PATH)

include(
    'base.py',
    'logging.py',
    'custom.py',
    optional(LOCAL_SETTINGS_PATH),
    'envars.py',
)
