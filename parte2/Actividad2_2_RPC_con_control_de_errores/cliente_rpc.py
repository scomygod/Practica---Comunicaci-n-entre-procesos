import xmlrpc.client

# Conectar al proxy del servidor
proxy = xmlrpc.client.ServerProxy("http://localhost:8080/")

print("--- PRUEBAS DE CÁLCULO DE IMC (RPC) ---\n")

print("1. Prueba Normal:")
print("Enviando 70kg, 1.75m...")
print("Respuesta:", proxy.calcular_imc(70, 1.75))

print("\n2. Prueba Sobrepeso:")
print("Enviando 85kg, 1.70m...")
print("Respuesta:", proxy.calcular_imc(85, 1.70))

print("\n3. Prueba de Error (Valores negativos):")
print("Enviando -10kg, 1.80m...")
print("Respuesta:", proxy.calcular_imc(-10, 1.80))

print("\n4. Prueba de Error (División por cero evitada):")
print("Enviando 80kg, 0m...")
print("Respuesta:", proxy.calcular_imc(80, 0))

print("\n--- HISTORIAL DE OPERACIONES ---")
historial = proxy.historial()

# Como enviamos un diccionario desde el servidor, lo recorremos
if isinstance(historial, list):
    for idx, reg in enumerate(historial, 1):
        print(f"{idx}. Peso: {reg['peso']}kg | Altura: {reg['altura']}m ---> IMC: {reg['imc']} ({reg['categoria']})")
else:
    print(historial)
