import os
import requests
import telebot
from telebot import types

TOKEN = '7543204938:AAF2aFj-53vR88J61z-oK7xQ_Hj'
bot = telebot.TeleBot(TOKEN)

WALLET_ADDRESS = '0xf33b6991a8aaf23575b1162a04df19fdfd2d244'
TEMPLATE_LINK = 'https://drive.google.com/drive/folders/YOUR_TEMPLATE_LINK_HERE'

USED_TXIDS = set()

def verify_bep20_transaction(txid):
    try:
        url = f"https://api.bscscan.com/api?module=proxy&action=eth_getTransactionByHash&txhash={txid}"
        response = requests.get(url, timeout=10).json()
        
        tx_data = response.get('result')
        if not tx_data:
            return False, "Transaction not found or invalid."

        to_address = tx_data.get('to')
        if not to_address or to_address.lower() != WALLET_ADDRESS.lower():
            return False, "This transaction was not sent to your specified wallet address!"
        
        return True, "Verified successfully"
    except Exception as e:
        return False, f"Network connection error: {str(e)}"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    btn_buy = types.InlineKeyboardButton("💳 Buy Berlin Fast Logistics Template (25 USDT)", callback_data='buy_template')
    markup.add(btn_buy)
    
    welcome_text = (
        "Welcome to the automated logistics and transport template sales bot! 🚚\n\n"
        "To get your website template (Berlin Fast Logistics) instantly and automatically:\n"
        "1. Transfer 25 USDT (BEP20 network) to the wallet address displayed on the website.\n"
        "2. Click the purchase button below and send your Transaction ID (TxID)."
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'buy_template')
def ask_for_txid(call):
    msg = bot.send_message(call.message.chat.id, "Please send your **Transaction ID (TxID)** for the 25 USDT transfer now:")
    bot.register_next_step_handler(msg, process_txid)

def process_txid(message):
    txid = message.text.strip()
    chat_id = message.chat.id

    if txid in USED_TXIDS:
        bot.send_message(chat_id, "❌ Error: This Transaction ID has already been used! It cannot be used again.")
        return

    bot.send_message(chat_id, "⏳ Verifying transaction on the blockchain and confirming payment arrival, please wait...")

    is_valid, reason = verify_bep20_transaction(txid)

    if is_valid:
        USED_TXIDS.add(txid)
        
        success_text = (
            "✅ **Payment Confirmed Successfully!**\n\n"
            "Thank you for purchasing the Berlin Fast Logistics template.\n"
            f"Here is your template access link:\n{TEMPLATE_LINK}\n\n"
            "We wish you great success with your digital project!"
        )
        bot.send_message(chat_id, success_text, parse_mode="Markdown")
    else:
        bot.send_message(chat_id, f"❌ Sorry, transaction verification failed:\n{reason}\n\nMake sure your TxID is correct and was sent to the proper address.")

if __name__ == '__main__':
    print("Bot is running...")
    bot.infinity_polling()
