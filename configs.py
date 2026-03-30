# Coded by @SMDxTG - if Any Query Ask him Directly 

import os
from dotenv import load_dotenv

load_dotenv()  # Load from .env file

# Telegram
API_ID = int(os.getenv("API_ID", ""))
API_HASH = os.getenv("API_HASH", "")
USER_SESSION = os.getenv("USER_SESSION", "") # Use Pyrogram V2 String Session 
#if you don't have string Gen bot - use it my bot @SMD_StringBot

# Web
PORT = int(os.getenv("PORT", "8080")) 
URL = os.getenv("URL", "") # Heroku or Koyeb Or Render Base Url 

# MongoDB
DATABASE_URL = os.getenv("DATABASE_URL", "") #Mongodb Url 
DATABASE_NAME = os.getenv("DATABASE_NAME", "") # example Cluster0

# TamilMV settings
TMV_URL = os.getenv("TMV_URL", "https://www.1tamilmv.immo/")
TMV_TORRENT = int(os.getenv("TMV_TORRENT", "-1003807443810"))
TMV_LEECH_GRP = int(os.getenv("TMV_LEECH_GRP", "-1002744205359"))
TMV_MIRROR_GRP = int(os.getenv("TMV_MIRROR_GRP", "-1002744205359"))
TMV_TORRENT_THUMB = os.getenv("TMV_TORRENT_THUMB", "https://i.ibb.co/vCn6v8YD/photo-2026-03-30-09-22-38-7622976671569674256.jpg") #torrant Pic
BOT_TAG = os.getenv("BOT_TAG", "@ML_FILES") # File Prefix

# Internal
PING_INTERVAL = int(os.getenv("PING_INTERVAL", "120"))
SCRAPE_INTERVAL = int(os.getenv("SCRAPE_INTERVAL", "300"))  # 5 min
SIZE_LIMIT_GB = int(os.getenv("SIZE_LIMIT_GB", 50))  # Default: 50 GB
