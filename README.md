# Instrucciones de instalación y ejecución

## Instalación
La única dependencia del proyecto, aparte de las bibliotecas estandar de python3, es cplex.
De todas formas, se encuentra especificado en requirements.txt, y se puede instalar con:
- pip3 install -r requirements.txt
(Se puede instalar en un entorno virtual ejecutando antes de la instalación:
  python3 -m venv .
  source bin/activate
)

## Ejecución
- Programa principal:
python3 trabajoPL.py <entrada.txt> <salida.txt>
Escribe en <salida.txt> las soluciones (y los tiempos) de los problemas descritos en
<entrada.txt>, ambos con la sintaxis descrita en la memoria del trabajo. Además, muestra
por salida estandar detalles de la resolución de los problemas.
- Generación de problemas:
generar_problemas.py <salida.txt> [num_problemas] [<min_n>,<max_n>] [<min_m>,<max_m>] [<min_v>,<max_v>]
Genera en salida.txt un fichero con la sintaxis descrita en la memoria: num_problemas problemas, cada uno con
n, m y los valores v en los rangos indicados en los otros argumentos si se han incluido.
Todos los parametros con corchetes son opcionales y tienen valores por defecto.
