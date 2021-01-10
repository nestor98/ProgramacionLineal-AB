"""
Autor: Monzón González, Néstor
Adaptado a partir de escenario.py, de la practica 2 de la asignatura (con Andres Otero)
"""

import cplex
from timeit import default_timer as timer

def line_to_tuple(linea):
    """
    Separa linea (str) en sus dos numeros, separados por espacio.
    (Y asegura que sean numeros y que sean dos)
    Los devuelve en una tupla.
    """
    lista = linea.replace("\n", "").split(" ")
    if len(lista) != 2:
        print('Error de sintaxis:', linea, 'debe ser dos numeros separados por un espacio (como \"3 12\")')
        exit(1)
    return (int(lista[0]), int(lista[1]))

class Problema:
    """
    Contiene toda la información de un problema:
    n: número de herederos
    m: número de bienes
    v: lista con el valor de cada bien
    """
    def __init__(self, f, max_tiempo=300.0):
        """
        Inicializa el problema a partir de los datos del fichero f
        """
        # la primera línea contiene n y m
        (self.n, self.m) = line_to_tuple(f.readline())

        # la segunda, los valores de las minas
        self.v = f.readline().replace("\n", "").split(" ")
        self.v = [int(val) for val in self.v] # aseguramos que sean enteros

        if len(self.v) != self.m: # comprobamos que los numeros coincidan
            print('el numero de valores v no coincide con m: ', len(self.v), self.m)
            exit(1)

        self.max_tiempo = max_tiempo # por defecto 300 s, 5 min

    def __str__(self):
        """
        Devuelve la representación en string del problema. Principalmente para debug.
        Ejemplo de salida:
            Problema con n=4, m=10
            Valores: 80,310,229,825,129,671,95,91,902,270
        """
        string = "Problema con n=" + str(self.n) + ", m=" + str(self.m)
        v_str = [str(val) for val in self.v] # a string otra vez para el join:
        string += "\nValores: " + ",".join(v_str)
        return string


    def resolver(self):
        """
        Resuelve el problema instanciado con la libreria cplex. Guarda en self.solucion
        la lista con los valores asignados a cada variable. Muestra por salida estandar
        el progreso en las computaciones de cplex.
        """
        # instanciamos el problema:
        problem = cplex.Cplex()

        # para que sea menos verboso:
        n = self.n
        m = self.m
        v = self.v


        # Queremos minimizar la f objetivo:
        problem.objective.set_sense(problem.objective.sense.minimize)

        # Variables:
        #   xij: 1 sii el heredero i hereda j
        #   bi beneficio del heredero i (suma de los valores de los bienes asignados al heredero)
        #   maxb maximo bi pt i en [1, n],
        #   minb minimo
        names = ['x'+str(i+1)+str(j+1) for i in range(n) for j in range(m)] + ['b'+str(i+1) for i in range(n)] + ['maxb', 'minb']

        # Funcion objetivo: maxb - minb
        # los coeficientes de todas las variables son pues:
        objective = [0]*n*(m+1) + [1,-1]
        # (todas las x son 0: n*m; todas las b son 0: +n; maxb-minb: 1, -1)
        # por ej, para n=2, m=4: objective = [0,0,0,0,0,0,0,0,0,0,1,-1]

        # Tipos: las x (n*m) son binarias, el resto (bi, maxb y minb, n+2 en total) enteras
        tipos = [problem.variables.type.binary for i in range(n*m)] + [problem.variables.type.integer for i in range(n+2)]

        # añadimos estas variables:
        problem.variables.add(obj = objective,
                              names = names,
                              types = tipos)

        # Constraints, restricciones:
        # numero:
        n_constraints = 3*n + m # Porque:
        # 3*n: por cada heredero, hay una para minb, una para maxb y una para bi
        # m: por cada bien j, una constraint del tipo sum(xij)=1 pt i

        # las llamamos ck con k en [1, n_constraints]:
        constraint_names = ['c'+str(i+1) for i in range(n_constraints)]


        # constraints de maxb, especifican que maxb sea efectivamente el max
        # primer indice: bi con i en 1..n
        # segundo: maxb
        # expresa la izq de bi-maxb <= 0
        c_max = [[[n*m+i, n*m+n], [1, -1]] for i in range(n)]

        # constraints de minb, especifican que minb sea efectivamente el min
        # primer indice: bi con i en 1..n
        # segundo: minb
        # expresa la izq de minb-bi <= 0
        c_min = [[[n*m+i, n*m+n+1], [-1, 1]] for i in range(n)]
        #print('c_min')
        #print(c_min)

        # constraints de bi: hacen que bi sea el valor de lo heredado por i
        # [i*m+j for j in range(m)], donde i es el heredero, devuelve los m
        # indices correspondientes a las x del mismo
        # (ej: con n=4, m=4 y i=1: [x11, x12, x13, x14])
        # A esto se le añade [n*m+i], que es el beneficio del heredero i: bi
        # Los coeficientes de cada una de estas variables son v para las primeras
        # (los valores de esos bienes) y -1 para bi, ya que debe dar a:
        # sum(vi*xij)=bi pt j en 1..m, pt i en 1..n -> sum(vi*xij)-bi=0
        c_b =  [[[i*m+j for j in range(m)]+[n*m+i], v+[-1]] for i in range(n)]
        #print('c_b')
        #print(c_b)

        # constraints de xij: dado j, con i en 1..n, sum(vij)=1. Es decir, solo
        # un heredero puede heredar el bien j (y debe heredarlo alguien)
        # formalmente, esto da m constraints, una para cada bien, cuyos x deben sumar 1
        # en las variables, los indices de los x de un mismo bien estan separados por
        # m elementos:
        c_x = [[[i*m+j for i in range(n)], [1]*n] for j in range (m)]
        #print('c_x')
        #print(c_x)
        #print([(i, names[i]) for i in range(len(names))])

        constraints = c_max+c_min+c_b+c_x
        #print(len(c_max), len(c_min), len(c_b), len(c_x))

        # la parte derecha de las desigualdades: 0 para todas menos las c_x, que
        # son las m ultimas
        rhs = [0]*3*n+[1]*m
        #print('rhs', rhs)

        # sentidos de las desigualdades:
        # las de maxb y minb son <= (L), el resto son igualdades (E)
        constraint_senses = ["L"]*2*n+["E"]*(n+m)

        # Añadimos las restricciones definidas al problema:
        problem.linear_constraints.add(lin_expr = constraints,
                                       senses = constraint_senses,
                                       rhs = rhs,
                                       names = constraint_names)

        # fijamos el limite de tiempo:
        problem.parameters.timelimit.set(self.max_tiempo)

        ini = timer()
        # Y lo resolvemos:
        problem.solve()
        fin = timer()
        self.tiempo = fin-ini
        # Guardar la solucion:
        self.solucion = problem.solution.get_values()
        self.sol_dict = dict(zip(names, self.solucion)) # diccionario con {nombre_variable: valor_var}
        # print('---------quality metrics:---------')
        # print(problem.solution.get_quality_metrics())
        # print('----------------------------------')
        print('tiempo a mano:', self.tiempo)
        # And #print the solutions
        # print(problem.solution.get_values())



    def resumir_solucion(self):
        """
        Devuelve una string con el resumen (el reparto de bienes) de la solucion alcanzada, por ejemplo:
            maxima diferencia: 68
            heredero 1 (item valor):
            1 549
            4 978
            TOTAL: 1527
            heredero 2 (item valor):
            2 669
            3 926
            TOTAL: 1595
        """
        string = ""
        bienes = [str(j+1) for j in range(self.m)] # indice cada bien en str
        if not self.solucion:
            string = "Aun no se ha solucionado el problema"
        else:
            # string += 'maxima diferencia: ' + str(self.solucion[self.n*(self.m+1)]-self.solucion[self.n*(self.m+1)+1])
            string += 'maxima diferencia: ' + str(int(self.sol_dict['maxb']-self.sol_dict['minb']))
            for heredero in range(self.n):
                string += '\nheredero ' + str(heredero+1) + ' (item valor):\n' + '\n'.join([bienes[i]+' '+str(self.v[i]) for i in range(self.m) if self.solucion[i+self.m*heredero]])
                string += '\nTOTAL: ' + str(sum([self.v[i] for i in range(self.m) if self.solucion[i+self.m*heredero]]))
                # bienes_heredero = [bienes[i] for i in range(self.m) if self.solucion[i+self.m*heredero]]
                # for j in range(self.m):
                #     string += str(bienes[i])
        return(string)


    def guardar_solucion(self, f):
        """"
        Escribe en f una linea con la solucion en formato csv (numeros separados por espacio):
            n m t max_dif(objetivo) x11 .. xnm b1 .. bn maxb minb
        Si ha habido timeout (se ha superado el maximo tiempo fijado max_t) en lugar de las x escribe:
            n m t timeout! (maximo: <max_t>)
        """
        if self.solucion:
            lista = [self.n, self.m, self.tiempo, int(self.sol_dict['maxb']-self.sol_dict['minb'])]
            lista = [str(i) for i in lista] # a str
            sol_str = [str(int(i)) for i in self.solucion]
            f.write(' '.join(lista) + '\n' + ' '.join(sol_str) + '\n')

        else: # no hay solucion (asumimos que ha habido timeout, puede que se haya invocado antes de solucionar...)
            lista = [self.n, self.m, self.tiempo]
            lista = [str(i) for i in lista] # a str
            f.write(' '.join(lista) + '\n' + "timeout! (maximo: " + str(self.max_tiempo) + ")\n")
        # que se vaya escribiendo, para evitar perder todos los problemas si termina inesperadamente:
        f.flush()
