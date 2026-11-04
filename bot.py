import os
from flask import Flask
from threading import Thread

# ফ্লাস্ক সার্ভার তৈরি করা যাতে রেন্ডার পোর্ট পেয়ে যায়
app = Flask('')

@app.route('/')
def home():
    return "I am alive!"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

def keep_alive():
    t = Thread(target=run)
    t.start()

# বটের কোড শুরু হওয়ার আগেই এটি কল করতে হবে
if __name__ == "__main__":
    keep_alive()
    # এখানে আপনার মূল বটের কোড বা স্টার্ট ফাংশন থাকবে
import logging
import re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler, MessageHandler, filters

# Logging setup
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# ব্যবসায়িক তথ্য ও কনফিগারেশন
BKASH_NUM = "01759247217"
NAGAD_NUM = "01338824580"
ADMIN_USER = "@rabbibhai9"
ADMIN_CHAT_ID = "8160215257" 

# /start হ্যান্ডলার - প্রিমিয়াম ওয়েলকাম মেনু
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🛒 প্লে-পয়েন্ট কিনুন", callback_data="buy_points")],
        [InlineKeyboardButton("🎁 রেফার কোড ও অফার", callback_data="referral_offer")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = (
        "✨ **স্বাগতম! আমাদের প্রিমিয়াম সার্ভিস হাবে আপনাকে স্বাগতম** ✨\n\n"
        "আপনার প্রয়োজনীয় সেবাটি গ্রহণ করতে নিচের যেকোনো একটি অপশনে ট্যাপ করুন:"
    )
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")

# বাটন ইন্টার‌্যাকশন হ্যান্ডলার
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "buy_points":
        text = (
            "🛒 **প্লে-পয়েন্ট অ্যাকাউন্ট ক্রয় প্রক্রিয়া** 🛒\n\n"
            "💰 **মূল্য:** ১০ টাকা মাত্র\n\n"
            "📌 **পেমেন্ট করার নিয়ম:**\n"
            f"🔹 **বিকাশ (Send Money):** `{BKASH_NUM}`\n"
            f"🔹 **নগদ (Send Money):** `{NAGAD_NUM}`\n\n"
            "⚠️ টাকা পাঠানোর পর আপনার **নম্বর** এবং **টাকা পাঠানোর স্ক্রিনশটটি** এই বক্সে পাঠান।"
        )
        await query.message.edit_text(text, parse_mode="Markdown")
        
    elif query.data == "referral_offer":
        text = (
            "🎁 **১৭% ডিসকাউন্ট অফার** 🎁\n\n"
            "আমাদের ইউটিউব চ্যানেল ও টিকটক অ্যাকাউন্ট ফলো এবং সাবস্ক্রাইব করে স্ক্রিনশট দিন। যাচাই করে ডিসকাউন্ট কোড দেওয়া হবে!"
        )
        await query.message.edit_text(text, parse_mode="Markdown")

# স্ক্রিনশট রিসিভ ও প্রসেসিং অ্যানিমেশন
async def handle_screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    username = f"@{user.username}" if user.username else "ইউজারনেম নেই"
    
    # লোডিং অ্যানিমেশন বার্তা
    await update.message.reply_text("⏳ আপনার পেমেন্ট এবং স্ক্রিনশটটি **যাচাইকরণ হচ্ছে**...\nদয়া করে একটু অপেক্ষা করুন।")
    
    # অ্যাডমিনকে পেমেন্ট ডিটেইলস পাঠানো
    admin_notification = (
        "🚨 **নতুন পেমেন্ট স্ক্রিনশট জমা পড়েছে!** 🚨\n\n"
        f"👤 **প্রেরক:** {user.first_name} ({username})\n"
        f"🆔 **User ID:** `{user.id}`\n\n"
        "👉 পেমেন্ট সঠিক থাকলে এই মেসেজটির রিপ্লাই হিসেবে `/confirm` লিখে পাঠান।"
    )
    try:
        await context.bot.send_photo(
            chat_id=ADMIN_CHAT_ID,
            photo=update.message.photo[-1].file_id,
            caption=admin_notification,
            parse_mode="Markdown"
        )
    except Exception as e:
        print(f"অ্যাডমিনকে মেসেজ পাঠাতে সমস্যা হয়েছে: {e}")

# পেমেন্ট কনফার্মেশন ও অনারের কন্টাক্ট প্রদান
async def confirm_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != int(ADMIN_CHAT_ID):
        return

    reply_message = update.message.reply_to_message
    if reply_message and reply_message.caption:
        user_id_match = re.search(r"User ID:\s*`(\d+)`", reply_message.caption)
        if user_id_match:
            target_user_id = user_id_match.group(1)
            
            success_text = (
                "🎉 **অভিনন্দন! আপনার পেমেন্ট সফলভাবে যাচাই করা হয়েছে** 🎉\n\n"
                "প্লে-পয়েন্ট অ্যাকাউন্ট বা সেবাটি গ্রহণ করার জন্য অনুগ্রহ করে আমাদের অনার বা অ্যাডমিনের সাথে যোগাযোগ করুন:\n\n"
                f"👤 **Contact:** {ADMIN_USER}\n\n"
                "⭐⭐⭐⭐⭐\n"
                "আমাদের প্রিমিয়াম সেবাটি ব্যবহার করার জন্য আপনাকে অসংখ্য ধন্যবাদ! আপনার দিনটি শুভ হোক। আশা করি ভবিষ্যতে আবারও আমাদের সেবা গ্রহণ করবেন। আবার দেখা হবে! 👋"
            )
            await context.bot.send_message(chat_id=target_user_id, text=success_text, parse_mode="Markdown")
            await update.message.reply_text("✅ ইউজারকে সফলভাবে কনফার্মেশন ও কন্টাক্ট মেসেজ পাঠানো হয়েছে।")

if __name__ == '__main__':
    TOKEN = "9016031285:AAHf6-B6rbIvWcnK280auGe89vpKnxOYvRY"
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.PHOTO, handle_screenshot))
    app.add_handler(CommandHandler("confirm", confirm_payment))
    app.add_handler(CommandHandler("confirm", confirm_payment))

    print("🤖 প্রিমিয়াম বট সফলভাবে সচল হয়েছে...")
    app.run_polling()
