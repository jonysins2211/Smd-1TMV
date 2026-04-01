import os
import re
import random
import asyncio
import requests
import cloudscraper
from pyrogram import Client
from bs4 import BeautifulSoup
from urllib.parse import unquote, urljoin
from database import tmv_collection, add_tmv 
from configs import TMV_URL, BOT_TAG, TMV_TORRENT, TMV_LEECH_GRP, TMV_MIRROR_GRP, TMV_TORRENT_THUMB, SIZE_LIMIT_GB

# ================= Thumbnail Setup =================
tmvthumb_path = "/tmp/tmv_torrent_thumb.jpg"
if not os.path.exists(tmvthumb_path):
    try:
        resp = requests.get(TMV_TORRENT_THUMB, timeout=15)
        if resp.status_code == 200:
            with open(tmvthumb_path, "wb") as f:
                f.write(resp.content)
    except:
        tmvthumb_path = None

# ================= Utilities =================
def clean_filename(name: str) -> str:
    name = unquote(name.strip())
    name = re.sub(r'^\s*(www\.[^-\s]+[\s-]*)+', '', name, flags=re.I)
    name = re.sub(r'^\s*(\S*TamilMV\S*[\s-]*)+', '', name, flags=re.I)
    name = re.sub(r'[\\/*?:"<>|]', "_", name)
    if not name.lower().endswith(".torrent"): name += ".torrent"
    return f"{BOT_TAG} - {name}" if not name.startswith(BOT_TAG) else name

def fix_url(href: str) -> str:
    return href if href.startswith("http") else urljoin(TMV_URL, href)

def categorize_content(title: str) -> str:
    """Detects if it's a Movie or Web Series based on title."""
    t = title.lower()
    series_patterns = [r's\d{1,2}', r'ep\s?\d+', r'episode', r'season', r'complete', r'hdrip']
    
    if any(re.search(p, t) for p in series_patterns) or "web series" in t or "tv show" in t:
        return "Series"
    if "dubbed" in t or "tam+" in t or "multi" in t:
        return "Dubbed"
    return "Movies"

def download_file(scraper, url: str, filename: str) -> bool:
    try:
        response = scraper.get(url, stream=True, timeout=60)
        if response.status_code == 200:
            with open(filename, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            return os.path.getsize(filename) > 0
    except: return False

# ================= Telegram Upload =================
async def send_torrent(user: Client, file_path, category, file_name, file_url, magnet, size_mb=0):
    clean_name = os.path.basename(file_path)
    caption = f"<b>{clean_name}\n\n#{category} #TamilMV\n\nPowered By ✨ {BOT_TAG}</b>"

    async def safe_send(chat_id, reply_cmd=None):
        try:
            msg = await user.send_document(
                chat_id=chat_id,
                document=file_path,
                caption=caption,
                thumb=tmvthumb_path if tmvthumb_path and os.path.exists(tmvthumb_path) else None,
            )
            if reply_cmd:
                await user.send_message(chat_id=chat_id, text=reply_cmd, reply_to_message_id=msg.id)
        except Exception as e:
            print(f"⚠️ Send failed: {e}")

    await safe_send(TMV_TORRENT)
    await safe_send(TMV_LEECH_GRP, reply_cmd="/qbleech")
    await safe_send(TMV_MIRROR_GRP, reply_cmd="/qbmirror")
    # FIX 1: Pass category to add_tmv so it saves correctly
    await add_tmv(file_name, file_url, magnet, size_mb, category)

# ================= TamilMV Scraper =================
async def tmv_scraper(user: Client):
    scraper = cloudscraper.create_scraper()
    print("🔍 Scraping TamilMV...")

    try:
        resp = scraper.get(TMV_URL, timeout=30)
        soup = BeautifulSoup(resp.text, "html.parser")
        # FIX 2: Reduced from [:40] to [:15] — grabs only newest topics, avoids re-scraping old ones
        topics = [fix_url(a["href"]) for a in soup.find_all("a", href=True) if "topic" in a["href"]][:15]
        
        for topic_url in topics:
            await asyncio.sleep(random.uniform(2, 4))
            try:
                topic_html = scraper.get(topic_url, timeout=30).text
                topic_soup = BeautifulSoup(topic_html, "html.parser")
                posts = topic_soup.find_all("div", class_="cPost_contentWrap")
                
                for post in posts:
                    for a in post.find_all("a", href=True):
                        link_text = a.get_text(strip=True)
                        if "torrent" not in link_text.lower():
                            continue
                            
                        href = fix_url(a["href"])
                        if await tmv_collection.find_one({"file_url": href}):
                            continue

                        size_mb = 0
                        for sib in a.find_all_next(string=True, limit=6):
                            match = re.search(r"(\d+(\.\d+)?)\s*(gb|mb)", str(sib), re.I)
                            if match:
                                val = float(match.group(1))
                                unit = match.group(3).lower()
                                size_mb = val * 1024 if unit == "gb" else val
                                break

                        if SIZE_LIMIT_GB and size_mb > (SIZE_LIMIT_GB * 1024):
                            continue

                        category = categorize_content(link_text)
                        filename = clean_filename(link_text)
                        if await asyncio.to_thread(download_file, scraper, href, filename):
                            print(f"✅ [{category}] Found: {link_text}")
                            await send_torrent(user, filename, category, link_text, href, href, size_mb)
                            if os.path.exists(filename): os.remove(filename)

            except: continue
    except Exception as e:
        print(f"🛑 Error: {e}")

