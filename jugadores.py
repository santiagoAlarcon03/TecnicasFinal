import json  # Module to handle data in JSON format
from utils import cargar_datos, guardar_datos, Despejar  # Utility functions for persistence and screen clearing

def registrar_jugador():
    #Allows you to register a new player with unique ID, name, starting balance and blank statistics.
    #Validates that the ID is not repeated and that the balance is a positive number.
    datos = cargar_datos()
    
    print("\n--- REGISTRO DE NUEVO JUGADOR ---")
    
    while True:
        id_jugador = input("Ingrese ID único (alfanumérico): ").strip().upper()
        if not id_jugador:
            print("El ID no puede estar vacío.")
            continue
        
        if id_jugador in datos['jugadores']:
            print("Este ID ya está registrado. Intente con otro.")
        else:
            break
    
    nombre = input("Nombre completo: ").strip()
    
    while True:
        try:
            saldo = float(input("Saldo inicial: $"))
            if saldo < 0:
                print("El saldo no puede ser negativo.")
            else:
                break
        except ValueError:
            print("Ingrese un valor numérico válido.")
    
    nuevo_jugador = {
        'nombre': nombre,
        'saldo': saldo,
        'historial': [],
        'estadisticas': {
            'juegos_ganados': 0,
            'juegos_perdidos': 0,
            'total_apostado': 0
        }
    }
    
    datos['jugadores'][id_jugador] = nuevo_jugador
    guardar_datos(datos)
    print(f"\n¡Jugador {nombre} registrado con éxito! ID: {id_jugador}")


def gestionar_jugadores():
    # Player management menu with options to register, consult, modify, delete and list players.
    while True:
        print("\n--- GESTIÓN DE JUGADORES ---")
        print("1. Registrar nuevo jugador")
        print("2. Consultar jugador")
        print("3. Modificar jugador")
        print("4. Eliminar jugador")
        print("5. Listar todos los jugadores")
        print("6. Volver al menú principal")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            Despejar()
            registrar_jugador()
        elif opcion == "2":
            Despejar()
            consultar_jugador()
        elif opcion == "3":
            Despejar()
            modificar_jugador()
        elif opcion == "4":
            Despejar()
            eliminar_jugador()
        elif opcion == "5":
            Despejar()
            listar_jugadores()
        elif opcion == "6":
            break
        else:
            print("Opción no válida. Intente nuevamente.")


def consultar_jugador():
    #Allows you to search and print detailed information about a registered player, including statistics and history.
    datos = cargar_datos()
    id_jugador = input("Ingrese ID del jugador a consultar: ").upper()
    
    if id_jugador in datos['jugadores']:
        jugador = datos['jugadores'][id_jugador]
        print("\n--- INFORMACIÓN DEL JUGADOR ---")
        print(f"ID: {id_jugador}")
        print(f"Nombre: {jugador['nombre']}")
        print(f"Saldo: ${jugador['saldo']:.2f}")
        print(f"Juegos ganados: {jugador['estadisticas']['juegos_ganados']}")
        print(f"Juegos perdidos: {jugador['estadisticas']['juegos_perdidos']}")
        print(f"Total apostado: ${jugador['estadisticas']['total_apostado']:.2f}")
        print("\nHistorial reciente:")
        for accion in jugador['historial'][-5:]:
            print(f"- {accion}")
    else:
        print("Jugador no encontrado.")


def modificar_jugador():
    #Allows you to modify the name and balance of an existing player. Validate that the new balance is valid.
    datos = cargar_datos()
    id_jugador = input("Ingrese el ID del jugador que desea modificar: ").upper()

    if id_jugador not in datos['jugadores']:
        print(" Jugador no encontrado.")
        return

    jugador = datos['jugadores'][id_jugador]
    print(f"\n--- Modificando a {jugador['nombre']} ---")

    nuevo_nombre = input("Nuevo nombre (Enter para mantener actual): ").strip()
    if nuevo_nombre:
        jugador['nombre'] = nuevo_nombre

    while True:
        print(f"Saldo actual: {jugador['saldo']}")
        nuevo_saldo = input("Nuevo saldo (Enter para mantener actual): ").strip()
        if not nuevo_saldo:
            break
        try:
            saldo_float = float(nuevo_saldo)
            if saldo_float < 0:
                print(" El saldo no puede ser negativo.")
            else:
                jugador['saldo'] = saldo_float
                break
        except ValueError:
            print(" Ingrese un valor numérico válido.")

    datos['jugadores'][id_jugador] = jugador
    guardar_datos(datos)
    print(" Jugador modificado con éxito.")


def eliminar_jugador():
    #Eliminate a player if they are not in any game queue. Requires user confirmation.
    datos = cargar_datos()
    id_jugador = input("Ingrese ID del jugador a eliminar: ").upper()
    
    if id_jugador not in datos['jugadores']:
        print("Jugador no encontrado.")
        return
    
    # Check if the player is in a game queue
    en_cola = False
    for juego, cola in datos['colas_juegos'].items():
        if id_jugador in cola:
            en_cola = True
            break
    
    if en_cola:
        print("No se puede eliminar: el jugador está en una cola de juego.")
        return
    
    #Deletion confirmation
    jugador = datos['jugadores'][id_jugador]
    confirmacion = input(f"¿Está seguro de eliminar a {jugador['nombre']} (ID: {id_jugador})? (s/n): ").lower()
    
    if confirmacion == 's':
        del datos['jugadores'][id_jugador]
        guardar_datos(datos)
        print("Jugador eliminado exitosamente.")
    else:
        print("Eliminación cancelada.")


def listar_jugadores():
    #Displays a table with all registered players, including main statistics.
    datos = cargar_datos()
    
    if not datos['jugadores']:
        print("No hay jugadores registrados.")
        return
    
    print("\n--- LISTADO DE JUGADORES ---")
    print("{:<10} {:<20} {:<10} {:<10} {:<10}".format(
        "ID", "Nombre", "Saldo", "Ganados", "Perdidos"))
    print("-" * 60)
    
    for id_jugador, jugador in datos['jugadores'].items():
        print("{:<10} {:<20} ${:<9.2f} {:<10} {:<10}".format(
            id_jugador,
            jugador['nombre'],
            jugador['saldo'],
            jugador['estadisticas']['juegos_ganados'],
            jugador['estadisticas']['juegos_perdidos']))


# Stack type data structure
class Pila:
    def __init__(self, max_elementos=10):
        #Stack type data structure
        self.elementos = []
        self.max = max_elementos

    def push(self, item):
        #Adds an item to the stack. If the maximum is exceeded, the oldest is deleted (FIFO).
        if len(self.elementos) >= self.max:
            self.elementos.pop(0)
        self.elementos.append(item)

    def __str__(self):
        #Returns a string representation of the stack.
        return str(self.elementos)

    def to_list(self):
        #Returns a copy of the stack as a list (useful for saving to JSON).
        return self.elementos.copy()


# Queue type data structure
class Cola:
    def __init__(self):
        #Initializes an empty queue.
        self.items = []
    
    def encolar(self, item):
        #Adds an element to the end of the queue.
        self.items.append(item)
    
    def desencolar(self):
        #Delete and return the first element of the queue. Returns None if empty.
        return self.items.pop(0) if self.items else None
    
    def __str__(self):
        #Returns a string representation of the queue.
        return str(self.items)
