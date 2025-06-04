from MesasService import MesaService
from utils import Despejar

def gestionar_mesas():

    #Main function to manage tables in the system.
    #Allows you to create, delete, list tables, add and delete players,
    #and move players from the waiting queue to the active table.

    service = MesaService()  # Instance the service that handles the table logic

    while True:
        print("\n--- GESTIÓN DE MESAS ---")
        print("1. Crear mesa")
        print("2. Borrar mesa")
        print("3. Ver mesas")
        print("4. Agregar jugador a mesa")
        print("5. Mover siguiente jugador de cola a mesa")
        print("6. Eliminar jugador de mesa o cola")
        print("0. Volver al menú principal")

        opcion = input("Seleccione una opción: ")  # Read the option entered by the user

        if opcion == "1":
            Despejar()  # Clean the console or screen for a better presentation
            nombre_juego = input("Nombre del juego: ").strip().lower()  # Ask for the name of the game, in lower case and without extra spaces

            # Request the maximum number of players, validating that it is a number > 0
            while True:
                try:
                    can_jug = int(input("Cantidad máxima de jugadores: "))
                    if can_jug <= 0:
                        print("Debe ser mayor que 0.")
                    else:
                        break  # If valid, exit the loop
                except ValueError:
                    print("Ingrese un número válido.")  # Message if value is not numeric

            # Create the table with the game name and maximum number of players
            mesa = service.crearMesa(nombre_juego, can_jug)
            print(f"Mesa creada con ID: {mesa['mesa_id']}")  # Shows the ID generated for the table

        elif opcion == "2":
            Despejar()
            mid = input("ID de la mesa a borrar: ").strip().upper()  # Request the ID of the table to be deleted in capital letters

            # Try deleting the table; shows message according to result
            if service.borrarMesa(mid):
                print("Mesa borrada.")
            else:
                print("Mesa no encontrada.")

        elif opcion == "3":
            Despejar()

            # If there are no registered tables, notify the user
            if not service.mesas:
                print("No hay mesas registradas.")
            else:
                print("\nMesas actuales:")
                # Iterates over each table and displays its detailed information
                for m in service.mesas:
                    print(f"ID: {m['mesa_id']} | Juego: {m['juego']} | Max jugadores: {m['canJugadores']} | Activa: {m['activa']}")
                    print(f"  Jugadores: {m['jugadores']}")        # List of players at the table
                    print(f"  Cola: {m['cola_espera']}")           # List of players in queue

        elif opcion == "4":
            Despejar()
            mid = input("ID de la mesa: ").strip().upper()       # Request ID of the table to add a player to
            jid = input("ID del jugador a agregar: ").strip().upper()  # Request player ID

            # Try to add player to table and receive response (ok, message)
            ok, msg = service.agregar_jugador_a_mesa(mid, jid)
            print(msg)  # Show the result (success or error)

        elif opcion == "5":
            Despejar()
            mid = input("ID de la mesa: ").strip().upper()  #Request ID of the table where to move player

            # Try to move next player in queue to the table
            ok, msg = service.mover_siguiente_jugador(mid)
            print(msg)  # Shows result of the operation

        elif opcion == "6":
            Despejar()
            mid = input("ID de la mesa: ").strip().upper()       # Request table ID
            jid = input("ID del jugador a eliminar: ").strip().upper()  # Request ID of the player to be eliminated

            # Try to remove player from the table or queue
            ok, msg = service.eliminar_jugador_de_mesa(mid, jid)
            print(msg)  # Displays success or error message

        elif opcion == "0":
            break  # Exit the loop and return to the main menu

        else:
            print("Opción inválida. Intente nuevamente.")  #Message if an invalid option is entered
