#! /usr/bin/env python3
# vim:fenc=utf-8
#
# Copyright © 2024 epeat <epeat@epeat-facu>
#
# Distributed under terms of the MIT license.

import csv

nombre_archivo = 'tabla.csv'


class Tarea:

    def __init__(self, nombre, duracion, dependencias, es, ef, ls, lf):
        self.nombre = nombre
        self.duracion = duracion
        self.dependencias = dependencias
        self.es = es
        self.ef = ef
        self.ls = ls
        self.lf = lf

    def __str__(self):
        return f"nombre : {self.nombre} \n \t duracion : {self.duracion} \n \t dependencias : {self.dependencias} \n \t es : {self.es} \n \t ef : {self.ef} \n \t ls : {self.ls} \n \t lf : {self.lf}"


tareas = []
rutas_criticas = []
matriz_de_adyacencia = [[]]

with open(nombre_archivo, mode='r', encoding='utf-8') as archivo:
    lector = csv.DictReader(archivo)

    for fila in lector:
        tareas.append(Tarea(fila["Tareas"], fila["Duraciones"], fila["Dependencias"].split(","), 0, 0, 0, 0))
    print("Tareas:")
    for tarea in tareas:
        print(f"{tarea.nombre}: \n \t {tarea.__str__()}")
