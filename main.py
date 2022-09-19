from random import randint


def mark(maze, pos):
    """
         Función de marcado, utilizada para marcar la posición de la historia.
         : param maze: un laberinto de matriz bidimensional de tamaño m * n
         : param pos: las coordenadas de la posición actual que se marcarán pos = (x, y), x = pos [0], y = pos [1]
    """
    maze[pos[0]][pos[1]] = 2  # Marque la posición pasada como 2


def move(maze, pos):
    """
         Función de movimiento, utilizada para probar si la posición actual puede continuar moviéndose, la condición de movimiento es que la posición actual es 0
         : param maze: un laberinto de matriz bidimensional de tamaño m * n
         : param pos: las coordenadas de la posición actual que se marcarán pos = (x, y), x = pos [0], y = pos [1]
         : return: tipo bool
    """
    return maze[pos[0]][pos[1]] == 0


move_path = []  # Registre las coordenadas de la ruta en movimiento que puede llegar con éxito a la salida
path_direction = []  # Registre la dirección de la trayectoria de movimiento que puede alcanzar con éxito la salida


def find_path(maze, start, end):
    """
         Función de búsqueda de ruta
         : param maze: un laberinto de matriz bidimensional de tamaño m * n
         : inicio del parámetro: coordenada de la posición del punto de inicio, inicio = (1, 1)
         : param end: las coordenadas del punto final, end = (m, n)
         : return: tipo bool
    """
    mark(maze, start)  # Marcar la posición inicial
    if start == end:  # La condición de terminación de la búsqueda de ruta (recursiva) es llegar al final
        move_path.append(start)
        return True

    # Cuando no se alcanza el punto final, hay 4 direcciones de movimiento posibles, a saber, arriba (-1, 0), abajo (1, 0), izquierda (0, -1), derecha (0, 1)
    move_direction = [
        (-1, 0), (1, 0), (0, -1), (0, 1)
    ]
    direction = ['↑', '↓', '←', '→']
    for i in range(4):  # Atraviesa 4 direcciones posibles
        next_start = (start[0] + move_direction[i][0], start[1] + move_direction[i][1])  # Las coordenadas del próximo punto de partida posible
        if move(maze, next_start):  # Encuentra las coordenadas del siguiente punto de partida que se puede mover si hay 0 e ingresa la recursividad
            if find_path(maze, next_start, end):
                # La razón por la que las coordenadas del punto de inicio todavía se agregan aquí es porque cuando se consulta la siguiente posición, es el punto final o cuando se puede alcanzar el punto final, se registra la posición actual.
                move_path.append(start)
                path_direction.append(direction[i])  # Dirección de ruta de registro
                return True
    return False  # Después de atravesar las 4 direcciones posibles y aún no puedes llegar al final, significa que no puedes salir del laberinto.


def gen_maze(m, n):
    """
         Generar matriz de laberinto aleatorio
         : param m: tipo int
         : param n: tipo int
    :return: maze
    """
    m += 2
    n += 2  # myn son ambos +2 para construir el 1 más externo
    maze = [[1 for i in range(n)] for j in range(m)]  # Inicializar una matriz bidimensional con un tamaño de m * ny todos los valores de 1
    for x in range(1, m-1):
        for y in range(1, n-1):
            """
                         Aquí, el rango de valores de x, y es x ∈ [1, m-1), e y ∈ [1, n-1) se debe a que configuramos la capa más externa (alrededor) del laberinto en 1, como por ejemplo:
                         Considerando una matriz de 3 * 3, una posible matriz es:
            [
              _  |←--- n:y ---→|
              ↑  [1, 1, 1, 1, 1],
              |  [1, 0, 1, 0, 1],
            m:x  [1, 0, 0, 1, 1],
              |  [1, 1, 0, 0, 1],
              ↓  [1, 1, 1, 1, 1]  
            ]
            """
            if (x == 1 and y == 1) or (x == m - 2 and y == n - 2):
                maze[x][y] = 0  # El punto de inicio y el punto final deben ser 0
            else:
                maze[x][y] = randint(0, 1)  # En el caso de que la capa más externa sea 1, la selección aleatoria interna 0, 1
    return maze


def print_maze(maze, text='El laberinto original es:', end1='   ', end2='\n\n', xs=0, xe=0, ys=0, ye=0):
    """
         Matriz de laberinto de salida, no es necesario, la anotación se puede eliminar
         : param maze: un laberinto de matriz bidimensional de tamaño m * n
         : texto param: mensaje de salida
         : param end1: controla el final de cada línea
         : param end2: controla el final de cada línea
         : param xs: controla si se emite el anillo superior 1, se emite 0, no se emite 1
         : param xe: Controla si se emite el anillo superior 1, se emite 0, no se emite 1
         : param ys: controla si se emite el anillo superior 1, se emite 0, no se emite 1
         : param ye: controla si se emite el anillo superior 1, se emite 0, no se emite 1
    """
    print(text)
    n, m = len(maze[0]), len(maze)
    for x in range(xs, m-xe):
        for y in range(ys, n-ye):
            print(maze[x][y], end=end1)
        print(end=end2)


def path_maze(maze, directions_map):
    """
         Genera una matriz de laberinto con caminos en movimiento.
         : param maze: un laberinto de matriz bidimensional de tamaño m * n
         : param Directions_map: Un diccionario que registra las coordenadas de la dirección de movimiento, con ↑, ↓, ←, → 4 elementos
    :return: path_maze
    """
    n, m = len(maze[0]), len(maze)
    for x in range(1, m-1):
        for y in range(1, n-1):
            maze[x][y] = maze[x][y] if maze[x][y] != 2 else 0  # Restaurar el 2 marcado a 0

    for x in range(m):
        for i in range(1, 2 * n - 1, 2):
            maze[x].insert(i, '   ')  # Reinicializar laberinto, insertar un marcador de posición '' 3 espacios entre cada dos elementos

    for x in range(1, 2 * m - 1, 2):
        maze.insert(x, [' ', '   '] * (n-1) + [''])  # Inserte dos marcadores de posición de espacio '' y ''

    for direction in directions_map:
        for directions_position in directions_map[direction]:
            i, j = directions_position
            i = 2 * i
            j = 2 * j
            if direction == "↑":
                maze[i - 1][j] = "↑"
            if direction == "↓":
                maze[i + 1][j] = "↓"
            if direction == "←":
                maze[i][j] = " ← "
            if direction == "→":
                maze[i][j + 1] = " → "
    return maze


def main():
    # maze = gen_maze(m=10, n=12)
    maze = \
        [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1],
            [1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1],
            [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1],
            [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
            [1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1],
            [1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]  # Ingrese la matriz de estilo, donde la capa más externa está rodeada por un anillo 1, el propósito es facilitar el procesamiento posterior, puede usar la función gen_maze () para autogenerar
    print_maze(maze)
    if find_path(maze, start=(1, 1), end=(10, 12)):
        mp = move_path[::-1]
        pd = path_direction[::-1]
        # Aquí pos [0] y pos [1] son ​​ambos -1 porque hay el anillo 1 más externo en el cálculo recursivo original
        print('El orden del movimiento de coordenadas es:', [(pos[0]-1, pos[1]-1) for pos in mp])
        path_direction_map = {
            '↑': [],
            '↓': [],
            '←': [],
            '→': []
        }  # Tabla de mapeo de dirección de ruta
        for i in range(len(pd)):
            path_direction_map[pd[i]].append(mp[i])
        maze = path_maze(maze, path_direction_map)
        print_maze(maze, text='El camino en movimiento del laberinto es:', end1='', end2='\n', xs=1, xe=1, ys=1, ye=1)
    else:
        print('Este laberinto no tiene solución')


if __name__ == '__main__':
    main()
