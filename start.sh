#!/bin/bash

# تأكد من أنك في مجلد المشروع الصحيح (اختياري حسب الهيكل)
cd "$(dirname "$0")"

# تشغيل البوت
./llama_telegram_bot.py
