from collections import deque  # Optional import in this case, but useful for queue-like structures
from utils import cargar_datos, guardar_datos  # Functions to read and save data from/to a JSON file

class MesaService:
    def __init__(self):
        #Constructor that initializes the table service.
        #Loads the data from persistent storage and ensures that the key 'tables' exists.
        # The tables will be saved within the general JSON, in key 'tables'
        self.datos = cargar_datos()
        if 'mesas' not in self.datos:
            self.datos['mesas'] = []
            guardar_datos(self.datos)

        # At startup, we load the tables into memory
        self.mesas = self.datos['mesas']

    def _guardar(self):
        #Internal method to update the JSON file with the tables in memory.
        self.datos['mesas'] = self.mesas
        guardar_datos(self.datos)

    def _generar_nuevo_id(self):
        #Generates a new sequential table ID based on the last registered ID.
        if not self.mesas:
            return "M1"
        ultimo_id = self.mesas[-1]['mesa_id']
        numero = int(ultimo_id[1:]) + 1
        return f"M{numero}"

    def crearMesa(self, nombre_juego, canJugadores, activa=True):
        #Creates a new table with the given parameters and stores it.
        # Create a new table and add it
        mesa_id = self._generar_nuevo_id()

        nueva_mesa = {
            "mesa_id": mesa_id,
            "juego": nombre_juego,
            "canJugadores": canJugadores,
            "activa": activa,
            "jugadores": [],  # list of player IDs on the table
            "cola_espera": []  # list of player IDs in queue
        }
        self.mesas.append(nueva_mesa)
        self._guardar()
        return nueva_mesa

    def borrarMesa(self, mesa_id):
        # Delete a table given its ID. Returns True if deleted, False if not found.
        original = len(self.mesas)
        self.mesas = [m for m in self.mesas if m['mesa_id'] != mesa_id]
        if len(self.mesas) < original:
            self._guardar()
            return True
        return False

    def buscarMesa(self, mesa_id):
        #Searches and returns a table by its ID. If it is not found, it returns None.
        for mesa in self.mesas:
            if mesa['mesa_id'] == mesa_id:
                return mesa
        return None

    def actualizarMesa(self, mesa_id, nombre_juego=None, canJugadores=None, activa=None):
        #Updates the data of an existing table. Returns True if it was modified, False if it was not found.
        mesa = self.buscarMesa(mesa_id)
        if not mesa:
            return False
        if nombre_juego:
            mesa['juego'] = nombre_juego
        if canJugadores is not None:
            mesa['canJugadores'] = canJugadores
        if activa is not None:
            mesa['activa'] = activa
        self._guardar()
        return True

    def agregar_jugador_a_mesa(self, mesa_id, id_jugador):
        #Add a player to a table if there is space. If there isn't one, it adds it to the waiting queue.
        #Avoid duplicates at the table or queue. Return tuple (ok: bool, message: str).
        mesa = self.buscarMesa(mesa_id)
        if not mesa:
            return False, "Mesa no encontrada"

        if id_jugador in mesa['jugadores'] or id_jugador in mesa['cola_espera']:
            return False, "Jugador ya está en la mesa o en la cola"

        if len(mesa['jugadores']) < mesa['canJugadores']:
            mesa['jugadores'].append(id_jugador)
            self._guardar()
            return True, f"Jugador {id_jugador} agregado a la mesa {mesa_id}"
        else:
            mesa['cola_espera'].append(id_jugador)
            self._guardar()
            return True, f"Jugador {id_jugador} agregado a la cola de espera de la mesa {mesa_id}"

    def mover_siguiente_jugador(self, mesa_id):
        #Move the first player in the queue to the table if there is space.
        #Return tuple (ok: bool, message: str).
        mesa = self.buscarMesa(mesa_id)
        if not mesa:
            return False, "Mesa no encontrada"

        if len(mesa['jugadores']) >= mesa['canJugadores']:
            return False, "La mesa está llena"

        if not mesa['cola_espera']:
            return False, "No hay jugadores en la cola de espera"

        siguiente = mesa['cola_espera'].pop(0)
        mesa['jugadores'].append(siguiente)
        self._guardar()
        return True, f"Jugador {siguiente} movido a la mesa {mesa_id}"

    def eliminar_jugador_de_mesa(self, mesa_id, id_jugador):
        #Remove a player from a table or from your waiting queue.
        #Return tuple (ok: bool, message: str).
        mesa = self.buscarMesa(mesa_id)
        if not mesa:
            return False, "Mesa no encontrada"

        if id_jugador in mesa['jugadores']:
            mesa['jugadores'].remove(id_jugador)
            self._guardar()
            return True, f"Jugador {id_jugador} eliminado de la mesa {mesa_id}"

        if id_jugador in mesa['cola_espera']:
            mesa['cola_espera'].remove(id_jugador)
            self._guardar()
            return True, f"Jugador {id_jugador} eliminado de la cola de espera de la mesa {mesa_id}"

        return False, "Jugador no encontrado en la mesa o cola"

    def obtener_jugadores_mesa(self, mesa_id):
        #Returns the list of IDs of players present at a table.
        #If the table is not found, it returns an empty list.
        mesa = self.buscarMesa(mesa_id)
        if not mesa:
            return []
        return mesa['jugadores']

    def obtener_cola_espera(self, mesa_id):
        #Returns the list of player IDs in a table's queue.
        #If the table is not found, it returns an empty list.
        mesa = self.buscarMesa(mesa_id)
        if not mesa:
            return []
        return mesa['cola_espera']
