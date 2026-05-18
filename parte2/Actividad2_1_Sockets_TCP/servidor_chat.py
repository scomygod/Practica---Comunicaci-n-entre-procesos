import socket
import threading
from datetime import datetime

HOST = '127.0.0.1'
PORT = 65432


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    
    print(f"Escuchando en {HOST}:, {PORT}")
    # --- CAMBIO ---
    # Antes: el servidor solo aceptaba UN cliente y trabajaba con ese socket directamente.
    # Ahora: se usará un bucle infinito + hilos para soportar múltiples clientes simultáneamente.
    
    # --- CÓDIGO ORIGINAL (ECHO, UN SOLO CLIENTE) ---
    # conn, addr = s.accept()
    # with conn:
    #     print(f"Conectado desde {addr}")
    #     while True:
    #         data = conn.recv(1024)
    #         if not data:
    #             break
    #         conn.sendall(data)  # Echo: devuelve lo mismo
    #
    # --- CAMBIO ---
    # Se elimina este flujo porque solo maneja un cliente.
    # En su lugar se implementa manejo concurrente con threads.

    clientes = []
    def manejar_cliente(conn, addr):
        # --- CAMBIO ---
        # Esta función ahora maneja la comunicación de UN cliente en un hilo independiente.
        # Antes no existía: toda la lógica estaba en el hilo principal.
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    break

                mensaje = data.decode().strip()

                # --- CAMBIO ---
                # Se agrega control explícito de desconexión para evitar errores en el servidor.
                # SALIR: desconexión limpia
                if mensaje == "SALIR":
                    clientes.remove(conn)
                    conn.close()
                    print(f"Cliente desconectado: {addr}")
                    break

                # --- CAMBIO ---
                # Se agrega registro con timestamp para cumplir el requisito del enunciado.
                # LOG con timestamp
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"[{timestamp}] {addr[0]}:{addr[1]} → '{mensaje}'")

                # --- CAMBIO ---
                # Antes: conn.sendall(data) (echo al mismo cliente)
                # Ahora: se envía el mensaje a TODOS los clientes excepto el emisor (broadcast)
                # BROADCAST (a todos menos el emisor)
                for c in clientes:
                    if c != conn:
                        c.sendall(data)

            # --- CAMBIO ---
            # Manejo de errores para evitar que el servidor se caiga si un cliente se desconecta inesperadamente.
            except:
                clientes.remove(conn)
                conn.close()
                break

    # --- CAMBIO ---
    # Bucle principal que acepta múltiples clientes.
    # Antes solo había un accept(), ahora es continuo.
    while True:
        conn, addr = s.accept()
        clientes.append(conn)
        print(f"Conectado desde {addr}")

        # --- CAMBIO ---
        # Se crea un hilo por cada cliente para permitir concurrencia.
        threading.Thread(target=manejar_cliente, args=(conn, addr)).start()