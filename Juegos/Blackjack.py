import random
import time
from utils import cargar_datos, guardar_datos  # Funciones para cargar y guardar datos de jugadores y mesas
from jugadores import Pila  # Clase Pila para manejo del historial de juego

def blackjack(mesa):
    datos = cargar_datos()  # Cargar datos desde almacenamiento persistente (ej: JSON)

    # Buscar mesas activas para el juego Blackjack
    mesas_disponibles = [m for m in mesa.mesas if m['juego'].lower() == "blackjack" and m['activa']]

    # Si no hay mesas disponibles, informar y salir
    if not mesas_disponibles:
        print("No hay mesas disponibles para BlackJack.")
        time.sleep(2)
        return

    # Mostrar las mesas disponibles con número, id y cantidad de jugadores actuales
    print("\nMesas disponibles para BlackJack:")
    for i, mesa in enumerate(mesas_disponibles, 1):
        print(f"{i}. Mesa {mesa['mesa_id']} - Jugadores: {len(mesa['jugadores'])}/{mesa['canJugadores']}")

    # Pedir al usuario que seleccione una mesa, validando entrada
    try:
        seleccion = int(input("\nSeleccione una mesa: ")) - 1
        if seleccion < 0 or seleccion >= len(mesas_disponibles):
            print("Selección inválida.")
            time.sleep(2)
            return
    except ValueError:
        print("Debe ingresar un número válido.")
        time.sleep(2)
        return

    mesa_seleccionada = mesas_disponibles[seleccion]  # Mesa elegida

    # Verificar que haya al menos un jugador en la mesa
    if len(mesa_seleccionada['jugadores']) < 1:
        print("\nSe necesitan al menos 1 jugador para jugar BlackJack.")
        time.sleep(3)
        return

    print(f"\nIniciando juego en la mesa {mesa_seleccionada['mesa_id']} con {len(mesa_seleccionada['jugadores'])} jugadores.")    
    time.sleep(3)

    print("\n🂡 BIENVENIDO A BLACKJACK 🂡")
    jugador_id = input("Ingrese su ID de jugador: ").strip().upper()

    # Verificar que el ID de jugador exista en los datos
    if jugador_id not in datos['jugadores']:
        print("❌ ID no encontrado. Debe registrarse primero.")
        return

    jugador = datos['jugadores'][jugador_id]
    wallet = jugador['saldo']  # Saldo actual del jugador
    historial = jugador.get('historial', [])  # Historial de partidas previas

    # Convertir historial a pila para poder usar operaciones LIFO
    if isinstance(historial, list):
        pila_historial = Pila()
        for item in historial:
            pila_historial.push(item)
        historial = pila_historial

    # Definir cartas y palos para formar el mazo completo
    cartas = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    palos = ['♠', '♥', '♦', '♣']
    mazo = [f"{valor}{palo}" for valor in cartas for palo in palos]  # Mazo completo con combinaciones

    # Función para repartir 'n' cartas del mazo (elimina cartas usadas)
    def repartir_carta(n):
        return [mazo.pop() for _ in range(n)]

    # Función para calcular la suma de las cartas, considerando As como 1 u 11
    def calcular_suma(cartas):
        suma = 0
        ases = 0
        for carta in cartas:
            valor = carta[:-1]  # Extraer valor ignorando el palo
            if valor in ['J', 'Q', 'K']:
                suma += 10  # Figuras valen 10
            elif valor == 'A':
                suma += 11  # As cuenta inicialmente como 11
                ases += 1
            else:
                suma += int(valor)  # Cartas numéricas suman su valor
        # Ajustar As de 11 a 1 si la suma supera 21
        while suma > 21 and ases > 0:
            suma -= 10
            ases -= 1
        return suma

    # Bucle principal mientras el jugador tenga saldo para apostar
    while wallet > 0:
        print(f"\n💰 Saldo actual: ${wallet:.2f}")
        try:
            apuesta = float(input("Ingrese su apuesta o 0 para salir: $"))
        except ValueError:
            print("❌ Ingrese un número válido.")
            continue

        if apuesta == 0:
            print("Gracias por jugar!")
            break

        if apuesta <= 0 or apuesta > wallet:
            print("❌ Apuesta inválida.")
            continue

        wallet -= apuesta  # Restar apuesta del saldo
        random.shuffle(mazo)  # Barajar mazo antes de repartir
        jugador_cartas = repartir_carta(2)  # Repartir dos cartas al jugador
        crupier_cartas = repartir_carta(2)  # Repartir dos cartas al crupier

        # Turno del jugador: pedir cartas o plantarse
        while True:
            suma_jugador = calcular_suma(jugador_cartas)
            print(f"Tus cartas: {jugador_cartas} | Suma: {suma_jugador}")
            if suma_jugador > 21:
                print("❌ Te pasaste de 21. Perdiste.")
                resultado = f"BlackJack: Apostó ${apuesta}, perdió."
                jugador['estadisticas']['total_apostado'] += apuesta
                jugador['estadisticas']['juegos_perdidos'] += 1
                break

            opcion = input("¿Quieres PEDIR (1) o PLANTARTE (2)? ").strip()
            if opcion == "1":
                jugador_cartas += repartir_carta(1)  # Repartir carta extra al jugador
            elif opcion == "2":
                break  # Plantarse, terminar turno
            else:
                print("❌ Opción inválida.")

        # Si el jugador no se pasó, turno del crupier
        if suma_jugador <= 21:
            suma_crupier = calcular_suma(crupier_cartas)
            print(f"Crupier: {crupier_cartas} | Suma: {suma_crupier}")
            # El crupier pide cartas mientras suma menos de 17
            while suma_crupier < 17:
                crupier_cartas += repartir_carta(1)
                suma_crupier = calcular_suma(crupier_cartas)

            print(f"Crupier final: {crupier_cartas} | Suma: {suma_crupier}")

            jugador['estadisticas']['total_apostado'] += apuesta

            # Determinar resultado final y actualizar saldo y estadísticas
            if suma_crupier > 21 or suma_jugador > suma_crupier:
                ganancia = apuesta * 2
                wallet += ganancia
                print(f"🎉 Ganaste! Tu ganancia es: ${ganancia:.2f}")
                resultado = f"BlackJack: Apostó ${apuesta}, ganó ${ganancia}"
                jugador['estadisticas']['juegos_ganados'] += 1
            elif suma_jugador == suma_crupier:
                wallet += apuesta
                print("🤝 Empate. Se devuelve la apuesta.")
                resultado = f"BlackJack: Apostó ${apuesta}, empate."
            else:
                print("❌ Perdiste la ronda.")
                resultado = f"BlackJack: Apostó ${apuesta}, perdió."
                jugador['estadisticas']['juegos_perdidos'] += 1

        historial.push(resultado)  # Guardar resultado en historial
        print(f"💼 Saldo actualizado: ${wallet:.2f}")
        datos['estadisticas_juegos']['blackjack'] += 1
        time.sleep(2)

    # Guardar saldo actualizado e historial convertido a lista
    jugador['saldo'] = wallet
    jugador['historial'] = historial.elementos  # Convertir pila a lista para guardar
    datos['jugadores'][jugador_id] = jugador
    guardar_datos(datos)  # Guardar cambios en almacenamiento persistente
    print("\n✔ Datos guardados. ¡Hasta la próxima!")
