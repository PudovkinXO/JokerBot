import telebot
import requests
import os
from dotenv import load_dotenv
from telebot import types

load_dotenv()

BOT_API_TOKEN = os.getenv("BOT_API_TOKEN") # bot token from BotFather
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") # key from ProxyApi
PROXY_URL = "https://api.proxyapi.ru/openai/v1/chat/completions" 

bot = telebot.TeleBot(BOT_API_TOKEN)

def joke_from_chatgpt(prompt): # ChatGPT integration
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "gpt-4",
        "messages": [
            {"role": "system", "content": "Ты бот-шутник уровня профессиональных StandUp'ов. Ты можешь выдавать только шутки на данные темы и ничего больше. Используй чёрный юмор, но не перегибай палку."},
            {"role": "user", "content": f"Сделай шутку на тему: {prompt}"}
        ],
        "max_tokens": 150,
        "temperature": 0.5
    }
    
    response = requests.post(PROXY_URL, headers=headers, json=payload) 
    
    try:
        response_data = response.json()
        if "choices" in response_data:
            return response_data["choices"][0]["message"]["content"].strip()
        elif "error" in response_data:
            return f"Ошибка: {response_data['error']['message']}"
        else:
            return "Неизвестная ошибка при получении ответа от ChatGPT.", 
    except requests.exceptions.JSONDecodeError:
        return "Ошибка декодирования JSON. Возможно, сервер недоступен."

@bot.message_handler(commands = ['start'])
def start_message(message): # sending a welcome message
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    btn1 = types.KeyboardButton('▶️ Шутить')
    btn2 = types.KeyboardButton('⚙️ Обо мне')
    markup.add(btn1, btn2)
    bot.send_message(message.from_user.id, "Привет, я — JokerBot! 😎\nХочешь сначала узнать, кто я такой? Или сразу перейти к порции юмора?\nВыбирай мудро, но знай: мои шутки уже заряжены! 🎤😂", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def get_message(message): # commands processing
    
    if message.text == '⚙️ Обо мне':
        bot.send_message(message.from_user.id, 'Я — настоящий бот-комик, только без гонораров! 😂\nКак только нажмёшь "Шутить", тебе предстоит дать мне тему, а дальше — наслаждайся моим искусством выдавать остроты!\nОсторожно, возможны шутки уровня "папа в магазине"! 😆', parse_mode='Markdown')
            
    elif message.text == '▶️ Шутить':
        msg = bot.send_message(message.from_user.id, "Напиши тему шутки! 😆")
        bot.register_next_step_handler(msg, generate_joke)
    
    else: 
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        btn1 = types.KeyboardButton('▶️ Шутить')
        btn2 = types.KeyboardButton('⚙️ Обо мне')
        markup.add(btn1, btn2)
        bot.send_message(message.from_user.id, 'Ой, ну конечно! Твои сообщения — это же просто шедевры мирового чата! 🤩\nНо знаешь что? Меня они совершенно не волнуют! 🙃\nДавай, реши наконец, что ты хочешь, и нажми на гребанную кнопку! 🚀')
    
def generate_joke(message): # joke generator
    topic = message.text
    bot.send_message(message.chat.id, "Пришучиваю шуточку... 😏")
    joke = joke_from_chatgpt(topic)
    bot.send_message(message.chat.id, joke)
    
if __name__ == "__main__":
    print('Бот запущен')
    bot.polling(none_stop=True)