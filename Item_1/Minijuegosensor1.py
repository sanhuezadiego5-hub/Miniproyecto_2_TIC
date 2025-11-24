#BovedaMrPhantom
import time, random, sys
from gpiozero import LED, Button, PWMOutputDevice

# ---------------- Pines (BCM) ----------------
LED_R = 21   # LED rojo
LED_G = 20   # LED verde
LED_B = 16   # LED azul

BTN_R = 26   # Botón rojo
BTN_Y = 19   # Botón amarillo
BTN_B = 13   # Botón azul

BUZZ_PIN = 6   # buzzer pasivo (PWM)

# -------------- Inicialización ---------------
# Buzzer pasivo como PWM
buzzer = PWMOutputDevice(BUZZ_PIN, active_high=True, initial_value=0, frequency=440)

# LEDs
led_r = LED(LED_R)
led_g = LED(LED_G)
led_b = LED(LED_B)

# Botones
btn_r = Button(BTN_R, pull_up=True, bounce_time=0.05)
btn_y = Button(BTN_Y, pull_up=True, bounce_time=0.05)
btn_b = Button(BTN_B, pull_up=True, bounce_time=0.05)

# Encender LED mientras se presiona su botón
btn_r.when_pressed  = led_r.on
btn_r.when_released = led_r.off
btn_y.when_pressed  = led_g.on
btn_y.when_released = led_g.off
btn_b.when_pressed  = led_b.on
btn_b.when_released = led_b.off

# -------------- Sonidos ----------------------
def tone(freq, dur=0.1, duty=0.5):
    """Tono en buzzer pasivo (usando PWMOutputDevice)."""
    buzzer.frequency = freq
    buzzer.value = duty
    time.sleep(dur)
    buzzer.off()

def bip_ok():    tone(1200, 0.08)
def bip_fail():  tone(300,  0.12)

def melody_victory():
    for f, d in [(800, 0.12), (1000, 0.12), (1200, 0.18)]:
        tone(f, d); time.sleep(0.04)

def melody_gameover():
    for f, d in [(400, 0.25), (300, 0.20)]:
        tone(f, d); time.sleep(0.06)

# -------------- Utilidades -------------------
def pedir_bool(msg):
    while True:
        s = input(msg + " (s/n): ").strip().lower()
        if s in ("s", "n"): return s == "s"

def pedir_tiempo(msg):
    while True:
        try:
            t = float(input(msg + " (segundos): ").strip())
            if t > 0: return t
        except:
            pass
        print("Ingresa un número positivo.")

def imprimir_tiempo_restante(t_rest):
    sys.stdout.write(f"\rTiempo restante: {t_rest:4.1f} s ")
    sys.stdout.flush()

def leer_boton_una_vez():
    """Espera hasta detectar una pulsación completa (press+release)."""
    while True:
        if btn_r.is_pressed:
            while btn_r.is_pressed: time.sleep(0.005)
            return 1
        if btn_y.is_pressed:
            while btn_y.is_pressed: time.sleep(0.005)
            return 2
        if btn_b.is_pressed:
            while btn_b.is_pressed: time.sleep(0.005)
            return 3
        time.sleep(0.003)

def gen_secuencia(allow_repeat):
    base = [1, 2, 3]  # 1=rojo, 2=amarillo, 3=azul
    seq = []
    while len(seq) < 3:
        x = random.choice(base)
        if allow_repeat or x not in seq:
            seq.append(x)
    return seq

def nombre_btn(i):
    return {1: "Rojo", 2: "Amarillo", 3: "Azul"}[i]

# -------------- Inicio con ENTER -------------
def esperar_inicio_con_enter():
    input("Presiona ENTER para comenzar el juego...")

# -------------- Juego ------------------------
def juego():
    Ttotal = pedir_tiempo("Tiempo total del juego")
    permitir_rep = pedir_bool("¿Permitir repetición de botón en la secuencia?")
    seq = gen_secuencia(permitir_rep)
    print("Secuencia creada (oculta). [debug]:", [nombre_btn(i) for i in seq])

    esperar_inicio_con_enter()

    t0 = time.time()
    progreso = 0
    penal = 0.0

    while True:
        trans = time.time() - t0
        t_rest = max(0.0, Ttotal - trans - penal)
        imprimir_tiempo_restante(t_rest)
        if t_rest <= 0:
            print("\n¡Tiempo agotado!")
            melody_gameover()
            return False

        boton = leer_boton_una_vez()
        esperado = seq[progreso]

        if boton == esperado:
            progreso += 1
            bip_ok()
            print(f"\nCorrecto: {nombre_btn(boton)} (paso {progreso}/3)")
            if progreso == 3:
                print("¡Secuencia completa! ¡Ganaste!")
                melody_victory()
                return True
        else:
            bip_fail()
            progreso = 0
            penal += 1.0
            print(f"\nFallo: {nombre_btn(boton)} no era el esperado. -1.0 s (total desc {penal:.1f}s)")

def main():
    try:
        while True:
            _ = juego()
            s = input("¿Jugar otra vez? (s/n): ").strip().lower()
            if s != "s":
                break
    finally:
        # Apagar/limpiar
        led_r.off(); led_g.off(); led_b.off()
        buzzer.off()
        print("Fin.")

if __name__ == "__main__":
    main()