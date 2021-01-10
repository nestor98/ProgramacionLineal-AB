"""
Autor: Nestor Monzon
Adaptado a partir de p2.py, de la practica 2 de la asignatura (con Andres Otero)
Asignatura: Algoritmia Basica
Ejecucion: python3 trabajoPL.py <entrada.txt> <salida.txt>
Escribe en <salida.txt> las soluciones (y los tiempos) a los problemas descritos en
<entrada.txt>, ambos con la sintaxis descrita en la memoria del trabajo
"""

import sys
from problema import Problema
# from escenario import leer_escenario
# from solucionar import solucionar
# from timeit import default_timer as timer
# from arbol import Nodo

if __name__ == '__main__':
    if len(sys.argv) < 3: # se debe invocar con dos parametros
        print('Invocar como:\n' + sys.argv[0] + ' <entrada.txt> <salida.txt>')
        exit(1)

    f = open(sys.argv[1], "r")  # leer archivo
    f_out = open(sys.argv[2], "w")

    n = int(f.readline().replace("\n", ""))  # leer el numero de problemas
    problemas = []
    for i in range(n):
        problemas.append(Problema(f)) # leemos cada problema del fichero
    f.close()
    for numero, p in enumerate(problemas):
        # prints para leerlo mientras se ejecuta
        print('(' + str(numero) + ')', p)
        print('Solucionando...')
        p.resolver()
        print('----------------------------------------------------------')
        print('Resumen de la solucion:')
        print(p.resumir_solucion())
        print('----------------------------------------------------------')
        print('----------------------------------------------------------')
        # guardar en el fichero de salida (ver guardar_solucion en problema.py):
        p.guardar_solucion(f_out)
    f_out.close()
