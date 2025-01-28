from telegram.ext import Updater, CommandHandler
import requests

# توکن ربات تلگرام
TOKEN = "7542986703:AAGP4G6UL1zJszI-YY2qiK8n1F_zDJebfuY"

# تابع برای گرفتن اخبار
def get_ai_news():
    url = "https://newsapi.org/v2/everything"  # API اخبار
    params = {
        "q": "Artificial Intelligence",
        "apiKey": "9601417c98fa4e73b59f21e8f38b2e7a",  # توکن API اخبار
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        articles = response.json().get("articles", [])
        if articles:
            return articles[0]["title"] + "\n" + articles[0]["url"]
    return "هیچ خبری پیدا نشد."

# تابع برای ارسال اخبار به چت ربات
def send_news(context):
    job = context.job
    news = get_ai_news()
    context.bot.send_message(chat_id=job.context, text=news)

# تابع استارت و زمان‌بندی
def start(update, context):
    chat_id = update.message.chat_id  # آی‌دی کاربری که پیام داده
    update.message.reply_text("ارسال اخبار هر 12 ساعت شروع شد!")
    # زمان‌بندی ارسال پیام (هر 12 ساعت)
    context.job_queue.run_repeating(send_news, interval=300, first=5, context=chat_id)

# شروع ربات
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))

    # استارت JobQueue
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
