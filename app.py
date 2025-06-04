from jugadores import gestionar_jugadores
from Juegos.Tragamonedas import tragamonedas
from Juegos.Blackjack import blackjack
from utils import Despejar, cargar_datos
from Mesas import gestionar_mesas
from MesasService import MesaService

def mostrar_menu():
    print("\n--- CASINO PYTHON ---")
    print("1. Gestión de Jugadores")
    print("2. Jugar")
    print("3. Gestión de mesas")
    print("4. Reportes")
    print("5. Salir")

def mostrar_menu_juegos():
    print("\n=== JUEGOS DISPONIBLES ===")
    print("1. BlackJack")
    print("2. Tragamonedas")
    print("0. Volver al menú principal")

def jugar():
    while True:
        mostrar_menu_juegos()
        opcion = input("Seleccione un juego: ")

        if opcion == "1":
            Despejar()
            mesa = MesaService()
            blackjack(mesa)     
        elif opcion == "2":
            Despejar()
            mesa = MesaService()
            tragamonedas(mesa)
        elif opcion == "0":
            break
        else:
            print("Opción no válida. Intente nuevamente.")

def generar_reportes():
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
        for id_j, info in top[:5]:
            print(f"{info['nombre']} (ID: {id_j}) - Saldo: ${info['saldo']}")

    elif opcion == "2":
        Despejar()
        id_j = input("Ingrese ID del jugador: ").strip().upper()
        if id_j in jugadores:
            print(f"\nHistorial de {jugadores[id_j]['nombre']}:")
            for h in reversed(jugadores[id_j]['historial']):
                print(" -", h)
        else:
            print("Jugador no encontrado.")

    elif opcion == "3":
        Despejar()
        print("\n--- Ranking por juegos ganados ---")
        ranking = sorted(jugadores.items(), key=lambda x: x[1]['estadisticas']['juegos_ganados'], reverse=True)
        for id_j, info in ranking[:5]:
            ganados = info['estadisticas']['juegos_ganados']
            print(f"{info['nombre']} (ID: {id_j}) - Juegos Ganados: {ganados}")
    
    elif opcion == "4":
        Despejar()
        print("\n--- Jugadores con más juegos perdidos ---")
        ranking = sorted(jugadores.items(), key=lambda x: x[1]['estadisticas']['juegos_perdidos'], reverse=True)
        for id_j, info in ranking[:5]:
            print(f"{info['nombre']} (ID: {id_j}) - Juegos Perdidos: {info['estadisticas']['juegos_perdidos']}")

    elif opcion == "5":
        Despejar()
        print("\n--- Juegos con mayor cantidad de participaciones ---")
        estadisticas = datos.get('estadisticas_juegos', {})
        ranking = sorted(estadisticas.items(), key=lambda x: x[1], reverse=True)
        for juego, cantidad in ranking:
            print(f"{juego.capitalize()}: {cantidad} partidas jugadas")

    else:
        print("Opción no válida.")


def main():
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            gestionar_jugadores()
        elif opcion == "2":
            jugar() 
        elif opcion == "3":
            gestionar_mesas()
        elif opcion == "4":
            generar_reportes() 
        elif opcion == "5":
            print("¡Gracias por visitar nuestro casino!")
            break
        else:
            print("Opción no válida. Intente nuevamente.")

if __name__ == "__main__":
    main()