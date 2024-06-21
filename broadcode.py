import telebot # pip install pyTelegramBotAPI
import os
import json

TOKEN = "6816768229:AAGD_PIHTFYuHFrYRuAGJ1DnweFUCyRKh4w" # replace with your bot token
CHANNEL_ID = "-1002114707908" # replace with your channel ID
bot = telebot.TeleBot(TOKEN)

# Load existing bot users from file
try:
    with open('bot_users.json', 'r') as file:
        bot_users = json.load(file)
except FileNotFoundError:
    bot_users = {}

@bot.message_handler(commands=['start', 'join'])
def join(message):
    if message.from_user.id not in bot_users:
        bot_users[message.from_user.id] = message.from_user.username
        bot.send_message(message.chat.id, "Hello, it.")
        # Save the new user to the file
        with open('bot_users.json', 'w') as file:
            json.dump(bot_users, file)
    else:
        bot.send_message(message.chat.id, "You are already a bot user.")

@bot.message_handler(content_types=['document', 'photo', 'audio', 'video', 'animation'])
def handle_files(message):
    if message.from_user.id in bot_users:
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
    else:
        bot.send_message(message.chat.id, "Please use the /join command to join the bot.")

@bot.message_handler(commands=['broadcast'])
def broadcast(message):
    if message.from_user.id == 6897230899:
        for user_id in bot_users:
            if user_id != message.from_user.id:
                if message.reply_to_message:
                    if message.reply_to_message.content_type == 'document':
                        bot.send_document(user_id, message.reply_to_message.document.file_id)
                    elif message.reply_to_message.content_type == 'photo':
                        bot.send_photo(user_id, message.reply_to_message.photo[-1].file_id)
                    elif message.reply_to_message.content_type == 'audio':
                        bot.send_audio(user_id, message.reply_to_message.audio.file_id)
                    elif message.reply_to_message.content_type == 'video':
                        bot.send_video(user_id, message.reply_to_message.video.file_id)
                    elif message.reply_to_message.content_type == 'animation':
                        bot.send_animation(user_id, message.reply_to_message.animation.file_id)
                    else:
                        bot.send_message(user_id, message.reply_to_message.text)
                else:
                    bot.send_message(user_id, "No message to broadcast.")
    else:
        bot.send_message(message.chat.id, "You are not authorized to use the /broadcast command.")

bot.polling()
