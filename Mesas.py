from MesasService import MesaService
from utils import Despejar

def gestionar_mesas():
    """
    Función principal para gestionar mesas en el sistema.
    Permite crear, borrar, listar mesas, agregar y eliminar jugadores,
    y mover jugadores desde la cola de espera hacia la mesa activa.
    """
    service = MesaService()  # Instancia el servicio que maneja la lógica de mesas

    while True:
        print("\n--- GESTIÓN DE MESAS ---")
        print("1. Crear mesa")
        print("2. Borrar mesa")
        print("3. Ver mesas")
        print("4. Agregar jugador a mesa")
        print("5. Mover siguiente jugador de cola a mesa")
        print("6. Eliminar jugador de mesa o cola")
        print("0. Volver al menú principal")

        opcion = input("Seleccione una opción: ")  # Lee la opción ingresada por el usuario

        if opcion == "1":
            Despejar()  # Limpia la consola o pantalla para mejor presentación
            nombre_juego = input("Nombre del juego: ").strip().lower()  # Pide nombre del juego, en minúsculas y sin espacios extra

            # Solicita la cantidad máxima de jugadores, validando que sea un número > 0
            while True:
                try:
                    can_jug = int(input("Cantidad máxima de jugadores: "))
                    if can_jug <= 0:
                        print("Debe ser mayor que 0.")
                    else:
                        break  # Si es válido, sale del ciclo
                except ValueError:
                    print("Ingrese un número válido.")  # Mensaje si el valor no es numérico

            # Crea la mesa con el nombre de juego y cantidad máxima de jugadores
            mesa = service.crearMesa(nombre_juego, can_jug)
            print(f"Mesa creada con ID: {mesa['mesa_id']}")  # Muestra el ID generado para la mesa

        elif opcion == "2":
            Despejar()
            mid = input("ID de la mesa a borrar: ").strip().upper()  # Solicita el ID de la mesa a borrar en mayúsculas

            # Intenta borrar la mesa; muestra mensaje según resultado
            if service.borrarMesa(mid):
                print("Mesa borrada.")
            else:
                print("Mesa no encontrada.")

        elif opcion == "3":
            Despejar()

            # Si no hay mesas registradas, avisa al usuario
            if not service.mesas:
                print("No hay mesas registradas.")
            else:
                print("\nMesas actuales:")
                # Itera sobre cada mesa y muestra su información detallada
                for m in service.mesas:
                    print(f"ID: {m['mesa_id']} | Juego: {m['juego']} | Max jugadores: {m['canJugadores']} | Activa: {m['activa']}")
                    print(f"  Jugadores: {m['jugadores']}")        # Lista de jugadores en la mesa
                    print(f"  Cola: {m['cola_espera']}")           # Lista de jugadores en cola de espera

        elif opcion == "4":
            Despejar()
            mid = input("ID de la mesa: ").strip().upper()       # Pide ID de la mesa a la cual agregar jugador
            jid = input("ID del jugador a agregar: ").strip().upper()  # Pide ID del jugador

            # Intenta agregar jugador a mesa y recibe respuesta (ok, mensaje)
            ok, msg = service.agregar_jugador_a_mesa(mid, jid)
            print(msg)  # Muestra el resultado (exito o error)

        elif opcion == "5":
            Despejar()
            mid = input("ID de la mesa: ").strip().upper()  # Pide ID de la mesa donde mover jugador

            # Intenta mover siguiente jugador de la cola a la mesa
            ok, msg = service.mover_siguiente_jugador(mid)
            print(msg)  # Muestra resultado de la operación

        elif opcion == "6":
            Despejar()
            mid = input("ID de la mesa: ").strip().upper()       # Pide ID de la mesa
            jid = input("ID del jugador a eliminar: ").strip().upper()  # Pide ID del jugador a eliminar

            # Intenta eliminar jugador de la mesa o cola
            ok, msg = service.eliminar_jugador_de_mesa(mid, jid)
            print(msg)  # Muestra mensaje de éxito o error

        elif opcion == "0":
            break  # Sale del bucle y vuelve al menú principal

        else:
            print("Opción inválida. Intente nuevamente.")  # Mensaje si se ingresa una opción no válida
