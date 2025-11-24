# TIC IS AMONG US - Principal
# ==============================================
import os, time, json, random, datetime, importlib, paramiko

# ---- Minijuegos ----
import Minijuego1
import Minijuego2
import Minijuegosensor1
import Minijuegosensor2

# ------------- Configuración general -----------
PLAYER_ID   = 1
LOG_FILE    = "Player_logs.log"

# ---- Config SSH ----
HOST          = "192.168.0.24"
USERNAME      = "minipc"
PASSWORD      = "P0ck3tM0nst3rs"
DESTINO_HOST  = f"/home/minipc/Desktop/Game_App/Player_logs/{LOG_FILE}"

ssh_client = None
sftp_client = None

# ----------------- UTILIDADES ------------------
def log_event(stage, action, game_id=None, result=None, score=None, extra=None):
    entry = {
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "game_stage": stage,
        "PlayerID": PLAYER_ID,
        "Action": action
    }
    if game_id is not None: entry["GameID"] = game_id
    if result  is not None: entry["Result"]  = result
    if score   is not None: entry["Score"]   = score
    if extra:               entry.update(extra)
    with open(LOG_FILE, "a") as f: f.write(json.dumps(entry) + "\n")
    return entry


# ===================================================
#   *** NUEVA FUNCIÓN CONECTAR CON HOST ***
# ===================================================
def conectar_con_host():
    global ssh_client, sftp_client

    print("Intentando conectar al host...")
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=HOST, port=22, username=USERNAME, password=PASSWORD, timeout=5)
        sftp_client = ssh_client.open_sftp()
        print("✔ Conexión establecida con el host.\n")
        return True
   
    except Exception as e:
        print("❌ No fue posible conectar con el host.")
        print("Error:", e)
        print("\nEl juego NO puede comenzar sin conexión al host.")
        return False



def enviar_log_al_host():
    if sftp_client:
        sftp_client.put(LOG_FILE, DESTINO_HOST)


def cerrar_conexion_host():
    try:
        if sftp_client: sftp_client.close()
        if ssh_client: ssh_client.close()
    except:
        pass



# --------------- LOBBY --------------
def lobby_connection():

    # Si no se conecta, NO seguir
    if not conectar_con_host():
        print("\nEl juego se cerrará porque no hay host disponible.\n")
        exit()

    log_event("Lobby", "Join")
    enviar_log_al_host()

    print("Esperando respuesta del host (Accepted)...")

    while True:
        try:
            sftp_client.get(
                "/home/usuario_host/TIC_MiniProyecto2/game_status.log",
                "game_status_local.log"
            )

            with open("game_status_local.log") as f:
                lineas = f.readlines()
                if any('"Accepted"' in linea for linea in lineas):
                    print("✔ Host aceptó al jugador.\n")
                    break

        except:
            pass

        time.sleep(0.5)

    log_event("Lobby", "Ready")
    enviar_log_al_host()



# ---------- EJECUTAR JUEGO --------
def ejecutar_minijuego(game_id):
    if game_id == 1:
        return Minijuego1.jugar_ahorcado()
    elif game_id == 2:
        return Minijuego2.jugar_pokemon()
    elif game_id == 3:
        return Minijuegosensor1.jugar_sensor1()
    elif game_id == 4:
        return Minijuegosensor2.jugar_sensor2()



# --------------- RONDAS -------------
def rondas():

    # Si se pierde la conexión después del lobby, no ejecutar nada
    if sftp_client is None:
        print("❌ No se detecta conexión al host. Abortando juego.")
        return

    for stage in ["R1", "R2"]:
        log_event(stage, "Start")
        enviar_log_al_host()

        print(f"Esperando Assign del host para {stage}...")

        game_id = None

        while True:
            try:
                sftp_client.get(
                    "/home/usuario_host/TIC_MiniProyecto2/game_status.log",
                    "game_status_local.log"
                )

                with open("game_status_local.log") as f:
                    lineas = f.readlines()

                for linea in lineas:
                    if '"Assign"' in linea and stage in linea:
                        data = json.loads(linea.strip())
                        game_id = data.get("GameID", None)
                        break

            except:
                print("❌ Error: conexión perdida con el host.")
                return

            if game_id is not None:
                print(f"✔ Host asignó minijuego {game_id}")
                break
            time.sleep(0.5)

        # Ejecutar el minijuego
        log_event(stage, "Assign", game_id=game_id)
        enviar_log_al_host()

        ejecutar_minijuego(game_id)
        enviar_log_al_host()



# ------------------- MAIN ----------------------
def main():

    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)

    print("\n===== TIC IS AMONG US - Jugador =====\n")

    try:
        lobby_connection()
        rondas()

    finally:
        cerrar_conexion_host()
        print("\nSesión finalizada.\n")



if __name__ == "__main__":
    main()

