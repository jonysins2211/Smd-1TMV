# Coded by @SMDxTG - if Any Query Ask him Directly 

import os
from dotenv import load_dotenv

load_dotenv()  # Load from .env file


def _get_int_env(name: str, default: int | None = None) -> int:
    """
    Safely parse integer env vars.
    Falls back to the provided default when var is empty/invalid.
    """
    raw = os.getenv(name)
    if raw is None or raw.strip() == "":
        if default is None:
            raise ValueError(f"Missing required integer environment variable: {name}")
        return default
    try:
        return int(raw)
    except ValueError:
        if default is None:
            raise ValueError(f"Invalid integer value for {name}: {raw!r}") from None
        return default

# Telegram
API_ID = _get_int_env("API_ID", 0)
API_HASH = os.getenv("API_HASH", "")
USER_SESSION = os.getenv("USER_SESSION", "") # Use Pyrogram V2 String Session 
#if you don't have string Gen bot - use it my bot @SMD_StringBot

# Web
PORT = _get_int_env("PORT", 8080)
URL = os.getenv("URL", "") # Heroku or Koyeb Or Render Base Url 

# MongoDB
DATABASE_URL = os.getenv("DATABASE_URL", "") #Mongodb Url 
DATABASE_NAME = os.getenv("DATABASE_NAME", "") # example Cluster0

# TamilMV settings
TMV_URL = os.getenv("TMV_URL", "https://www.1tamilmv.gripe/")
TMV_TORRENT = _get_int_env("TMV_TORRENT", -1003807443810)
TMV_LEECH_GRP = _get_int_env("TMV_LEECH_GRP", -1002744205359)
TMV_MIRROR_GRP = _get_int_env("TMV_MIRROR_GRP", -1003569007568)
TMV_TORRENT_THUMB = os.getenv("TMV_TORRENT_THUMB", "https://i.ibb.co/vCn6v8YD/photo-2026-03-30-09-22-38-7622976671569674256.jpg") #torrant Pic
BOT_TAG = os.getenv("BOT_TAG", "@ML_FILES") # File Prefix

# Internal
PING_INTERVAL = _get_int_env("PING_INTERVAL", 120)
SCRAPE_INTERVAL = _get_int_env("SCRAPE_INTERVAL", 300)  # 5 min
SIZE_LIMIT_GB = _get_int_env("SIZE_LIMIT_GB", 50)  # Default: 50 GB
