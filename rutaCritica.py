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


def obtenerRutasCriticas(nodo, ruta, rutas_criticas):
    if len(nodo.dependientes) == 0:
        ruta.append(nodo)
        rutas_criticas.append(ruta)
        return nodo
    if nodo.lf - nodo.ef == 0:
        ruta.append(nodo)
    for dependiente in nodo.dependientes:
        if dependiente.lf - dependiente.ef == 0:
            obtenerRutasCriticas(dependiente, ruta, rutas_criticas)


tareas = []
dependencias = []
rutas_criticas = []
encabezados = ["Tareas", "Duraciones", "Dependencias",
               "ES", "EF", "LS", "LF", "Holgura", "Rutas Criticas"]
filas = []

with open(nombre_archivo, mode='r', encoding='utf-8') as archivo:
    lector = csv.DictReader(archivo)

    for indice, fila in enumerate(lector):
        tareas.append(Tarea(fila["Tareas"], int(
            fila["Duraciones"]), 0, 0, 0, 0))
        dependencias.append(fila["Dependencias"])

for indice, tarea in enumerate(tareas):

    if dependencias[indice] == "-":
        continue

    nombres_dependencias = set(dependencias[indice].split(','))

    dependencias_a_agregar = [
        dependencia for dependencia in tareas if dependencia.nombre in nombres_dependencias]

    tarea.agregarDependencias(dependencias_a_agregar)

for tarea in tareas:
    for dependencia in tarea.dependencias:
        dependencia.agregarDependiente(tarea)


calcular_es_ef(tareas)
duracion_proyecto = max(tarea.ef for tarea in tareas)
calcular_ls_lf(tareas, duracion_proyecto)

for indice, tarea in enumerate(tareas):
    fila = {}
    fila["Tareas"] = tarea.nombre
    fila["Duraciones"] = tarea.duracion
    fila["Dependencias"] = dependencias[indice]
    fila["ES"] = tarea.es
    fila["EF"] = tarea.ef
    fila["LS"] = tarea.ls
    fila["LF"] = tarea.lf
    fila["Holgura"] = tarea.lf - tarea.ef
    filas.append(fila)

with open(nombre_archivo, mode='w', newline='', encoding='utf-8') as archivo:
    escritor = csv.DictWriter(archivo, fieldnames=encabezados)
    escritor.writeheader()
    escritor.writerows(filas)

obtenerRutasCriticas(tareas[0], [], rutas_criticas)
for ruta in rutas_criticas:
    for tarea in ruta:
        print(f"{tarea.nombre}", end="->")
    print("")
