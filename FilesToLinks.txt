import telebot # pip install pyTelegramBotAPI
import os

TOKEN = "6816768229:AAGD_PIHTFYuHFrYRuAGJ1DnweFUCyRKh4w" # replace with your bot token
CHANNEL_ID = "-1002114707908" # replace with your channel ID
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Hello, I'm a file sharing bot. You can send me any file and I will give you a link to download it.")

@bot.message_handler(content_types=['document', 'photo', 'audio', 'video', 'animation'])
def handle_files(message):
    if message.content_type == 'document':
        file_id = message.document.file_id
    elif message.content_type == 'photo':
        file_id = message.photo[-1].file_id  # get the highest resolution photo
    elif message.content_type == 'audio':
        file_id = message.audio.file_id
    elif message.content_type == 'video':
        file_id = message.video.file_id
    elif message.content_type == 'animation':
        file_id = message.animation.file_id

    file_info = bot.get_file(file_id)
    file_path = file_info.file_path
    file_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_path}"

    # Forward the document to the channel
    bot.forward_message(CHANNEL_ID, message.chat.id, message.message_id)

    bot.send_message(message.chat.id, f"Here is your file link: {file_url}")

bot.polling()
