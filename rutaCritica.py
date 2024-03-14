#! /usr/bin/env python3
# vim:fenc=utf-8
#
# Copyright © 2024 epeat <epeat@epeat-facu>
#
# Distributed under terms of the MIT license.

import csv

# Reemplaza 'nombre_de_archivo.csv' con el nombre de tu archivo CSV
nombre_archivo = 'tabla.csv'

tareas = []
dependencias = []
duraciones = []

# Abre el archivo CSV
with open(nombre_archivo, mode='r', encoding='utf-8') as archivo:
    lector = csv.DictReader(archivo)

    # Itera sobre las fila del archivo CSV
    for fila in lector:
        dependencias.append(fila["Dependencias"])
        tareas.append(fila["Tareas"])
        duraciones.append(fila["Duraciones"])

    print(f"Dependencias: {dependencias}")
    print(f"Tareas: {tareas}")
    print(f"Duraciones: {duraciones}")
