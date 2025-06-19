import telebot 
from config import token
from logic import Pokemon
from logic import Fighter
from random import randint
from logic import Wizard
bot = telebot.TeleBot(token) 

@bot.message_handler(commands=['go'])
def create_pokemon(message):
    if not message.from_user.username:
        bot.reply_to(message, "Сначала установите username в настройках Telegram")
        return
        
    if message.from_user.username not in Pokemon.pokemons:
        # Уменьшаем шанс получения покемонов с супер-силой (1 из 4)
        chance = randint(1, 4)
        if chance == 1:
            pokemon = Wizard(message.from_user.username)
            type_name = "Волшебник"
        elif chance == 2:
            pokemon = Fighter(message.from_user.username)
            type_name = "Боец"
        else:
            pokemon = Pokemon(message.from_user.username)
            type_name = "Обычный"
            
        bot.send_message(message.chat.id, f"Ты получил покемона ({type_name})!\n{pokemon.info()}")
        bot.send_photo(message.chat.id, pokemon.show_img())
    else:
        bot.reply_to(message, "У тебя уже есть покемон!")

@bot.message_handler(commands=['feed'])
def feed_pokemon(message):
    if not message.from_user.username:
        bot.reply_to(message, "Сначала установите username в настройках Telegram")
        return
        
    if message.from_user.username in Pokemon.pokemons:
        pokemon = Pokemon.pokemons[message.from_user.username]
        result = pokemon.feed()
        bot.reply_to(message, result)
    else:
        bot.reply_to(message, "Сначала создай покемона командой /go")

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

@bot.message_handler(commands=['attack'])
def attack_pokemon(message):
    if not message.reply_to_message:
        bot.reply_to(message, "Ответь на сообщение игрока, чтобы атаковать его покемона")
        return
    
    attacker = message.from_user.username
    defender = message.reply_to_message.from_user.username
    
    if attacker == defender:
        bot.reply_to(message, "Нельзя атаковать самого себя!")
        return
        
    if attacker not in Pokemon.pokemons:
        bot.reply_to(message, "Сначала создай покемона командой /go")
        return
        
    if defender not in Pokemon.pokemons:
        bot.reply_to(message, "У этого игрока нет покемона")
        return
    
    attacker_pokemon = Pokemon.pokemons[attacker]
    defender_pokemon = Pokemon.pokemons[defender]
    
    result = attacker_pokemon.attack(defender_pokemon)
    bot.reply_to(message, result)

bot.infinity_polling(none_stop=True)

