from random import randint
import requests

class Pokemon:
    pokemons = {}
    
    def __init__(self, pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer
        self.pokemon_number = randint(1, 1000)
        self.name = self.get_name()
        self.img = self.get_img()
        self.type = self.get_type()
        self.height = self.get_height()
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