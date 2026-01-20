import os
from os import environ

# ─────────── Utility ───────────
def _to_int(value, default=0):
    try:
        return int(str(value).strip())
    except Exception:
        return default

# ─────────── API Configuration ───────────
API_ID = _to_int(environ.get("API_ID", "21113148"))
API_HASH = environ.get("API_HASH", "908feafcf7973178ac490b8c35c087d9")
BOT_TOKEN = environ.get("BOT_TOKEN", "7999635672:AAFZsPzCrdvO1JFxcgbSjoAtnf7D-iMYqBs")

CREDIT = environ.get("CREDIT", "KITTU")

# ─────────── Database Configuration ───────────
DATABASE_NAME = environ.get("DATABASE_NAME", "KITTU")
DATABASE_URL = environ.get(
    "DATABASE_URL",
    "mongodb+srv://USER:PASS@cluster0.mongodb.net/?retryWrites=true&w=majority"
)
MONGO_URL = DATABASE_URL

# ─────────── Owner / Admin ───────────
OWNER_ID = _to_int(environ.get("OWNER_ID", "6658266490"))
ADMINS = [
    _to_int(x) for x in environ.get("ADMINS", str(OWNER_ID)).split()
]

# ─────────── Upload Target (IMPORTANT) ───────────
# Group / Channel jahan files upload hongi
UPLOAD_CHAT_ID = _to_int(environ.get("UPLOAD_CHAT_ID", "0"))  
# Example: -1001234567890

# Forum Topic ID (optional)
# Agar 0 ya blank hoga → normal group upload (no error)
TOPIC_ID = _to_int(environ.get("TOPIC_ID", "0"))  
# Example: 12

# ─────────── Channels / Links ───────────
PREMIUM_CHANNEL = environ.get(
    "PREMIUM_CHANNEL",
    "https://t.me/your_channel"
)

# ─────────── Thumbnail Configuration ───────────
THUMBNAILS = list(
    map(
        str,
        environ.get(
            "THUMBNAILS",
            "https://files.catbox.moe/fh731v.jpg"
        ).split()
    )
)

# ─────────── Web Server ───────────
WEB_SERVER = environ.get("WEB_SERVER", "False").lower() == "true"
WEBHOOK = True
PORT = _to_int(environ.get("PORT", "8000"), 8000)

# ─────────── Auth / System Messages ───────────
AUTH_MESSAGES = {
    "subscription_active": """<b>🎉 Subscription Activated!</b>

<blockquote>
Your subscription is active till {expiry_date}.
You can now use the bot!
</blockquote>

Type /start to begin.
""",

    "subscription_expired": """<b>⚠️ Subscription Expired</b>

<blockquote>
Your access has ended.
Please contact admin to renew.
</blockquote>
""",

    "user_added": """<b>✅ User Added!</b>

<blockquote>
👤 Name: {name}
🆔 ID: {user_id}
📅 Expiry: {expiry_date}
</blockquote>
""",

    "user_removed": """<b>✅ User Removed</b>

<blockquote>User ID {user_id} removed.</blockquote>
""",

    "access_denied": """<b>⛔ Access Denied</b>

<blockquote>
You are not authorized.
Contact admin for access.
</blockquote>
""",

    "not_admin": "⚠️ You are not allowed to use this command.",

    "invalid_format": """❌ <b>Invalid Format</b>

<blockquote>
Expected: {format}
</blockquote>
"""
}

