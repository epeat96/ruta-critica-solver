#! /usr/bin/env python3
# vim:fenc=utf-8
#
# Copyright © 2024 epeat <epeat@epeat-facu>
#
# Distributed under terms of the MIT license.

import csv

nombre_archivo = 'tabla.csv'

tareas = []
duraciones = []
dependencias = []
es = []
ef = []
fs = []
fs = []
holgura = []
rutas_criticas = []

with open(nombre_archivo, mode='r', encoding='utf-8') as archivo:
    lector = csv.DictReader(archivo)

    for fila in lector:
        dependencias.append(fila["Dependencias"])
        tareas.append(fila["Tareas"])
        duraciones.append(fila["Duraciones"])

    for tarea, indice in enumerate(tareas):


    print(f"Dependencias: {dependencias}")
    print(f"Tareas: {tareas}")
    print(f"Duraciones: {duraciones}")
