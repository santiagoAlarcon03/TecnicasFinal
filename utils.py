import json  # Para trabajar con archivos JSON
import os    # Para verificar existencia de archivos y limpiar pantalla


def cargar_datos():
    # Carga los datos desde el archivo JSON o los inicializa si no existe o está corrupto
    datos_iniciales = {
        'jugadores': {},  # Diccionario para almacenar información de jugadores
        'colas_juegos': {  # Estructura para manejar las colas de espera por juego
            'tragamonedas': [],
            'blackjack': []
        },
        'estadisticas_juegos': {  # Contador de cuántas veces se jugó cada juego
            'tragamonedas': 0,
            'blackjack': 0
        }
    }

    if not os.path.exists('datos.json'):  # Si no existe el archivo, lo crea con estructura inicial
        with open('datos.json', 'w') as f:
            json.dump(datos_iniciales, f, indent=4)
        return datos_iniciales

    try:
        with open('datos.json', 'r') as f:
            datos = json.load(f)  # Intenta leer el JSON
    except json.JSONDecodeError:
        # Archivo vacío o corrupto: lo inicializa de nuevo
        with open('datos.json', 'w') as f:
            json.dump(datos_iniciales, f, indent=4)
        return datos_iniciales

    # Verifica que existan todas las claves necesarias (por compatibilidad futura)
    if 'jugadores' not in datos:
        datos['jugadores'] = {}

    if 'colas_juegos' not in datos:
        datos['colas_juegos'] = {
            'tragamonedas': [],
            'blackjack': []
        }

    if 'estadisticas_juegos' not in datos:
        datos['estadisticas_juegos'] = {
            'tragamonedas': 0,
            'blackjack': 0
        }

    return datos  # Retorna los datos cargados o inicializados

def Despejar():
    # Limpia la consola según el sistema operativo
    os.system('cls' if os.name == 'nt' else 'clear')

def guardar_datos(datos):
    # Guarda los datos en el archivo JSON con formato legible
    with open('datos.json', 'w') as f:
        json.dump(datos, f, indent=4)

def validar_id_unico(id_jugador):
    # Verifica si un ID de jugador ya está registrado
    datos = cargar_datos()
    return id_jugador not in datos['jugadores']

def serializar_datos(datos):
    # Prepara los datos para ser guardados en JSON, asegurando que todo sea serializable
    datos_guardar = {
        'jugadores': {},  # Nuevo diccionario para jugadores serializados
        'colas_juegos': datos['colas_juegos'].copy()  # Copia de las colas de juego
    }
    
    for id_jugador, jugador in datos['jugadores'].items():
        jugador_copy = jugador.copy()  # Copia del jugador para modificar sin afectar el original
        if hasattr(jugador['historial'], 'a_lista'):  # Si historial es un objeto con método a_lista()
            jugador_copy['historial'] = jugador['historial'].a_lista()  # Se convierte a lista para serializar
        datos_guardar['jugadores'][id_jugador] = jugador_copy  # Se agrega al nuevo diccionario
    
    return datos_guardar  # Devuelve los datos listos para guardar
