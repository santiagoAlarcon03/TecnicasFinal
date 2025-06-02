from jugadores import gestionar_jugadores

def mostrar_menu():
    print("\n--- CASINO PYTHON ---")
    print("1. Gestión de Jugadores")
    print("2. Jugar")
    print("3. Reportes")
    print("4. Salir")

def main():
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            gestionar_jugadores()
        elif opcion == "2":
            jugar()
        elif opcion == "3":
            generar_reportes()
        elif opcion == "4":
            print("¡Gracias por visitar nuestro casino!")
            break
        else:
            print("Opción no válida. Intente nuevamente.")

if __name__ == "__main__":
    main()