from collections import deque  # Importación opcional en este caso, pero útil para estructuras tipo cola
from utils import cargar_datos, guardar_datos  # Funciones para leer y guardar datos desde/para un archivo JSON

class MesaService:
    def __init__(self):
        """
        Constructor que inicializa el servicio de mesas.
        Carga los datos desde almacenamiento persistente y asegura que exista la clave 'mesas'.
        """
        # Las mesas se guardarán dentro del JSON general, en clave 'mesas'
        self.datos = cargar_datos()
        if 'mesas' not in self.datos:
            self.datos['mesas'] = []
            guardar_datos(self.datos)

        # Al iniciar, cargamos las mesas en memoria
        self.mesas = self.datos['mesas']

    def _guardar(self):
        """
        Método interno para actualizar el archivo JSON con las mesas en memoria.
        """
        self.datos['mesas'] = self.mesas
        guardar_datos(self.datos)

    def _generar_nuevo_id(self):
        """
        Genera un nuevo ID de mesa secuencial basado en el último ID registrado.
        """
        if not self.mesas:
            return "M1"
        ultimo_id = self.mesas[-1]['mesa_id']
        numero = int(ultimo_id[1:]) + 1
        return f"M{numero}"

    def crearMesa(self, nombre_juego, canJugadores, activa=True):
        """
        Crea una nueva mesa con los parámetros dados y la almacena.
        """
        # Crear una nueva mesa y agregarla
        mesa_id = self._generar_nuevo_id()

        nueva_mesa = {
            "mesa_id": mesa_id,
            "juego": nombre_juego,
            "canJugadores": canJugadores,
            "activa": activa,
            "jugadores": [],  # lista de IDs de jugadores en la mesa
            "cola_espera": []  # lista de IDs de jugadores en cola
        }
        self.mesas.append(nueva_mesa)
        self._guardar()
        return nueva_mesa

    def borrarMesa(self, mesa_id):
        """
        Elimina una mesa dado su ID. Retorna True si se elimina, False si no se encuentra.
        """
        original = len(self.mesas)
        self.mesas = [m for m in self.mesas if m['mesa_id'] != mesa_id]
        if len(self.mesas) < original:
            self._guardar()
            return True
        return False

    def buscarMesa(self, mesa_id):
        """
        Busca y retorna una mesa por su ID. Si no la encuentra, retorna None.
        """
        for mesa in self.mesas:
            if mesa['mesa_id'] == mesa_id:
                return mesa
        return None

    def actualizarMesa(self, mesa_id, nombre_juego=None, canJugadores=None, activa=None):
        """
        Actualiza los datos de una mesa existente. Retorna True si fue modificada, False si no se encontró.
        """
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
        """
        Agrega un jugador a una mesa si hay espacio. Si no hay, lo agrega a la cola de espera.
        Evita duplicados en mesa o cola. Retorna tupla (ok: bool, mensaje: str).
        """
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
        """
        Mueve el primer jugador en la cola de espera a la mesa si hay espacio.
        Retorna tupla (ok: bool, mensaje: str).
        """
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
        """
        Elimina un jugador de una mesa o de su cola de espera.
        Retorna tupla (ok: bool, mensaje: str).
        """
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
        """
        Retorna la lista de IDs de jugadores presentes en una mesa.
        Si no se encuentra la mesa, retorna lista vacía.
        """
        mesa = self.buscarMesa(mesa_id)
        if not mesa:
            return []
        return mesa['jugadores']

    def obtener_cola_espera(self, mesa_id):
        """
        Retorna la lista de IDs de jugadores en la cola de espera de una mesa.
        Si no se encuentra la mesa, retorna lista vacía.
        """
        mesa = self.buscarMesa(mesa_id)
        if not mesa:
            return []
        return mesa['cola_espera']
