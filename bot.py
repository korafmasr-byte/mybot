import os
import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = "8852742742:AAE434cwjZHRkJagQToYICJ36Z4BJgFhqKo"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً بك! أرسل رابط الفيديو وسأقوم بتحميله لك فوراً.")

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    if not (url.startswith("http://") or url.startswith("https://")):
        await update.message.reply_text("يرجى إرسال رابط صحيح.")
        return

    msg = await update.message.reply_text("جاري التحميل... ⏳")
    
    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'outtmpl': f'downloads/{update.effective_user.id}_%(id)s.%(ext)s',
        'max_filesize': 49 * 1024 * 1024,
        'quiet': True
    }

    try:
        os.makedirs('downloads', exist_ok=True)
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        await msg.edit_text("جاري الرفع إلى تيليجرام... 🚀")
        with open(filename, 'rb') as video_file:
            await update.message.reply_video(video=video_file, caption="تم التحميل بنجاح ✅")
            
        if os.path.exists(filename):
            os.remove(filename)
        await msg.delete()
    except Exception:
        await msg.edit_text("عذراً، حدث خطأ أثناء التحميل أو حجم الفيديو أكبر من 50 ميغابايت.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), download_video))
    app.run_polling()
