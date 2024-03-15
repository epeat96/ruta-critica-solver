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
        return f"nombre : {self.nombre} \n \t duracion : {self.duracion} \n \t es : {self.es} \n \t ef : {self.ef} \n \t ls : {self.ls} \n \t lf : {self.lf}"

    def agregarDependencias(self,dependencias):
        self.dependencias.extend(dependencias)

    def agregarDependientes(self,dependientes):
        self.dependientes.extend(dependientes)


tareas = []
dependencias = []
rutas_criticas = []
matriz_de_adyacencia = [[]]

with open(nombre_archivo, mode='r', encoding='utf-8') as archivo:
    lector = csv.DictReader(archivo)

    for indice, fila in enumerate(lector):
        tareas.append(Tarea(fila["Tareas"], fila["Duraciones"], 0, 0, 0, 0))
        dependencias.append(fila["Dependencias"])
    for indice, tarea in enumerate(tareas):

        if dependencias[indice] == "-":
            continue

        nombres_dependencias = set(dependencias[indice].split(','))

        dependencias_a_agregar = [dependencia for dependencia in tareas if dependencia.nombre in nombres_dependencias]

        tarea.agregarDependencias(dependencias_a_agregar)

        print(f"Tarea: {tarea} \n Dependencias:")
        for dependencia in dependencias_a_agregar:
            print(dependencia)
