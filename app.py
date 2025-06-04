from jugadores import gestionar_jugadores  # Importa el menú de gestión de jugadores
from Juegos.Tragamonedas import tragamonedas  # Importa el juego de tragamonedas
from Juegos.Blackjack import blackjack  # Importa el juego de Blackjack
from utils import Despejar, cargar_datos  # Despejar: limpia pantalla. cargar_datos: carga datos del JSON
from Mesas import gestionar_mesas  # Menú de gestión de mesas
from MesasService import MesaService  # Clase que maneja la lógica de las mesas
from Juegos.backtracking_tragamonedas import menu_optimizacion  # Módulo de IA para optimizar tragamonedas

def mostrar_menu():
    # Muestra el menú principal del casino
    print("\n--- CASINO PYTHON ---")
    print("1. Gestión de Jugadores")
    print("2. Jugar")
    print("3. Gestión de mesas")
    print("4. Reportes")
    print("5. Salir")

def mostrar_menu_juegos():
    # Muestra las opciones de juegos disponibles
    print("\n=== JUEGOS DISPONIBLES ===")
    print("1. BlackJack")
    print("2. Tragamonedas")
    print("3. Optimizar estrategia de tragamonedas con IA (Backtracking)")
    print("0. Volver al menú principal")

def jugar():
    # Muestra el submenú para jugar y gestiona la elección del usuario
    while True:
        mostrar_menu_juegos()
        opcion = input("Seleccione un juego: ")

        if opcion == "1":
            Despejar()  # Limpia pantalla
            mesa = MesaService()  # Instancia del servicio de mesas
            blackjack(mesa)  # Ejecuta el juego de Blackjack
        elif opcion == "2":
            Despejar()
            mesa = MesaService()
            tragamonedas(mesa)  # Ejecuta el juego de tragamonedas
        elif opcion == "3":
            Despejar()
            menu_optimizacion()  # Ejecuta el optimizador de tragamonedas por backtracking
        elif opcion == "0":
            break  # Sale del submenú de juegos
        else:
            print("Opción no válida. Intente nuevamente.")  # Validación de entrada

def generar_reportes():
    # Genera distintos tipos de reportes estadísticos sobre jugadores y juegos
    datos = cargar_datos()
    jugadores = datos['jugadores']
    print("\n--- REPORTES ---")
    print("1. Jugadores con mayor saldo")
    print("2. Ver historial de un jugador")
    print("3. Ranking por juegos ganados")
    print("4. Jugadores con más juegos perdidos")
    print("5. Juegos con mayor cantidad de participaciones")

    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        Despejar()
        print("\n--- Jugadores con mayor saldo ---")
        top = sorted(jugadores.items(), key=lambda x: x[1]['saldo'], reverse=True)
        for id_j, info in top[:5]:  # Top 5 por saldo
            print(f"{info['nombre']} (ID: {id_j}) - Saldo: ${info['saldo']}")

    elif opcion == "2":
        Despejar()
        id_j = input("Ingrese ID del jugador: ").strip().upper()
        if id_j in jugadores:
            print(f"\nHistorial de {jugadores[id_j]['nombre']}:")
            for h in reversed(jugadores[id_j]['historial']):  # Muestra el historial en orden inverso
                print(" -", h)
        else:
            print("Jugador no encontrado.")

    elif opcion == "3":
        Despejar()
        print("\n--- Ranking por juegos ganados ---")
        ranking = sorted(jugadores.items(), key=lambda x: x[1]['estadisticas']['juegos_ganados'], reverse=True)
        for id_j, info in ranking[:5]:  # Top 5 por juegos ganados
            ganados = info['estadisticas']['juegos_ganados']
            print(f"{info['nombre']} (ID: {id_j}) - Juegos Ganados: {ganados}")
    
    elif opcion == "4":
        Despejar()
        print("\n--- Jugadores con más juegos perdidos ---")
        ranking = sorted(jugadores.items(), key=lambda x: x[1]['estadisticas']['juegos_perdidos'], reverse=True)
        for id_j, info in ranking[:5]:  # Top 5 por perdidos
            print(f"{info['nombre']} (ID: {id_j}) - Juegos Perdidos: {info['estadisticas']['juegos_perdidos']}")

    elif opcion == "5":
        Despejar()
        print("\n--- Juegos con mayor cantidad de participaciones ---")
        estadisticas = datos.get('estadisticas_juegos', {})  # Verifica si existen estadísticas
        ranking = sorted(estadisticas.items(), key=lambda x: x[1], reverse=True)
        for juego, cantidad in ranking:  # Muestra todas las estadísticas disponibles
            print(f"{juego.capitalize()}: {cantidad} partidas jugadas")

    else:
        print("Opción no válida.")  # Validación de entrada

def main():
    # Función principal que mantiene el menú del programa activo
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            gestionar_jugadores()  # Entra al submenú de jugadores
        elif opcion == "2":
            jugar()  # Entra al submenú de juegos
        elif opcion == "3":
            gestionar_mesas()  # Entra al submenú de mesas
        elif opcion == "4":
            generar_reportes()  # Muestra menú de reportes
        elif opcion == "5":
            print("¡Gracias por visitar nuestro casino!")  # Mensaje de salida
            break
        else:
            print("Opción no válida. Intente nuevamente.")  # Validación de entrada

if __name__ == "__main__":
    main()  # Llama al programa principal si se ejecuta directamente
