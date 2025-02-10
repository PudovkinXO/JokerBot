import telebot
from telebot import types

API_TOKEN = '7160442723:AAGjdZkIc2ccjRRK_CdqzhVs9w-I5Glfht4'

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands = ['start'])
def start_message(message): # отправка приветсвенного сообщения с кнопками
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    btn1 = types.KeyboardButton('▶️ Шутить')
    btn2 = types.KeyboardButton('⚙️ Обо мне')
    markup.add(btn1, btn2)
    bot.send_message(message.from_user.id, "Привет, я — JokerBot! 😎\nХочешь сначала узнать, кто я такой? Или сразу перейти к порции юмора?\nВыбирай мудро, но знай: мои шутки уже заряжены! 🎤😂", reply_markup=markup)
    
@bot.message_handler(content_types=['text'])
def get_message(message): # обработка ответов
    
    if message.text == '⚙️ Обо мне':
        bot.send_message(message.from_user.id, 'Я — настоящий бот-комик, только без гонораров! 😂\nКак только нажмёшь "Шутить", тебе предстоит дать мне тему, а дальше — наслаждайся моим искусством выдавать остроты!\nОсторожно, возможны шутки уровня "папа в магазине"! 😆', parse_mode='Markdown')
            
    elif message.text == '▶️ Шутить':
        bot.send_message(message.from_user.id, 'Класс! Начнём!!!', parse_mode='Markdown')
    
    else: 
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        btn1 = types.KeyboardButton('▶️ Шутить')
        btn2 = types.KeyboardButton('⚙️ Обо мне')
        markup.add(btn1, btn2)
        bot.send_message(message.from_user.id, 'Ой, ну конечно! Твои сообщения — это же просто шедевры мирового чата! 🤩\nНо знаешь что? Меня они совершенно не волнуют! 🙃\nДавай, реши наконец, что ты хочешь, и нажми на гребанные кнопки! 🚀')
        
if __name__ == "__main__":
    bot.polling(none_stop=True)

    