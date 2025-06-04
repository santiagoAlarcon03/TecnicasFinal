import random
import time
from utils import cargar_datos, guardar_datos
from jugadores import Pila

def blackjack(mesa):

    datos = cargar_datos()
    # Buscar mesas disponibles para blackjack (juego guardado como string)
    mesas_disponibles = [m for m in mesa.mesas if m['juego'].lower() == "blackjack" and m['activa']]

    if not mesas_disponibles:
        print("No hay mesas disponibles para BlackJack.")
        time.sleep(2)
        return

    # Mostrar mesas disponibles
    print("\nMesas disponibles para BlackJack:")
    for i, mesa in enumerate(mesas_disponibles, 1):
        print(f"{i}. Mesa {mesa['mesa_id']} - Jugadores: {len(mesa['jugadores'])}/{mesa['canJugadores']}")

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

    mesa_seleccionada = mesas_disponibles[seleccion]

    # Verificar que haya al menos 1 jugador en la mesa
    if len(mesa_seleccionada['jugadores']) < 1:
        print("\nSe necesitan al menos 1 jugador para jugar BlackJack.")
        time.sleep(3)
        return

    print(f"\nIniciando juego en la mesa {mesa_seleccionada['mesa_id']} con {len(mesa_seleccionada['jugadores'])} jugadores.")    
    time.sleep(3)

    print("\n🂡 BIENVENIDO A BLACKJACK 🂡")
    jugador_id = input("Ingrese su ID de jugador: ").strip().upper()

    if jugador_id not in datos['jugadores']:
        print("❌ ID no encontrado. Debe registrarse primero.")
        return

    jugador = datos['jugadores'][jugador_id]
    wallet = jugador['saldo']
    historial = jugador.get('historial', [])
    if isinstance(historial, list):
        pila_historial = Pila()
        for item in historial:
            pila_historial.push(item)
        historial = pila_historial

    cartas = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    palos = ['♠', '♥', '♦', '♣']
    mazo = [f"{valor}{palo}" for valor in cartas for palo in palos]

    def repartir_carta(n):
        return [mazo.pop() for _ in range(n)]

    def calcular_suma(cartas):
        suma = 0
        ases = 0
        for carta in cartas:
            valor = carta[:-1]
            if valor in ['J', 'Q', 'K']:
                suma += 10
            elif valor == 'A':
                suma += 11
                ases += 1
            else:
                suma += int(valor)
        while suma > 21 and ases > 0:
            suma -= 10
            ases -= 1
        return suma

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

        wallet -= apuesta
        random.shuffle(mazo)
        jugador_cartas = repartir_carta(2)
        crupier_cartas = repartir_carta(2)

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
                jugador_cartas += repartir_carta(1)
            elif opcion == "2":
                break
            else:
                print("❌ Opción inválida.")

        if suma_jugador <= 21:
            suma_crupier = calcular_suma(crupier_cartas)
            print(f"Crupier: {crupier_cartas} | Suma: {suma_crupier}")
            while suma_crupier < 17:
                crupier_cartas += repartir_carta(1)
                suma_crupier = calcular_suma(crupier_cartas)

            print(f"Crupier final: {crupier_cartas} | Suma: {suma_crupier}")

            jugador['estadisticas']['total_apostado'] += apuesta

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

        historial.push(resultado)
        print(f"💼 Saldo actualizado: ${wallet:.2f}")
        datos['estadisticas_juegos']['blackjack'] += 1
        time.sleep(2)

    jugador['saldo'] = wallet
    jugador['historial'] = historial.elementos  # ✅ Conversión a lista para JSON
    datos['jugadores'][jugador_id] = jugador
    guardar_datos(datos)
    print("\n✔ Datos guardados. ¡Hasta la próxima!")

