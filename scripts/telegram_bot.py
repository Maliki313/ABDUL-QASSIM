"""
telegram_bot.py
---------------

هذا السكربت يربط ملفاتك النصية ببوت تلغرام حتى تقدر تسأل ويجاوبك محلياً.
لازم يكون عندك متغير البيئة `TELEGRAM_BOT_TOKEN` موجود حتى يشتغل البوت.

الاستخدام:
    python telegram_bot.py data_dir
"""

import os
import sys
from telegram.ext import Updater, MessageHandler, Filters

from offline_bot import load_sentences, simple_search


def handle_message(update, context):
    """الغرض من هذه الدالة الرد على رسائل المستخدمين بطريقة بسيطة.

    المدخلات:
        update (telegram.Update): التحديث الوارد من تلغرام.
        context (telegram.CallbackContext): السياق المصاحب للتحديث.
    المخرجات:
        لا يوجد. ترجع الرد مباشرة إلى المستخدم.
    Notes: تعتمد على دالة `simple_search` للبحث بالكلمات.
    """
    query = update.message.text
    results = simple_search(context.sentences, query)
    if not results:
        update.message.reply_text("ماكو نتائج، جرّب كلمات ثانية.")
    else:
        reply = "\n".join(
            f"[{name}] {sentence}" for name, sentence in results[:5]
        )
        update.message.reply_text(reply)


def main():
    """تشغيل البوت بالتوصيل على الداتا دير وتوفير التوكن.

    المدخلات: مسار المجلد الذي يحتوي على الملفات النصية.
    المخرجات: لا شيء.
    Notes: يجب ضبط متغير `TELEGRAM_BOT_TOKEN` في البيئة.
    """
    if len(sys.argv) != 2:
        print("Usage: python telegram_bot.py data_dir")
        return
    data_dir = sys.argv[1]
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        print("Error: TELEGRAM_BOT_TOKEN not set")
        return
    updater = Updater(token)
    sentences = load_sentences(data_dir)
    updater.dispatcher.sentences = sentences
    updater.dispatcher.add_handler(
        MessageHandler(Filters.text & ~Filters.command, handle_message)
    )
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
