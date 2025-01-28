from telegram.ext import Updater, CommandHandler, JobQueue
from googletrans import Translator
import requests

# تنظیمات اولیه
TOKEN = "7542986703:AAGP4G6UL1zJszI-YY2qiK8n1F_zDJebfuY"  # توکن ربات خود را اینجا قرار دهید
CHAT_ID = None  # چت آیدی را به‌صورت پویا ذخیره می‌کنیم

# تابع ترجمه به فارسی
def translate_to_farsi(text):
    translator = Translator()
    translated = translator.translate(text, src='en', dest='fa')
    return translated.text

# دریافت و ارسال اخبار مرتبط با هوش مصنوعی
def send_ai_news(context):
    try:
        # دریافت اخبار مرتبط با هوش مصنوعی
        url = "https://newsapi.org/v2/everything?q=artificial%20intelligence&apiKey=9601417c98fa4e73b59f21e8f38b2e7a"
        response = requests.get(url)
        data = response.json()

        # بررسی وجود اخبار
        if "articles" in data and data["articles"]:
            article = data["articles"][0]  # اولین خبر
            title = article["title"]
            description = article["description"]
            link = article["url"]

            # ترجمه عنوان و توضیحات به فارسی
            title_farsi = translate_to_farsi(title)
            description_farsi = translate_to_farsi(description)

            # ساخت پیام نهایی
            message = f"📢 *خبر جدید در حوزه هوش مصنوعی:*\n\n" \
                      f"🔹 {title}\n{description}\n" \
                      f"🌍 [مشاهده خبر اصلی]({link})\n\n" \
                      f"📜 *ترجمه به فارسی:*\n" \
                      f"🔹 {title_farsi}\n{description_farsi}"

            # ارسال پیام به چت
            context.bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="Markdown", disable_web_page_preview=True)
        else:
            context.bot.send_message(chat_id=CHAT_ID, text="❌ هیچ خبری در حوزه هوش مصنوعی پیدا نشد.")

    except Exception as e:
        print(f"❌ خطا در دریافت یا ارسال خبر: {e}")
        if CHAT_ID:
            context.bot.send_message(chat_id=CHAT_ID, text="❌ خطایی در دریافت اخبار رخ داد.")

# تابع برای ذخیره چت آیدی
def start(update, context):
    global CHAT_ID
    CHAT_ID = update.message.chat_id
    update.message.reply_text("✅ ربات فعال شد! اخبار هوش مصنوعی به این چت ارسال خواهد شد.")

# راه‌اندازی بات
def main():
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    job_queue = updater.job_queue

    # ثبت دستور /start برای شروع
    dispatcher.add_handler(CommandHandler("start", start))

    # تنظیم زمان‌بندی ارسال اخبار (هر 5 دقیقه)
    job_queue.run_repeating(send_ai_news, interval=300, first=5)

    # شروع Polling
    try:
        updater.start_polling()
        updater.idle()
    except Exception as e:
        print(f"❌ خطای کلی: {e}")

if __name__ == "__main__":
    main()
