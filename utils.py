import json  # To work with JSON files
import os    # To verify file existence and clear screen


def cargar_datos():
    # Load data from JSON file or initialize it if it does not exist or is corrupt
    datos_iniciales = {
        'jugadores': {},  # Dictionary to store player information
        'colas_juegos': {  # Structure to manage queues per game
            'tragamonedas': [],
            'blackjack': []
        },
        'estadisticas_juegos': {  # Counter of how many times each game was played
            'tragamonedas': 0,
            'blackjack': 0
        }
    }

    if not os.path.exists('datos.json'):  # If the file does not exist, it creates it with initial structure
        with open('datos.json', 'w') as f:
            json.dump(datos_iniciales, f, indent=4)
        return datos_iniciales

    try:
        with open('datos.json', 'r') as f:
            datos = json.load(f)  # Try reading the JSON
    except json.JSONDecodeError:
        # Empty or corrupt file: initialize it again
        with open('datos.json', 'w') as f:
            json.dump(datos_iniciales, f, indent=4)
        return datos_iniciales

    # Verify that all necessary keys exist (for future compatibility)
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

    return datos  # Returns the initialized data

def Despejar():
    # Clean the console according to the operating system
    os.system('cls' if os.name == 'nt' else 'clear')

def guardar_datos(datos):
    # Save the data in the JSON file in readable format
    with open('datos.json', 'w') as f:
        json.dump(datos, f, indent=4)

def validar_id_unico(id_jugador):
    # Check if a player ID is already registered
    datos = cargar_datos()
    return id_jugador not in datos['jugadores']

def serializar_datos(datos):
    # Prepare data to be saved in JSON, ensuring everything is serializable
    datos_guardar = {
        'jugadores': {},  # New dictionary for serialized players
        'colas_juegos': datos['colas_juegos'].copy()  # Copy of game queues
    }
    
    for id_jugador, jugador in datos['jugadores'].items():
        jugador_copy = jugador.copy()  # Player copy to modify without affecting the original
        if hasattr(jugador['historial'], 'a_lista'):  # If history is an object with a_list() method
            jugador_copy['historial'] = jugador['historial'].a_lista()  # Converts to ready to serialize
        datos_guardar['jugadores'][id_jugador] = jugador_copy  # Added to new dictionary
    
    return datos_guardar  # Returns data ready to save
