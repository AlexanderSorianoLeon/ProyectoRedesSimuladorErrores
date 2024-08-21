import random

def segmentar_mensaje(mensaje):
    paquetes = [mensaje[i:i+10] for i in range(0, len(mensaje), 10)]
paquetes = [(i, len(paquete), paquete) for i, paquete in enumerate(paquetes)]
    return paquetes

def simular_errores(paquetes):
    tipo_error = random.random()
    if tipo_error < 0.2:  #20% de probabilidad de que este bien todo
        return paquetes, "Mensaje recibido correctamente"
    elif tipo_error < 0.4:  #20% de probabilidad de perdida de paquete
        paquetes = [paquete for paquete in paquetes if random.random() < 0.8]
        return paquetes, "Error: Pérdida de paquete"
    elif tipo_error < 0.6: #20% de probabilidad de envio fuera de orden
        paquetes = paquetes[:] # se crea una copia de la lista
        random.shuffle(paquetes)  # se desordena la lista
        return paquetes, "Error: Envío fuera de orden"
    elif tipo_error < 0.8: 
        paquetes = [(secuencia, longitud, ''.join([chr(ord(c) + random.randint(-1, 1)) for c in paquete])) for secuencia, longitud, paquete in paquetes]
        return paquetes, "Error: Falta de integridad de mensaje"
    else:  # 20% de probabilidad de error combinado
        paquetes = [paquete for paquete in paquetes if random.random() < 0.8]
        paquetes = paquetes[:]  
        random.shuffle(paquetes)  
        paquetes = [(secuencia, longitud, ''.join([chr(ord(c) + random.randint(-1, 1)) for c in paquete])) for secuencia, longitud, paquete in paquetes]
        return paquetes, "Error: Error combinado"
