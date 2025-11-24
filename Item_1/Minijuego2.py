import random

def jugar_pokemon():
    print("=== Minijuego 2: Adivina el Pok�mon ===")

    pokemons = [
        {"name": "Bulbasaur", "generation": 1, "color": "Verde", "type": "planta"},
        {"name": "Charmander", "generation": 1, "color": "Naranja", "type": "Fuego"},
        {"name": "Squirtle", "generation": 1, "color": "Celeste", "type": "Agua"},
        {"name": "Chikorita", "generation": 2, "color": "Verde", "type": "Planta"},
        {"name": "Cyndaquil", "generation": 2, "color": "Azul", "type": "Fuego"},
        {"name": "Totodile", "generation": 2, "color": "Azul", "type": "Agua"},
        {"name": "Treecko", "generation": 3, "color": "Verde", "type": "Planta"},
        {"name": "Torchic", "generation": 3, "color": "Naranja", "type": "Fuego"},
        {"name": "Mudkip", "generation": 3, "color": "Celeste", "type": "Agua"},
    ]

    p = random.choice(pokemons)

    print(f"Pista 1: Generaci�n {p['generation']}")
    guess = input("Respuesta: ").capitalize()
    if guess == p["name"]:
        return {"Result":"Win","Score":100}

    print(f"Pista 2: Color {p['color']}")
    guess = input("Respuesta: ").capitalize()
    if guess == p["name"]:
        return {"Result":"Win","Score":67}

    print(f"Pista 3: Tipo {p['type']}")
    guess = input("Respuesta: ").capitalize()
    if guess == p["name"]:
        return {"Result":"Win","Score":33}

    return {"Result":"Lose","Score":0}
