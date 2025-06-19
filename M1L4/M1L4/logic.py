from random import randint
import requests
from datetime import datetime, timedelta

class Pokemon:
    pokemons = {}
    
    def __init__(self, pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer
        self.pokemon_number = randint(1, 1000)
        self.name = self.get_name()
        self.img = self.get_img()
        self.type = self.get_type()
        self.height = self.get_height()
        self.hp = randint(50, 100)
        self.power = randint(10, 20)
        self.last_feed_time = datetime.now()  # Время последнего кормления
        Pokemon.pokemons[pokemon_trainer] = self

    def get_img(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()['sprites']['front_default']
        return "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png"

    def get_name(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        return response.json()['forms'][0]['name'] if response.status_code == 200 else "Pikachu"

    def attack(self, enemy):
        chit = randint(1,5)
        if isinstance(enemy, Wizard) and randint(1,5) == 1:
            if chit == 1:
                return f" Волшебник {enemy.name} использовал щит и блокировал атаку!"
        
        elif enemy.hp > self.power:
            enemy.hp -= self.power
            return (
                f" {self.name} атаковал {enemy.name}!\n"
                f"Урон: {self.power}\n"
                f"У {enemy.name} осталось {enemy.hp} HP"
            )
        else:
            enemy.hp = 0
            return f" {self.name} победил {enemy.name}!"

    def get_type(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()['types'][0]['type']['name']
        return "normal"

    def get_height(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        return response.json()['height'] if response.status_code == 200 else 0

    def info(self):
        return f"Имя твоего покемона: {self.name}"
    
    def show_img(self):
        return self.img
    
    def full_info(self):
        return (
            f"Имя: {self.name}\n"
            f"Тип: {self.type}\n"
            f"Рост: {self.height} дм\n"
            f"Тренер: {self.pokemon_trainer}"
        )
    
    def feed(self, feed_interval=20, hp_increase=10):
        current_time = datetime.now()
        delta_time = timedelta(seconds=feed_interval)
        
        if (current_time - self.last_feed_time) > delta_time:
            self.hp += hp_increase
            self.last_feed_time = current_time
            return f"Здоровье покемона увеличено. Текущее здоровье: {self.hp}"
        else:
            next_feed_time = self.last_feed_time + delta_time
            remaining_time = next_feed_time - current_time
            return f"Следующее кормление через: {int(remaining_time.total_seconds())} сек."


class Fighter(Pokemon):
    def __init__(self, pokemon_trainer):
        super().__init__(pokemon_trainer)
        self.critical_chance = randint(1, 5)
    
    def attack(self, enemy):
        super_power = randint(5, 15)
        self.power += super_power
        result = super().attack(enemy)
        self.power -= super_power
        return result + f"\n Боец применил супер-атаку силой {super_power}!"
    
    def info(self):
        return super().info() + f"\nШанс крита: 20%"
    
    def feed(self):
        # Бойцы получают +20 HP, но кормить можно только раз в 30 секунд
        return super().feed(feed_interval=30, hp_increase=20)


class Wizard(Pokemon):
    def __init__(self, pokemon_trainer):
        super().__init__(pokemon_trainer)
        self.magic_power = randint(7, 20)
    
    def info(self):
        return super().info() + f"\n Магическая сила: {self.magic_power}"
    
    def feed(self):
        # Волшебники получают +10 HP, но кормить можно чаще - каждые 10 секунд
        return super().feed(feed_interval=10, hp_increase=10)
