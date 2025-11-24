#BotonTiempo
import time
from gpiozero import Button
from datetime import datetime

# ------------------- Configuracion -------------------
BUTTON_PIN = 17  # Cambia al pin real donde conectes el bot�n
button = Button(BUTTON_PIN, pull_up=True)

def juego_tiempo_10s():
    print(" Minijuego: Presiona el boton exactamente a los 10.0 segundos!")
    print("Cuando estes listo, presiona ENTER para comenzar...")
    input()
    print("Empieza a contar en tu mente... ??")

    t_inicio = time.time()
    # Esperar a que el jugador presione el boton una vez
    button.wait_for_press()
    t_fin = time.time()

    tiempo_transcurrido = t_fin - t_inicio
    diferencia = abs(tiempo_transcurrido - 10.0)

    print(f" Tiempo medido: {tiempo_transcurrido:.3f} s")
    print(f" Diferencia con 10.0 s: {diferencia:.3f} s")

    # Determinar resultado
    if diferencia <= 0.25:  
        print(" Excelente! Lo hiciste casi perfecto.")
        resultado = "Win"
        score = 100
    if diferencia <=0.75 and diferencia > 0.25:
        print(" Excelente! Lo hiciste casi bien.")
        resultado = "Win"
        score = 50
    else:
        print(" Fallaste el tiempo. Intenta de nuevo.")
        resultado = "Lose"
        score = 0

    # Registrar evento (como en tus otros minijuegos)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f'\n{timestamp} {{"game_stage": "R1", "PlayerID": 1, "GameID": 3, "Result": "{resultado}", "Score": {score}}}')

def main():
    while True:
        juego_tiempo_10s()
        again = input(" Jugar otra vez? (s/n): ").strip().lower()
        if again != "s":
            print("Gracias por jugar. ??")
            break

if __name__ == "__main__":
    main()
