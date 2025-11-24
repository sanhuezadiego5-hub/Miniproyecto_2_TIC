import random
import time
from datetime import datetime

def jugar_ahorcado():

    print("=== Minijuego 1: Ahorcado ===")

    print(" Elige el numero de letras del color (entre 3 y 10):")
    nletras = int(input("Numero de letras: "))
    intentos = int(input("Numero de intentos: "))

    palabras = ["rojo", "naranja", "amarillo", "verde", "azul", "morado",
                "rosado", "celeste", "blanco", "negro", "gris"]

    palabras = [p.lower() for p in palabras]
    palabras_filtradas = [p for p in palabras if len(p) == nletras]

    if not palabras_filtradas:
        print("No hay palabras con ese largo.")
        return {"Result":"Lose","Score":0}

    palabra = random.choice(palabras_filtradas)
    guiones = "_" * nletras

    print("\nPalabra seleccionada:", guiones)
    print("Tienes 15 segundos para adivinar.\n")

    time_start = time.time()
    intentos_rest = intentos

    resultado = ""

    while intentos_rest > 0:

        if time.time() - time_start >= 15:
            print("Se acabo el tiempo.")
            resultado = "Lose"
            break

        letra = input("Ingresa una letra o palabra completa: ").lower()

        if letra == palabra:
            resultado = "Win"
            break

        if len(letra) == 1 and letra in palabra:
            guiones = "".join(letra if palabra[i]==letra else guiones[i] for i in range(nletras))
            print(guiones)
            if guiones == palabra:
                resultado = "Win"
                break
        else:
            intentos_rest -= 1
            print("Incorrecto. Te quedan", intentos_rest, "intentos.")
            if intentos_rest == 0:
                resultado = "Lose"

    score = 100 if resultado == "Win" else 0
    return {"Result":resultado, "Score":score}
