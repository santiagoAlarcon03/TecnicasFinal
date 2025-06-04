import random
import time
from utils import cargar_datos, guardar_datos
from jugadores import Pila  # Clase para manejar el historial del jugador con estructura de pila

def tragamonedas(mesa):
    datos = cargar_datos()  # Cargar todos los datos del sistema (jugadores, estadísticas, etc.)

    # Filtrar las mesas que tienen el juego 'tragamonedas' y están activas
    mesas_disponibles = [m for m in mesa.mesas if m['juego'].lower() == "tragamonedas" and m['activa']]

    if not mesas_disponibles:  # Si no hay mesas disponibles
        print("No hay mesas disponibles para Tragamonedas.")
        time.sleep(2)
        return

    # Mostrar las mesas disponibles para jugar
    print("\nMesas disponibles para Tragamonedas:")
    for i, mesa_disp in enumerate(mesas_disponibles, 1):
        print(f"{i}. Mesa {mesa_disp['mesa_id']} - Jugadores: {len(mesa_disp['jugadores'])}/{mesa_disp['canJugadores']}")

    # Solicitar al usuario que seleccione una mesa
    try:
        seleccion = int(input("\nSeleccione una mesa: ")) - 1
        if seleccion < 0 or seleccion >= len(mesas_disponibles):
            print("Selección inválida.")
            time.sleep(2)
            return
    except ValueError:  # Validar que se ingrese un número
        print("Debe ingresar un número válido.")
        time.sleep(2)
        return

    # Obtener la mesa seleccionada
    mesa_seleccionada = mesas_disponibles[seleccion]

    # Validar que haya al menos un jugador en la mesa
    if len(mesa_seleccionada['jugadores']) < 1:
        print("\nSe necesita al menos 1 jugador para jugar Tragamonedas.")
        time.sleep(3)
        return

    # Mensaje de inicio del juego
    print(f"\nIniciando juego en la mesa {mesa_seleccionada['mesa_id']} con {len(mesa_seleccionada['jugadores'])} jugadores.")
    time.sleep(3)

    # Explicación del funcionamiento del juego
    print("\n🎮BIENVENIDO A UNA TRAGAMONEDAS \n " \
          "El juego es sencillo, la máquina tirará 15 veces, tres símbolos aleatorios. \n " \
          "Si en esa tirada, entre esos símbolos hay 2 o más Bonus, habrá un multiplicador aleatorio para tu apuesta. \n " \
          "Es decir, tu dinero se multiplicará una vez por cada tirada en la que ocurra esto. \n " \
          "Tu dinero se puede multiplicar por 5, 10, 25, 50 o 100! \n " \
          "🎲 ¡BUENA SUERTE!")

    # Ingreso del ID del jugador
    id_jugador = input("Ingrese su ID de jugador: ").strip().upper()

    # Verificar si el ID existe en el sistema
    if id_jugador not in datos['jugadores']:
        print("❌ ID no encontrado. Debe registrarse primero.")
        return

    # Obtener datos del jugador
    jugador = datos['jugadores'][id_jugador]
    wallet = jugador['saldo']  # Saldo actual del jugador

    # Cargar historial del jugador (si existe) en una pila
    historial_datos = jugador.get('historial', [])
    historial = Pila()
    for item in historial_datos:
        historial.push(item)

    # Definir los símbolos posibles y los multiplicadores
    simbolos = ['Bonus', 'uvas', 'Banano', 'Limon', 'Pera', 'Fresa']
    multiplicadores = [5, 10, 25, 50, 100]

    # Mientras el jugador tenga saldo, puede seguir jugando
    while wallet > 0:
        print(f"\n💰 Saldo actual: ${wallet:.2f}")
        try:
            apuesta = int(input("Ingresa tu apuesta o 0 para salir: $"))
        except ValueError:  # Validar que se ingrese un número válido
            print("Ingreso inválido. Solo números.")
            time.sleep(1.5)
            continue

        # Salir del juego si apuesta 0
        if apuesta == 0:
            print("Gracias por jugar!")
            break

        # Verificar que la apuesta sea válida
        if apuesta > wallet or apuesta <= 0:
            print("Apuesta inválida.")
            time.sleep(1.5)
            continue

        gananciasTotales = 0  # Acumulador de ganancias por ronda
        print("\n🎰 COMENCEMOS...\n")
        time.sleep(1)

        # Simulación de 15 tiradas de la máquina tragamonedas
        for i in range(15):
            linea1 = random.choice(simbolos)
            linea2 = random.choice(simbolos)
            linea3 = random.choice(simbolos)

            combo = [linea1, linea2, linea3]
            bonus_count = combo.count("Bonus")  # Contar cuántos "Bonus" hay

            print(f"[{i+1:02}] | {linea1} | {linea2} | {linea3} |", end=" ")

            if bonus_count >= 2:
                multiplicador = random.choice(multiplicadores)
                ganancias = apuesta * multiplicador
                gananciasTotales += ganancias
                print(f"🎉 ¡Ganaste! multiplicador x{multiplicador}")
            else:
                print("❌ No ganaste")

            time.sleep(0.3)  # Pausa para mostrar cada tirada

        # Actualizar el saldo después de la ronda
        wallet -= apuesta
        wallet += gananciasTotales

        # Guardar el resultado en el historial
        resultado = f"Tragamonedas: Apostó ${apuesta}, ganó ${gananciasTotales}"
        historial.push(resultado)

        # Actualizar estadísticas del jugador
        jugador['estadisticas']['total_apostado'] += apuesta
        if gananciasTotales > 0:
            jugador['estadisticas']['juegos_ganados'] += 1
        else:
            jugador['estadisticas']['juegos_perdidos'] += 1

        # Mostrar resultados al jugador
        print(f"\n🎯 Ganancia total en la ronda: ${gananciasTotales}")
        print(f"💼 Saldo actualizado: ${wallet:.2f}")

        # Aumentar el contador global de partidas jugadas en tragamonedas
        datos['estadisticas_juegos']['tragamonedas'] += 1
        time.sleep(3)

    # Guardar los cambios al terminar de jugar
    jugador['saldo'] = wallet  # Guardar saldo final
    jugador['historial'] = historial.to_list()  # Convertir la pila a lista para guardar
    datos['jugadores'][id_jugador] = jugador  # Actualizar los datos del jugador
    guardar_datos(datos)  # Guardar todos los datos en el sistema

    print("\n✔ Datos guardados. ¡Hasta la próxima!")  # Mensaje final
