

import socket
import threading

HOST = '127.0.0.1'
PORT = 65432

# --- CÓDIGO ORIGINAL (ECHO, UNA SOLA INTERACCIÓN) ---
# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.connect((HOST, PORT))
#     s.sendall(b'Hola, servidor!')
#     data = s.recv(1024)
#     print(f"Recibido: {data!r}")
# # Output: b'Hola, servidor!'

# --- CAMBIO ---
# El cliente original solo enviaba un mensaje y terminaba.
# Ahora se convierte en un cliente de chat interactivo:
# - Envía múltiples mensajes
# - Recibe mensajes en tiempo real
# - Usa hilos para enviar y recibir simultáneamente

def recibir(sock):
    # --- CAMBIO ---
    # Este hilo se encarga de recibir mensajes del servidor continuamente
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                break
            print(data.decode())
        except:
            break

def enviar(sock):
    # --- CAMBIO ---
    # Este hilo permite enviar mensajes desde la terminal
    while True:
        msg = input()
        sock.sendall(msg.encode())

        # SALIR: desconexión limpia
        if msg == "SALIR":
            sock.close()
            break

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print("Conectado al servidor. Escribir mensajes (SALIR para terminar):")

    # --- CAMBIO ---
    # Se inicia un hilo para recibir mensajes en paralelo
    threading.Thread(target=recibir, args=(s,), daemon=True).start()

    # El hilo principal se usa para enviar mensajes
    enviar(s)