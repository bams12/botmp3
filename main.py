import os
import subprocess
from telegram.ext import Updater, CommandHandler
from telegram import ChatAction

BOT_TOKEN = os.getenv("BOT_TOKEN")
COOKIES_FILE = "cookies.json"

def start(update, context):
    update.message.reply_text("Kirim /mp3 <link YouTube> untuk download MP3.")

def download_mp3(update, context):
    if not context.args:
        update.message.reply_text("Contoh: /mp3 https://youtu.be/video_id")
        return

    url = context.args[0]
    update.message.chat.send_action(ChatAction.UPLOAD_DOCUMENT)

    try:
        update.message.reply_text("🎵 Sedang memproses...")

        cmd = [
            "yt-dlp",
            "--extract-audio",
            "--audio-format", "mp3",
            "--audio-quality", "320",
            "--embed-thumbnail",
            "--add-metadata",
            "--no-playlist",
            "--cookies", "COOKIES",
            url
        ]
        subprocess.run(cmd, check=True)

        for file in os.listdir():
            if file.endswith(".mp3"):
                update.message.reply_audio(audio=open(file, "rb"))
                os.remove(file)

    except Exception as e:
        update.message.reply_text(f"❌ Error: {e}")

if __name__ == "__main__":
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("mp3", download_mp3))
    updater.start_polling()
    updater.idle()
