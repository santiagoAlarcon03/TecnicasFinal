import json
from utils import cargar_datos, guardar_datos

def registrar_jugador():
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
            registrar_jugador()
        elif opcion == "2":
            consultar_jugador()
        elif opcion == "3":
            modificar_jugador()
        elif opcion == "4":
            eliminar_jugador()
        elif opcion == "5":
            listar_jugadores()
        elif opcion == "6":
            break
        else:
            print("Opción no válida. Intente nuevamente.")


def consultar_jugador():
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
    datos = cargar_datos()
    id_jugador = input("Ingrese ID del jugador a eliminar: ").upper()
    
    if id_jugador not in datos['jugadores']:
        print("Jugador no encontrado.")
        return
    
    # Verificar si el jugador está en alguna cola de juego
    en_cola = False
    for juego, cola in datos['colas_juegos'].items():
        if id_jugador in cola:
            en_cola = True
            break
    
    if en_cola:
        print("No se puede eliminar: el jugador está en una cola de juego.")
        return
    
    # Confirmación de eliminación
    jugador = datos['jugadores'][id_jugador]
    confirmacion = input(f"¿Está seguro de eliminar a {jugador['nombre']} (ID: {id_jugador})? (s/n): ").lower()
    
    if confirmacion == 's':
        del datos['jugadores'][id_jugador]
        guardar_datos(datos)
        print("Jugador eliminado exitosamente.")
    else:
        print("Eliminación cancelada.")
        
def listar_jugadores():
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
        
        
class Pila:
    def __init__(self, max_elementos=10):
        self.elementos = []
        self.max = max_elementos

    def push(self, item):
        if len(self.elementos) >= self.max:
            self.elementos.pop(0)
        self.elementos.append(item)

    def __str__(self):
        return str(self.elementos)

    def to_list(self):
        return self.elementos.copy()  # Esto es lo importante para guardar en JSON


class Cola:
    def __init__(self):
        self.items = []
    
    def encolar(self, item):
        self.items.append(item)
    
    def desencolar(self):
        return self.items.pop(0) if self.items else None
    
    def __str__(self):
        return str(self.items)
    