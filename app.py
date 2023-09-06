import telebot
from config import keys, TOKEN
from extensions import APIExeption, CurrencyConverter

bot = telebot.TeleBot(TOKEN)

      
@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате: \n<имя валюты, цену которой хотите узнать> \
<имя валюты, в которой надо узнать цену первой валюты> \
<количество первой валюты>\n Увидеть список всех доступных валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)
    

@bot.message_handler(content_types=['text', ])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIExeption('Неверное количество параметров.\nПример ввода: доллар рубль 2')
    
        base, quote, amount = values
        total_quote = CurrencyConverter.get_price(base, quote, amount)
    except APIExeption as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f' Не удалось обработать команду\n{e}')
        
    else:
        text = f'Цена {amount} {base} в {quote} = {total_quote}.'
        bot.send_message(message.chat.id, text)


bot.polling()
