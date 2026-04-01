import asyncio, threading, time, requests
from aiohttp import web
from pyrogram import Client, idle
from configs import API_ID, API_HASH, USER_SESSION, PORT, URL, SCRAPE_INTERVAL, PING_INTERVAL
from tamilmv import tmv_scraper
from database import init_db

User = Client("User", api_id=API_ID, api_hash=API_HASH, session_string=USER_SESSION)

# ---------- Keep-alive Ping ----------
def ping_loop():
    while True:
        try:
            r = requests.get(URL, timeout=30)
            print("🍁 Ping successful" if r.status_code == 200 else f"👹 Ping failed: {r.status_code}")
        except Exception as e:
            print(f"❌ Ping exception: {e}")
        time.sleep(PING_INTERVAL)

threading.Thread(target=ping_loop, daemon=True).start()

# ---------- TamilMV Scraper Loop ----------
async def main_loop():
    while True:
        print("🌀 Starting TamilMV scraping...")
        await tmv_scraper(User)
        await asyncio.sleep(SCRAPE_INTERVAL)

# ---------- Web server ----------
routes = web.RouteTableDef()

@routes.get("/", allow_head=True)
async def root(request):
    return web.json_response("TamilMV RSS running ✅")

async def start_server():
    app = web.Application(client_max_size=30_000_000)
    app.add_routes(routes)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()

# ---------- Startup ----------
async def start_bot():
    await User.start()
    user = await User.get_me()
    print(f"✅ User logged in: @{user.username}")
    # FIX 3: Init DB index on startup
    await init_db()
    asyncio.create_task(main_loop())
    await start_server()
    await idle()
    await User.stop()

if __name__ == "__main__":
    try:
        asyncio.get_event_loop().run_until_complete(start_bot())
    except KeyboardInterrupt:
        print("🛑 Bot stopped manually.")
