import random as rd

# Función para segmentar y encapsular el mensaje
def segmentar_mensaje(mensaje):
    binario = ''.join(format(ord(c), '08b') for c in mensaje)
    paquetes = [binario[i:i + 80] for i in range(0, len(binario), 80)]
    paquetes = [(i, len(paquete), paquete, calcular_checksum(paquete)) for i, paquete in enumerate(paquetes)]
    return paquetes

def simular_errores(paquetes):
    tipo_error = rd.random()
    if tipo_error < 0.2:
        return paquetes, "Mensaje recibido correctamente"
    elif tipo_error < 0.4:
        paquetes = [paquete for paquete in paquetes if rd.random() < 0.8]
        return paquetes, "Error: Pérdida de paquete"
    elif tipo_error < 0.6:
        paquetes = paquetes[:]
        rd.shuffle(paquetes)
        return paquetes, "Error: Envío fuera de orden"
    elif tipo_error < 0.8:
        paquetes = [(secuencia, longitud, ''.join(
            str(rd.randint(0, 1)) if rd.random() < 0.1 else bit
            for bit in paquete), calcular_checksum(paquete))
                    for secuencia, longitud, paquete, checksum in paquetes]
        return paquetes, "Error: Falta de integridad de mensaje"
    else:
        paquetes = [paquete for paquete in paquetes if rd.random() < 0.8]
        paquetes = paquetes[:]
        rd.shuffle(paquetes)
        paquetes = [(secuencia, longitud, ''.join(
            str(rd.randint(0, 1)) if rd.random() < 0.1 else bit
            for bit in paquete), calcular_checksum(paquete))
                    for secuencia, longitud, paquete, checksum in paquetes]
        return paquetes, "Error: Error combinado"

def ordenar_y_verificar(paquetes, mensaje_error):
    errores = []
    paquetes_recibidos = {paquete[0]: paquete for paquete in paquetes}
    
    # Verifica si los paquetes están fuera de orden
    orden_correcto = all(paquetes[i][0] <= paquetes[i+1][0] for i in range(len(paquetes)-1))
    if not orden_correcto:
        errores.append("Error: Paquetes fuera de orden")
    
    # Verifica si falta algún paquete
    paquetes_esperados = max(paquete[0] for paquete in paquetes) + 1 if paquetes else 0
    paquetes_faltantes = []
    for i in range(paquetes_esperados):
        if i not in paquetes_recibidos:
            paquetes_faltantes.append(i)
            errores.append(f"Paquete {i} faltante")
    
    # Ordena los paquetes si no se especifica un error de orden
    if "Error: Paquetes fuera de orden" not in errores:
        paquetes.sort(key=lambda x: x[0])
    
    for i, paquete in enumerate(paquetes):
        if not verificar_paquete(paquete[2], paquete[3]):
            errores.append(f"Paquete {i} corrupto")
    
    return paquetes, errores

def calcular_checksum(paquete):
    return sum(int(bit) for bit in paquete)

def verificar_paquete(paquete, checksum):
    return calcular_checksum(paquete) == checksum

def guardar_y_mostrar_mensaje(paquetes):
    if not paquetes:
        return "El mensaje no se pudo reconstruir debido a errores en la transmisión."

    mensaje_binario = ''.join(paquete[2] for paquete in paquetes)
    mensaje = ''.join(
        chr(int(mensaje_binario[i * 8:i * 8 + 8], 2))
        for i in range(len(mensaje_binario) // 8)
    )
    with open("output.txt", "w", encoding="utf-8") as f:
        f.write(mensaje)
    return mensaje

def comunicacion_cliente_servidor(mensaje):
    # Simulación del cliente
    print("Cliente: Envia el mensaje...")
    paquetes = segmentar_mensaje(mensaje)
    paquetes_erroneos, mensaje_error = simular_errores(paquetes)

    # Simulación del servidor
    print("Servidor: Recibiendo los paquetes...")
    paquetes_ordenados, errores = ordenar_y_verificar(paquetes_erroneos, mensaje_error)

    if errores:
        print("Servidor: Se encontraron errores en la recepción:")
        for error in errores:
            print(f" - {error}")
    else:
        print("Servidor: Paquetes recibidos correctamente.")

    mensaje_reconstruido = guardar_y_mostrar_mensaje(paquetes_ordenados)

    return mensaje_reconstruido, mensaje_error

# Ejecución de la comunicación
mensaje = input("Ingrese mensaje a enviar: ")
mensaje_reconstruido, mensaje_error = comunicacion_cliente_servidor(mensaje)

print("\nMensaje original:", mensaje)
print("Mensaje recibido:", mensaje_reconstruido)
print("Mensaje del servidor:", mensaje_error)
