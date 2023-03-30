import telebot
from telebot import types

TOKEN = '5744319727:AAE6XN6P_s7ItvS4WOmWxUYa8uMmpy9UpEw'
bot = telebot.TeleBot(TOKEN)

age_flag = False
sex_flag = False
cp_flag = False
trestbps_flag = False
chol_flag = False
fbs_flag = False
restecg_flag = False
thalach_flag = False
exang_flag = False
oldpeak_flag = False
slope_flag = False

age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak = -1, -1, -1, -1, -1, -1, -1, -1, -1, -1.0
slope = -1

msg_id1, msg_id2 = -1, -1

msg1 = [
    "Приступаем к тесту!\n\nОтвечайте на запросы, чтобы запонить эти данные:",
    "\n\n🔴 1) Age:    Возраст пациента (лет)",
    "\n🔴 2) Sex:    Пол пациента",
    "\n🔴 3) ChestPainType:  Тип боли в груди",
    "\n🔴 4) RestingBP:  Артериальное давление в покое (мм рт.ст.)",
    "\n🔴 5) Cholesterol:    Холестерин сыворотки (мм/дл)",
    "\n🔴 6) FastingBS:  Уровень сахара в крови натощак (мг/дл)",
    "\n🔴 7) RestingECG: Результаты электрокардиограммы в покое",
    "\n🔴 8) MaxHR:  Достигнутая максимальная частота сердечных сокращений",
    "\n🔴 9) ExerciseAngina: Стенокардия, вызванная физической нагрузкой",
    "\n🔴 10) Oldpeak:   Числовое значение, измеренное при депрессии",
    "\n🔴 11) ST_Slope:  Наклон пикового сегмента ST при нагрузке",
]

not_del = -1


def df():
    global age_flag
    global sex_flag
    global cp_flag
    global trestbps_flag
    global chol_flag
    global fbs_flag
    global restecg_flag
    global thalach_flag
    global exang_flag
    global oldpeak_flag
    global slope_flag
    global msg1
    age_flag = False
    sex_flag = False
    cp_flag = False
    trestbps_flag = False
    chol_flag = False
    fbs_flag = False
    restecg_flag = False
    thalach_flag = False
    exang_flag = False
    oldpeak_flag = False
    slope_flag = False

    msg1 = [
        "Приступаем к тесту!\n\nОтвечайте на запросы, чтобы запонить эти данные:",
        "\n\n🔴 1) Age:    Возраст пациента (лет)",
        "\n🔴 2) Sex:    Пол пациента",
        "\n🔴 3) ChestPainType:  Тип боли в груди",
        "\n🔴 4) RestingBP:  Артериальное давление в покое (мм рт.ст.)",
        "\n🔴 5) Cholesterol:    Холестерин сыворотки (мм/дл)",
        "\n🔴 6) FastingBS:  Уровень сахара в крови натощак (мг/дл)",
        "\n🔴 7) RestingECG: Результаты электрокардиограммы в покое",
        "\n🔴 8) MaxHR:  Достигнутая максимальная частота сердечных сокращений",
        "\n🔴 9) ExerciseAngina: Стенокардия, вызванная физической нагрузкой",
        "\n🔴 10) Oldpeak:   Числовое значение, измеренное при депрессии",
        "\n🔴 11) ST_Slope:  Наклон пикового сегмента ST при нагрузке",
    ]


def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False


def msg(lst):
    s = ''
    for i in lst:
        s += i
    return s


def output(message):
    s = 'Ожидайте! Идет анализ данных...🔍'
    bot.edit_message_text(chat_id=message.chat.id, message_id=msg_id2, text=s)
    print(age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope)
    a = getPredictions_random(age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope)
    s = ''
    if str(a) == '[2]':
        s = 'К счастью, у вас нет болезней сердца!❤ Можете быть спокойным!'
    elif str(a) == '1':
        s = 'К сожалению, у вас больное сердце.‍❤️‍🩹 Мы настоятельно рекомендуем вам посетить кардиолога!'
    bot.edit_message_text(chat_id=message.chat.id, message_id=msg_id2, text=s)


def getPredictions_random(p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11):
    import joblib
    import numpy as np
    model = joblib.load('db/randomforest.pkl')
    arr = np.array([[p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11]])
    prediction = model.predict(arr)
    if prediction == 0:
        return "0"
    elif prediction == 1:
        return "1"
    else:
        return prediction


def del_mes(message):
    global not_del
    for i in range(message.message_id - not_del):
        try:
            bot.delete_message(message.chat.id, not_del + i + 1)
        except Exception as e:
            print(repr(e))
    not_del = message.message_id


@bot.message_handler(commands=['start'])
def start_command(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    a = types.KeyboardButton('/test')
    markup.add(a)
    sti1 = open('media/heart.tgs', 'rb')
    bot.send_sticker(message.chat.id, sti1)
    bot.send_message(message.chat.id,
                     "Добро пожаловать, " + message.from_user.first_name + "!"
                                                                           "\nЯ — бот, созданный, чтобы помочь вам "
                                                                           "выявить Сердечно-сосудистые заболевания с "
                                                                           "помощью Искусственного интеллекта."
                                                                           "\n\nВы можете управлять мной, отправив "
                                                                           "следующие команды: "
                                                                           "\n\n/test - начать тест 🔬."
                     .format(
                         message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup)


@bot.message_handler(commands=['test'])
def test_command(message):
    global msg_id1
    global msg_id2
    global not_del
    df()
    snt_msg = bot.send_message(message.chat.id, msg(msg1))
    msg_id1 = snt_msg.message_id
    snt_msg2 = bot.send_message(message.chat.id, "Напишите свой возраст: ")
    bot.register_next_step_handler(snt_msg2, age_handler)
    msg_id2 = snt_msg2.message_id
    not_del = msg_id2
    global age_flag
    age_flag = True


@bot.message_handler(content_types=['text'])
def age_handler(message):
    global age_flag
    global sex_flag
    if age_flag:
        if isinstance(message.text, str) and message.text.isdigit():
            global age
            age = int(message.text)
            age_flag = False

            msg1[1] = "\n\n🟢 1) Age:    " + message.text
            bot.edit_message_text(chat_id=message.chat.id, message_id=msg_id1, text=msg(msg1))

            del_mes(message)

            markup = types.InlineKeyboardMarkup()
            bM = types.InlineKeyboardButton('Мужской', callback_data='1')
            bF = types.InlineKeyboardButton('Женский', callback_data='2')
            markup.row(bM, bF)

            bot.edit_message_text(chat_id=message.chat.id, message_id=msg_id2, text="Выберите свой пол:",
                                  reply_markup=markup)

            sex_flag = True
        else:

            b = bot.send_message(message.chat.id, "Не правильная форма ввода. Напишите свой возраст: ")
            bot.register_next_step_handler(b, age_handler)
            age_flag = True


def trestbps_handler(message):
    global trestbps_flag
    global chol_flag
    if trestbps_flag:
        if isinstance(message.text, str) and message.text.isdigit():
            global trestbps
            trestbps = int(message.text)
            trestbps_flag = False

            msg1[4] = "\n🟢 4) RestingBP:  " + message.text
            bot.edit_message_text(chat_id=message.chat.id, message_id=msg_id1, text=msg(msg1))
            del_mes(message)

            chol_flag = True
            b = bot.edit_message_text(chat_id=message.chat.id, message_id=msg_id2,
                                      text="Напишите холестерин сыворотки (мм/дл)")
            bot.register_next_step_handler(b, chol_handler)
        else:
            b = bot.send_message(message.chat.id,
                                 "Не правильная форма ввода. Напишите артериальное давление в покое (мм рт.ст.)")
            bot.register_next_step_handler(b, trestbps_handler)
            trestbps_flag = True


def chol_handler(message):
    global chol_flag
    if chol_flag:
        if isinstance(message.text, str) and message.text.isdigit():
            global chol
            chol = int(message.text)
            chol_flag = False

            msg1[5] = "\n🟢 5) Cholesterol:    " + str(chol)
            bot.edit_message_text(chat_id=message.chat.id, message_id=msg_id1, text=msg(msg1))
            del_mes(message)

            global fbs_flag
            fbs_flag = True
            b = bot.edit_message_text(chat_id=message.chat.id, message_id=msg_id2,
                                      text="Напишите уровень сахара в крови натощак (мг/дл):")
            bot.register_next_step_handler(b, fbs_handler)
        else:
            b = bot.send_message(message.chat.id, "Не правильная форма ввода. Напишите холестерин сыворотки (мм/дл)")
            bot.register_next_step_handler(b, chol_handler)
            chol_flag = True


def fbs_handler(message):
    global fbs_flag
    if fbs_flag:
        if isinstance(message.text, str) and message.text.isdigit():
            global fbs

            fbs = int(message.text)
            fbs = max(min(fbs - 120, 1), 0) + 1
            fbs_flag = False

            msg1[6] = "\n🟢 6) FastingBS:  " + message.text
            bot.edit_message_text(chat_id=message.chat.id, message_id=msg_id1, text=msg(msg1))
            del_mes(message)

            markup = types.InlineKeyboardMarkup()
            b0 = types.InlineKeyboardButton('Обычный', callback_data='1')
            b1 = types.InlineKeyboardButton('Наличие аномалии ST-T', callback_data='2')
            b2 = types.InlineKeyboardButton("Гипертрофия левого желудочка", callback_data='3')
            markup.row(b0, b1)
            markup.row(b2)
            bot.edit_message_text(chat_id=message.chat.id, message_id=msg_id2,
                                  text="Выберите результаты электрокардиограммы в покое:", reply_markup=markup)
            global restecg_flag
            restecg_flag = True
        else:
            b = bot.send_message(message.chat.id,
                                 "Не правильная форма ввода. Напишите уровень сахара в крови натощак (мг/дл):")
            bot.register_next_step_handler(b, fbs_handler)
            fbs_flag = True


def thalach_handler(message):
    global thalach_flag
    if thalach_flag:
        if isinstance(message.text, str) and message.text.isdigit():
            global thalach
            thalach = int(message.text)
            thalach_flag = False

            msg1[8] = "\n🟢 8) MaxHR:  " + str(thalach)
            bot.edit_message_text(chat_id=message.chat.id, message_id=msg_id1, text=msg(msg1))
            del_mes(message)

            markup = types.InlineKeyboardMarkup()
            bM = types.InlineKeyboardButton('Дa', callback_data='2')
            bF = types.InlineKeyboardButton('Нет', callback_data='1')
            markup.row(bM, bF)
            bot.edit_message_text(chat_id=message.chat.id, message_id=msg_id2,
                                  text="Есть ли у вас стенокардия, вызванная физической нагрузкой?",
                                  reply_markup=markup)
            global exang_flag
            exang_flag = True
        else:
            b = bot.send_message(message.chat.id,
                                 "Не правильная форма ввода. Напишите максимальную достигнутую частоту "
                                 "сердечных сокращений:")
            bot.register_next_step_handler(b, thalach_handler)
            thalach = True


def oldpeak_handler(message):
    global oldpeak_flag
    if oldpeak_flag:
        if isinstance(message.text, str) and isfloat(message.text):
            global oldpeak
            oldpeak = float(message.text)
            oldpeak_flag = False

            msg1[10] = "\n🟢 10) Oldpeak:   " + message.text
            bot.edit_message_text(chat_id=message.chat.id, message_id=msg_id1, text=msg(msg1))
            del_mes(message)

            markup = types.InlineKeyboardMarkup()
            b1 = types.InlineKeyboardButton('Восходящий', callback_data='1')
            b2 = types.InlineKeyboardButton('Плоский', callback_data='2')
            b3 = types.InlineKeyboardButton('Спуск', callback_data='3')
            markup.row(b1, b2, b3)
            bot.edit_message_text(chat_id=message.chat.id, message_id=msg_id2,
                                  text="Выберите наклон пикового сегмента ST в упражнении :",
                                  reply_markup=markup)
            global slope_flag
            slope_flag = True
        else:
            bot.send_message(message.chat.id, "Напишите относительную депрессию ST, вызванную физическими упражнениями")
            oldpeak_flag = True


@bot.callback_query_handler(func=lambda call: True)
def handle(call):
    try:
        global sex_flag
        global cp_flag
        global restecg_flag
        global exang_flag
        global slope_flag
        if sex_flag:
            global sex
            sex = int(call.data)
            sex_flag = False

            gender = 'Мужской' if sex == 1 else 'Женский'
            msg1[2] = "\n🟢 2) Sex:    " + gender
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=msg_id1, text=msg(msg1))

            markup = types.InlineKeyboardMarkup()
            b1 = types.InlineKeyboardButton('Типичная стенокардия', callback_data='4')
            b2 = types.InlineKeyboardButton('Атипичная стенокардия', callback_data='1')
            b3 = types.InlineKeyboardButton('Неангинозная боль', callback_data='2')
            b4 = types.InlineKeyboardButton('Бессимптомный', callback_data='3')
            markup.row(b1, b2)
            markup.row(b3, b4)

            bot.edit_message_text(chat_id=call.message.chat.id, message_id=msg_id2, text="Выберите тип боли в груди:",
                                  reply_markup=markup)

            cp_flag = True
        elif cp_flag:
            global cp
            cp = int(call.data)
            cp_flag = False

            cp_msg = 'Атипичная стенокардия'
            if cp == 4:
                cp_msg = 'Типичная стенокардия'
            elif cp == 2:
                cp_msg = 'Неангинозная боль'
            elif cp == 3:
                cp_msg = 'Бессимптомный'

            msg1[3] = "\n🟢 3) ChestPainType:  " + cp_msg
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=msg_id1, text=msg(msg1))

            global trestbps_flag
            trestbps_flag = True

            _ms = bot.edit_message_text(chat_id=call.message.chat.id, message_id=msg_id2,
                                        text="Напиши артериальное давление в покое (мм рт.ст.)")
            bot.register_next_step_handler(_ms, trestbps_handler)

        elif restecg_flag:
            global restecg
            restecg = int(call.data)
            restecg_flag = False

            restecg_msg = 'Обычный'
            if restecg == 2:
                restecg_msg = 'Наличие аномалии ST-T'
            elif restecg == 3:
                restecg_msg = 'Гипертрофия левого желудочка'

            msg1[7] = "\n🟢 7) RestingECG: " + restecg_msg
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=msg_id1, text=msg(msg1))

            global thalach_flag
            thalach_flag = True
            _ms = bot.edit_message_text(chat_id=call.message.chat.id, message_id=msg_id2,
                                        text="Напишите максимальную достигнутую частоту сердечных сокращений:")
            bot.register_next_step_handler(_ms, thalach_handler)
        elif exang_flag:
            global exang
            exang = int(call.data)
            exang_flag = False

            exang_msg = 'Нет'
            if call.data == '2':
                exang_msg = 'Да'

            msg1[9] = "\n🟢 9) ExerciseAngina: " + exang_msg
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=msg_id1, text=msg(msg1))

            global oldpeak_flag
            oldpeak_flag = True
            _ms = bot.edit_message_text(chat_id=call.message.chat.id, message_id=msg_id2,
                                        text="Напишите относительную депрессию ST, вызванную физическими упражнениями")
            bot.register_next_step_handler(_ms, oldpeak_handler)
        elif slope_flag:
            global slope
            slope = int(call.data)
            slope_flag = False
            slope_msg = 'Восходящий'
            if slope == 2:
                slope_msg = 'Плоский'
            elif slope == 3:
                slope_msg = 'Спуск'

            msg1[11] = "\n🟢 11) ST_Slope:  " + slope_msg
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=msg_id1, text=msg(msg1))

            print('final', output(call.message))

    except Exception as e:
        print(repr(e))


bot.polling()
