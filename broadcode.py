import telebot
import os
import json

TOKEN = "6816768229:AAGD_PIHTFYuHFrYRuAGJ1DnweFUCyRKh4w"  # replace with your bot token
CHANNEL_ID = "-1002114707908"  # replace with your channel ID
AUTHORIZED_USER_ID = 6897230899  # replace with the authorized user's ID
bot = telebot.TeleBot(TOKEN)

# Load existing bot users from file
try:
    with open('bot_users.json', 'r') as file:
        bot_users = json.load(file)
except (FileNotFoundError, json.JSONDecodeError):
    bot_users = {}

@bot.message_handler(commands=['start', 'join'])
def join(message):
    try:
        if message.from_user.id not in bot_users:
            username = message.from_user.username if message.from_user.username else f"User {message.from_user.id}"
            bot_users[message.from_user.id] = username
            bot.send_message(message.chat.id, "Hello, I'm a file sharing bot. Send me any file and I'll provide a direct download link to it.")
            # Save the new user to the file
            with open('bot_users.json', 'w') as file:
                json.dump(bot_users, file)
        else:
            bot.send_message(message.chat.id, "You are already a bot user.")
    except Exception as e:
        print(f"Error in join command: {e}")

@bot.message_handler(content_types=['document', 'photo', 'audio', 'video', 'animation'])
def handle_files(message):
    try:
        if message.from_user.id in bot_users:
            if message.content_type == 'document':
                file_id = message.document.file_id
                file_name = message.document.file_name
            elif message.content_type == 'photo':
                file_id = message.photo[-1].file_id
                file_name = f"{message.photo[-1].file_id}.jpg"
            elif message.content_type == 'audio':
                file_id = message.audio.file_id
                file_name = message.audio.file_name
            elif message.content_type == 'video':
                file_id = message.video.file_id
                file_name = f"{message.video.file_id}.mp4"
            elif message.content_type == 'animation':
                file_id = message.animation.file_id
                file_name = f"{message.animation.file_id}.gif"

            file_info = bot.get_file(file_id)
            file_path = file_info.file_path
            file_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_path}"

            # Forward the document to the channel
            bot.forward_message(CHANNEL_ID, message.chat.id, message.message_id)

            bot.send_message(message.chat.id, f"Here is your file link: {file_url}")
            bot.send_message(message.chat.id, f"File name: {file_name}")
        else:
            bot.send_message(message.chat.id, "Please use the /join command to join the bot.")
    except Exception as e:
        print(f"Error in handle_files: {e}")

@bot.message_handler(commands=['broadcast'])
def broadcast(message):
    try:
        if message.from_user.id == AUTHORIZED_USER_ID:
            for user_id, username in bot_users.items():
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
    except Exception as e:
        print(f"Error in broadcast: {e}")

@bot.message_handler(commands=['get_users'])
def get_users(message):
    try:
        if message.from_user.id == AUTHORIZED_USER_ID:
            user_list = ""
            for user_id, username in bot_users.items():
                user_list += f"UserID: {user_id}, Username: @{username}\n"
            bot.send_message(message.chat.id, f"List of bot users:\n\n{user_list}")
        else:
            bot.send_message(message.chat.id, "You are not authorized to use the /get_users command.")
    except Exception as e:
        print(f"Error in get_users: {e}")

@bot.message_handler(commands=['load_users'])
def load_users(message):
    try:
        if message.from_user.id == AUTHORIZED_USER_ID:
            if message.reply_to_message:
                user_list = message.reply_to_message.text.split('\n')
                if user_list and user_list[0].startswith("List of bot users:"):
                    for user_info in user_list[1:]:
                        user_info_parts = user_info.split(', ')
                        if len(user_info_parts) == 2:
                            user_id = int(user_info_parts[0].split(': ')[1])
                            username = user_info_parts[1].split(': ')[1][1:]
                            bot_users[user_id] = username
                    with open('bot_users.json', 'w') as file:
                        json.dump(bot_users, file)
                    bot.send_message(message.chat.id, "Bot users updated successfully.")
                else:
                    bot.send_message(message.chat.id, "Invalid user list format.")
            else:
                bot.send_message(message.chat.id, "Please reply to a message containing the user list.")
        else:
            bot.send_message(message.chat.id, "You are not authorized to use the /load_users command.")
    except Exception as e:
        print(f"Error in load_users: {e}")

try:
    bot.polling()
except Exception as e:
    print(f"Error in bot polling: {e}")
