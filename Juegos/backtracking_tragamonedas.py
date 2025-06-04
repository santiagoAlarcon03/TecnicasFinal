import random
import time
from typing import List, Tuple, Dict
from dataclasses import dataclass
from utils import cargar_datos, guardar_datos
from jugadores import Pila

@dataclass
class ResultadoApuesta:
    """Clase para almacenar el resultado de una simulación de apuesta"""
    apuesta: int
    ganancia: float
    saldo_final: float
    exito: bool  # True si no se quedó sin dinero

class OptimizadorApuestas:
    """
    Clase que implementa backtracking para encontrar la mejor estrategia de apuestas
    en el juego de tragamonedas.
    
    ALGORITMO DE BACKTRACKING:
    1. Genera todas las posibles combinaciones de apuestas
    2. Para cada combinación, simula el juego completo
    3. Descarta combinaciones que resulten en saldo = 0
    4. Encuentra la combinación que maximiza las ganancias
    """
    
    def __init__(self, saldo_inicial: float, max_rondas: int = 5):
        self.saldo_inicial = saldo_inicial
        self.max_rondas = max_rondas
        self.mejor_estrategia = []
        self.mejor_ganancia = -float('inf')
        self.simulaciones_realizadas = 0
        
        # Configuración del juego (igual que tu tragamonedas)
        self.simbolos = ['Bonus', 'uvas', 'Banano', 'Limon', 'Pera', 'Fresa']
        self.multiplicadores = [5, 10, 25, 50, 100]
        
        # Tabla de apuestas posibles (porcentajes del saldo actual)
        self.porcentajes_apuesta = [0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4]
    
    def simular_ronda_tragamonedas(self, apuesta: float) -> float:
        """
        Simula una ronda de tragamonedas retorna las ganancias totales de la ronda.
        """
        ganancias_totales = 0
        
        # 15 tiradas por ronda (como en tu juego)
        for _ in range(15):
            # Generar combinación aleatoria
            combo = [random.choice(self.simbolos) for _ in range(3)]
            bonus_count = combo.count("Bonus")
            
            # Si hay 2 o más Bonus, aplicar multiplicador
            if bonus_count >= 2:
                multiplicador = random.choice(self.multiplicadores)
                ganancias = apuesta * multiplicador
                ganancias_totales += ganancias
        
        return ganancias_totales
    
    def simular_estrategia(self, estrategia_apuestas: List[float]) -> ResultadoApuesta:
        """
        Simula una estrategia completa de apuestas.
        
        Args:
            estrategia_apuestas: Lista de porcentajes de apuesta para cada ronda
        
        Returns:
            ResultadoApuesta: Resultado de la simulación
        """
        saldo_actual = self.saldo_inicial
        ganancia_total = 0
        
        for i, porcentaje in enumerate(estrategia_apuestas):
            if saldo_actual <= 0:
                # Se quedó sin dinero, estrategia fallida
                return ResultadoApuesta(0, ganancia_total, 0, False)
            
            # Calcular apuesta basada en porcentaje del saldo actual
            apuesta = saldo_actual * porcentaje
            
            # Verificar que la apuesta sea válida
            if apuesta > saldo_actual:
                apuesta = saldo_actual
            
            # Simular la ronda
            ganancias_ronda = self.simular_ronda_tragamonedas(apuesta)
            
            # Actualizar saldo
            saldo_actual -= apuesta  # Se resta la apuesta
            saldo_actual += ganancias_ronda  # Se suman las ganancias
            ganancia_total += ganancias_ronda - apuesta  # Ganancia neta
        
        return ResultadoApuesta(
            apuesta=sum(estrategia_apuestas) * self.saldo_inicial,
            ganancia=ganancia_total,
            saldo_final=saldo_actual,
            exito=saldo_actual > 0
        )
    
    def backtracking(self, estrategia_actual: List[float], ronda_actual: int):
        """
        ALGORITMO DE BACKTRACKING PRINCIPAL
        
        Este método explora recursivamente todas las posibles combinaciones
        de apuestas, podando las ramas que no son prometedoras.
        
        Args:
            estrategia_actual: Lista de porcentajes de apuesta construida hasta ahora
            ronda_actual: Número de ronda actual (para controlar la recursión)
        """
        self.simulaciones_realizadas += 1
        
        # CASO BASE: Si hemos planificado todas las rondas
        if ronda_actual >= self.max_rondas:
            # Simular la estrategia completa
            resultado = self.simular_estrategia(estrategia_actual)
            
            # Si la estrategia es exitosa y mejor que la actual
            if resultado.exito and resultado.ganancia > self.mejor_ganancia:
                self.mejor_ganancia = resultado.ganancia
                self.mejor_estrategia = estrategia_actual.copy()
            return
        
        # RECURSIÓN: Probar cada posible porcentaje de apuesta
        for porcentaje in self.porcentajes_apuesta:
            # PODA: Verificar si vale la pena continuar con esta rama
            if self.es_rama_prometedora(estrategia_actual + [porcentaje], ronda_actual):
                # Agregar la apuesta a la estrategia actual
                estrategia_actual.append(porcentaje)
                
                # LLAMADA RECURSIVA
                self.backtracking(estrategia_actual, ronda_actual + 1)
                
                # BACKTRACK: Remover la apuesta para probar otras opciones
                estrategia_actual.pop()
    
    def es_rama_prometedora(self, estrategia_parcial: List[float], ronda: int) -> bool:
        """
        FUNCIÓN DE PODA: Determina si vale la pena continuar explorando esta rama.
        
        Criterios de poda:
        1. Si la simulación parcial ya resulta en saldo = 0
        2. Si el patrón de apuestas es demasiado agresivo
        3. Si las primeras rondas muestran pérdidas excesivas
        """
        if not estrategia_parcial:
            return True
        
        # Poda 1: Verificar que no apostemos más del 50% en rondas consecutivas
        if len(estrategia_parcial) >= 2:
            if estrategia_parcial[-1] > 0.35 and estrategia_parcial[-2] > 0.35:
                return False
        
        # Poda 2: Simular parcialmente para verificar viabilidad
        if ronda >= 2:  # Solo verificar después de al menos 2 rondas planificadas
            resultado_parcial = self.simular_estrategia(estrategia_parcial)
            if not resultado_parcial.exito:
                return False
        
        return True
    
    def encontrar_mejor_estrategia(self) -> Tuple[List[float], float, Dict]:
        """
        MÉTODO PRINCIPAL: Encuentra la mejor estrategia de apuestas.
        
        Returns:
            Tuple con:
            - Lista de porcentajes de apuesta óptimos
            - Ganancia esperada máxima
            - Estadísticas del proceso
        """
        print("🔍 INICIANDO OPTIMIZACIÓN DE ESTRATEGIA CON BACKTRACKING...")
        print(f"💰 Saldo inicial: ${self.saldo_inicial}")
        print(f"🎯 Máximo de rondas: {self.max_rondas}")
        print(f"📊 Explorando {len(self.porcentajes_apuesta)**self.max_rondas:,} combinaciones posibles")
        
        tiempo_inicio = time.time()
        
        # Iniciar el backtracking
        self.backtracking([], 0)
        
        tiempo_total = time.time() - tiempo_inicio
        
        estadisticas = {
            'simulaciones_realizadas': self.simulaciones_realizadas,
            'tiempo_total': tiempo_total,
            'combinaciones_exploradas': len(self.porcentajes_apuesta)**self.max_rondas,
            'eficiencia_poda': 1 - (self.simulaciones_realizadas / (len(self.porcentajes_apuesta)**self.max_rondas))
        }
        
        return self.mejor_estrategia, self.mejor_ganancia, estadisticas

def optimizar_estrategia_tragamonedas():
    """
    FUNCIÓN PRINCIPAL para integrar con tu juego de tragamonedas.
    
    Esta función:
    1. Carga los datos del jugador
    2. Utiliza backtracking para encontrar la mejor estrategia
    3. Presenta los resultados al usuario
    4. Opcionalmente ejecuta la estrategia encontrada
    """
    datos = cargar_datos()
    
    print("\n🎯 OPTIMIZADOR DE ESTRATEGIAS PARA TRAGAMONEDAS")
    print("=" * 50)
    
    id_jugador = input("Ingrese su ID de jugador: ").strip().upper()
    
    if id_jugador not in datos['jugadores']:
        print("❌ ID no encontrado. Debe registrarse primero.")
        return
    
    jugador = datos['jugadores'][id_jugador]
    saldo_actual = jugador['saldo']
    
    if saldo_actual <= 0:
        print("❌ No tienes saldo suficiente para optimizar estrategias.")
        return
    
    print(f"\n💰 Tu saldo actual: ${saldo_actual:.2f}")
    
    # Configurar el optimizador
    max_rondas = int(input("¿Cuántas rondas quieres planificar? (recomendado: 3-5): ") or "3")
    
    optimizador = OptimizadorApuestas(saldo_actual, max_rondas)
    
    # Encontrar la mejor estrategia
    mejor_estrategia, mejor_ganancia, estadisticas = optimizador.encontrar_mejor_estrategia()
    
    # Mostrar resultados
    print("\n" + "="*60)
    print("🏆 MEJOR ESTRATEGIA ENCONTRADA")
    print("="*60)
    
    if mejor_estrategia:
        print(f"💎 Ganancia esperada máxima: ${mejor_ganancia:.2f}")
        print(f"📈 ROI estimado: {(mejor_ganancia/saldo_actual)*100:.1f}%")
        print("\n📋 ESTRATEGIA ÓPTIMA:")
        
        for i, porcentaje in enumerate(mejor_estrategia, 1):
            apuesta_sugerida = saldo_actual * porcentaje
            print(f"   Ronda {i}: Apostar {porcentaje*100:.1f}% del saldo actual (≈${apuesta_sugerida:.2f})")
        
        print(f"\n📊 ESTADÍSTICAS DEL PROCESO:")
        print(f"   ⏱️  Tiempo de cálculo: {estadisticas['tiempo_total']:.2f} segundos")
        print(f"   🔍 Simulaciones realizadas: {estadisticas['simulaciones_realizadas']:,}")
        print(f"   ✂️  Eficiencia de poda: {estadisticas['eficiencia_poda']*100:.1f}%")
        
        # Preguntar si quiere ejecutar la estrategia
        ejecutar = input("\n¿Quieres ejecutar esta estrategia optimizada? (s/n): ").lower()
        
        if ejecutar == 's':
            ejecutar_estrategia_optimizada(jugador, mejor_estrategia, id_jugador, datos)
    else:
        print("❌ No se pudo encontrar una estrategia viable con tu saldo actual.")
        print("💡 Considera aumentar tu saldo o reducir el número de rondas.")

def ejecutar_estrategia_optimizada(jugador: dict, estrategia: List[float], id_jugador: str, datos: dict):
    """
    Ejecuta la estrategia optimizada encontrada por backtracking.
    """
    print("\n🎮 EJECUTANDO ESTRATEGIA OPTIMIZADA...")
    print("=" * 50)
    
    # Inicializar historial
    historial_datos = jugador.get('historial', [])
    historial = Pila()
    for item in historial_datos:
        historial.push(item)
    
    # Configuración del juego
    simbolos = ['Bonus', 'uvas', 'Banano', 'Limon', 'Pera', 'Fresa']
    multiplicadores = [5, 10, 25, 50, 100]
    
    saldo_inicial = jugador['saldo']
    saldo_actual = saldo_inicial
    
    for ronda, porcentaje in enumerate(estrategia, 1):
        if saldo_actual <= 0:
            print("❌ Te has quedado sin saldo. Estrategia interrumpida.")
            break
        
        apuesta = saldo_actual * porcentaje
        print(f"\n🎯 RONDA {ronda}")
        print(f"💰 Saldo actual: ${saldo_actual:.2f}")
        print(f"🎲 Apuesta sugerida: ${apuesta:.2f} ({porcentaje*100:.1f}% del saldo)")
        
        input("Presiona Enter para continuar con la ronda...")
        
        # Ejecutar la ronda exactamente como en tu juego original
        ganancias_totales = 0
        print("\n🎰 COMENCEMOS...\n")
        
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
                ganancias_totales += ganancias
                print(f"🎉 ¡Ganaste! multiplicador x{multiplicador}")
            else:
                print("❌ No ganaste")
            
            time.sleep(0.3)
        
        # Actualizar saldo
        saldo_actual -= apuesta
        saldo_actual += ganancias_totales
        
        # Registrar en historial
        resultado = f"Estrategia Optimizada R{ronda}: Apostó ${apuesta:.2f}, ganó ${ganancias_totales:.2f}"
        historial.push(resultado)
        
        # Actualizar estadísticas
        jugador['estadisticas']['total_apostado'] += apuesta
        if ganancias_totales > apuesta:
            jugador['estadisticas']['juegos_ganados'] += 1
        else:
            jugador['estadisticas']['juegos_perdidos'] += 1
        
        print(f"\n🎯 Ganancia en esta ronda: ${ganancias_totales:.2f}")
        print(f"💼 Saldo actualizado: ${saldo_actual:.2f}")
        
        time.sleep(2)
    
    # Calcular resultado final
    ganancia_neta = saldo_actual - saldo_inicial
    
    print("\n" + "="*50)
    print("📊 RESULTADO FINAL DE LA ESTRATEGIA OPTIMIZADA")
    print("="*50)
    print(f"💰 Saldo inicial: ${saldo_inicial:.2f}")
    print(f"💰 Saldo final: ${saldo_actual:.2f}")
    print(f"📈 Ganancia neta: ${ganancia_neta:.2f}")
    print(f"📊 ROI real: {(ganancia_neta/saldo_inicial)*100:.1f}%")
    
    # Guardar cambios
    jugador['saldo'] = saldo_actual
    jugador['historial'] = historial.to_list()
    datos['jugadores'][id_jugador] = jugador
    datos['estadisticas_juegos']['tragamonedas'] += len(estrategia)
    guardar_datos(datos)
    
    print("\n✔ Datos guardados. ¡Estrategia completada!")

# Función para integrar con tu sistema existente
def menu_optimizacion():
    """Menú para acceder a la optimización de estrategias"""
    print("\n🎯 OPTIMIZACIÓN DE APUESTAS CON BACKTRACKING")
    print("1. Optimizar estrategia para tragamonedas")
    print("2. Volver al menú principal")
    
    opcion = input("Seleccione una opción: ")
    
    if opcion == "1":
        optimizar_estrategia_tragamonedas()
    elif opcion == "2":
        return
    else:
        print("Opción inválida")
        menu_optimizacion()

if __name__ == "__main__":
    # Para pruebas directas
    menu_optimizacion()