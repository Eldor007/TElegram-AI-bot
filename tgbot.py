import os
import openai
import time
import telegram
from telegram import Bot, Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, CallbackContext
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
import time
import threading
import urllib3


class ChatGPTBot:
    import openai
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

    def __init__(self, telegram_token, openai_api_key):
        self.bot = Bot(token=telegram_token)
        self.openai_api_key = openai_api_key
        openai.api_key = openai_api_key

        # Словарь для отслеживания реферралов
        self.referral_dict = {}

        # Хранилище для статистики
        self.referral_stats = {}

        self.user_requests = {}
        print("HUYYYYY ", telegram.__version__)
        self.reply_markup = self.create_reply_markup()
        self.updater = Updater(token=telegram_token, use_context=True)
        self.dispatcher = self.updater.dispatcher
        self.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, self.handle_message))
        # Обработчик для анализа реферральных ссылок
        self.dispatcher.add_handler(CallbackQueryHandler(self.referral_handler, pattern='^\\d+$'))
        # Обработчик команды /stats
        # user = update.message.from_user
        # chat_id = user.id
        self.dispatcher.add_handler(CommandHandler("stats", self.stats))
        # self.dispatcher.add_handler(CommandHandler("start", self.start_message(chat_id)))
        self.start_daily_reset_thread()
        self.start_polling()

    def is_user_subscribed(self, user_id, channel_username):
        try:
            user_status = self.bot.get_chat_member(chat_id=channel_username, user_id=user_id).status
            if user_status in ['member', 'administrator', 'creator']:
                return True
        except Exception as e:
            print(f"Error checking subscription status: {e}")
        return False

    def start_daily_reset_thread(self):
        # Создаем поток, который будет выполняться каждый день в 8 утра
        reset_thread = threading.Thread(target=self.daily_reset_thread)
        reset_thread.daemon = True
        reset_thread.start()

    def daily_reset_thread(self):
        while True:
            current_time = time.localtime()
            if current_time.tm_hour == 2 and current_time.tm_min == 29:
                # Сброс значений для всех пользователей
                self.reset_user_requests()
            # Ждем 1 минуту перед следующей проверкой
            time.sleep(60)

    def reset_user_requests(self):
        # Сброс значений для всех пользователей
        for user_id in self.user_requests:
            self.user_requests[user_id] = 10

    def start_message(self, chat_id):
        message = f"""🤖 Привет,{chat_id}! Я бот ChatGPT!

                                🔗 Вы можете задавать любые вопросы

                                Также бот иногда может грузить ответ в течении нескольких минут. Все зависит от серверов на стороне OpenAI!

                                Советы к правильному использованию:
                                – Задавайте осмысленные вопросы, расписывайте детальнее.
                                – Не пишите ерунду иначе одержите её же в ответ.

                                Примеры вопросов/запросов:
                                ~ Сколько будет 7 * 8?
                                ~ Когда началась Вторая Мировая?
                                ~ Напиши код калькулятора на Python
                                ~ Напиши сочинение как я провел лето

                                🔥 Чтобы начать общение, напиши что-нибудь CHATGPT в строку ниже 👇🏻"""
        return message

    def start(self, update: Update, context: CallbackContext):
        user_id = update.effective_user.id
        channel_username = '@uzbopenai'  # Replace with your channel's username
        check = self.is_user_subscribed(user_id, channel_username)
        if not check:
            update.message.reply_text(
                f'Пожалуйста подпишитесь на канал {channel_username} чтобы получить доступ к бесплатному чат-боту 🤖')
            return False
        else:
            # update.message.reply_text('Welcome to the bot! Thank you for subscribing.')
            return True



    def create_referal_message(self, update, chat_id):
        user = update.message.from_user
        referral_code = user.id  # Пример использования ID пользователя как реферрального кода
        self.referral_dict[referral_code] = user.id
        text = f"Привет, {user.first_name}! Твоя реферральная ссылка: t.me/Gptuz_chatbot?start={referral_code}"
        self.user_requests[chat_id] += 1
        return text

    def premium_podpiska(self, chat_id):
        premium_subscription_info = """
                Скоро Премиум Подписка!
🛠
Наши разработки Премиум Подписки почти завершены. 
Ожидайте доступ в ближайшие дни. 
Спасибо за ваш интерес!

                """
        self.bot.send_message(chat_id=chat_id, text=premium_subscription_info)

    def create_reply_markup(self):
        buttons = [
            [KeyboardButton("начать новый диалог")],
            [KeyboardButton("❓ Что я умею")],
            [KeyboardButton("👤 Мой профиль")],
            [KeyboardButton("🔒 Премиум подписка")],
        ]
        return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

    def create_referal_button(self):
        buttons = [
            [KeyboardButton("Пригласить человека")],
            [KeyboardButton("На главную страницу")],
        ]
        return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

    def send_loading_bar(self, chat_id):
        message = self.bot.send_message(chat_id, "Обработка")
        for i in range(1, 3):
            time.sleep(1)  # Simulate work
            progress = f"Обработка {'⌛' * i}"
            self.bot.edit_message_text(chat_id=chat_id, message_id=message.message_id, text=progress)

        self.bot.edit_message_text(chat_id=chat_id, message_id=message.message_id, text="Обработка завершена! ✅")
        return message.message_id

    def delete_message_by_id(self, chat_id, message_id):
        self.bot.delete_message(chat_id=chat_id, message_id=message_id)

    def handle_message(self, update: Update, context: CallbackContext):

        if not self.start(update, context):
            return
        user_input = update.message.text
        chat_id = update.effective_chat.id
        context.bot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.TYPING)

        if user_input == "❓ Что я умею":
            predefined_message = self.generate_predefined_message()
            self.bot.send_message(chat_id=chat_id, text=predefined_message, reply_markup=self.reply_markup)
        elif user_input == "👤 Мой профиль":
            self.generate_user_profile(chat_id)
        elif user_input == "🔒 Премиум подписка":
            self.premium_podpiska(chat_id)
        elif user_input == "Пригласить человека":
            predefined_message = self.create_referal_message(update, chat_id)
            self.bot.send_message(chat_id=chat_id, text=predefined_message, reply_markup=self.reply_markup)
        elif user_input == "На главную страницу":
            predefined_message = self.generate_predefined_message()
            self.bot.send_message(chat_id=chat_id, text=predefined_message, reply_markup=self.reply_markup)
        elif user_input == "start":
            self.start_message(chat_id)
        elif user_input == "test_channel":
            self.start(chat_id)


        else:
            if chat_id not in self.user_requests:
                self.user_requests[chat_id] = 5

            if self.user_requests[chat_id] > 0:
                self.user_requests[chat_id] -= 1
                processing_id = self.send_loading_bar(chat_id)
                response = self.generate_response(user_input)
                self.bot.send_message(chat_id=chat_id, text=response, reply_markup=self.reply_markup)
                self.delete_message_by_id(chat_id, processing_id)
            else:
                self.bot.send_message(chat_id=chat_id,
                                      text="У вас закончились запросы. Пожалуйста, обратитесь за подпиской или пригласите друзей.",
                                      reply_markup=self.reply_markup)

    def generate_response(self, user_input):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Вы - полезный ассистент."},
                {"role": "user", "content": user_input},
            ],
        )
        response_text = response['choices'][0]['message']['content']
        return response_text

    def generate_predefined_message(self):
        predefined_message = """
    🔥 Давай расскажу чем я могу тебе помочь?

    1️⃣ Создать резюме. С моей помощью ты можешь устроиться на работу мечты, ведь я могу написать хорошее резюме
    2️⃣ Написать текст на любую тему. Это поможет тебе в работе и учебе
    3️⃣ Перевести текст с иностранного языка
    4️⃣ Ответить на интересующие тебя вопросы. Чаще всего у меня получается это лучше, чем у известных поисковиков
    5️⃣ Написать код, перевести его с одного языка на другой и найти ошибки
    6️⃣ Планировать и осуществлять расчеты. Например, ты можешь за считанные секунды получить готовый план питания для похудения

    💡 Это лишь малая часть моего функционала. Задавай мне любые задачи, а я постараюсь тебе помочь.

    Просто отправь мне сообщение 👇🏻
    """
        return predefined_message

    def generate_user_profile(self, user_id):

        if user_id not in self.user_requests:
            self.user_requests[user_id] = 5
        available_requests = self.user_requests[user_id]
        user_profile = f"""
    💬 Доступно запросов для ChatGPT: {available_requests}
    
    Зачем нужны запросы ChatGPT?

    Задавая вопросы - ты тратишь 1 запрос. Бесплатно можно тратить 5 запросов каждый день. Запросы восстанавливаются каждый день в 08:00 по Московскому времени.

    Не хватает запросов ChatGPT?

    1️⃣ Вы можете купить премиум-подписку для ChatGPT или запросы и не париться о лимитах.
    2️⃣ Вы можете пригласить человека в бота и получить за него 3 бесплатных запроса.
    3️⃣ Подписаться на наши каналы и получить бесплатный бонус в виде 5 бесплатных запросов, но это можно сделать лишь единожды
    """
        self.bot.send_message(chat_id=user_id, text=user_profile, reply_markup=self.create_referal_button())
        self.create_referal_button()
        return user_profile

    def start_polling(self):
        self.updater.start_polling()
        self.updater.idle()

    def referral_handler(self, update, context):
        query = update.callback_query
        referred_user_id = query.from_user.id
        chat_id = referred_user_id
        referring_user_id = int(query.data)

        if referring_user_id in self.referral_dict:
            referring_user = context.bot.get_chat(self.referral_dict[referring_user_id])
            referred_user = query.from_user
            query.answer(f"Ты присоединился с реферральной ссылкой от {referring_user.first_name}!")
            # Здесь вы можете добавить код для награждения пригласившего пользователя

    def stats(self, update, context):

        user = update.message.from_user
        print(user.id)
        MISHA_CHAT_ID = 364954921
        ELDOR_CHAT_ID = 121396902
        ADMIN_USER_ID = ELDOR_CHAT_ID

        if user.id == ADMIN_USER_ID or user.id == MISHA_CHAT_ID:  # Замените ADMIN_USER_ID на реальный ID администратора
            stats = self.referral_dict
            message = "Статистика реферральной активности:\n\n"
            for referring_user, referred_count in stats.items():
                referring_user_info = context.bot.get_chat(referring_user)
                message += f"{referring_user_info.first_name}: {referred_count} приглашенных\n"
            update.message.reply_text(message)
            print("referral_Stats: ", self.referral_stats)
            print("referral_dict: ", self.referral_dict)

        else:
            update.message.reply_text("У вас нет доступа к статистике.")


if __name__ == "__main__":
    # Set your Telegram bot token and OpenAI API key
    TELEGRAM_BOT_TOKEN = 'YOUR_TELEGRAMBOT_APIKEY'
    OPENAI_API_KEY = 'YOUR_OPENAI_APIKEY'
    chatgpt_bot = ChatGPTBot(TELEGRAM_BOT_TOKEN, OPENAI_API_KEY)