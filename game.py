import os
import telebot
from telebot import types
import logging

# تنظیمات لاگینگ
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# دریافت توکن از متغیر محیطی
BOT_TOKEN = os.environ.get('8233712038:AAE9TGFT-V_dfCDGUBphQyt4U79yXEDJrGY')

if not BOT_TOKEN:
    logger.error("❌ لطفا BOT_TOKEN را تنظیم کنید")
    exit(1)

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    try:
        welcome_text = """
        🤖 به ربات Duo Challenge خوش آمدید!
        
        ✅ ربات با موفقیت روی Railway اجرا شد!
        
        🎮 برای شروع بازی از دستورات زیر استفاده کنید:
        /play - شروع بازی جدید
        /profile - مشاهده پروفایل
        """
        bot.reply_to(message, welcome_text)
        
    except Exception as e:
        logger.error(f"خطا: {e}")

@bot.message_handler(commands=['play'])
def start_game(message):
    keyboard = types.InlineKeyboardMarkup()
    btn_math = types.InlineKeyboardButton("🧮 چالش ریاضی", callback_data="game_math")
    btn_word = types.InlineKeyboardButton("🔤 چالش کلمات", callback_data="game_word")
    keyboard.add(btn_math, btn_word)
    
    bot.send_message(message.chat.id, "🎯 نوع بازی را انتخاب کنید:", reply_markup=keyboard)

@bot.message_handler(commands=['profile'])
def show_profile(message):
    user = message.from_user
    profile_text = f"""
    👤 پروفایل کاربری:
    
    🆔 نام: {user.first_name or "ناشناس"}
    📧 یوزرنیم: @{user.username or "ندارد"}
    🆔 آی‌دی: {user.id}
    """
    bot.send_message(message.chat.id, profile_text)

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    if call.data.startswith("game_"):
        game_type = call.data.split("_")[1]
        bot.send_message(call.message.chat.id, f"🎮 بازی {game_type} شروع شد! به زودی ویژگی‌های کامل اضافه می‌شود.")
        bot.answer_callback_query(call.id, "بازی شروع شد!")

if __name__ == '__main__':
    logger.info("🚀 ربات در حال راه اندازی...")
    bot.infinity_polling()