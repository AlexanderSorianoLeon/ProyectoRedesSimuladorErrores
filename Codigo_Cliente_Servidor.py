import random as rd

def segmentar_mensaje(mensaje):
    paquetes = [mensaje[i:i+10] for i in range(0, len(mensaje), 10)]
    paquetes = [(i, len(paquete), paquete) for i, paquete in enumerate(paquetes)]
    return paquetes

def simular_errores(paquetes):
    tipo_error = rd.random()
    if tipo_error < 0.2:  #20% de probabilidad de que este bien todo
        return paquetes, "Mensaje recibido correctamente"
    elif tipo_error < 0.4:  #20% de probabilidad de perdida de paquete
        paquetes = [paquete for paquete in paquetes if rd.random() < 0.8]
        return paquetes, "Error: Pérdida de paquete"
    elif tipo_error < 0.6: #20% de probabilidad de envio fuera de orden
        paquetes = paquetes[:] # se crea una copia de la lista
        rd.shuffle(paquetes)  # se desordena la lista
        return paquetes, "Error: Envío fuera de orden"
    elif tipo_error < 0.8: 
        paquetes = [(secuencia, longitud, ''.join([chr(ord(c) + rd.randint(-1, 1)) for c in paquete])) for secuencia, longitud, paquete in paquetes]
        return paquetes, "Error: Falta de integridad de mensaje"
    else:  # 20% de probabilidad de error combinado
        paquetes = [paquete for paquete in paquetes if rd.random() < 0.8]
        paquetes = paquetes[:]  
        rd.shuffle(paquetes)  
        paquetes = [(secuencia, longitud, ''.join([chr(ord(c) + rd.randint(-1, 1)) for c in paquete])) for secuencia, longitud, paquete in paquetes]
        return paquetes, "Error: Error combinado"


def ordenar_y_verificar(paquetes, mensaje_error):
    if "Error: Envío fuera de orden" in mensaje_error:
        errores = []
        return paquetes, errores
    else:
        paquetes.sort(key=lambda x: x[0])
        errores = []
        for i, paquete in enumerate(paquetes):
            if paquete[0] != i:
                errores.append(f"Paquete {i} faltante")
        return paquetes, errores
    

def guardar_y_mostrar_mensaje(paquetes):
    mensaje = ''.join([paquete[2] for paquete in paquetes])
    with open("output.txt", "w", encoding="utf-8") as f:
        f.write(mensaje)
