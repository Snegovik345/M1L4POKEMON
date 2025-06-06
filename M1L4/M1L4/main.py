import telebot 
from config import token
from logic import Pokemon

bot = telebot.TeleBot(token) 

@bot.message_handler(commands=['go'])
def go(message):
    if message.from_user.username not in Pokemon.pokemons.keys():
        pokemon = Pokemon(message.from_user.username)
        bot.send_message(message.chat.id, pokemon.info())
        bot.send_photo(message.chat.id, pokemon.show_img())
    else:
        bot.reply_to(message, "Ты уже создал себе покемона")
@bot.message_handler(commands=['info'])
def show_info(message):
        
    pokemon = Pokemon.pokemons[message.from_user.username]
    bot.send_message(message.chat.id, pokemon.full_info())

@bot.message_handler(commands=['type'])
def show_type(message):
        
    pokemon = Pokemon.pokemons[message.from_user.username]
    bot.send_message(message.chat.id, f"Тип твоего покемона: {pokemon.type}")

@bot.message_handler(commands=['height'])
def show_height(message):
        
    pokemon = Pokemon.pokemons[message.from_user.username]
    bot.send_message(message.chat.id, f"Рост твоего покемона: {pokemon.height} дм")

bot.infinity_polling(none_stop=True)

