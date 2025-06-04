from jugadores import gestionar_jugadores
from Juegos.Tragamonedas import tragamonedas
from Juegos.Blackjack import blackjack


def mostrar_menu():
    print("\n--- CASINO PYTHON ---")
    print("1. Gestión de Jugadores")
    print("2. Jugar")
    print("3. Reportes")
    print("4. Salir")

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
            blackjack()
        elif opcion == "2":
            tragamonedas()
        elif opcion == "0":
            break
        else:
            print("Opción no válida. Intente nuevamente.")

def main():
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            gestionar_jugadores()
        elif opcion == "2":
            jugar()  # 👈 
        elif opcion == "3":
            generar_reportes() 
        elif opcion == "4":
            print("¡Gracias por visitar nuestro casino!")
            break
        else:
            print("Opción no válida. Intente nuevamente.")

if __name__ == "__main__":
    main()