import os, random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("TOKEN")

def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("لعبة أسرع من يرسل 🆕", callback_data="fast")],
        [InlineKeyboardButton("قسم الهمسة 🎲", callback_data="hamsa"), InlineKeyboardButton("قسم الميوزك 🎵", callback_data="music")],
        [InlineKeyboardButton("📩 تحميل من مواقع التواصل", callback_data="download")],
        [InlineKeyboardButton("قسم الألعاب الزوجية ( القياس ) 💋", callback_data="couple")],
        [InlineKeyboardButton("🎯 قسم الألعاب التنافسية", callback_data="comp")],
        [InlineKeyboardButton("🔥 توب الستريك", callback_data="top_streak"), InlineKeyboardButton("توب المتصدرين", callback_data="top")],
    ])

def back_home_btn():
    return InlineKeyboardMarkup([[InlineKeyboardButton("🔙 الرئيسية", callback_data="main")]])

MEASURES = [
    ("الحضن 🫂", "hug"), ("البوسة 💋", "kiss"),
    ("اللواته 🐸", "lawata"), ("الدلع 💕", "dalaa"),
    ("العفوية 🌟", "afwiya"), ("الخوة 💞", "khuwa"),
    ("الحزن 🖤", "huzn"), ("كره الصيف ☀️", "summer"),
    ("نية الزواج 💍", "zawaj"), ("حب الشتاء ❄️", "winter"),
    ("نسبة الحب ❤️", "love"), ("نسبة الخيانة 🌚", "khiyana"),
    ("نسبه الغيره 😁", "gheera"), ("نسبه النظافه 💧", "nathafa"),
    ("البكمنه 👧🏻", "bakmana"), ("نسبه اخلاقك 🤓", "akhlaq"),
    ("الحموظه", "hmoodha"), ("قياس الكلام الزايد", "kalam"),
    ("الانوثه", "onotha"),
]

def couple_menu():
    kb = []
    kb.append([InlineKeyboardButton("الحضن 🫂", callback_data="m_hug"), InlineKeyboardButton("البوسة 💋", callback_data="m_kiss")])
    kb.append([InlineKeyboardButton("اللواته 🐸", callback_data="m_lawata"), InlineKeyboardButton("الدلع 💕", callback_data="m_dalaa")])
    kb.append([InlineKeyboardButton("العفوية 🌟", callback_data="m_afwiya"), InlineKeyboardButton("الخوة 💞", callback_data="m_khuwa")])
    kb.append([InlineKeyboardButton("الحزن 🖤", callback_data="m_huzn")])
    kb.append([InlineKeyboardButton("كره الصيف ☀️", callback_data="m_summer"), InlineKeyboardButton("نية الزواج 💍", callback_data="m_zawaj")])
    kb.append([InlineKeyboardButton("حب الشتاء ❄️", callback_data="m_winter"), InlineKeyboardButton("نسبة الحب ❤️", callback_data="m_love")])
    kb.append([InlineKeyboardButton("نسبة الخيانة 🌚", callback_data="m_khiyana")])
    kb.append([InlineKeyboardButton("نسبه الغيره 😁", callback_data="m_gheera"), InlineKeyboardButton("نسبه النظافه 💧", callback_data="m_nathafa")])
    kb.append([InlineKeyboardButton("البكمنه 👧🏻", callback_data="m_bakmana"), InlineKeyboardButton("نسبه اخلاقك 🤓", callback_data="m_akhlaq")])
    kb.append([InlineKeyboardButton("الحموظه", callback_data="m_hmoodha"), InlineKeyboardButton("قياس الكلام الزايد", callback_data="m_kalam")])
    kb.append([InlineKeyboardButton("الانوثه", callback_data="m_onotha")])
    kb.append([InlineKeyboardButton("🔙 الرئيسية", callback_data="main")])
    return InlineKeyboardMarkup(kb)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    txt = "مرحباً بك في بوت كشك الالعاب والميوزك 🎧\n\nاختر القسم الذي تريد استخدامه من الأسفل 👇❤️"
    if update.message:
        await update.message.reply_text(txt, reply_markup=main_menu())
    else:
        await update.callback_query.edit_message_text(txt, reply_markup=main_menu())

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    data = q.data
    user = q.from_user
    if data == "main":
        await q.edit_message_text("مرحباً بك في بوت كشك الالعاب والميوزك 🎧\n\nاختر القسم الذي تريد استخدامه من الأسفل 👇❤️", reply_markup=main_menu())
        return
    if data == "couple":
        await q.edit_message_text("💋 قسم الألعاب الزوجية (القياس)\n\nاختر القياس الذي تريده:", reply_markup=couple_menu())
        return
    if data.startswith("m_"):
        code = data[2:]
        name = next((n for n, c in MEASURES if c == code), code)
        kb = [[InlineKeyboardButton("قياس النسبة مع الأصدقاء", callback_data=f"mf_{code}")],[InlineKeyboardButton("قياس نسبتك هُنا", callback_data=f"mm_{code}")],[InlineKeyboardButton("رجوع", callback_data="couple")]]
        await q.edit_message_text(f"🎯 قوة {name}\n\nاختر طريقة القياس:", reply_markup=InlineKeyboardMarkup(kb))
        return
    if data.startswith("mm_"):
        code = data[3:]
        name = next((n for n, c in MEASURES if c == code), code)
        pct = random.randint(2, 99)
        bar = "█" * (pct//10) + "░" * (10 - pct//10)
        await q.edit_message_text(f"🎯 قوة {name}\n\n👤 {user.first_name}\n\nنسبتك: {pct}%\n[{bar}]\n\n😂🔥", reply_markup=back_home_btn())
        return
    if data.startswith("mf_"):
        code = data[3:]
        context.user_data["measure"] = code
        await q.edit_message_text("رد على رسالة صديقك واكتب /qias حتى اقيس النسبة بينكم 😍", reply_markup=back_home_btn())
        return
    if data == "comp":
        kb = [[InlineKeyboardButton("🤖 لعب اللعبة مع البوت", callback_data="rps_bot")],[InlineKeyboardButton("🎮 لعب مع الاصدقاء", callback_data="rps_friends")],[InlineKeyboardButton("رجوع ❓", callback_data="main")]]
        await q.edit_message_text("✂️ لعبة حجرة ورقة مقص", reply_markup=InlineKeyboardMarkup(kb))
        return
    if data == "rps_bot":
        kb = [[InlineKeyboardButton("🪨 حجرة", callback_data="rps_rock"), InlineKeyboardButton("📄 ورقة", callback_data="rps_paper"), InlineKeyboardButton("✂️ مقص", callback_data="rps_scissors")],[InlineKeyboardButton("رجوع", callback_data="comp")]]
        await q.edit_message_text("اختر:", reply_markup=InlineKeyboardMarkup(kb))
        return
    if data in ["rps_rock", "rps_paper", "rps_scissors"]:
        mp = {"rps_rock": "🪨 حجرة", "rps_paper": "📄 ورقة", "rps_scissors": "✂️ مقص"}
        bot = random.choice(list(mp.keys()))
        win = {"rps_rock": "rps_scissors", "rps_paper": "rps_rock", "rps_scissors": "rps_paper"}
        if data == bot: res = "🤝 تعادل!"
        elif win[data] == bot: res = "🏆 فزت انت!"
        else: res = "😂 فاز البوت عليك!"
        await q.edit_message_text(f"انت: {mp[data]}\nالبوت: {mp[bot]}\n\n{res}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العب مرة ثانية", callback_data="rps_bot")],[InlineKeyboardButton("رجوع", callback_data="main")]]))
        return
    if data == "rps_friends":
        await q.edit_message_text("دز /rps بالكروب حتى تلعبون وية اصدقائك 🎮", reply_markup=back_home_btn())
        return
    if data == "fast":
        txt = "⚡ أهلاً بك في قسم لعبة الأسرع!\n\n🎯 فكرة اللعبة: ينشر البوت كلمة في قناتك، ويتنافس أعضاء القناة على إرسالها إلى البوت بأسرع وقت ممكن.\nتُسجَّل الإجابات الصحيحة حسب وقت وصولها، ثم تُعلن نتيجة كل جولة ويُحدَّد الأسرع بين المشاركين.\n\n📣 اختر قناتك من الأزرار أدناه لبدء اللعبة الآن.\n\n🔹 يمكنك تفعيل إشعارات اللعبة لكي تصلك رسالة خاصة عند نشر لعبة أسرع جديدة.\n\n📩 لم تقم بإضافة أي قناة بعد.\nاضغط زر إضافة قناة للبدء، وتأكد أنك مالك أو مشرف في القناة وأن البوت مشرف لديه صلاحية النشر."
        kb = [[InlineKeyboardButton("➕ إضافة قناة للبدء", callback_data="add_channel")],[InlineKeyboardButton("🔔 تفعيل الإشعارات : معطّل", callback_data="toggle")],[InlineKeyboardButton("رجوع", callback_data="main")]]
        await q.edit_message_text(txt, reply_markup=InlineKeyboardMarkup(kb))
        return
    if data == "add_channel":
        await q.edit_message_text("ضيف البوت مشرف بقناتك، وبعدها دز معرف القناة مثل @channel", reply_markup=back_home_btn())
        return
    if data == "toggle":
        await q.answer("تم تفعيل الإشعارات 🔔", show_alert=True)
        return
    if data == "hamsa":
        await q.edit_message_text("🎲 قسم الهمسة\n\nدز /hamsa بالكروب", reply_markup=back_home_btn())
        return
    if data == "music":
        await q.edit_message_text("🎵 قسم الميوزك\n\nدز اسم الاغنية هنا", reply_markup=back_home_btn())
        return
    if data == "download":
        await q.edit_message_text("📩 تحميل من مواقع التواصل\n\nدز رابط تيك توك / انستا / يوتيوب", reply_markup=back_home_btn())
        return
    if data == "top":
        await q.edit_message_text("🏆 توب المتصدرين\n\nالعب اكثر حتى تصعد!", reply_markup=back_home_btn())
        return
    if data == "top_streak":
        await q.edit_message_text("🔥 توب الستريك\n\nبعده ماكو ستريك", reply_markup=back_home_btn())
        return

async def qias_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text("رد على رسالة صديقك واكتب /qias")
        return
    code = context.user_data.get("measure", "love")
    name = next((n for n, c in MEASURES if c == code), "الحب")
    me = update.effective_user.first_name
    target = update.message.reply_to_message.from_user.first_name
    pct = random.randint(2, 99)
    bar = "█" * (pct//10) + "░" * (10 - pct//10)
    await update.message.reply_text(f"🎯 قوة {name}\n\n👤 {me} ➡️ {target}\n\nالنسبة: {pct}%\n[{bar}]\n\n😍🔥")

async def rps_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✂️ حجرة ورقة مقص!\nالكل يدز حجرة / ورقة / مقص")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("qias", qias_cmd))
    app.add_handler(CommandHandler("rps", rps_cmd))
    app.add_handler(CallbackQueryHandler(button))
    print("Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
