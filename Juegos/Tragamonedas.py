import random
import time
from utils import cargar_datos, guardar_datos
from jugadores import Pila  # Asegúrate de importar correctamente tu clase Pila

def tragamonedas():
    datos = cargar_datos()

    print("\n🎮BIENVENIDO A UNA TRAGAMONEDAS \n " \
          "El juego es sencillo, la máquina tirará 15 veces, tres símbolos aleatorios. \n " \
          "Si en esa tirada, entre esos símbolos hay 2 o más Bonus, habrá un multiplicador aleatorio para tu apuesta. \n " \
          "Es decir, tu dinero se multiplicará una vez por cada tirada en la que ocurra esto. \n " \
          "Tu dinero se puede multiplicar por 5, 10, 25, 50 o 100! \n " \
          "🎲 ¡BUENA SUERTE!")

    id_jugador = input("Ingrese su ID de jugador: ").strip().upper()

    if id_jugador not in datos['jugadores']:
        print("❌ ID no encontrado. Debe registrarse primero.")
        return

    jugador = datos['jugadores'][id_jugador]
    wallet = jugador['saldo']

    historial_datos = jugador.get('historial', [])
    historial = Pila()
    for item in historial_datos:
        historial.push(item)

    simbolos = ['Bonus', 'uvas', 'Banano', 'Limon', 'Pera', 'Fresa']
    multiplicadores = [5, 10, 25, 50, 100]

    while wallet > 0:
        print(f"\n💰 Saldo actual: ${wallet:.2f}")
        try:
            apuesta = int(input("Ingresa tu apuesta o 0 para salir: $"))
        except ValueError:
            print("Ingreso inválido. Solo números.")
            time.sleep(1.5)
            continue

        if apuesta == 0:
            print("Gracias por jugar!")
            break

        if apuesta > wallet or apuesta <= 0:
            print("Apuesta inválida.")
            time.sleep(1.5)
            continue

        gananciasTotales = 0
        print("\n🎰 COMENCEMOS...\n")
        time.sleep(1)

        for i in range(15):
            linea1 = random.choice(simbolos)
            linea2 = random.choice(simbolos)
            linea3 = random.choice(simbolos)

            combo = [linea1, linea2, linea3]
            bonus_count = combo.count("Bonus")

            print(f"[{i+1:02}] | {linea1} | {linea2} | {linea3} |", end=" ")

            if bonus_count >= 2:
                multiplicador = random.choice(multiplicadores)
                ganancias = apuesta * multiplicador
                gananciasTotales += ganancias
                print(f"🎉 ¡Ganaste! multiplicador x{multiplicador}")
            else:
                print("❌ No ganaste")

            time.sleep(0.3)

        wallet -= apuesta
        wallet += gananciasTotales

        resultado = f"Tragamonedas: Apostó ${apuesta}, ganó ${gananciasTotales}"
        historial.push(resultado)

        # Actualizar estadísticas
        jugador['estadisticas']['total_apostado'] += apuesta
        if gananciasTotales > 0:
            jugador['estadisticas']['juegos_ganados'] += 1
        else:
            jugador['estadisticas']['juegos_perdidos'] += 1

        print(f"\n🎯 Ganancia total en la ronda: ${gananciasTotales}")
        print(f"💼 Saldo actualizado: ${wallet:.2f}")
        datos['estadisticas_juegos']['tragamonedas'] += 1
        time.sleep(3)

    # Guardar cambios
    jugador['saldo'] = wallet
    jugador['historial'] = historial.to_list()  # convertir la pila a lista
    datos['jugadores'][id_jugador] = jugador
    guardar_datos(datos)

    print("\n✔ Datos guardados. ¡Hasta la próxima!")
