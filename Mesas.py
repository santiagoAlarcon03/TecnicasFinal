from MesasService import MesaService

def gestionar_mesas():
    service = MesaService()

    while True:
        print("\n--- GESTIÓN DE MESAS ---")
        print("1. Crear mesa")
        print("2. Borrar mesa")
        print("3. Ver mesas")
        print("4. Agregar jugador a mesa")
        print("5. Mover siguiente jugador de cola a mesa")
        print("6. Eliminar jugador de mesa o cola")
        print("0. Volver al menú principal")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            nombre_juego = input("Nombre del juego: ").strip().lower()
            while True:
                try:
                    can_jug = int(input("Cantidad máxima de jugadores: "))
                    if can_jug <= 0:
                        print("Debe ser mayor que 0.")
                    else:
                        break
                except ValueError:
                    print("Ingrese un número válido.")
            mesa = service.crearMesa(nombre_juego, can_jug)
            print(f"Mesa creada con ID: {mesa['mesa_id']}")

        elif opcion == "2":
            mid = input("ID de la mesa a borrar: ").strip().upper()
            if service.borrarMesa(mid):
                print("Mesa borrada.")
            else:
                print("Mesa no encontrada.")

        elif opcion == "3":
            if not service.mesas:
                print("No hay mesas registradas.")
            else:
                print("\nMesas actuales:")
                for m in service.mesas:
                    print(f"ID: {m['mesa_id']} | Juego: {m['juego']} | Max jugadores: {m['canJugadores']} | Activa: {m['activa']}")
                    print(f"  Jugadores: {m['jugadores']}")
                    print(f"  Cola: {m['cola_espera']}")

        elif opcion == "4":
            mid = input("ID de la mesa: ").strip().upper()
            jid = input("ID del jugador a agregar: ").strip().upper()
            ok, msg = service.agregar_jugador_a_mesa(mid, jid)
            print(msg)

        elif opcion == "5":
            mid = input("ID de la mesa: ").strip().upper()
            ok, msg = service.mover_siguiente_jugador(mid)
            print(msg)

        elif opcion == "6":
            mid = input("ID de la mesa: ").strip().upper()
            jid = input("ID del jugador a eliminar: ").strip().upper()
            ok, msg = service.eliminar_jugador_de_mesa(mid, jid)
            print(msg)

        elif opcion == "0":
            break
        else:
            print("Opción inválida. Intente nuevamente.")