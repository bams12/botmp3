import os
import subprocess
import tempfile
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Kirim link YouTube untuk saya ubah jadi MP3 🎵")

async def download_mp3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    if not url.startswith("http"):
        await update.message.reply_text("❌ Kirim link YouTube yang valid.")
        return

    await update.message.reply_text("⏳ Sedang download & convert ke MP3...")

    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = os.path.join(tmpdir, "audio.mp3")

        try:
            # yt-dlp fix SABR: force bestaudio dan non-DASH
            subprocess.run([
                "yt-dlp",
                "-f", "bestaudio",
                "--extract-audio",
                "--audio-format", "mp3",
                "--audio-quality", "0",
                "--no-playlist",
                "--downloader", "ffmpeg",
                "--geo-bypass",
                "--force-ipv4",
                "-o", output_path,
                url
            ], check=True)

            await update.message.reply_audio(audio=open(output_path, "rb"))

        except subprocess.CalledProcessError:
            await update.message.reply_text("❌ Gagal download. Coba link lain atau video lebih pendek.")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_mp3))

if __name__ == "__main__":
    app.run_polling()
