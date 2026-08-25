import os
import telebot

# Retrieve the token securely from Railway's environment variables
TOKEN = os.environ.get('BOT_TOKEN')

if not TOKEN:
    print("Error: BOT_TOKEN environment variable not found!")
    exit(1)

bot = telebot.TeleBot(TOKEN)

# Handle the /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to Berlin Logistics Bot! 🚀\nThe bot is up and running successfully.")

# Handle any other text message sent by the user
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    bot.reply_to(message, f"Hello! I have received your message: {message.text}")

print("Bot is up and running...")
bot.infinity_polling()
