"""
Autor: Monzón González, Néstor
Adaptado a partir de generar_escenarios.py, de la práctica 2 de la asignatura (con Andrés Otero)
Uso: generar_problemas.py <salida.txt> [num_problemas] [<min_n>,<max_n>] [<min_m>,<max_m>] [<min_v>,<max_v>]
Genera en salida.txt un fichero con la sintaxis descrita en la memoria: num_problemas problemas, cada uno con
n, m y los valores v en los rangos indicados en los otros argumentos si se han incluido.
"""

import sys
from random import randint

def sep_coma(arg):
    """
    Devuelve en una tupla los dos numeros separados por coma en arg
    Comprueba que sean 2 parametros
    """
    lista = arg.split(",")
    if len(lista) != 2:
        print('Error:', arg, 'debe ser dos numeros separados por una coma (como \"3,1\")')
        exit(1)
    return (int(lista[0]), int(lista[1]))

def escribir_valores(f, m, min_val, max_val):
    """
    Escribe en f m enteros (pseudo)aleatorios entre min_val y max_val
    separados por espacios
    """
    lista = [str(randint(min_val, max_val)) for _ in range(m)] # lista de m numeros
    f.write(" ".join(lista)) # se escriben separados por espacio

def escribir_problema(f, n, m, min_val=1, max_val=10):
    """
    Imprime en las dos siguientes lineas del fichero f
    el problema con los parametros de los argumentos
    """
    # n y m:
    f.write(str(n) + ' ' + str(m) + '\n')
    # valores:
    escribir_valores(f, m, min_val, max_val)
    f.write('\n')

if __name__ == "__main__":
    if len(sys.argv) < 2: # invocado sin parametros (al menos necesita el fichero)
        print('Invocar como:\n' + sys.argv[0] + ' <salida.txt> [num_problemas] [<min_n>,<max_n>] [<min_m>,<max_m>] [<min_v>,<max_v>]')
        exit(1)

    f = open(sys.argv[1], "w") # abrir el archivo

    # Parametros por defecto:
    n_problemas = 1
    min_n = 5 # numero de herederos
    max_n = 5
    min_m = 10 # num de bienes
    max_m = 10
    min_v = 1 # valores de los bienes
    max_v = 500

    # Rangos explicitos:
    if len(sys.argv) > 2: # numero de problemas
        n_problemas = int(sys.argv[2])  # leer el numero de problemas

    if len(sys.argv) > 3: # de herederos
        (min_n, max_n) = sep_coma(sys.argv[3])

    if len(sys.argv) > 4: # de bienes
        (min_m, max_m) = sep_coma(sys.argv[4])

    if len(sys.argv) > 5: # de valores
        (min_v, max_v) = sep_coma(sys.argv[5])

    #print(n_problemas, min_n, max_n, min_m, max_m, min_v, max_v)

    f.write(str(n_problemas) + '\n') # escribir en f el numero de problemas
    # y cada problema:
    for i_prob in range(n_problemas):
        n = randint(min_n, max_n)
        m = randint(min_m, max_m)
        escribir_problema(f, n, m, min_val=min_v, max_val=max_v)

    # feedback:
    print('Generados', n_problemas, 'problemas con:\nn (numero de herederos) entre', min_n, 'y', max_n, \
          '\nm (numero de bienes) entre', min_m, 'y', max_m, '\nv (valor de los bienes) entre', min_v, 'y', max_v)

    f.close()
