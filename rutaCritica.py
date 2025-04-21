#! /usr/bin/env python3
# vim:fenc=utf-8
#
# Copyright © 2024 epeat <epeat@epeat-facu>
#
# Distributed under terms of the MIT license.

import csv

nombre_archivo = 'tabla.csv'


class Tarea:

    def __init__(self, nombre, duracion, es, ef, ls, lf):
        self.nombre = nombre
        self.duracion = duracion
        self.es = es
        self.ef = ef
        self.ls = ls
        self.lf = lf
        self.dependencias = []
        self.dependientes = []

    def __str__(self):
        dependencias_nombres = ', '.join(
            dep.nombre for dep in self.dependencias)
        dependientes_nombres = ', '.join(
            dep.nombre for dep in self.dependientes)

        return (
            f"Tarea: {self.nombre}\n"
            f"  Duración: {self.duracion}\n"
            f"  ES (Early Start): {self.es}\n"
            f"  EF (Early Finish): {self.ef}\n"
            f"  LS (Late Start): {self.ls}\n"
            f"  LF (Late Finish): {self.lf}\n"
            f"  Dependencias: {dependencias_nombres or 'Ninguna'}\n"
            f"  Dependientes: {dependientes_nombres or 'Ninguno'}"
        )

    def agregarDependencias(self, dependencias):
        self.dependencias.extend(dependencias)

    def agregarDependiente(self, dependiente):
        self.dependientes.append(dependiente)


def calcular_es_ef(tareas):
    for tarea in tareas:
        if not tarea.dependencias:
            tarea.es = 0
            tarea.ef = tarea.duracion
        else:
            tarea.es = max([dep.ef for dep in tarea.dependencias])
            tarea.ef = tarea.es + tarea.duracion


def calcular_ls_lf(tareas, duracion_proyecto):
    for tarea in reversed(tareas):
        if not tarea.dependientes:
            tarea.lf = duracion_proyecto
            tarea.ls = tarea.lf - tarea.duracion
        else:
            tarea.lf = min([dep.ls for dep in tarea.dependientes])
            tarea.ls = tarea.lf - tarea.duracion


def es_tarea_critica(tarea):
    # Una tarea es crítica si su holgura es cero
    return tarea.ls - tarea.es == 0


def obtener_tareas_iniciales(tareas):
    # Devuelve las tareas que no tienen dependencias
    return [tarea for tarea in tareas if not tarea.dependencias]


def obtener_rutas_criticas(tareas):
    # Encontrar todas las tareas iniciales
    tareas_iniciales = obtener_tareas_iniciales(tareas)
    rutas_criticas = []
    
    # Para cada tarea inicial, buscar rutas críticas
    for tarea_inicial in tareas_iniciales:
        if es_tarea_critica(tarea_inicial):
            explorar_ruta_critica(tarea_inicial, [tarea_inicial], rutas_criticas)
    
    return rutas_criticas


def explorar_ruta_critica(tarea_actual, ruta_actual, rutas_criticas):
    # Si la tarea no tiene dependientes, es el final de una ruta
    if not tarea_actual.dependientes:
        rutas_criticas.append(ruta_actual.copy())
        return
    
    # Explorar cada dependiente que sea crítico
    tiene_dependientes_criticos = False
    for dependiente in tarea_actual.dependientes:
        if es_tarea_critica(dependiente):
            tiene_dependientes_criticos = True
            nueva_ruta = ruta_actual.copy()
            nueva_ruta.append(dependiente)
            explorar_ruta_critica(dependiente, nueva_ruta, rutas_criticas)
    
    # Si no hay dependientes críticos, entonces esta ruta termina aquí
    if not tiene_dependientes_criticos and ruta_actual:
        rutas_criticas.append(ruta_actual.copy())


# Leer el archivo CSV y crear las tareas
tareas = []
dependencias = []
encabezados = ["Tareas", "Duraciones", "Dependencias",
               "ES", "EF", "LS", "LF", "Holgura", "Rutas Criticas"]
filas = []

with open(nombre_archivo, mode='r', encoding='utf-8') as archivo:
    # Leer el contenido completo para manejar posibles errores de formato
    contenido = archivo.read().strip()
    if not contenido:
        raise ValueError(f"El archivo {nombre_archivo} está vacío")
    
    # Volver al inicio del archivo para leerlo como CSV
    archivo.seek(0)
    lector = csv.DictReader(archivo)

    for indice, fila in enumerate(lector):
        # Asegurarse de que los campos requeridos existan y estén correctamente formateados
        if "Tareas" not in fila or not fila["Tareas"].strip():
            raise ValueError(f"Fila {indice+1}: Falta el nombre de la tarea o está vacío")
        
        try:
            duracion = int(fila["Duraciones"])
            if duracion <= 0:
                raise ValueError(f"Fila {indice+1}: La duración debe ser un número positivo")
        except (ValueError, KeyError):
            raise ValueError(f"Fila {indice+1}: La duración no es un número válido")
        
        if "Dependencias" not in fila:
            raise ValueError(f"Fila {indice+1}: Falta la columna de dependencias")
        
        # Crear la tarea y guardar sus dependencias
        tareas.append(Tarea(fila["Tareas"].strip(), duracion, 0, 0, 0, 0))
        dependencias.append(fila["Dependencias"].strip())

# Establecer las dependencias entre tareas
for indice, tarea in enumerate(tareas):
    if dependencias[indice] == "-":
        continue

    # Asegurar que todas las dependencias estén correctamente recortadas (sin espacios)
    nombres_dependencias = [dep.strip() for dep in dependencias[indice].split(',') if dep.strip()]
    
    # Imprimir para debugging si hay problemas con las dependencias
    if not nombres_dependencias:
        print(f"Advertencia: La tarea {tarea.nombre} tiene formato de dependencias incorrecto: '{dependencias[indice]}'")
    
    dependencias_a_agregar = [
        dependencia for dependencia in tareas if dependencia.nombre in nombres_dependencias]
    
    # Verificar si no se encontraron todas las dependencias
    if len(dependencias_a_agregar) != len(nombres_dependencias):
        encontradas = [dep.nombre for dep in dependencias_a_agregar]
        faltantes = [nombre for nombre in nombres_dependencias if nombre not in encontradas]
        print(f"Advertencia: No se encontraron las siguientes dependencias para {tarea.nombre}: {faltantes}")

    tarea.agregarDependencias(dependencias_a_agregar)

# Establecer relaciones de dependientes
for tarea in tareas:
    for dependencia in tarea.dependencias:
        dependencia.agregarDependiente(tarea)

# Calcular ES, EF, LS, LF
calcular_es_ef(tareas)
duracion_proyecto = max(tarea.ef for tarea in tareas)
calcular_ls_lf(tareas, duracion_proyecto)

# Obtener las rutas críticas
rutas_criticas = obtener_rutas_criticas(tareas)

# Convertir las rutas críticas a cadenas de texto
rutas_criticas_texto = []
for ruta in rutas_criticas:
    rutas_criticas_texto.append(" -> ".join([tarea.nombre for tarea in ruta]))

# Preparar datos para el CSV
datos_csv = []

# Primero agregamos las filas de tareas
for indice, tarea in enumerate(tareas):
    fila = {}
    fila["Tareas"] = tarea.nombre
    fila["Duraciones"] = tarea.duracion
    fila["Dependencias"] = dependencias[indice]
    fila["ES"] = tarea.es
    fila["EF"] = tarea.ef
    fila["LS"] = tarea.ls
    fila["LF"] = tarea.lf
    fila["Holgura"] = tarea.ls - tarea.es  # La holgura correcta es LS-ES (o LF-EF)
    fila["Rutas Criticas"] = ""  # Inicialmente vacío
    datos_csv.append(fila)

# Luego agregamos las rutas críticas en las primeras filas
for i, ruta_texto in enumerate(rutas_criticas_texto):
    if i < len(datos_csv):  # Si hay suficientes filas, usamos las existentes
        datos_csv[i]["Rutas Criticas"] = ruta_texto
    else:  # Si hay más rutas que tareas, creamos filas vacías adicionales
        fila_vacia = {campo: "" for campo in encabezados}
        fila_vacia["Rutas Criticas"] = ruta_texto
        datos_csv.append(fila_vacia)

# Escribir al archivo CSV
with open(nombre_archivo, mode='w', newline='', encoding='utf-8') as archivo:
    escritor = csv.DictWriter(archivo, fieldnames=encabezados)
    escritor.writeheader()
    escritor.writerows(datos_csv)

# Mostrar las rutas críticas en la consola
print(f"Se encontraron {len(rutas_criticas)} rutas críticas:")
for i, ruta in enumerate(rutas_criticas, 1):
    print(f"Ruta {i}: ", end="")
    ruta_texto = " -> ".join([tarea.nombre for tarea in ruta])
    print(ruta_texto)