import vk_api, json, flashtext
import re
from vk_api.longpoll import VkLongPoll, VkEventType
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from platform import python_version
from flashtext.keyword import KeywordProcessor


vk_session = vk_api.VkApi(token="7450d860be2562a49962c50a4616fb6cdb985c0546fc8c5f217a88164b59bc2527d58c7efe7f2e69ade64")
vk = vk_session.get_api()
longpol = VkLongPoll(vk_session)


def get_but(text, color):
    return {
        "action": {
            "type": "text",
            "payload": "{\"button\": \"" + "1" + "\"}",
            "label": f"{text}"
        },
        "color": f"{color}"
    }


keyboarda = {
    "one_time": True,
    "buttons": [
        [get_but('Да', 'positive'), get_but('Нет', 'negative')],
    ]
}
keyboarda = json.dumps(keyboarda, ensure_ascii=False).encode('utf-8')
keyboarda = str(keyboarda.decode('utf-8'))

keyboardb = {
    "one_time": True,
    "buttons": [
        [get_but('Не могу войти на сайт', 'positive')],
        [get_but('Иные проблемы', 'primary')]
    ]
}
keyboardb = json.dumps(keyboardb, ensure_ascii=False).encode('utf-8')
keyboardb = str(keyboardb.decode('utf-8'))

keyboardс = {
    "one_time": True,
    "buttons": [
        [get_but('Я обучаюсь в ВГУ', 'primary'), get_but('Я сторонний пользователь', 'negative')],
        [get_but('Я преподаватель или сотрудник ВГУ', 'positive')]
    ]
}
keyboardс = json.dumps(keyboardс, ensure_ascii=False).encode('utf-8')
keyboardс = str(keyboardс.decode('utf-8'))

keyboard_otmena = {
    "one_time": True,
    "buttons": [
        [get_but('Отменить', 'negative')]
    ]
}
keyboard_otmena = json.dumps(keyboard_otmena, ensure_ascii=False).encode('utf-8')
keyboardс_otmena = str(keyboard_otmena.decode('utf-8'))

keyboard_hi = {
    "one_time": True,
    "buttons": [
        [get_but('Привет', 'positive'), get_but('Пока', 'primary')]
    ]
}
keyboard_hi = json.dumps(keyboard_hi, ensure_ascii=False).encode('utf-8')
keyboard_hi = str(keyboard_hi.decode('utf-8'))

keyboard_vsu = {
    "one_time": True,
    "buttons": [
        [get_but('Изучение учебных курсов', 'positive'), get_but('Загрузка ВКР', 'positive')],
        [get_but('Доступ к рабочим программам', 'positive'), get_but('Другое', 'secondary')]
    ]
}
keyboard_vsu = json.dumps(keyboard_vsu, ensure_ascii=False).encode('utf-8')
keyboard_vsu = str(keyboard_vsu.decode('utf-8'))

keyboard_good = {
    "one_time": True,
    "buttons": [
        [get_but('OK', 'positive'), get_but('Отменить', 'negative')]
    ]
}
keyboard_good = json.dumps(keyboard_good, ensure_ascii=False).encode('utf-8')
keyboard_good = str(keyboard_good.decode('utf-8'))

def sendera(id, some_text):
    vk_session.method('messages.send', {'user_id': id, 'message': some_text, 'random_id': 0, 'keyboard': keyboarda})

def senderb(id, some_text):
    vk_session.method('messages.send', {'user_id': id, 'message': some_text, 'random_id': 0, 'keyboard': keyboardb})

def senderс(id, some_text):
    vk_session.method('messages.send', {'user_id': id, 'message': some_text, 'random_id': 0, 'keyboard': keyboardс})

def sender_otmena(id, some_text):
    vk_session.method('messages.send', {'user_id': id, 'message': some_text, 'random_id': 0, 'keyboard': keyboard_otmena})

def sender_hi(id, some_text):
    vk_session.method('messages.send', {'user_id': id, 'message': some_text, 'random_id': 0, 'keyboard': keyboard_hi})

def sender_vsu(id, some_text):
    vk_session.method('messages.send', {'user_id': id, 'message': some_text, 'random_id': 0, 'keyboard': keyboard_vsu})

def sender_good(id, some_text):
    vk_session.method('messages.send', {'user_id': id, 'message': some_text, 'random_id': 0, 'keyboard': keyboard_good})



def logic():
    for event in longpol.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                id = event.user_id
                msg = event.text.lower()
                if msg == 'не могу войти на сайт':
                    senderс(id, "Ничего страшного, выберите один из вариантов в меню!")
                    logic_password()
                    break
                else:
                    sender_otmena(id, "Кратко опишите свою проблему!")
                    logic_other()
                    break

def logic_other():
    for event in longpol.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                id = event.user_id
                msg_old = event.text.lower()




                meseg = re.sub(r'[^\w\s]', ' ', msg_old)
                keyword_processor = KeywordProcessor()
                keyword_processor.add_keyword_from_file('msg_list.txt')
                new_sentence = keyword_processor.replace_keywords(meseg)
                msg_list = new_sentence.split()
                with open("question_list.txt", "r", encoding="utf-8") as f:
                    questions_list = f.readlines()
                    f.close()
                number_of_elements = len(questions_list)
                number = int(number_of_elements / 2)

                with open("question_list.txt", "r", encoding="utf-8") as f:

                    for x in range(number):
                        slovo = f.readline()
                        question = f.readline()
                        slovo = slovo.strip()
                        question = question.strip()
                        if slovo in msg_list:
                            break
                    f.close()

                dostup_list = ['логин', 'пароль']

                if slovo in msg_list:
                    sendera(id, question)
                    for event in longpol.listen():
                        if event.type == VkEventType.MESSAGE_NEW:
                            if event.to_me:
                                id = event.user_id
                                msg2 = event.text.lower()
                                if msg2 == 'да':
                                    if slovo in dostup_list:
                                        senderс(id, "Ничего страшного, довольно частое явление! Выберите один из вариантов в меню ниже!")
                                        logic_password()
                                    else:
                                        sender_otmena(id, "Так-так... Оставьте свою электронную почту для ответа техподдержки!")
                                        logic_email(msg_old, question)
                                        break
                                else:
                                    sender_otmena(id, "Так-так... Оставьте свою электронную почту для ответа техподдержки!")
                                    question = "Предположений нет."
                                    logic_email(msg_old, question)
                else:
                    if msg_old == 'отменить':
                        sender_hi(id, "Обращайтесь когда понадобится помощь! Бип-боп!")
                        main()
                        break
                    else:
                        sender_otmena(id, "Оставьте свою электронную почту для ответа техподдержки!")
                        question = "Предположений нет."
                        logic_email(msg_old, question)


def logic_email(msg_old, question):
    for event in longpol.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                id = event.user_id
                msg2 = event.text.lower()
                if msg2 == 'отменить':
                    sender_hi(id, "Обращайтесь когда понадобится помощь! Бип-боп!")
                    main()
                    break
                else:
                    sender_hi(id, "Письмо с описанием вашей проблемы отправлено на почту тех поддержки, ждите ответа!")

                    server = 'smtp.gmail.com'
                    user = 'aakorotchenko@gmail.com'
                    password = 'TP1M9da5ebr'

                    recipients = ['ankorotchenko@gmail.com']
                    otpravitel = 'aakorotchenko@gmail.com'
                    subject = 'ВК_БОТ_ТЕХПОДЕРЖКА'
                    x = str(id)
                    q = question
                    z = "Предположение темы вопроса созданное ботом: "
                    c = "Запрос на помощь пользователю: "
                    d = "Сообщение о проблеме от пользователя: "
                    e = "Email пользователя: "
                    text = msg2
                    html = '<html><head></head><body><p>' + c + '<br>' + d + "(" + msg_old + ")" + '<br>' + z + q + '<br>' + e + text + '<br>' + "id" + x + '</p></body></html>'

                    soobshenie = MIMEMultipart('alternative')
                    soobshenie['Subject'] = subject
                    soobshenie['From'] = 'Сообщение техподдеркже <' + otpravitel + '>'
                    soobshenie['To'] = ', '.join(recipients)
                    soobshenie['Reply-To'] = otpravitel
                    soobshenie['Return-Path'] = otpravitel
                    soobshenie['X-Mailer'] = 'Python/' + (python_version())

                    part_text = MIMEText(text, 'plain')
                    part_html = MIMEText(html, 'html')

                    soobshenie.attach(part_text)
                    soobshenie.attach(part_html)

                    mail = smtplib.SMTP_SSL(server)
                    mail.login(user, password)
                    mail.sendmail(otpravitel, recipients, soobshenie.as_string())
                    mail.quit()

                    main()


def logic_password():
    for event in longpol.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                id = event.user_id
                msg = event.text.lower()
                if msg == 'я обучаюсь в вгу':
                    sender_good(id, "Пожалуйста, заполните форму и с вами свяжется техподдержка!")
                    logic_student()
                    break
                else:
                    sender_otmena(id, "Оставьте свою электронную почту для ответа техподдержки!")
                    msg_old = "Преподователь, работник или иной пользователь не обучающийся в вгу."
                    question = "Востановление пароля или логина."
                    logic_email(msg_old, question)
                    break

def logic_student():
    for event in longpol.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                id = event.user_id
                msg = event.text.lower()
                if msg == 'отменить':
                    sender_hi(id, "Обращайтесь когда понадобится помощь! Бип-боп!")
                    main()
                    break
                else:
                    sender_vsu(id, "Укажите цель использования портала на выбор из меню ниже!")
                    logic_student_a()

def logic_student_a():
    for event in longpol.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                id = event.user_id
                msg = event.text.lower()
                if msg == 'отменить':
                    sender_hi(id, "Обращайтесь когда понадобится помощь! Бип-боп!")
                    main()
                    break
                else:
                    sender_otmena(id, "Укажите фамилию!")
                    x = str(id)
                    with open("recovery_list.txt", "a", encoding="utf-8") as f:
                        f.write("Студент. Запрос на востановление доступа:" + '\n' + "id" + x + " Укажите цель! " + " Ответ: " + msg + '\n')

                    logic_student_b()


def logic_student_b():
    for event in longpol.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                id = event.user_id
                msg = event.text.lower()
                if msg == 'отменить':
                    sender_hi(id, "Обращайтесь когда понадобится помощь! Бип-боп!")
                    main()
                    break
                else:
                    sender_otmena(id, "Укажите имя!")
                    x = str(id)
                    with open("recovery_list.txt", "a", encoding="utf-8") as f:
                        f.write("id" + x + " Укажите фамилию! " + " Ответ: " + msg + '\n')
                    logic_student_с()

def logic_student_с():
    for event in longpol.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                id = event.user_id
                msg = event.text.lower()
                if msg == 'отменить':
                    sender_hi(id, "Обращайтесь когда понадобится помощь! Бип-боп!")
                    main()
                    break
                else:
                    sender_otmena(id, "Укажите отчество!")
                    x = str(id)
                    with open("recovery_list.txt", "a", encoding="utf-8") as f:
                        f.write("id" + x + " Укажите имя! " + " Ответ: " + msg + '\n')
                    logic_student_d()

def logic_student_d():
    for event in longpol.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                id = event.user_id
                msg = event.text.lower()
                if msg == 'отменить':
                    sender_hi(id, "Обращайтесь когда понадобится помощь! Бип-боп!")
                    main()
                    break
                else:
                    sender_otmena(id, "Номер студ. билета!")
                    x = str(id)
                    with open("recovery_list.txt", "a", encoding="utf-8") as f:
                        f.write("id" + x + " Укажите отчество! " + " Ответ: " + msg + '\n')
                    logic_student_e()

def logic_student_e():
    for event in longpol.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                id = event.user_id
                msg = event.text.lower()
                if msg == 'отменить':
                    sender_hi(id, "Обращайтесь когда понадобится помощь! Бип-боп!")
                    main()
                    break
                else:
                    sender_otmena(id, "Номер паспорта!")
                    x = str(id)
                    with open("recovery_list.txt", "a", encoding="utf-8") as f:
                        f.write("id" + x + " Номер студ. билета! " + " Ответ: " + msg + '\n')
                    logic_student_f()

def logic_student_f():
    for event in longpol.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                id = event.user_id
                msg = event.text.lower()
                if msg == 'отменить':
                    sender_hi(id, "Обращайтесь когда понадобится помощь! Бип-боп!")
                    main()
                    break
                else:
                    sender_otmena(id, "Электронная почта!")
                    x = str(id)
                    with open("recovery_list.txt", "a", encoding="utf-8") as f:
                        f.write("id" + x + " Номер паспорта! " + " Ответ: " + msg + '\n')
                    logic_student_g()

def logic_student_g():
    for event in longpol.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                id = event.user_id
                msg = event.text.lower()
                if msg == 'отменить':
                    sender_hi(id, "Обращайтесь когда понадобится помощь! Бип-боп!")
                    main()
                    break
                else:
                    sender_otmena(id, "Факультет!")
                    x = str(id)
                    with open("recovery_list.txt", "a", encoding="utf-8") as f:
                        f.write("id" + x + " Электронная почта! " + " Ответ: " + msg + '\n')
                    logic_student_h()

def logic_student_h():
    for event in longpol.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                id = event.user_id
                msg = event.text.lower()
                if msg == 'отменить':
                    sender_hi(id, "Обращайтесь когда понадобится помощь! Бип-боп!")
                    main()
                    break
                else:
                    sender_otmena(id, "Ступень образования!")
                    x = str(id)
                    with open("recovery_list.txt", "a", encoding="utf-8") as f:
                        f.write("id" + x + " Факультет! " + " Ответ: " + msg + '\n')
                    logic_student_i()

def logic_student_i():
    for event in longpol.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                id = event.user_id
                msg = event.text.lower()
                if msg == 'отменить':
                    sender_hi(id, "Обращайтесь когда понадобится помощь! Бип-боп!")
                    main()
                    break
                else:
                    sender_otmena(id, "Год поступления!")
                    x = str(id)
                    with open("recovery_list.txt", "a", encoding="utf-8") as f:
                        f.write("id" + x + " Ступень образования! " + " Ответ: " + msg + '\n')
                    logic_student_j()

def logic_student_j():
    for event in longpol.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                id = event.user_id
                msg = event.text.lower()
                if msg == 'отменить':
                    sender_hi(id, "Обращайтесь когда понадобится помощь! Бип-боп!")
                    main()
                    break
                else:
                    sender_otmena(id, "Страна рождения!")
                    x = str(id)
                    with open("recovery_list.txt", "a", encoding="utf-8") as f:
                        f.write("id" + x + " Год поступления! " + " Ответ: " + msg + '\n')
                    logic_student_k()

def logic_student_k():
    for event in longpol.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                id = event.user_id
                msg = event.text.lower()
                if msg == 'отменить':
                    sender_hi(id, "Обращайтесь когда понадобится помощь! Бип-боп!")
                    main()
                    break
                else:
                    sender_otmena(id, "Дата рождения!")
                    x = str(id)
                    with open("recovery_list.txt", "a", encoding="utf-8") as f:
                        f.write("id" + x + " Страна рождения! " + " Ответ: " + msg + '\n')
                    logic_student_l()

def logic_student_l():
    for event in longpol.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                id = event.user_id
                msg = event.text.lower()
                if msg == 'отменить':
                    sender_hi(id, "Обращайтесь когда понадобится помощь! Бип-боп!")
                    main()
                    break
                else:
                    sender_hi(id, "Ожидайте ответа от техподдержки на почте!")
                    x = str(id)
                    with open("recovery_list.txt", "a", encoding="utf-8") as f:
                        f.write("id" + x + " Дата рождения! " + " Ответ: " + msg + '\n')

                    with open("recovery_list.txt", "r", encoding="utf-8") as f:
                        txt = f.readlines()
                        text = (txt[0])
                        text1 = (txt[1])
                        text2 = (txt[2])
                        text3 = (txt[3])
                        text4 = (txt[4])
                        text5 = (txt[5])
                        text6 = (txt[6])
                        text7 = (txt[7])
                        text8 = (txt[8])
                        text9 = (txt[9])
                        text10 = (txt[10])
                        text11 = (txt[11])
                        text12 = (txt[12])

                    server = 'smtp.gmail.com'
                    user = 'aakorotchenko@gmail.com'
                    password = 'TP1M9da5ebr'

                    recipients = ['ankorotchenko@gmail.com']
                    otpravitel = 'aakorotchenko@gmail.com'
                    subject = 'ВК_БОТ_ТЕХПОДЕРЖКА'
                    html = '<html><head></head><body><p>' + text + '<br>' + '<br>' + text1 + '<br>' + text2 + '<br>' + text3 + '<br>' + text4 + '<br>' + text5 + '<br>' + text6 + '<br>' + text7 + '<br>' + text8 + '<br>' + text9 + '<br>' + text10 + '<br>' + text11 + '<br>' + text12 + '</p></body></html>'

                    soobshenie = MIMEMultipart('alternative')
                    soobshenie['Subject'] = subject
                    soobshenie['From'] = 'Сообщение техподдержке <' + otpravitel + '>'
                    soobshenie['To'] = ', '.join(recipients)
                    soobshenie['Reply-To'] = otpravitel
                    soobshenie['Return-Path'] = otpravitel
                    soobshenie['X-Mailer'] = 'Python/' + (python_version())

                    part_text = MIMEText(text, 'plain')
                    part_html = MIMEText(html, 'html')

                    soobshenie.attach(part_text)
                    soobshenie.attach(part_html)

                    mail = smtplib.SMTP_SSL(server)
                    mail.login(user, password)
                    mail.sendmail(otpravitel, recipients, soobshenie.as_string())
                    mail.quit()

                    main()

def main():
    for event in longpol.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                id = event.user_id
                msg = event.text.lower()
                f = open('recovery_list.txt', 'w')
                f.close()
                if msg == 'пока':
                    sender_hi(id, "Всего хорошего!")
                    break
                else:
                    sendera(id, "Здравствуйте! Это бот помощи по порталу edu.vsu.ru! Вам нужна помощь?")
                    for event in longpol.listen():
                        if event.type == VkEventType.MESSAGE_NEW:
                            if event.to_me:
                                id = event.user_id
                                meseg = event.text.lower()
                                keyword_processor = KeywordProcessor()
                                keyword_processor.add_keyword_from_file('msg_list.txt')
                                new_sentence = keyword_processor.replace_keywords(meseg)
                                msg = new_sentence
                                if msg == 'да':
                                    senderb(id, "Чем вам помочь? Ориентируйтесь по меню ниже!")
                                    logic()
                                    break
                                else:
                                    sender_hi(id, "Обращайтесь когда понадобится помощь! Бип-боп!")
                                    main()
                                    break


while True:
    main()