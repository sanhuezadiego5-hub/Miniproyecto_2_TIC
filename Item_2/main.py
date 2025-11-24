import sys, os, json, random
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt

# ============================
# LED EN RASPBERRY PI
# ============================
from gpiozero import RGBLED

# Pines BCM (modíficalos si tu LED usa otros)
led = RGBLED(red=17, green=27, blue=22)

# Mapeo de colores por tipo (0-1 rango RGB)
COLOR_MAP = {
    "Agua": (0, 0, 1),       # azul
    "Fuego": (1, 0, 0),      # rojo
    "Planta": (0, 1, 0),     # verde
    "Electrico": (1, 1, 0),  # amarillo
    "Normal": (1, 1, 1),     # blanco
    "Psiquico": (1, 0, 1),   # magenta
    "Hielo": (0, 1, 1),      # celeste
    "Roca": (0.6, 0.4, 0.2),
    "Tierra": (0.5, 0.3, 0.1),
    "Siniestro": (0.1, 0.1, 0.1),
}

DATA_FOLDER = "/home/raspi/Desktop/TIC/Miniproyecto2/Pokedex/pokemon_data"
IMG_FOLDER = "/home/raspi/Desktop/TIC/Miniproyecto2/Pokedex/images"

class Pokedex(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Pokedex Realista")
        self.setFixedSize(860, 622)

        # Fondo Pokedex
        self.bg = QLabel(self)
        self.bg.setPixmap(QPixmap("/home/raspi/Desktop/TIC/Miniproyecto2/Pokedex/pokedex.png"))
       
        # ============================
        # PANTALLA DERECHA (TEXTO)
        # ============================
        self.desc = QLabel(self)
        self.desc.setGeometry(481, 192, 296, 243)
        self.desc.setWordWrap(True)
        self.desc.setFont(QFont("Arial", 13))
        self.desc.setStyleSheet("background:#00ff66; border:2px solid black; padding:10px;")

        # ============================
        # PANTALLA IZQUIERDA (POKEMON)
        # ============================
        self.display = QLabel(self)
        self.display.setGeometry(165, 145, 230, 280)
        self.display.setStyleSheet("background: transparent;")
        self.display.setAlignment(Qt.AlignCenter)

        # ============================
        # BOTONES SOBRE LA IMAGEN
        # ============================

        # Flecha izquierda
        self.btn_prev = QPushButton("", self)
        self.btn_prev.setGeometry(514, 455, 50, 40)
        self.btn_prev.setStyleSheet("background:transparent; border:none;")
        self.btn_prev.clicked.connect(self.prev_pokemon)

        # Flecha derecha
        self.btn_next = QPushButton("", self)
        self.btn_next.setGeometry(573, 455, 50, 40)
        self.btn_next.setStyleSheet("background:transparent; border:none;")
        self.btn_next.clicked.connect(self.next_pokemon)

        # Boton aleatorio sobre el circulo amarillo
        self.btn_rand = QPushButton("", self)
        self.btn_rand.setGeometry(705, 452, 40, 40)
        self.btn_rand.setStyleSheet("background: transparent; border: none;")
        self.btn_rand.clicked.connect(self.random_pokemon)

        # Lista de pokémon
        self.pokemon_files = sorted(os.listdir(DATA_FOLDER))
        self.index = 0
        self.load_pokemon()

    def load_pokemon(self):
        file_path = os.path.join(DATA_FOLDER, self.pokemon_files[self.index])
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Ajuste perfecto del tamaño del Pokémon
        pix = QPixmap(os.path.join(IMG_FOLDER, data["image"]))
        w = int(self.display.width() * 0.8)
        h = int(self.display.height() * 0.8)
        pix = pix.scaled(w, h, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.display.setPixmap(pix)

        texto = f"<b>Nombre:</b> {data['name']}<br><b>Tipo:</b> {data['type']}<br><br>{data['description']}"
        self.desc.setText(texto)

        # ============================
        # ACTUALIZAR COLOR DEL LED
        # ============================
        tipo = data["type"]
        tipo_sin_tilde = tipo.replace("í", "i").replace("é", "e").replace("á", "a").replace("ó", "o").replace("ú", "u")

        if tipo_sin_tilde in COLOR_MAP:
            led.color = COLOR_MAP[tipo_sin_tilde]
        else:
            led.color = (1, 1, 1)  # blanco por defecto

    def next_pokemon(self):
        self.index = (self.index + 1) % len(self.pokemon_files)
        self.load_pokemon()

    def prev_pokemon(self):
        self.index = (self.index - 1) % len(self.pokemon_files)
        self.load_pokemon()

    def random_pokemon(self):
        self.index = random.randint(0, len(self.pokemon_files) - 1)
        self.load_pokemon()


app = QApplication(sys.argv)
win = Pokedex()
win.show()
sys.exit(app.exec_())