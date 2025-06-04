from jugadores import gestionar_jugadores  # Import the player management menu
from Juegos.Tragamonedas import tragamonedas  # Import the player management menu
from Juegos.Blackjack import blackjack  # Blackjack game matters
from utils import Despejar, cargar_datos  # Clear: clear screen. load_data: load data from JSON
from Mesas import gestionar_mesas  # Table management menu
from MesasService import MesaService  # Class that handles table logic
from Juegos.backtracking_tragamonedas import menu_optimizacion  # AI module to optimize slots

def mostrar_menu():
    # Shows the main casino menu
    print("\n--- CASINO PYTHON ---")
    print("1. Gestión de Jugadores")
    print("2. Jugar")
    print("3. Gestión de mesas")
    print("4. Reportes")
    print("5. Salir")

def mostrar_menu_juegos():
    # Shows available game options
    print("\n=== JUEGOS DISPONIBLES ===")
    print("1. BlackJack")
    print("2. Tragamonedas")
    print("3. Optimizar estrategia de tragamonedas con IA (Backtracking)")
    print("0. Volver al menú principal")

def jugar():
    #Show submenu to play and manage user choice
    while True:
        mostrar_menu_juegos()
        opcion = input("Seleccione un juego: ")

        if opcion == "1":
            Despejar()  # Clean screen
            mesa = MesaService()  # Table service instance
            blackjack(mesa)  # Run the Blackjack game
        elif opcion == "2":
            Despejar()
            mesa = MesaService()
            tragamonedas(mesa)  # Run the slot game
        elif opcion == "3":
            Despejar()
            menu_optimizacion()  # Run the backtracking slot optimizer
        elif opcion == "0":
            break  # Exits the games submenu
        else:
            print("Opción no válida. Intente nuevamente.")  # Input validation

def generar_reportes():
    # Generate different types of statistical reports about players and games
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
        for id_j, info in top[:5]:  # Top 5 by balance
            print(f"{info['nombre']} (ID: {id_j}) - Saldo: ${info['saldo']}")

    elif opcion == "2":
        Despejar()
        id_j = input("Ingrese ID del jugador: ").strip().upper()
        if id_j in jugadores:
            print(f"\nHistorial de {jugadores[id_j]['nombre']}:")
            for h in reversed(jugadores[id_j]['historial']):  # Show history in reverse order
                print(" -", h)
        else:
            print("Jugador no encontrado.")

    elif opcion == "3":
        Despejar()
        print("\n--- Ranking por juegos ganados ---")
        ranking = sorted(jugadores.items(), key=lambda x: x[1]['estadisticas']['juegos_ganados'], reverse=True)
        for id_j, info in ranking[:5]:  # Top 5 for games won
            ganados = info['estadisticas']['juegos_ganados']
            print(f"{info['nombre']} (ID: {id_j}) - Juegos Ganados: {ganados}")
    
    elif opcion == "4":
        Despejar()
        print("\n--- Jugadores con más juegos perdidos ---")
        ranking = sorted(jugadores.items(), key=lambda x: x[1]['estadisticas']['juegos_perdidos'], reverse=True)
        for id_j, info in ranking[:5]:  # Top 5 for lost
            print(f"{info['nombre']} (ID: {id_j}) - Juegos Perdidos: {info['estadisticas']['juegos_perdidos']}")

    elif opcion == "5":
        Despejar()
        print("\n--- Juegos con mayor cantidad de participaciones ---")
        estadisticas = datos.get('estadisticas_juegos', {})  # Check if statistics exist
        ranking = sorted(estadisticas.items(), key=lambda x: x[1], reverse=True)
        for juego, cantidad in ranking:  # Shows all available statistics
            print(f"{juego.capitalize()}: {cantidad} partidas jugadas")

    else:
        print("Opción no válida.")  # Input validation

def main():
    # Main function that keeps the program menu active
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            gestionar_jugadores()  # Enter the players submenu
        elif opcion == "2":
            jugar()  # Enter the games submenu
        elif opcion == "3":
            gestionar_mesas()  # Enter the tables submenu
        elif opcion == "4":
            generar_reportes()  # Show report menu
        elif opcion == "5":
            print("¡Gracias por visitar nuestro casino!")  # Outgoing message
            break
        else:
            print("Opción no válida. Intente nuevamente.")  # Input validation

if __name__ == "__main__":
    main()  # Calls the main program if executed directly
