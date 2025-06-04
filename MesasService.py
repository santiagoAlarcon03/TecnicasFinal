from collections import deque
from utils import cargar_datos, guardar_datos

class MesaService:
    def __init__(self):
        # Las mesas se guardarán dentro del JSON general, en clave 'mesas'
        self.datos = cargar_datos()
        if 'mesas' not in self.datos:
            self.datos['mesas'] = []
            guardar_datos(self.datos)

        # Al iniciar, cargamos las mesas en memoria
        self.mesas = self.datos['mesas']

    def _guardar(self):
        self.datos['mesas'] = self.mesas
        guardar_datos(self.datos)

    def _generar_nuevo_id(self):
        if not self.mesas:
            return "M1"
        ultimo_id = self.mesas[-1]['mesa_id']
        numero = int(ultimo_id[1:]) + 1
        return f"M{numero}"

    def crearMesa(self, nombre_juego, canJugadores, activa=True):
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
        original = len(self.mesas)
        self.mesas = [m for m in self.mesas if m['mesa_id'] != mesa_id]
        if len(self.mesas) < original:
            self._guardar()
            return True
        return False

    def buscarMesa(self, mesa_id):
        for mesa in self.mesas:
            if mesa['mesa_id'] == mesa_id:
                return mesa
        return None

    def actualizarMesa(self, mesa_id, nombre_juego=None, canJugadores=None, activa=None):
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
        mesa = self.buscarMesa(mesa_id)
        if not mesa:
            return []
        return mesa['jugadores']

    def obtener_cola_espera(self, mesa_id):
        mesa = self.buscarMesa(mesa_id)
        if not mesa:
            return []
        return mesa['cola_espera']