import requests
import time

BASE_URL = "http://127.0.0.1:8000"

def imprimir_respuesta(metodo, url, response):
    print(f"\n[{metodo}] {url}")
    print(f"Status: {response.status_code}")
    print(f"Cuerpo JSON: {response.json()}")
    time.sleep(1) # Pausa para que se lea bien en consola

print("--- INICIANDO PRUEBAS DE LA API REST ---")

# 1. Crear 3 tareas
print("\n>>> 1. CREANDO 3 TAREAS (POST)")
requests.post(f"{BASE_URL}/tareas", json={"titulo": "Aprender FastAPI", "descripcion": "Leer documentación oficial"})
requests.post(f"{BASE_URL}/tareas", json={"titulo": "Hacer capturas", "descripcion": "Tomar screenshots para el informe"})
requests.post(f"{BASE_URL}/tareas", json={"titulo": "Comprar café", "descripcion": "Necesario para programar"})
print("3 tareas creadas con éxito.")

# 2. Listar todas las tareas
print("\n>>> 2. LISTAR TAREAS (GET)")
resp_listar = requests.get(f"{BASE_URL}/tareas")
imprimir_respuesta("GET", "/tareas", resp_listar)

# 3. Completar una tarea (La ID 1)
print("\n>>> 3. COMPLETAR TAREA ID=1 (PUT)")
resp_completar = requests.put(f"{BASE_URL}/tareas/1")
imprimir_respuesta("PUT", "/tareas/1", resp_completar)

# 4. Eliminar una tarea (La ID 3)
print("\n>>> 4. ELIMINAR TAREA ID=3 (DELETE)")
resp_eliminar = requests.delete(f"{BASE_URL}/tareas/3")
imprimir_respuesta("DELETE", "/tareas/3", resp_eliminar)

# 5. Verificar listado final
print("\n>>> 5. VERIFICAR LISTADO FINAL (GET)")
resp_final = requests.get(f"{BASE_URL}/tareas")
imprimir_respuesta("GET", "/tareas", resp_final)

# 6. Intento GET con ID inexistente (ID 99)
print("\n>>> 6. CONSULTAR TAREA INEXISTENTE (GET - ESPERANDO 404)")
resp_error = requests.get(f"{BASE_URL}/tareas/99")
imprimir_respuesta("GET", "/tareas/99", resp_error)
