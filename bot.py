import sys
import traceback
import re
import os
from datetime import datetime
from dotenv import load_dotenv

# Загружаем переменные из .env (если файл есть)
load_dotenv()

try:
    import telebot
    from telebot import types
except Exception as e:
    print("=" * 50)
    print("❌ ОШИБКА ИМПОРТА. Убедитесь, что установлена библиотека pyTelegramBotAPI")
    print(traceback.format_exc())
    print("=" * 50)
    sys.exit(1)

# ========= НАСТРОЙКА =========
# Если есть файл .env, токен возьмется оттуда. Иначе используется токен ниже (замените его на свой!)
BOT_TOKEN = os.getenv('BOT_TOKEN', "8728576355:AAGDDpJ7tLCP-rvcNMnBGn38BuUjZ1YyqDA")
YOUR_TELEGRAM_ID = 869236093

if not BOT_TOKEN:
    print("❌ КРИТИЧЕСКАЯ ОШИБКА: Токен бота не найден!")
    sys.exit(1)

bot = telebot.TeleBot(BOT_TOKEN)
user_states = {}
applications = []
app_id_counter = 1
user_data = {}
admin_reply_mode = {}
client_conversation_history = {}

PHONE = "+7 812 985 6005"
EMAIL = "Fulldrives@yandex.ru"

MAIN_MENU_TEXT = """
🚗 Главное меню автошколы «Фулл Драйв»

Выберите интересующий раздел:
• 🚗 Тарифы и стоимость обучения
• 📚 Как проходит обучение
• 💳 Способы оплаты
• 💰 Оплатить обучение
• 📝 Записаться на обучение
• 📞 Связаться с менеджером
"""

TARIFFS_MAIN = """
🚗 Тарифы на обучение

Выберите категорию прав:
• 🚙 Категория B (легковые автомобили)
• 🏍️ Категория A (мотоциклы)

Нажмите на кнопку ниже 👇
"""

TARIFFS_B = """
🚙 Тарифы на категорию B

——————————————————
1️⃣ Тариф «Стандарт»
💰 63 541 ₽
📅 Рассрочка от 2 410 ₽/мес

⏱ Срок обучения: 3,5 месяца
✅ Полный курс теории онлайн
✅ 30 занятий по вождению
✅ Отработка маршрутов ГАИ
✅ Сопровождение на экзамены

Включено:
• Занятия на рулевом тренажере
• Топливо
• Страховка
• Поддержка онлайн-преподавателя
• Беспроцентная рассрочка

——————————————————
2️⃣ Тариф «Комби»
💰 68 750 ₽
📅 Рассрочка от 2 672 ₽/мес

⏱ Срок обучения: 3,5 месяца
✅ Теория в классе по инд. графику
✅ Доступ к учебному контенту
✅ 30 занятий по вождению
✅ Отработка маршрутов ГАИ
✅ Сопровождение на экзамены

Включено:
• Занятия на рулевом тренажере
• Топливо
• Страховка
• Поддержка онлайн-преподавателя
• Беспроцентная рассрочка

——————————————————
3️⃣ Тариф «Макси»
💰 78 125 ₽
📅 Рассрочка от 3 930 ₽/мес

⏱ Срок обучения: от 4,5 месяцев
✅ Теория в классе или онлайн
✅ 50 занятий по вождению
✅ Тренинг по защитному вождению
✅ Сопровождение на экзамены
✅ Отработка маршрутов ГАИ

Включено:
• Занятия на рулевом тренажере
• Топливо
• Страховка
• Поддержка онлайн-преподавателя
• Беспроцентная рассрочка
• Выбор удобной даты экзамена

——————————————————
4️⃣ Тариф «Экспресс»
💰 60 416 ₽
📅 Рассрочка от 3 039 ₽/мес

⏱ Срок обучения: 2,5 месяца
✅ Полный курс теории онлайн
✅ 20 занятий по вождению
✅ Отработка маршрутов ГАИ
✅ Сопровождение на экзамены

Включено:
• Занятия на рулевом тренажере
• Топливо
• Страховка
• Поддержка онлайн-преподавателя
• Беспроцентная рассрочка
• Ускоренный инд. график
• Выбор удобной даты экзамена

📝 Для записи выберите «Записаться на обучение» в меню.
"""

TARIFFS_A = """
🏍️ Тарифы на категорию A

——————————————————
1️⃣ Тариф «Базовый»
💰 30 208 ₽

✅ Полный курс теории онлайн
✅ 4 часа вождения
✅ Сопровождение на экзамены в ГАИ

Включено:
• Топливо
• Страховка
• Экипировка и снаряжение
• Поддержка онлайн-преподавателя
• Беспроцентная рассрочка

🚀 Ждать набора не надо — начинаете учиться сразу!

——————————————————
2️⃣ Тариф «Стандарт»
💰 40 625 ₽

✅ Полный курс теории онлайн
✅ 8 часов вождения
✅ Сопровождение на экзамены в ГАИ

Включено:
• Топливо
• Страховка
• Экипировка и снаряжение
• Поддержка онлайн-преподавателя
• Беспроцентная рассрочка

🚀 Ждать набора не надо — начинаете учиться сразу!

📝 Для записи выберите «Записаться на обучение» в меню.
"""

LEARNING_PROCESS = """
📚 Как проходит обучение в «Фулл Драйв»

✅ Теория:
— Очные занятия в классе (будни/выходные)
— Онлайн занятия проходят на учебном контенте в приложении или на компьютере 
Просматриваете мультимедийные видео уроки и решаете билеты по темам 
А если появился вопрос, задаете его в чате с онлайн преподавателем 

✅ Практика:
— Занятия в удобном районе 
— Инструкторы с опытом от 5 лет
— Вождение по городу и на автодроме 
— Отработка экзаменационных маршрутов ГИБДД 

✅ Экзамены:
- Обучение в автошколе заканчивается внутренним экзаменом в школе, который включает в себя тестирование по ПДД - 1 билет 20 вопросов и вождение по городу. 
После успешной сдачи внутреннего экзамена выдается Свидетельство об окончании автошколы, которое дает право сдавать экзамены в ГАИ на всей территории РФ, как самостоятельно, так и в составе учебной группы 

- Первичная сдача экзамена в ГИБДД в составе учебной группы уже включена в каждый наш тариф

📌 Для уточнения деталей свяжитесь с менеджером 👇
"""

PAYMENT_METHODS = """
💳 Способы оплаты

💵 Способы оплаты:
— Наличными в офисе
— Перевод по реквизитам 
— QR-код / СБП

📅 Рассрочка:

1️⃣ От школы-1 (беспроцентная):
• Первый взнос 5 000 ₽ при записи
• Остаток через 2 недели
• Без процентов и переплат

2️⃣ От банка-партнёра (Т-Банк):
• Срок от 3 до 24 месяцев
• Первый взнос через месяц после договора
• Стоимость от 2 044 ₽/месяц

3️⃣ От школы-2 (беспроцентная):
• Первый взнос ~25% от стоимости при записи
• Остаток через 4 недели
• Без процентов и переплат

📌 Для уточнения деталей свяжитесь с менеджером
"""

PAYMENT_DETAILS_GROUP1 = """Благодарим Вас за заявку на обучение🙌🚙 

Оплатить обучение в размере 100% возможно переводом всей суммы:

💳 Т-Банк номер карты: 2200700637160077

📱 Или по СБП: +79313411006
(Т-Банк / Озон / Яндекс)
Получатель: Анна Алексеевна Г.

🌐 Или частично на сайте: https://фуллдрайв.рф/forma-oplaty/
(первый взнос 5 000 ₽)

📎 После оплаты пришлите, пожалуйста, чек сюда.

⚠️ Оплачивая обучение, Вы принимаете условия обучения и акцептируете Публичную Оферту:
https://фуллдрайв.рф/publichnaya-oferta/"""

PAYMENT_DETAILS_GROUP2 = """Благодарим Вас за заявку на обучение🙌🚙 

Оплатить обучение в размере 100% возможно переводом всей суммы:

💳 Озон Банк: 2204 2401 7903 7181

💳 Т-Банк: 2200 7005 9580 0052

💳 Яндекс Банк: 2204 3101 0546 1506

Получатель: Мария П.

🌐 Или частично на сайте: https://фуллдрайв.рф/forma-oplaty/
(первый взнос 5 000 ₽)

📎 После оплаты пришлите, пожалуйста, чек сюда.

⚠️ Оплачивая обучение, Вы принимаете условия обучения и акцептируете Публичную Оферту:
https://фуллдрайв.рф/publichnaya-oferta/"""

CHOOSE_BRANCH_TEXT = """💰 Оплата обучения

Выберите ваш филиал для получения реквизитов:

📍 Московский пр-кт 183-185 лит.А (м. Московская)
📍 Апраксин пер. д.4 (м. Садовая)
📍 Белы Куна д.4Г (м. Международная)
📍 Коллонтай ул. д.5/1 (м. Пр-кт Большевиков)
📍 Гжатская ул. 22 корп.2 (м. Академическая)
📍 Сестрорецкая ул. д.6 (м. Черная речка)

Нажмите на кнопку с вашим филиалом 👇"""

MAIN_MENU_BUTTONS = [
    "🚗 Тарифы и стоимость",
    "📚 Как проходит обучение",
    "💳 Способы оплаты",
    "💰 Оплатить обучение",
    "📝 Записаться на обучение",
    "📞 Связаться с менеджером",
]

def main_keyboard():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    for btn in MAIN_MENU_BUTTONS:
        kb.add(types.KeyboardButton(btn))
    return kb

def category_keyboard():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    kb.add(types.KeyboardButton("🚙 Категория B"), types.KeyboardButton("🏍️ Категория A"))
    kb.add(types.KeyboardButton("🔙 Назад в меню"))
    return kb

def branches_keyboard():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    branches = [
        "📍 Московский пр-кт 183-185",
        "📍 Апраксин пер. д.4",
        "📍 Белы Куна д.4Г",
        "📍 Коллонтай ул. д.5/1",
        "📍 Гжатская ул. 22 корп.2",
        "📍 Сестрорецкая ул. д.6",
    ]
    for branch in branches:
        kb.add(types.KeyboardButton(branch))
    kb.add(types.KeyboardButton("🔙 Назад в меню"))
    return kb

def phone_request_keyboard():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    kb.add(types.KeyboardButton("📱 Поделиться номером", request_contact=True))
    kb.add(types.KeyboardButton("🔙 Назад в меню"))
    return kb

def name_input_keyboard():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    kb.add(types.KeyboardButton("🔙 Назад в меню"))
    return kb

def save_conversation(chat_id, message_text, is_from_client=True):
    if chat_id not in client_conversation_history:
        client_conversation_history[chat_id] = []
    
    timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    msg_type = "👤 Клиент" if is_from_client else "👨‍💼 Менеджер"
    
    client_conversation_history[chat_id].append({
        "time": timestamp,
        "type": msg_type,
        "text": message_text
    })
    
    if len(client_conversation_history[chat_id]) > 50:
        client_conversation_history[chat_id] = client_conversation_history[chat_id][-50:]

def send_conversation_history(admin_chat_id, client_chat_id):
    if client_chat_id not in client_conversation_history or not client_conversation_history[client_chat_id]:
        bot.send_message(admin_chat_id, f"📭 История переписки с клиентом {client_chat_id} пуста.")
        return
    
    history_text = f"📜 **ИСТОРИЯ ПЕРЕПИСКИ С КЛИЕНТОМ**\n🆔 ID: {client_chat_id}\n\n"
    
    for msg in client_conversation_history[client_chat_id]:
        history_text += f"**[{msg['time']}] {msg['type']}:**\n{msg['text']}\n\n"
        if len(history_text) > 3800:
            bot.send_message(admin_chat_id, history_text, parse_mode='Markdown')
            history_text = ""
    
    if history_text:
        bot.send_message(admin_chat_id, history_text, parse_mode='Markdown')

@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if message.chat.id != YOUR_TELEGRAM_ID:
        bot.send_message(message.chat.id, "⛔ У вас нет доступа к админ-панели.")
        return
    
    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.add(
        types.InlineKeyboardButton("📋 Просмотреть заявки", callback_data="view_applications"),
        types.InlineKeyboardButton("👥 Просмотреть историю переписки", callback_data="view_conversations")
    )
    bot.send_message(message.chat.id, "👨‍💼 **Панель администратора**\n\nВыберите действие:", reply_markup=kb, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: call.data == "view_applications")
def view_applications(call):
    if call.message.chat.id != YOUR_TELEGRAM_ID: return
    if not applications:
        bot.edit_message_text("📭 Заявок пока нет.", call.message.chat.id, call.message.message_id)
        return
    
    text = "📋 ВСЕ ЗАЯВКИ:\n\n"
    for app in applications:
        status_emoji = {"new": "🆕", "processing": "🔄", "completed": "✅"}.get(app['status'], "🆕")
        text += f"{status_emoji} Заявка #{app['id']}\n👤 {app['name']}\n📱 {app['phone']}\n🚗 {app['tariff']}\n📅 {app['start_date']}\n🕐 {app['time']}\n📌 Статус: {app['status']}\n➖➖➖➖➖➖➖➖➖➖\n"
    
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("🔄 Обновить", callback_data="refresh_admin"))
    kb.add(types.InlineKeyboardButton("🔙 Назад", callback_data="back_to_admin"))
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=kb)

@bot.callback_query_handler(func=lambda call: call.data == "view_conversations")
def view_conversations(call):
    if call.message.chat.id != YOUR_TELEGRAM_ID: return
    if not client_conversation_history:
        bot.edit_message_text("📭 История переписки пуста.", call.message.chat.id, call.message.message_id)
        return
    
    clients_list = "👥 **Список клиентов:**\n\n"
    kb = types.InlineKeyboardMarkup(row_width=1)
    
    for client_id in client_conversation_history.keys():
        client_name = user_data.get(client_id, {}).get("full_name", f"Клиент {client_id}")
        clients_list += f"🆔 {client_id} - {client_name}\n"
        kb.add(types.InlineKeyboardButton(f"📜 {client_name}", callback_data=f"show_history_{client_id}"))
    
    kb.add(types.InlineKeyboardButton("🔙 Назад", callback_data="back_to_admin"))
    bot.edit_message_text(clients_list, call.message.chat.id, call.message.message_id, reply_markup=kb, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: call.data.startswith("show_history_"))
def show_history(call):
    if call.message.chat.id != YOUR_TELEGRAM_ID: return
    client_id = int(call.data.split("_")[2])
    send_conversation_history(call.message.chat.id, client_id)
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("✏️ Ответить клиенту", callback_data=f"reply_to_{client_id}"))
    kb.add(types.InlineKeyboardButton("🔙 Назад к списку", callback_data="view_conversations"))
    bot.send_message(call.message.chat.id, "Выберите действие:", reply_markup=kb)

@bot.callback_query_handler(func=lambda call: call.data == "back_to_admin")
def back_to_admin(call):
    if call.message.chat.id != YOUR_TELEGRAM_ID: return
    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.add(
        types.InlineKeyboardButton("📋 Просмотреть заявки", callback_data="view_applications"),
        types.InlineKeyboardButton("👥 Просмотреть историю переписки", callback_data="view_conversations")
    )
    bot.edit_message_text("👨‍💼 **Панель администратора**\n\nВыберите действие:", call.message.chat.id, call.message.message_id, reply_markup=kb, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: call.data == "refresh_admin")
def refresh_admin(call):
    if call.message.chat.id != YOUR_TELEGRAM_ID: return
    if not applications:
        bot.edit_message_text("📭 Заявок пока нет.", call.message.chat.id, call.message.message_id)
        return
    
    text = "📋 ВСЕ ЗАЯВКИ:\n\n"
    for app in applications:
        status_emoji = {"new": "🆕", "processing": "🔄", "completed": "✅"}.get(app['status'], "🆕")
        text += f"{status_emoji} Заявка #{app['id']}\n👤 {app['name']}\n📱 {app['phone']}\n🚗 {app['tariff']}\n📅 {app['start_date']}\n🕐 {app['time']}\n📌 Статус: {app['status']}\n➖➖➖➖➖➖➖➖➖➖\n"
    
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("🔄 Обновить", callback_data="refresh_admin"))
    kb.add(types.InlineKeyboardButton("🔙 Назад", callback_data="back_to_admin"))
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=kb)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    save_conversation(message.chat.id, "Пользователь начал диалог с ботом (команда /start)")
    bot.send_message(message.chat.id, "Добро пожаловать в автошколу «Фулл Драйв»! 🚘\n\n" + MAIN_MENU_TEXT, reply_markup=main_keyboard())

@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    chat_id = message.chat.id
    phone_number = message.contact.phone_number
    save_conversation(chat_id, f"Отправил номер телефона: {phone_number}")
    
    if chat_id not in user_states or user_states[chat_id].get("step") != "phone":
        bot.send_message(chat_id, "❓ Сейчас мы не ожидаем номер телефона. Начните запись заново: /start", reply_markup=main_keyboard())
        return
    
    if phone_number.startswith('7') and len(phone_number) == 11:
        formatted_phone = f"+{phone_number[0]} {phone_number[1:4]} {phone_number[4:7]} {phone_number[7:9]} {phone_number[9:11]}"
    elif phone_number.startswith('8') and len(phone_number) == 11:
        phone_number = '7' + phone_number[1:]
        formatted_phone = f"+{phone_number[0]} {phone_number[1:4]} {phone_number[4:7]} {phone_number[7:9]} {phone_number[9:11]}"
    else:
        formatted_phone = phone_number
    
    user_states[chat_id]["phone"] = phone_number
    user_states[chat_id]["formatted_phone"] = formatted_phone
    user_states[chat_id]["step"] = "tariff"
    
    bot.send_message(chat_id, f"📱 Номер: {formatted_phone}\n\n🚘 Теперь выберите категорию прав и тариф:\n\nНапример: B / Стандарт или А / Базовый", reply_markup=main_keyboard())

@bot.message_handler(content_types=['text', 'photo', 'document', 'video', 'audio', 'voice', 'sticker'])
def handle_all_messages(message):
    chat_id = message.chat.id
    
    if message.content_type == 'text':
        text = message.text.strip()
        content_description = f"💬 Сообщение: {text}"
    elif message.content_type == 'photo':
        text = None
        content_description = f"📷 Фото"
        if message.caption: content_description += f"\n💬 Подпись: {message.caption}"
    elif message.content_type == 'document':
        text = None
        content_description = f"📄 Документ: {message.document.file_name}"
        if message.caption: content_description += f"\n💬 Подпись: {message.caption}"
    elif message.content_type == 'video':
        text = None
        content_description = "🎥 Видео"
        if message.caption: content_description += f"\n💬 Подпись: {message.caption}"
    elif message.content_type == 'audio':
        text = None
        content_description = "🎵 Аудио"
    elif message.content_type == 'voice':
        text = None
        content_description = "🎤 Голосовое сообщение"
    elif message.content_type == 'sticker':
        text = None
        content_description = f"🏷️ Стикер (эмодзи: {message.sticker.emoji})"
    else:
        text = None
        content_description = f"📎 Медиафайл ({message.content_type})"
    
    if chat_id != YOUR_TELEGRAM_ID:
        save_conversation(chat_id, content_description)
        username = message.from_user.username
        first_name = message.from_user.first_name
        last_name = message.from_user.last_name
        user_data[chat_id] = {
            "username": f"@{username}" if username else "нет username",
            "first_name": first_name,
            "last_name": last_name or "",
            "full_name": f"{first_name} {last_name or ''}".strip()
        }

    if chat_id == YOUR_TELEGRAM_ID and chat_id in admin_reply_mode:
        if message.content_type == 'text':
            reply_to_user(chat_id, text)
        else:
            try:
                user_id = admin_reply_mode[chat_id]
                bot.copy_message(user_id, chat_id, message.message_id)
                bot.send_message(chat_id, f"✅ Медиафайл отправлен пользователю {user_id}")
                save_conversation(user_id, f"📎 Медиафайл от менеджера", is_from_client=False)
                del admin_reply_mode[chat_id]
            except Exception as e:
                bot.send_message(chat_id, f"❌ Ошибка отправки медиа: {e}")
        return

    if message.content_type != 'text':
        if chat_id != YOUR_TELEGRAM_ID:
            forward_media_to_admin(message, chat_id, content_description)
        return

    if chat_id in user_states:
        process_booking(chat_id, text)
        return

    if text == "🚗 Тарифы и стоимость":
        bot.send_message(chat_id, TARIFFS_MAIN, reply_markup=category_keyboard())
        return
    
    if text == "🚙 Категория B":
        bot.send_message(chat_id, TARIFFS_B, reply_markup=category_keyboard())
        return
    
    if text == "🏍️ Категория A":
        bot.send_message(chat_id, TARIFFS_A, reply_markup=category_keyboard())
        return
    
    if text == "🔙 Назад в меню":
        if chat_id in user_states: del user_states[chat_id]
        bot.send_message(chat_id, MAIN_MENU_TEXT, reply_markup=main_keyboard())
        return

    if text == "💰 Оплатить обучение":
        bot.send_message(chat_id, CHOOSE_BRANCH_TEXT, reply_markup=branches_keyboard())
        return
    
    branch_payment_map = {
        "📍 Московский пр-кт 183-185": PAYMENT_DETAILS_GROUP1,
        "📍 Апраксин пер. д.4": PAYMENT_DETAILS_GROUP1,
        "📍 Белы Куна д.4Г": PAYMENT_DETAILS_GROUP1,
        "📍 Коллонтай ул. д.5/1": PAYMENT_DETAILS_GROUP1,
        "📍 Гжатская ул. 22 корп.2": PAYMENT_DETAILS_GROUP2,
        "📍 Сестрорецкая ул. д.6": PAYMENT_DETAILS_GROUP2,
    }
    
    if text in branch_payment_map:
        bot.send_message(chat_id, branch_payment_map[text], reply_markup=main_keyboard())
        return

    if text == "📚 Как проходит обучение":
        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton("📞 Связаться с менеджером", url="https://t.me/fulldrives"))
        bot.send_message(chat_id, LEARNING_PROCESS, reply_markup=kb)
        return
    
    if text == "💳 Способы оплаты":
        bot.send_message(chat_id, PAYMENT_METHODS, reply_markup=main_keyboard())
        return
    
    if text == "📝 Записаться на обучение":
        if chat_id in user_states:
            bot.send_message(chat_id, "⚠️ У вас уже есть незавершенная запись. Завершите её или нажмите «Назад в меню»", reply_markup=main_keyboard())
            return
        user_states[chat_id] = {"step": "name"}
        bot.send_message(chat_id, "📝 Давайте запишем вас на обучение!\n\nНачнем со знакомства.\nПожалуйста, введите ваше имя:", reply_markup=name_input_keyboard())
        return
    
    if text == "📞 Связаться с менеджером":
        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton("💬 Написать менеджеру", url="https://t.me/fulldrives"))
        bot.send_message(chat_id, "📞 Нажмите на кнопку ниже, чтобы связаться с менеджером:", reply_markup=kb)
        return

    if text.startswith("/answer") and chat_id == YOUR_TELEGRAM_ID:
        try:
            parts = text.split()
            user_id = int(parts[1])
            admin_reply_mode[chat_id] = user_id
            bot.send_message(chat_id, f"✏️ Введите ответ для пользователя {user_id}. Для отмены /cancel_answer")
        except:
            bot.send_message(chat_id, "❌ Используйте: /answer [ID пользователя]")
        return
    
    if text == "/cancel_answer" and chat_id == YOUR_TELEGRAM_ID:
        if chat_id in admin_reply_mode:
            del admin_reply_mode[chat_id]
            bot.send_message(chat_id, "✅ Режим ответа отключён")
        return

    if chat_id != YOUR_TELEGRAM_ID:
        forward_text_to_admin(chat_id, text, content_description)

def forward_text_to_admin(chat_id, text, content_description):
    user_info = user_data.get(chat_id, {})
    username = user_info.get("username", "неизвестный")
    full_name = user_info.get("full_name", "Неизвестный")
    
    forward_text = f"""
📩 СООБЩЕНИЕ ОТ КЛИЕНТА

👤 Имя: {full_name}
🏷️ Username: {username}
🆔 ID: {chat_id}
{content_description}
🕐 Время: {datetime.now().strftime("%d.%m.%Y %H:%M")}

📌 Для ответа: /answer {chat_id}
    """
    
    kb = types.InlineKeyboardMarkup()
    kb.add(
        types.InlineKeyboardButton("✏️ Ответить", callback_data=f"reply_to_{chat_id}"),
        types.InlineKeyboardButton("📜 История переписки", callback_data=f"show_history_{chat_id}")
    )
    
    try:
        bot.send_message(YOUR_TELEGRAM_ID, forward_text, reply_markup=kb)
    except Exception as e:
        print(f"❌ Ошибка пересылки админу: {e}")
    
    bot.send_message(chat_id, "📩 Ваше сообщение отправлено менеджеру. Мы ответим в ближайшее время!", reply_markup=main_keyboard())

def forward_media_to_admin(message, chat_id, content_description):
    user_info = user_data.get(chat_id, {})
    username = user_info.get("username", "неизвестный")
    full_name = user_info.get("full_name", "Неизвестный")
    
    info_text = f"""
📩 МЕДИАФАЙЛ ОТ КЛИЕНТА

👤 Имя: {full_name}
🏷️ Username: {username}
🆔 ID: {chat_id}
📎 Тип: {content_description}
🕐 Время: {datetime.now().strftime("%d.%m.%Y %H:%M")}

📌 Для ответа: /answer {chat_id}
    """
    
    kb = types.InlineKeyboardMarkup()
    kb.add(
        types.InlineKeyboardButton("✏️ Ответить", callback_data=f"reply_to_{chat_id}"),
        types.InlineKeyboardButton("📜 История переписки", callback_data=f"show_history_{chat_id}")
    )
    
    try:
        bot.send_message(YOUR_TELEGRAM_ID, info_text, reply_markup=kb)
        bot.copy_message(YOUR_TELEGRAM_ID, chat_id, message.message_id)
    except Exception as e:
        bot.send_message(YOUR_TELEGRAM_ID, f"❌ Не удалось переслать файл от {full_name} (ID: {chat_id}): {e}")
    
    bot.send_message(chat_id, "📩 Ваше сообщение отправлено менеджеру. Мы ответим в ближайшее время!", reply_markup=main_keyboard())

def process_booking(chat_id, text):
    global app_id_counter
    state = user_states[chat_id]["step"]

    if state == "name":
        if text == "🔙 Назад в меню":
            del user_states[chat_id]
            bot.send_message(chat_id, "❌ Запись отменена.", reply_markup=main_keyboard())
            bot.send_message(chat_id, MAIN_MENU_TEXT, reply_markup=main_keyboard())
            return
        
        user_states[chat_id]["name"] = text
        user_states[chat_id]["step"] = "phone"
        bot.send_message(chat_id, "📱 Напишите ваш контактный номер телефона\n\nНажмите на кнопку **«Поделиться номером»** ниже или отправьте номер в формате: 79998887766", reply_markup=phone_request_keyboard(), parse_mode='Markdown')

    elif state == "phone":
        if text == "🔙 Назад в меню":
            del user_states[chat_id]
            bot.send_message(chat_id, "❌ Запись отменена.", reply_markup=main_keyboard())
            bot.send_message(chat_id, MAIN_MENU_TEXT, reply_markup=main_keyboard())
            return
        
        clean_number = re.sub(r'[^\d+]', '', text)
        if clean_number.startswith('+'): clean_number = clean_number[1:]
        
        if len(clean_number) == 11 and (clean_number.startswith('7') or clean_number.startswith('8')):
            if clean_number.startswith('8'): clean_number = '7' + clean_number[1:]
            formatted_phone = f"+{clean_number[0]} {clean_number[1:4]} {clean_number[4:7]} {clean_number[7:9]} {clean_number[9:11]}"
            user_states[chat_id]["phone"] = clean_number
            user_states[chat_id]["formatted_phone"] = formatted_phone
            user_states[chat_id]["step"] = "tariff"
            bot.send_message(chat_id, f"📱 Номер: {formatted_phone}\n\n🚘 Теперь выберите категорию прав и тариф:\n\nНапример: B / Стандарт или А / Базовый", reply_markup=main_keyboard())
        else:
            bot.send_message(chat_id, "❌ **Номер введен в неправильном формате.**\n\nПожалуйста, нажмите на кнопку **«Поделиться номером»** ниже или отправьте номер в формате: 79998887766\n\nПример: 79998887766", reply_markup=phone_request_keyboard(), parse_mode='Markdown')

    elif state == "tariff":
        if text == "🔙 Назад в меню":
            del user_states[chat_id]
            bot.send_message(chat_id, "❌ Запись отменена.", reply_markup=main_keyboard())
            bot.send_message(chat_id, MAIN_MENU_TEXT, reply_markup=main_keyboard())
            return
        
        user_states[chat_id]["tariff"] = text
        user_states[chat_id]["step"] = "start_date"
        bot.send_message(chat_id, "📅 Когда планируете начать обучение?\n\n(Напишите месяц или дату, или «как можно скорее»)")

    elif state == "start_date":
        if text == "🔙 Назад в меню":
            del user_states[chat_id]
            bot.send_message(chat_id, "❌ Запись отменена.", reply_markup=main_keyboard())
            bot.send_message(chat_id, MAIN_MENU_TEXT, reply_markup=main_keyboard())
            return
        
        user_states[chat_id]["start_date"] = text
        user = user_states.pop(chat_id)

        application = {
            "id": app_id_counter,
            "name": user['name'],
            "phone": user.get('formatted_phone', user['phone']),
            "tariff": user['tariff'],
            "start_date": user['start_date'],
            "time": datetime.now().strftime("%d.%m.%Y %H:%M"),
            "status": "new"
        }
        applications.append(application)
        app_id_counter += 1

        app_text = f"""
📝 **НОВАЯ ЗАЯВКА #{application['id']}**

👤 Имя: {user['name']}
📱 Телефон: {application['phone']}
🚗 Тариф: {user['tariff']}
📅 Начало: {user['start_date']}
🕐 Время: {application['time']}
        """
        
        kb = types.InlineKeyboardMarkup()
        kb.add(
            types.InlineKeyboardButton("✅ В обработку", callback_data=f"status_{application['id']}_processing"),
            types.InlineKeyboardButton("✔️ Выполнено", callback_data=f"status_{application['id']}_completed"),
            types.InlineKeyboardButton("📜 История переписки", callback_data=f"show_history_{chat_id}")
        )

        try:
            bot.send_message(YOUR_TELEGRAM_ID, app_text, reply_markup=kb, parse_mode='Markdown')
        except Exception as e:
            print(f"❌ Ошибка отправки заявки админу: {e}")

        bot.send_message(chat_id, f"✅ **Спасибо! Ваша заявка принята.** 🙌\n\nМенеджер свяжется с вами в ближайшее время.\n\n📞 По любым вопросам: {PHONE}", reply_markup=main_keyboard(), parse_mode='Markdown')

def reply_to_user(admin_chat_id, text):
    user_id = admin_reply_mode[admin_chat_id]
    try:
        save_conversation(user_id, text, is_from_client=False)
        bot.send_message(user_id, f"📩 **Ответ от менеджера:**\n\n{text}\n\n_Если у вас есть ещё вопросы, просто напишите сюда._", reply_markup=main_keyboard(), parse_mode='Markdown')
        bot.send_message(admin_chat_id, f"✅ Ответ отправлен пользователю {user_id}")
    except Exception as e:
        bot.send_message(admin_chat_id, f"❌ Ошибка отправки: {e}")
    del admin_reply_mode[admin_chat_id]

@bot.callback_query_handler(func=lambda call: call.data.startswith("reply_to_"))
def start_reply(call):
    if call.message.chat.id != YOUR_TELEGRAM_ID:
        bot.answer_callback_query(call.id, "⛔ Нет доступа")
        return
    user_id = int(call.data.split("_")[2])
    admin_reply_mode[call.message.chat.id] = user_id
    bot.answer_callback_query(call.id, "✏️ Введите ответ")
    bot.send_message(call.message.chat.id, f"✏️ Введите ответ для пользователя {user_id}. Для отмены /cancel_answer")

@bot.callback_query_handler(func=lambda call: call.data.startswith("status_"))
def change_status(call):
    if call.message.chat.id != YOUR_TELEGRAM_ID:
        bot.answer_callback_query(call.id, "⛔ Нет доступа")
        return
    
    parts = call.data.split("_")
    app_id = int(parts[1])
    new_status = parts[2]
    
    for app in applications:
        if app['id'] == app_id:
            app['status'] = new_status
            break
    
    status_text = {"processing": "🔄 В обработке", "completed": "✅ Выполнено"}
    bot.answer_callback_query(call.id, f"Статус изменён на: {status_text.get(new_status, new_status)}")
    
    if not applications:
        bot.edit_message_text("📭 Заявок пока нет.", call.message.chat.id, call.message.message_id)
        return
    
    text = "📋 ВСЕ ЗАЯВКИ:\n\n"
    for app in applications:
        status_emoji = {"new": "🆕", "processing": "🔄", "completed": "✅"}.get(app['status'], "🆕")
        text += f"{status_emoji} Заявка #{app['id']}\n👤 {app['name']}\n📱 {app['phone']}\n🚗 {app['tariff']}\n📅 {app['start_date']}\n🕐 {app['time']}\n📌 Статус: {app['status']}\n➖➖➖➖➖➖➖➖➖➖\n"
    
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("🔄 Обновить", callback_data="refresh_admin"))
    kb.add(types.InlineKeyboardButton("🔙 Назад", callback_data="back_to_admin"))
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=kb)

# ========= ЗАПУСК БОТА =========
if __name__ == "__main__":
    print("=" * 50)
    print("🚗 Бот «Фулл Драйв» запущен!")
    print(f"📋 Заявки приходят на ID: {YOUR_TELEGRAM_ID}")
    print("=" * 50)
    # Убираем input(), так как бот работает в фоне
    bot.infinity_polling()