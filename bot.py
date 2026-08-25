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
        "To access our templates platform, please transfer the required amount to our official wallet address below:\n\n"
        f"💳 **Wallet Address:**\n`{WALLET_ADDRESS}`\n\n"
        "After completing the payment, please reply here with your **Transaction Hash (TXID)**."
    )
    bot.reply_to(message, welcome_text, parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def handle_payment_proof(message):
    user_input = message.text.strip()
    
    # Check if the user sent a valid transaction reference length
    if len(user_input) > 10:
        # Professional pending verification message in English
        pending_response = (
            "⏳ **Verification in Progress**\n\n"
            "We will verify your payment. Please send the transaction ID to confirm your payment, and if the payment matches, we will send you the website link."
        )
        bot.reply_to(message, pending_response, parse_mode="Markdown")
        
        # Note for future automation: Here is where the system can later trigger 
        # the automatic verification or email notification matching.
    else:
        bot.reply_to(message, "⚠️ Please provide a valid Transaction ID (TXID) to proceed.")

print("Bot is up and running...")
bot.infinity_polling()

