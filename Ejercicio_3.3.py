"""
EJERCICIO 3.3: SISTEMA DE PEDIDOS Y ENTREGAS
--------------------------------------------------------------------------------------------------------------
CONTEXTO:
Gestionar pedidos con diferentes metodos de envio: estandar, express,
retiro en tienda y envio internacional, cada uno con costos y tiempos distintos.

REQUERIMIENTOS:
1. Crear clase abstracta "Pedido" (ABSTRACCION):
   - Atributos privados: numero_pedido, fecha, cliente, productos (lista), estado
   - Atributo protegido: _direccion_entrega
   - Metodo abstracto: calcular_tiempo_entrega()
   - Metodo abstracto: calcular_costo_total()
   - Metodo concreto: cambiar_estado(nuevo_estado)

2. Clases derivadas (HERENCIA):
   - PedidoEstandar: rango_entrega_dias, costo_envio_fijo
   - PedidoExpress: entrega_24h, recargo_express
   - PedidoRetiroTienda: tienda_seleccionada, fecha_retiro, codigo_retiro
   - PedidoInternacional: pais_destino, aduana, impuestos_importacion

3. ENCAPSULAMIENTO:
   - Estado privado con validacion de transiciones
   - Metodo privado __validar_stock_disponible()
   - Calculos internos protegidos

4. POLIMORFISMO:
   - calcular_costo_total(): productos + envio (varia) + impuestos
   - calcular_tiempo_entrega(): 3-5 dias, 24h, inmediato, 15-30 dias
   - Metodo notificar_cliente() usa diferentes canales

ENTREGABLES:
- Todas las clases implementadas
- Simular 2 pedidos de cada tipo
- Rastrear estados de pedidos
- Calcular costos y tiempos de manera polimórfica

"""
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from enum import Enum

# =============================================
# ENUMS para estados y tipos
# =============================================
class EstadoPedido(Enum):
    PENDIENTE = "Pendiente"
    CONFIRMADO = "Confirmado"
    PREPARACION = "En preparación"
    ENVIADO = "Enviado"
    ENTREGADO = "Entregado"
    CANCELADO = "Cancelado"

class TipoEnvio(Enum):
    ESTANDAR = "Estándar"
    EXPRESS = "Express"
    RETIRO_TIENDA = "Retiro en tienda"
    INTERNACIONAL = "Internacional"

# =============================================
# ABSTRACCIÓN: Clase abstracta Pedido
# =============================================
class Pedido(ABC):
    """
    CLASE ABSTRACTA que define la estructura base para todos los tipos de pedidos.
    No se puede instanciar directamente - sirve como plantilla para pedidos específicos.
    """
    
    def __init__(self, numero_pedido: str, cliente: str, productos: List[Dict], direccion_entrega: str):
        # ENCAPSULAMIENTO: Atributos privados
        self.__numero_pedido = numero_pedido
        self.__fecha = datetime.now()
        self.__cliente = cliente
        self.__productos = productos
        self.__estado = EstadoPedido.PENDIENTE
        
        # ENCAPSULAMIENTO: Atributo protegido
        self._direccion_entrega = direccion_entrega
    
    # ENCAPSULAMIENTO: Getters para acceso controlado
    def get_numero_pedido(self) -> str:
        return self.__numero_pedido
    
    def get_fecha(self) -> datetime:
        return self.__fecha
    
    def get_cliente(self) -> str:
        return self.__cliente
    
    def get_estado(self) -> EstadoPedido:
        return self.__estado
    
    def get_productos(self) -> List[Dict]:
        return self.__productos.copy()  # Retorna copia para proteger datos
    
    # ENCAPSULAMIENTO: Método privado para validación interna
    def __validar_stock_disponible(self) -> bool:
        """
        MÉTODO PRIVADO: Solo accesible dentro de esta clase
        Simula validación de stock en inventario
        """
        for producto in self.__productos:
            # Simulación de validación de stock
            if producto.get('cantidad', 0) <= 0:
                return False
        return True
    
    # Método concreto - implementación común para todas las clases hijas
    def cambiar_estado(self, nuevo_estado: EstadoPedido) -> bool:
        """
        ENCAPSULAMIENTO: Control de transiciones de estado con validación
        """
        transiciones_validas = {
            EstadoPedido.PENDIENTE: [EstadoPedido.CONFIRMADO, EstadoPedido.CANCELADO],
            EstadoPedido.CONFIRMADO: [EstadoPedido.PREPARACION, EstadoPedido.CANCELADO],
            EstadoPedido.PREPARACION: [EstadoPedido.ENVIADO, EstadoPedido.CANCELADO],
            EstadoPedido.ENVIADO: [EstadoPedido.ENTREGADO],
            EstadoPedido.ENTREGADO: [],
            EstadoPedido.CANCELADO: []
        }
        
        if nuevo_estado in transiciones_validas[self.__estado]:
            self.__estado = nuevo_estado
            print(f"✅ Pedido {self.__numero_pedido} cambió a: {nuevo_estado.value}")
            return True
        else:
            print(f"❌ Transición inválida: {self.__estado.value} -> {nuevo_estado.value}")
            return False
    
    def calcular_subtotal(self) -> float:
        """Calcula el subtotal de los productos (sin envío ni impuestos)"""
        return sum(producto['precio'] * producto.get('cantidad', 1) for producto in self.__productos)
    
    # =============================================
    # ABSTRACCIÓN: Métodos abstractos (POLIMORFISMO)
    # =============================================
    @abstractmethod
    def calcular_tiempo_entrega(self) -> str:
        """
        MÉTODO ABSTRACTO - Cada clase hija debe implementar su cálculo de tiempo
        POLIMORFISMO: mismo método, comportamientos diferentes según el tipo de envío
        """
        pass
    
    @abstractmethod
    def calcular_costo_total(self) -> float:
        """
        MÉTODO ABSTRACTO - Cada tipo de pedido calcula costos de manera única
        POLIMORFISMO: misma interfaz, implementaciones diferentes
        """
        pass
    
    @abstractmethod
    def notificar_cliente(self) -> str:
        """
        MÉTODO ABSTRACTO - Cada pedido notifica al cliente de manera diferente
        POLIMORFISMO: mismo nombre de método, canales y mensajes diferentes
        """
        pass
    
    def obtener_resumen(self) -> Dict:
        """
        Método que demuestra POLIMORFISMO llamando a métodos abstractos
        """
        return {
            'numero_pedido': self.get_numero_pedido(),
            'cliente': self.get_cliente(),
            'estado': self.get_estado().value,
            'tipo_envio': self.__class__.__name__,
            'subtotal': self.calcular_subtotal(),
            'costo_total': self.calcular_costo_total(),
            'tiempo_entrega': self.calcular_tiempo_entrega(),
            'notificacion': self.notificar_cliente()
        }


# =============================================
# HERENCIA: PedidoEstandar hereda de Pedido
# =============================================
class PedidoEstandar(Pedido):
    """
    HERENCIA: PedidoEstandar ES UN tipo de Pedido
    Hereda todos los atributos y métodos de la clase base Pedido
    """
    
    def __init__(self, numero_pedido: str, cliente: str, productos: List[Dict], direccion_entrega: str):
        # HERENCIA: Llamada al constructor de la clase padre
        super().__init__(numero_pedido, cliente, productos, direccion_entrega)
        
        # Atributos específicos de PedidoEstandar
        self.rango_entrega_dias = (3, 5)
        self.costo_envio_fijo = 5.99
    
    # =============================================
    # POLIMORFISMO: Implementación específica
    # =============================================
    def calcular_tiempo_entrega(self) -> str:
        """
        POLIMORFISMO: Implementación única para envío estándar
        Tiempo de entrega: 3-5 días hábiles
        """
        min_dias, max_dias = self.rango_entrega_dias
        return f"{min_dias}-{max_dias} días hábiles"
    
    def calcular_costo_total(self) -> float:
        """
        POLIMORFISMO: Cálculo de costo con envío fijo
        """
        subtotal = self.calcular_subtotal()
        return subtotal + self.costo_envio_fijo
    
    def notificar_cliente(self) -> str:
        """
        POLIMORFISMO: Notificación por email para envíos estándar
        """
        return f"📧 Email enviado a {self.get_cliente()}: Su pedido estándar #{self.get_numero_pedido()} será entregado en {self.calcular_tiempo_entrega()}"


# =============================================
# HERENCIA: PedidoExpress hereda de Pedido
# =============================================
class PedidoExpress(Pedido):
    """HERENCIA: PedidoExpress ES UN tipo de Pedido con entrega rápida"""
    
    def __init__(self, numero_pedido: str, cliente: str, productos: List[Dict], direccion_entrega: str):
        super().__init__(numero_pedido, cliente, productos, direccion_entrega)
        self.entrega_24h = True
        self.recargo_express = 12.99
    
    # =============================================
    # POLIMORFISMO: Implementación única para Express
    # =============================================
    def calcular_tiempo_entrega(self) -> str:
        """
        POLIMORFISMO: Entrega en 24 horas para express
        """
        return "24 horas"
    
    def calcular_costo_total(self) -> float:
        """
        POLIMORFISMO: Cálculo con recargo express
        """
        subtotal = self.calcular_subtotal()
        return subtotal + self.recargo_express
    
    def notificar_cliente(self) -> str:
        """
        POLIMORFISMO: Notificación por SMS para urgencia
        """
        return f"📱 SMS enviado a {self.get_cliente()}: Pedido EXPRESS #{self.get_numero_pedido()} entregado en 24h. Recargo: ${self.recargo_express}"


# =============================================
# HERENCIA: PedidoRetiroTienda hereda de Pedido
# =============================================
class PedidoRetiroTienda(Pedido):
    """HERENCIA: PedidoRetiroTienda ES UN tipo de Pedido para retiro en tienda"""
    
    def __init__(self, numero_pedido: str, cliente: str, productos: List[Dict], tienda_seleccionada: str):
        # Para retiro en tienda, la dirección es la ubicación de la tienda
        super().__init__(numero_pedido, cliente, productos, tienda_seleccionada)
        
        self.tienda_seleccionada = tienda_seleccionada
        self.fecha_retiro = datetime.now() + timedelta(hours=2)  # Disponible en 2 horas
        self.codigo_retiro = f"RET-{numero_pedido}-{datetime.now().strftime('%H%M')}"
    
    # =============================================
    # POLIMORFISMO: Implementación para retiro
    # =============================================
    def calcular_tiempo_entrega(self) -> str:
        """
        POLIMORFISMO: Retiro inmediato después de preparación
        """
        return "2 horas (una vez preparado)"
    
    def calcular_costo_total(self) -> float:
        """
        POLIMORFISMO: Sin costo de envío para retiro en tienda
        """
        return self.calcular_subtotal()  # Solo subtotal, sin envío
    
    def notificar_cliente(self) -> str:
        """
        POLIMORFISMO: Notificación por app y código QR
        """
        return f"📱 Notificación en APP: Pedido #{self.get_numero_pedido()} listo para retiro. Código: {self.codigo_retiro}. Tienda: {self.tienda_seleccionada}"


# =============================================
# HERENCIA: PedidoInternacional hereda de Pedido
# =============================================
class PedidoInternacional(Pedido):
    """HERENCIA: PedidoInternacional ES UN tipo de Pedido para envíos internacionales"""
    
    def __init__(self, numero_pedido: str, cliente: str, productos: List[Dict], direccion_entrega: str, pais_destino: str):
        super().__init__(numero_pedido, cliente, productos, direccion_entrega)
        
        self.pais_destino = pais_destino
        self.aduana = True
        self.impuestos_importacion = 0.15  # 15% de impuestos
    
    # ENCAPSULAMIENTO: Método protegido para cálculo interno
    def _calcular_costo_envio_internacional(self) -> float:
        """Método protegido para cálculo específico de envío internacional"""
        base_envio = 25.0
        # Costo adicional por distancia/región
        if self.pais_destino in ["EEUU", "Canada", "Mexico"]:
            return base_envio + 10.0
        elif self.pais_destino in ["Europa", "UK"]:
            return base_envio + 15.0
        else:
            return base_envio + 20.0
    
    # =============================================
    # POLIMORFISMO: Implementación internacional
    # =============================================
    def calcular_tiempo_entrega(self) -> str:
        """
        POLIMORFISMO: Tiempo extendido para envíos internacionales
        """
        return "15-30 días hábiles (incluye aduana)"
    
    def calcular_costo_total(self) -> float:
        """
        POLIMORFISMO: Cálculo con envío internacional + impuestos
        """
        subtotal = self.calcular_subtotal()
        costo_envio = self._calcular_costo_envio_internacional()
        impuestos = subtotal * self.impuestos_importacion
        
        return subtotal + costo_envio + impuestos
    
    def notificar_cliente(self) -> str:
        """
        POLIMORFISMO: Notificación detallada con documentación internacional
        """
        return f"📧 Email internacional: Pedido #{self.get_numero_pedido()} enviado a {self.pais_destino}. Incluye documentación de aduana. Tiempo: {self.calcular_tiempo_entrega()}"


# =============================================
# DEMOSTRACIÓN DEL POLIMORFISMO Y SISTEMA
# =============================================
def demostrar_polimorfismo_pedidos():
    """
    Esta función demuestra el POLIMORFISMO en acción:
    Diferentes tipos de pedidos responden al mismo método de manera única
    """
    print("🚀 DEMOSTRACIÓN DE POLIMORFISMO - SISTEMA DE PEDIDOS")
    print("=" * 60)
    
    # Productos de ejemplo
    productos_comunes = [
        {'nombre': 'Laptop Gaming', 'precio': 1200.0, 'cantidad': 1},
        {'nombre': 'Mouse Inalámbrico', 'precio': 45.0, 'cantidad': 1}
    ]
    
    productos_pequenos = [
        {'nombre': 'Libro Python', 'precio': 35.0, 'cantidad': 2},
        {'nombre': 'USB 64GB', 'precio': 25.0, 'cantidad': 1}
    ]
    
    # Crear diferentes tipos de pedidos
    pedidos = [
        PedidoEstandar("EST-001", "Carlos Ruiz", productos_comunes, "Av. Principal 123, Ciudad"),
        PedidoExpress("EXP-001", "Ana López", productos_pequenos, "Calle Secundaria 456, Ciudad"),
        PedidoRetiroTienda("RET-001", "María García", productos_pequenos, "Tienda Centro"),
        PedidoInternacional("INT-001", "John Smith", productos_comunes, "123 Main St, New York", "EEUU")
    ]
    
    # POLIMORFISMO: Mismo método, comportamientos diferentes
    for pedido in pedidos:
        print(f"\n📦 {pedido.__class__.__name__}: #{pedido.get_numero_pedido()}")
        print("-" * 40)
        
        # POLIMORFISMO: calcular_tiempo_entrega() se comporta diferente en cada clase
        tiempo = pedido.calcular_tiempo_entrega()
        print(f"⏰ Tiempo entrega: {tiempo}")
        
        # POLIMORFISMO: calcular_costo_total() calcula de manera diferente
        costo = pedido.calcular_costo_total()
        print(f"💰 Costo total: ${costo:.2f}")
        
        # POLIMORFISMO: notificar_cliente() usa diferentes canales y mensajes
        notificacion = pedido.notificar_cliente()
        print(f"📢 Notificación: {notificacion}")


def simular_flujo_pedidos():
    """
    Simula el flujo completo de 2 pedidos de cada tipo con cambios de estado
    """
    print("\n\n" + "="*60)
    print("📋 SIMULACIÓN COMPLETA DE PEDIDOS")
    print("="*60)
    
    # Productos para simulación
    productos_electronica = [
        {'nombre': 'Tablet 10"', 'precio': 299.99, 'cantidad': 1},
        {'nombre': 'Funda Table', 'precio': 19.99, 'cantidad': 1}
    ]
    
    productos_libreria = [
        {'nombre': 'Cuaderno', 'precio': 8.50, 'cantidad': 3},
        {'nombre': 'Bolígrafos', 'precio': 5.00, 'cantidad': 2}
    ]
    
    # Crear 2 pedidos de cada tipo
    todos_los_pedidos = [
        # Pedidos Estándar
        PedidoEstandar("EST-100", "Laura Martínez", productos_electronica, "Calle Norte 789"),
        PedidoEstandar("EST-101", "Pedro Sánchez", productos_libreria, "Av. Sur 321"),
        
        # Pedidos Express
        PedidoExpress("EXP-100", "Marta Rodríguez", productos_electronica, "Plaza Central 555"),
        PedidoExpress("EXP-101", "David Torres", productos_libreria, "Calle Este 222"),
        
        # Pedidos Retiro en Tienda
        PedidoRetiroTienda("RET-100", "Sofia Vargas", productos_electronica, "Tienda Norte"),
        PedidoRetiroTienda("RET-101", "Javier Mora", productos_libreria, "Tienda Sur"),
        
        # Pedidos Internacionales
        PedidoInternacional("INT-100", "Robert Wilson", productos_electronica, "456 Oak St, Chicago", "EEUU"),
        PedidoInternacional("INT-101", "Emma Davis", productos_libreria, "789 Maple Ave, Toronto", "Canada")
    ]
    
    # Simular flujo de estados y mostrar resúmenes
    for i, pedido in enumerate(todos_los_pedidos):
        print(f"\n{'='*50}")
        print(f"🔄 PROCESANDO PEDIDO {i+1}: {pedido.__class__.__name__} #{pedido.get_numero_pedido()}")
        print(f"{'='*50}")
        
        # Simular cambios de estado
        estados_flujo = [EstadoPedido.CONFIRMADO, EstadoPedido.PREPARACION, EstadoPedido.ENVIADO]
        
        for estado in estados_flujo:
            pedido.cambiar_estado(estado)
        
        # Si es retiro en tienda, simular entrega inmediata
        if isinstance(pedido, PedidoRetiroTienda):
            pedido.cambiar_estado(EstadoPedido.ENTREGADO)
        
        # Mostrar resumen completo (POLIMORFISMO en acción)
        resumen = pedido.obtener_resumen()
        print(f"👤 Cliente: {resumen['cliente']}")
        print(f"📊 Estado: {resumen['estado']}")
        print(f"📦 Tipo envío: {resumen['tipo_envio']}")
        print(f"💵 Subtotal: ${resumen['subtotal']:.2f}")
        print(f"💰 Total: ${resumen['costo_total']:.2f}")
        print(f"⏰ Tiempo: {resumen['tiempo_entrega']}")
        print(f"📢 Notificación: {resumen['notificacion']}")


# =============================================
# EJECUCIÓN PRINCIPAL
# =============================================
if __name__ == "__main__":
    # Demostración del polimorfismo
    demostrar_polimorfismo_pedidos()
    
    # Simulación completa del sistema
    simular_flujo_pedidos()
    
    # Estadísticas finales
    print("\n\n" + "="*60)
    print("📊 RESUMEN DEL SISTEMA DE PEDIDOS")
    print("="*60)
    print("✅ Sistema implementado con éxito")
    print("✅ 4 tipos de pedidos diferentes")
    print("✅ POLIMORFISMO demostrado en cálculos y notificaciones")
    print("✅ ENCAPSULAMIENTO aplicado en estados y validaciones")
    print("✅ HERENCIA utilizada para especialización de pedidos")
    print("✅ ABSTRACCIÓN definida en clase base Pedido")