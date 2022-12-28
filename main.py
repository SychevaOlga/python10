import telebot, os.path, datetime
from telebot import types

bot = telebot.TeleBot("TOKEN")

def OpenListW():
    check_file = os.path.isfile('log.txt')
    if check_file == False:
        file = open('log.txt', 'w')
        file.close()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 'Привет. Это бот калькулятор. Посчитаем? /Yes')

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.send_message(message.from_user.id, "Введи любое число")
    bot.register_next_step_handler(message, number1)

def number1(message):
    number1 = message.text
    file = open('log.txt', 'a')
    file.write(str(f"{datetime.datetime.now()} {message.from_user.username}: {number1}\n"))
    file.close()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    itembtn1 = types.KeyboardButton('+')
    itembtn2 = types.KeyboardButton('-')
    itembtn3 = types.KeyboardButton('*')
    itembtn4 = types.KeyboardButton('/')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
    msg = bot.send_message(message.chat.id, "Выберете операцию", reply_markup=markup)
    bot.register_next_step_handler(msg, operator, number1)

def operator(message, number1):
    operator = message.text
    bot.send_message(message.from_user.id, f"Введи второе число")
    bot.register_next_step_handler(message, result, number1, operator)
    file = open('log.txt', 'a')
    file.write(str(f"{datetime.datetime.now()} {message.from_user.username}: {operator}\n"))
    file.close()

def result(message, number1, operator):
    number2 = message.text
    number1 = ''.join([i for i in number1 if i in '0123456789.'])
    number2 = ''.join([i for i in number2 if i in '0123456789.'])
    operator = ''.join([i for i in operator if i in '*/-+'])

    file = open('log.txt', 'a')
    file.write(str(f"{datetime.datetime.now()} {message.from_user.username}: {number2}\n"))

    if number1 != '' and number2 != '' and operator != '':
        number1, number2 = float(number1), float(number2)
        if operator == '/':
            summa = number1 / number2
            bot.send_message(message.from_user.id, f"Результат {number1} {operator} {number2} = {summa}")
        elif operator == '*':
            summa = number1 * number2
            bot.send_message(message.from_user.id, f"Результат {number1} {operator} {number2} = {summa}")
        elif operator == '-':
            summa = number1 - number2
            bot.send_message(message.from_user.id, f"Результат {number1} {operator} {number2} = {summa}")
        elif operator == '+':
            summa = number1 + number2
            bot.send_message(message.from_user.id, f"Результат {number1} {operator} {number2} = {summa}")

        bot.send_message(message.from_user.id, "Посчитаем еще? :-) /Yes")

        file.write(str(f"{datetime.datetime.now()} {message.from_user.username}: Результат {number1} {operator} {number2} = {summa}\n"))

    else:
        bot.send_message(message.from_user.id, "Что-то пошло не так. Начать сначала? /Yes")
        file.write(str(f"{datetime.datetime.now()} {message.from_user.username}: Что-то пошло не так"))

    file.close()

bot.polling()