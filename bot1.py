import telebot
from telebot import types

bot = telebot.TeleBot("6770824878:AAG9YHmQAgWYiu3S8g3gYNtnNDhW9F_fnFU")

# Создаем словарь для хранения данных пользователей
user_data = {}

# Создаем класс для хранения данных одного пользователя


class User:
    def __init__(self, name, surname, id, photo):
        self.name = name
        self.surname = surname
        self.id = id
        self.photo = photo


@bot.message_handler(commands=["start"])
def handle_start(message):
    # Проверяем, есть ли пользователь в словаре
    if message.chat.id not in user_data:
        # Если нет, создаем новый объект User и добавляем его в словарь
        user_data[message.chat.id] = User("", "", "", "")
        # Отправляем сообщение с просьбой отправить фото
        bot.send_message(message.chat.id, "Отправьте ваше фото")
        # Переходим к следующему шагу
        bot.register_next_step_handler(message, get_photo)
    else:
        # Если есть, отправляем сообщение с просьбой выбрать действие
        bot.send_message(message.chat.id, "Выберите действие")
        # Создаем инлайн клавиатуру с одной кнопкой
        keyboard = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton(
            "Показать данные", callback_data="show_data")
        keyboard.add(button)
        # Отправляем клавиатуру в ответ
        bot.send_message(message.chat.id, "Нажмите на кнопку",
                         reply_markup=keyboard)


def get_photo(message):
    # Получаем file_id фото, которое отправил пользователь
    file_id = message.photo[-1].file_id
    # Сохраняем file_id в объекте User
    user_data[message.chat.id].photo = file_id
    # Отправляем сообщение с просьбой ввести данные
    bot.send_message(message.chat.id, "Введите ваши данные")
    # Создаем инлайн клавиатуру с тремя кнопками
    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Имя", callback_data="get_name")
    button2 = types.InlineKeyboardButton(
        "Фамилия", callback_data="get_surname")
    button3 = types.InlineKeyboardButton("ID", callback_data="get_id")
    keyboard.add(button1, button2, button3)
    # Отправляем клавиатуру в ответ
    bot.send_message(message.chat.id, "Нажмите на кнопку",
                     reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    # Обрабатываем нажатия на кнопки
    if call.data == "get_name":
        # Отправляем сообщение с просьбой ввести имя
        bot.send_message(call.message.chat.id, "Введите ваше имя")
        # Переходим к следующему шагу
        bot.register_next_step_handler(call.message, save_name)
    elif call.data == "get_surname":
        # Отправляем сообщение с просьбой ввести фамилию
        bot.send_message(call.message.chat.id, "Введите вашу фамилию")
        # Переходим к следующему шагу
        bot.register_next_step_handler(call.message, save_surname)
    elif call.data == "get_id":
        # Отправляем сообщение с просьбой ввести ID
        bot.send_message(call.message.chat.id, "Введите ваш ID")
        # Переходим к следующему шагу
        bot.register_next_step_handler(call.message, save_id)
    elif call.data == "show_data":
        # Получаем объект User из словаря
        user = user_data[call.message.chat.id]
        # Формируем сообщение с данными пользователя
        msg = f"Ваши данные:\nИмя: {user.name}\nФамилия: {
            user.surname}\nID: {user.id}"
        # Отправляем сообщение в ответ
        bot.send_message(call.message.chat.id, msg)
        # Отправляем фото в ответ
        bot.send_photo(call.message.chat.id, user.photo)


def save_name(message):
    # Получаем имя пользователя и сохраняем его в объекте User
    user_data[message.chat.id].name = message.text
    # Отправляем сообщение с подтверждением
    bot.send_message(message.chat.id, "Ваше имя успешно сохранено")


def save_surname(message):
    # Получаем фамилию пользователя и сохраняем ее в объекте User
    user_data[message.chat.id].surname = message.text
    # Отправляем сообщение с подтверждением
    bot.send_message(message.chat.id, "Ваша фамилия успешно сохранена")


def save_id(message):
    # Получаем ID пользователя и сохраняем его в объекте User
    user_data[message.chat.id].id = message.text
    # Отправляем сообщение с подтверждением
    bot.send_message(message.chat.id, "Ваш ID успешно сохранен")
    # Создаем инлайн клавиатуру с одной кнопкой
    keyboard = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(
        "Показать данные", callback_data="show_data")
    keyboard.add(button)
    # Отправляем клавиатуру в ответ
    bot.send_message(message.chat.id, "Нажмите на кнопку",
                     reply_markup=keyboard)


bot.polling()
