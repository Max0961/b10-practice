import telebot
import extensions
import config

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_greeting(message):
    text_strings = list()
    text_strings.append('Команды:')
    text_strings.append('/values - посмотреть список валют')
    text_strings.append('/values <имя валюты> - посмотреть список валют '
                        'относительно <имя валюты>')
    text_strings.append('Конвертировать сумму:')
    text_strings.append('<имя валюты> <в какую валюту перевести> <количество>')
    text_strings.append('(дробная часть отделяется точкой)')
    text = '\n'.join(text_strings)
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def send_values(message: telebot.types.Message):
    try:
        if len(message.text.split()) > 1:
            data = extensions.Currency.get_sorted(message.text.split()[1])
        else:
            data = extensions.Currency.get_sorted()
    except Exception as e:
        text = e.__str__()
    else:
        text_strings = list()
        for k, v in data.items():
            text_strings.append(f'{k}:\t{v}')

        text = '\n'.join(text_strings)

    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text'])
def send_converted_amount(message):
    args = message.text.split()

    if len(args) == 3:
        try:
            text = f"{args[1].upper()}: {extensions.Conversion.get_price(*args)}"
        except Exception as e:
            text = e.__str__()
    else:
        text = '?'

    bot.send_message(message.chat.id, text)


bot.polling()