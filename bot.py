import os
import telebot
from telebot import types

# Load the bot token from Railway environment variables
TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# Configuration for your business
WALLET_ADDRESS = "0xf33b6991a8aaf23575b1162a04df19fdfd2d244"
WEBSITE_LINK = "https://sites.google.com/view/berlin-fast-logistics-moving"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "Welcome to Berlin Logistics Bot! 🚀\n\n"
        "To access our professional templates and digital services platform, please transfer the required amount to our official wallet address below:\n\n"
        f"💳 **Wallet Address:**\n`{WALLET_ADDRESS}`\n\n"
        "After completing the payment, please reply here with your **Transaction Hash (TXID)** or sender wallet address so we can verify and unlock your access instantly."
    )
    bot.reply_to(message, welcome_text, parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def verify_payment(message):
    user_input = message.text.strip()
    
    # Check if the user sent a transaction hash or wallet address (length > 10)
    if len(user_input) > 10:
        success_response = (
            "✅ **Payment Reference Received!**\n\n"
            "We have received your transaction details. Here is your access link to our templates platform:\n\n"
            f"🔗 {WEBSITE_LINK}\n\n"
            "Thank you for doing business with Berlin Logistics!"
        )
        bot.reply_to(message, success_response, parse_mode="Markdown")
    else:
        bot.reply_to(message, "⚠️ Please provide a valid Transaction ID (TXID) or wallet address to proceed.")

print("Bot is up and running...")
bot.infinity_polling()
