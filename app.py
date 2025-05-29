import os
from flask import Flask, request, render_template
import telebot

TOKEN = os.environ.get("7404159709:AAH5cMs5CmUzGxgStCdCisqSpLk45eFBlyw")
CHANNEL_USERNAME = '@StreamyFlixHD'

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
    bot.reply_to(message, f"✅ Uploaded!\n📺 [Watch Online]({stream_link})", parse_mode="Markdown")

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

if __name__ == "__main__":
    bot.polling(non_stop=True)