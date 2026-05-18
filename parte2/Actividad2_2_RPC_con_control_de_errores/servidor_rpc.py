from xmlrpc.server import SimpleXMLRPCServer

# Lista global para mantener el estado en memoria
historial_registros = []

def calcular_imc(peso_kg, altura_m):
    # 1. Manejo de Errores
    if peso_kg <= 0 or altura_m <= 0:
        return "ERROR: El peso y la altura deben ser valores positivos mayores a cero."

    # 2. Cálculo del IMC
    imc = round(peso_kg / (altura_m * altura_m), 2)

    # 3. Determinación de categoría
    if imc < 18.5:
        categoria = "Bajo peso"
    elif 18.5 <= imc <= 24.9:
        categoria = "Normal"
    elif 25.0 <= imc <= 29.9:
        categoria = "Sobrepeso"
    else:
        categoria = "Obesidad"

    resultado = f"IMC: {imc} - Categoría: {categoria}"

    # 4. Guardar en el historial
    registro = {"peso": peso_kg, "altura": altura_m, "imc": imc, "categoria": categoria}
    historial_registros.insert(0, registro) # Agrega al inicio de la lista

    # Mantener solo los últimos 5 cálculos
    if len(historial_registros) > 5:
        historial_registros.pop()

    return resultado

def historial():
    if not historial_registros:
        return "El historial está vacío."
    return historial_registros

# Configuración del servidor
server = SimpleXMLRPCServer(("localhost", 8080), logRequests=True)
server.register_function(calcular_imc)
server.register_function(historial)

print("Servidor RPC escuchando en el puerto 8080...")
server.serve_forever()
