import json
from Particula import Particula
from algoritmos import distancia_euclidiana


class listaParticula:
    def __init__(self):
        self.__particulas = []

    def agregar_inicio(self, particula: Particula):
        self.__particulas.insert(0, particula)

    def agregar_final(self, particula: Particula):
        self.__particulas.append(particula)

    def mostrar(self):
        for particula in self.__particulas:
            print(particula)

    def __str__(self):
        return "".join(
            str(particula) for particula in self.__particulas
        )

    def guardar(self, ubicacion):
        try:
            with open(ubicacion, 'w') as archivo:
                lista = [particula.to_dict()
                         for particula in self.__particulas]

                json.dump(lista, archivo, indent=5)
            return 1
        except:
            return 0

    def abrir(self, ubicacion):
        try:
            with open(ubicacion, 'r') as archivo:
                lista = json.load(archivo)
                self.__particulas = [Particula(**particula)
                                     for particula in lista]
            return 1
        except:
            return 0

    def __len__(self):
        return len(self.__particulas)

    def __iter__(self):
        self.cont = 0
        return self

    def __next__(self):
        if self.cont < len(self.__particulas):
            """ Asignamos la particula a devolver """
            particula = self.__particulas[self.cont]
            """ Incremenamos el contador """
            self.cont += 1
            return particula
        """ detemos la iteración si se sobrepasa el tamaño de la lista """
        raise StopIteration

    def sortById(self):
        self.__particulas.sort()

    def sortByDistance(self):
        self.__particulas.sort(key=sort_distance, reverse=True)

    def sortBySpeed(self):
        self.__particulas.sort(key=sort_speed)

    """ Metodo de busqueda por fuerza bruta """

    def puntos_cercanos(self):
        """ Almacenará los resultados de la detección """
        resultado = []
        for punto_i in self.__particulas:
            x = punto_i.origen_x
            y = punto_i.origen_y
            """ utilizamos una distancia considerablemente grande para forzar que el punto
             de comparación siempre tenga una distancia inferior al inicio, despues se obtendrá
             el punto verdaderamente más cercano"""
            minimo = 10000
            cercano = (0, 0)
            color = (punto_i.red,
                     punto_i.green,
                     punto_i.blue)
            """ Segundo recorrido para hacer la comparación con el elemento actual """
            for punto_j in self.__particulas:
                """ Evitamos comparar el punto inicial con el mismo """
                if (punto_i != punto_j):
                    """ Guardamos los nuevos puntos de comparación """
                    x_comparison = punto_j.origen_x
                    y_comparison = punto_j.origen_y
                    """ Obtenemos la distancia euclidiana entre los 2 puntos para determinar si es
                        mayor o menor """
                    d = distancia_euclidiana(x, y, x_comparison, y_comparison)
                    if d < minimo:
                        """ Corregimos el valor de la distancia minima para proximas comparaciones """
                        minimo = d
                        """ Asignamos al punto más cercanos con los valores de comparación actuales """
                        cercano = (x_comparison, y_comparison)
            """ Agregamos al arreglo el punto inicial de comparación y depues el punto que se
            detectó como el más cercano """
            resultado.append(((x, y), cercano, color))
        """ Finalmente retornamos los resultados obtenidos """
        return resultado


""" Metodos fuera de "lista particula" """


def sort_distance(particula):
    return particula.distancia


def sort_speed(particula):
    return particula.velocidad
