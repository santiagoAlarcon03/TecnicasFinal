import json
import os



def cargar_datos():
    datos_iniciales = {
        'jugadores': {},
        'colas_juegos': {
            'tragamonedas': [],
            'blackjack': []
        },
        'estadisticas_juegos': {
            'tragamonedas': 0,
            'blackjack': 0
        }
    }

    if not os.path.exists('datos.json'):
        with open('datos.json', 'w') as f:
            json.dump(datos_iniciales, f, indent=4)
        return datos_iniciales

    try:
        with open('datos.json', 'r') as f:
            datos = json.load(f)
    except json.JSONDecodeError:
        # Archivo vacío o corrupto: lo inicializamos
        with open('datos.json', 'w') as f:
            json.dump(datos_iniciales, f, indent=4)
        return datos_iniciales

    # Aseguramos que las claves necesarias existan (útil si se agregan en versiones futuras)
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

    return datos

def Despejar():
    os.system('cls' if os.name == 'nt' else 'clear')

def guardar_datos(datos):
    with open('datos.json', 'w') as f:
        json.dump(datos, f, indent=4)

def validar_id_unico(id_jugador):
    datos = cargar_datos()
    return id_jugador not in datos['jugadores']

def serializar_datos(datos):



                                                                       #It prepares data to save in JSON
    datos_guardar = {
        'jugadores': {},
        'colas_juegos': datos['colas_juegos'].copy()
    }
    
    for id_jugador, jugador in datos['jugadores'].items():
        jugador_copy = jugador.copy()
        if hasattr(jugador['historial'], 'a_lista'):
            jugador_copy['historial'] = jugador['historial'].a_lista()
        datos_guardar['jugadores'][id_jugador] = jugador_copy
    
    return datos_guardar

def deserializar_datos(datos_crudos):                                    
                                                                       #It makes the JSON´S data to objects
    datos = {
        'jugadores': {},
        'colas_juegos': datos_crudos['colas_juegos'].copy()
    }
    
    for id_jugador, jugador in datos_crudos['jugadores'].items():
        jugador_copy = jugador.copy()
        jugador_copy['historial'] = Pila.desde_lista(jugador.get('historial', []))
        datos['jugadores'][id_jugador] = jugador_copy
    
    return datos