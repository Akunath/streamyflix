import os
from flask import Flask, request, render_template
import telebot
from dotenv import load_dotenv
from threading import Thread

load_dotenv()

TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_USERNAME = "@StreamyFlixHD"

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

video_links = {}

@bot.message_handler(content_types=['video'])
def handle_video(message):
    sent = bot.forward_message(CHANNEL_USERNAME, message.chat.id, message.message_id)
    file_id = sent.video.file_id
    msg_id = sent.message_id
    public_link = f"https://t.me/{CHANNEL_USERNAME[1:]}/{msg_id}"
    stream_link = f"https://streamyflix.onrender.com/watch/{msg_id}"
    video_links[msg_id] = file_id
    bot.reply_to(message, f"✅ Uploaded!\n\n[Watch Online]({stream_link})", parse_mode="Markdown")

@app.route("/watch/<int:msg_id>")
def stream_video(msg_id):
    file_id = video_links.get(msg_id)
    if not file_id:
        return "Video not found"
    file_info = bot.get_file(file_id)
    video_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_info.file_path}"
    return render_template("player.html", video_url=video_url)

@app.route("/")
def index():
    return "✅ StreamyFlix bot is running!"

def run_bot():
    bot.polling(non_stop=True)

if __name__ == "__main__":
    Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
