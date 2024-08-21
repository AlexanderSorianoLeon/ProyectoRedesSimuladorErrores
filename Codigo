import random

def segmentar_mensaje(mensaje):
    paquetes = [mensaje[i:i+10] for i in range(0, len(mensaje), 10)]
paquetes = [(i, len(paquete), paquete) for i, paquete in enumerate(paquetes)]
    return paquetes

def simular_errores(paquetes):
    tipo_error = random.random()
    if tipo_error < 0.2:  
        return paquetes, "Mensaje recibido correctamente"
    elif tipo_error < 0.4:  
        paquetes = [paquete for paquete in paquetes if random.random() < 0.8]
        return paquetes, "Error: Pérdida de paquete"
    elif tipo_error < 0.6: 
        paquetes = paquetes[:] 
        random.shuffle(paquetes)  
        return paquetes, "Error: Envío fuera de orden"
    elif tipo_error < 0.8: 
        paquetes = [(secuencia, longitud, ''.join([chr(ord(c) + random.randint(-1, 1)) for c in paquete])) for secuencia, longitud, paquete in paquetes]
        return paquetes, "Error: Falta de integridad de mensaje"
    else:  
        paquetes = [paquete for paquete in paquetes if random.random() < 0.8]
        paquetes = paquetes[:]  
        random.shuffle(paquetes)  
        paquetes = [(secuencia, longitud, ''.join([chr(ord(c) + random.randint(-1, 1)) for c in paquete])) for secuencia, longitud, paquete in paquetes]
        return paquetes, "Error: Error combinado"
