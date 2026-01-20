# topic_manager.py
import re
from pyrogram import filters
from pyrogram.types import Message

# In-memory cache (restart pe reset)
TOPIC_CACHE = {}

def ensure_cache(chat_id: int):
    if chat_id not in TOPIC_CACHE:
        TOPIC_CACHE[chat_id] = {}

def extract_from_link(text: str):
    if not text:
        return {"topic_id": None, "msg_id": None, "raw": ""}

    s = text.strip()

    # thread/topic/comment query param
    m = re.search(r"(?:\?|&)(?:thread|topic|comment)=(\d+)", s)
    topic_id = int(m.group(1)) if m else None

    # msg id from t.me/c/.../msgid
    msg_id = None
    m3 = re.search(r"t\.me/c/\d+/(\d+)", s)
    if m3:
        msg_id = int(m3.group(1))

    return {"topic_id": topic_id, "msg_id": msg_id, "raw": s}


def register_topic_commands(bot, db=None, OWNER_ID=None):
    """
    bot: your Pyrogram Client instance (aapke code me 'bot')
    db: optional (agar aap owner/admin check db se karna chahte ho)
    OWNER_ID: optional (single owner)
    """

    def is_owner(user_id: int) -> bool:
        # priority: db.is_admin (agar diya hai)
        if db is not None:
            try:
                return db.is_admin(user_id)
            except Exception:
                pass

        # fallback: OWNER_ID
        if OWNER_ID is None:
            return True
        return user_id == OWNER_ID


    @bot.on_message(filters.command("checkforum") & filters.private)
    async def checkforum_cmd(client, message: Message):
        if len(message.command) < 2:
            await message.reply_text("❌ Usage:\n/checkforum [chat_id]\nExample:\n/checkforum -1001234567890")
            return

        try:
            chat_id = int(message.command[1])
            chat = await client.get_chat(chat_id)
            is_forum = getattr(chat, "is_forum", False)

            await message.reply_text(
                f"✅ **Chat Details**\n"
                f"• Title: `{chat.title}`\n"
                f"• ID: `{chat.id}`\n"
                f"• Type: `{chat.type}`\n"
                f"• Username: `{('@' + chat.username) if chat.username else 'N/A'}`\n"
                f"• Forum Enabled: `{'YES' if is_forum else 'NO'}`\n"
                f"• Topic Support: `{'OK' if is_forum else 'NOT AVAILABLE'}`"
            )
        except Exception as e:
            await message.reply_text(f"❌ Error: `{e}`\n\nBot ko us chat me admin hona chahiye.")


    @bot.on_message(filters.command("testtopic") & filters.private)
    async def testtopic_cmd(client, message: Message):
        if len(message.command) < 3:
            await message.reply_text("❌ Usage:\n/testtopic [chat_id] [topic_id]\nExample:\n/testtopic -1001234567890 12")
            return

        try:
            chat_id = int(message.command[1])
            topic_id = int(message.command[2])

            sent = await client.send_message(
                chat_id=chat_id,
                text=f"✅ Topic Test Message\nTopic ID: {topic_id}",
                message_thread_id=topic_id
            )
            await message.reply_text(f"✅ Sent!\n• Chat: `{chat_id}`\n• Topic: `{topic_id}`\n• Msg ID: `{sent.id}`")
        except Exception as e:
            await message.reply_text(f"❌ Failed: `{e}`\n\nCheck:\n1) Forum enabled\n2) Bot admin\n3) Manage Topics permission")


    @bot.on_message(filters.command("testextract") & filters.private)
    async def testextract_cmd(client, message: Message):
        text = ""
        if len(message.command) >= 2:
            text = message.text.split(maxsplit=1)[1]
        elif message.reply_to_message:
            text = (message.reply_to_message.text or message.reply_to_message.caption or "")
        else:
            await message.reply_text("❌ Usage:\n/testextract <t.me link>\nOr reply message par /testextract")
            return

        info = extract_from_link(text)
        await message.reply_text(
            f"✅ **Extract Preview**\n"
            f"• Raw: `{info['raw'][:200]}`\n"
            f"• Topic/Thread ID: `{info['topic_id']}`\n"
            f"• Msg ID: `{info['msg_id']}`"
        )


    @bot.on_message(filters.command("createtopic") & filters.private)
    async def createtopic_cmd(client, message: Message):
        if len(message.command) < 3:
            await message.reply_text("❌ Usage:\n/createtopic [chat_id] [name]\nExample:\n/createtopic -1001234567890 Hematology")
            return

        try:
            chat_id = int(message.command[1])
            name = message.text.split(maxsplit=2)[2].strip()
            if not name:
                await message.reply_text("❌ Topic name empty hai.")
                return

            topic = await client.create_forum_topic(chat_id, name=name)
            topic_id = getattr(topic, "message_thread_id", None) or getattr(topic, "id", None)

            ensure_cache(chat_id)
            if topic_id:
                TOPIC_CACHE[chat_id][name] = int(topic_id)

            await message.reply_text(f"✅ Topic Created!\n• Chat: `{chat_id}`\n• Name: `{name}`\n• Topic ID: `{topic_id}`")
        except Exception as e:
            await message.reply_text(f"❌ Create failed: `{e}`\n\nCheck:\n1) Forum enabled\n2) Bot admin\n3) Manage Topics permission")


    @bot.on_message(filters.command("listtopics") & filters.private)
    async def listtopics_cmd(client, message: Message):
        chat_id = None
        if len(message.command) >= 2:
            try:
                chat_id = int(message.command[1])
            except Exception:
                await message.reply_text("❌ chat_id number me do.")
                return

        if not TOPIC_CACHE:
            await message.reply_text("ℹ️ Cache empty hai. /createtopic se add hoga.")
            return

        if chat_id is not None:
            topics = TOPIC_CACHE.get(chat_id, {})
            if not topics:
                await message.reply_text(f"ℹ️ `{chat_id}` ke liye cache empty hai.")
                return
            out = [f"✅ Topics in `{chat_id}`:"]
            for n, tid in topics.items():
                out.append(f"• `{tid}` — {n}")
            await message.reply_text("\n".join(out))
            return

        out = ["✅ Cached Topics (All Chats):"]
        for cid, topics in TOPIC_CACHE.items():
            out.append(f"\n**Chat:** `{cid}`")
            if not topics:
                out.append("• (empty)")
            else:
                for n, tid in topics.items():
                    out.append(f"• `{tid}` — {n}")
        await message.reply_text("\n".join(out))


    @bot.on_message(filters.command("cleartopics") & filters.private)
    async def cleartopics_cmd(client, message: Message):
        if not message.from_user or not is_owner(message.from_user.id):
            await message.reply_text("❌ Owner/Admin only.")
            return
        TOPIC_CACHE.clear()
        await message.reply_text("✅ Topic cache cleared.")
