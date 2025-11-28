"""
EJERCICIO 3.4: SISTEMA DE PAGOS Y TRANSACCIONES
--------------------------------------------------------------------------------------------------------------
CONTEXTO:
La tienda acepta diferentes metodos de pago: tarjeta de credito, transferencia
bancaria, billeteras digitales y pago contra entrega, cada uno con validaciones
y procesos diferentes.

REQUERIMIENTOS:
1. Crear clase abstracta "MetodoPago" (ABSTRACCION):
   - Atributos privados: monto, fecha_transaccion, estado_pago
   - Atributo protegido: _comision_procesamiento
   - Metodo abstracto: procesar_pago()
   - Metodo abstracto: validar_fondos()
   - Metodo concreto: generar_comprobante()

2. Clases derivadas (HERENCIA):
   - PagoTarjeta: numero_tarjeta, cvv, fecha_expiracion, tipo_tarjeta
   - PagoTransferencia: banco_origen, numero_cuenta, codigo_verificacion
   - PagoBilleteraDigital: proveedor, email_cuenta, saldo_disponible
   - PagoContraEntrega: requiere_cambio, monto_entregado

3. ENCAPSULAMIENTO:
   - Datos financieros privados y cifrados
   - Metodo privado __encriptar_datos()
   - Validaciones de seguridad internas

4. POLIMORFISMO:
   - procesar_pago() diferente: Tarjeta (pasarela), Transferencia (banco),
     Billetera (API), Contra entrega (manual)
   - validar_fondos() varia en complejidad
   - Comisiones diferentes: 3%, 1%, 2%, 0%

ENTREGABLES:
- Implementar todas las clases
- Simular transacciones con cada metodo
- Validar seguridad de datos sensibles
- Reporte de comisiones por metodo de pago

"""

from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Dict, Optional
from enum import Enum
import hashlib
import secrets

# =============================================
# ENUMS para estados y tipos
# =============================================
class EstadoPago(Enum):
    PENDIENTE = "Pendiente"
    PROCESANDO = "Procesando"
    EXITOSO = "Exitoso"
    FALLIDO = "Fallido"
    REVERTIDO = "Revertido"

class TipoTarjeta(Enum):
    VISA = "Visa"
    MASTERCARD = "MasterCard"
    AMEX = "American Express"

class ProveedorBilletera(Enum):
    PAYPAL = "PayPal"
    MERCADOPAGO = "MercadoPago"
    DAVIPLATA = "DaviPlata"

# =============================================
# ABSTRACCIÓN: Clase abstracta MetodoPago
# =============================================
class MetodoPago(ABC):
    """
    CLASE ABSTRACTA que define la estructura base para todos los métodos de pago.
    No se puede instanciar directamente - sirve como plantilla para métodos específicos.
    """
    
    def __init__(self, monto: float):
        # ENCAPSULAMIENTO: Atributos privados
        self.__monto = monto
        self.__fecha_transaccion = datetime.now()
        self.__estado_pago = EstadoPago.PENDIENTE
        
        # ENCAPSULAMIENTO: Atributo protegido
        self._comision_procesamiento = 0.0
    
    # ENCAPSULAMIENTO: Getters para acceso controlado
    def get_monto(self) -> float:
        return self.__monto
    
    def get_fecha_transaccion(self) -> datetime:
        return self.__fecha_transaccion
    
    def get_estado_pago(self) -> EstadoPago:
        return self.__estado_pago
    
    def get_comision(self) -> float:
        return self._comision_procesamiento
    
    # ENCAPSULAMIENTO: Método privado para seguridad
    def __encriptar_datos(self, datos: str) -> str:
        """
        MÉTODO PRIVADO: Solo accesible dentro de esta clase
        Simula encriptación de datos sensibles usando hash
        """
        salt = secrets.token_hex(16)
        datos_con_salt = datos + salt
        return hashlib.sha256(datos_con_salt.encode()).hexdigest()[:20]
    
    def __validar_monto_positivo(self) -> bool:
        """Validación privada de monto positivo"""
        return self.__monto > 0
    
    # Método concreto - implementación común para todas las clases hijas
    def generar_comprobante(self) -> Dict:
        """
        Genera comprobante común para todos los métodos de pago
        """
        return {
            'fecha': self.__fecha_transaccion.strftime('%Y-%m-%d %H:%M:%S'),
            'monto': self.__monto,
            'estado': self.__estado_pago.value,
            'comision': self._comision_procesamiento,
            'total_con_comision': self.__monto + self._comision_procesamiento,
            'id_transaccion': f"TXN-{self.__encriptar_datos(str(self.__fecha_transaccion))}"
        }
    
    def _cambiar_estado(self, nuevo_estado: EstadoPago) -> None:
        """Método protegido para cambiar estado internamente"""
        self.__estado_pago = nuevo_estado
    
    # =============================================
    # ABSTRACCIÓN: Métodos abstractos (POLIMORFISMO)
    # =============================================
    @abstractmethod
    def procesar_pago(self) -> bool:
        """
        MÉTODO ABSTRACTO - Cada clase hija debe implementar su proceso de pago
        POLIMORFISMO: mismo método, comportamientos diferentes según el método de pago
        """
        pass
    
    @abstractmethod
    def validar_fondos(self) -> bool:
        """
        MÉTODO ABSTRACTO - Cada método valida fondos de manera única
        POLIMORFISMO: misma interfaz, validaciones diferentes
        """
        pass
    
    @abstractmethod
    def obtener_detalles_metodo(self) -> Dict:
        """
        MÉTODO ABSTRACTO - Cada método muestra detalles específicos
        POLIMORFISMO: mismo nombre de método, información diferente
        """
        pass

# =============================================
# HERENCIA: PagoTarjeta hereda de MetodoPago
# =============================================
class PagoTarjeta(MetodoPago):
    """
    HERENCIA: PagoTarjeta ES UN tipo de MetodoPago
    Hereda todos los atributos y métodos de la clase base MetodoPago
    """
    
    def __init__(self, monto: float, numero_tarjeta: str, cvv: str, 
                 fecha_expiracion: str, tipo_tarjeta: TipoTarjeta):
        # HERENCIA: Llamada al constructor de la clase padre
        super().__init__(monto)
        
        # ENCAPSULAMIENTO: Datos financieros privados y encriptados
        self.__numero_tarjeta = self._MetodoPago__encriptar_datos(numero_tarjeta)
        self.__cvv = self._MetodoPago__encriptar_datos(cvv)
        self.__fecha_expiracion = fecha_expiracion
        self.tipo_tarjeta = tipo_tarjeta
        
        # Comisión específica para tarjeta
        self._comision_procesamiento = monto * 0.03  # 3%
    
    # =============================================
    # POLIMORFISMO: Implementación específica
    # =============================================
    def procesar_pago(self) -> bool:
        """
        POLIMORFISMO: Procesamiento mediante pasarela de pago para tarjetas
        """
        print(f"💳 Procesando pago con {self.tipo_tarjeta.value}...")
        
        if not self.validar_fondos():
            self._cambiar_estado(EstadoPago.FALLIDO)
            return False
        
        # Simulación de conexión con pasarela de pago
        self._cambiar_estado(EstadoPago.PROCESANDO)
        
        # Validaciones de seguridad
        if not self.__validar_fecha_expiracion():
            print("❌ Tarjeta expirada")
            self._cambiar_estado(EstadoPago.FALLIDO)
            return False
        
        if not self.__validar_numero_tarjeta():
            print("❌ Número de tarjeta inválido")
            self._cambiar_estado(EstadoPago.FALLIDO)
            return False
        
        # Simulación de procesamiento exitoso
        print(f"✅ Pago con tarjeta procesado exitosamente")
        self._cambiar_estado(EstadoPago.EXITOSO)
        return True
    
    def validar_fondos(self) -> bool:
        """
        POLIMORFISMO: Validación compleja con entidad emisora de tarjeta
        """
        print("🔍 Validando fondos con entidad emisora...")
        
        # Simulación de validación con banco emisor
        fondos_suficientes = self.get_monto() <= 5000  # Límite simulado
        
        if not fondos_suficientes:
            print("❌ Fondos insuficientes en la tarjeta")
            return False
        
        print("✅ Fondos validados correctamente")
        return True
    
    def obtener_detalles_metodo(self) -> Dict:
        """
        POLIMORFISMO: Detalles específicos de pago con tarjeta
        """
        return {
            'tipo_metodo': 'Tarjeta de Crédito/Débito',
            'tipo_tarjeta': self.tipo_tarjeta.value,
            'tarjeta_enmascarada': f"****-****-****-{self.__numero_tarjeta[-4:]}",
            'fecha_expiracion': self.__fecha_expiracion,
            'comision_porcentaje': '3%'
        }
    
    # ENCAPSULAMIENTO: Métodos privados para validaciones internas
    def __validar_fecha_expiracion(self) -> bool:
        """Valida que la tarjeta no esté expirada"""
        try:
            mes, año = self.__fecha_expiracion.split('/')
            fecha_expiracion = datetime(int(año), int(mes), 1)
            return fecha_expiracion > datetime.now()
        except:
            return False
    
    def __validar_numero_tarjeta(self) -> bool:
        """Valida formato de número de tarjeta (simplificado)"""
        return len(self.__numero_tarjeta) >= 13 and self.__numero_tarjeta.isdigit()

# =============================================
# HERENCIA: PagoTransferencia hereda de MetodoPago
# =============================================
class PagoTransferencia(MetodoPago):
    """HERENCIA: PagoTransferencia ES UN tipo de MetodoPago mediante transferencia bancaria"""
    
    def __init__(self, monto: float, banco_origen: str, numero_cuenta: str, codigo_verificacion: str):
        super().__init__(monto)
        
        # ENCAPSULAMIENTO: Datos bancarios privados
        self.__banco_origen = banco_origen
        self.__numero_cuenta = self._MetodoPago__encriptar_datos(numero_cuenta)
        self.__codigo_verificacion = self._MetodoPago__encriptar_datos(codigo_verificacion)
        
        # Comisión específica para transferencia
        self._comision_procesamiento = monto * 0.01  # 1%
    
    # =============================================
    # POLIMORFISMO: Implementación única para Transferencia
    # =============================================
    def procesar_pago(self) -> bool:
        """
        POLIMORFISMO: Procesamiento mediante sistema bancario
        """
        print(f"🏦 Procesando transferencia bancaria desde {self.__banco_origen}...")
        
        if not self.validar_fondos():
            self._cambiar_estado(EstadoPago.FALLIDO)
            return False
        
        self._cambiar_estado(EstadoPago.PROCESANDO)
        
        # Simulación de validación bancaria
        if not self.__validar_cuenta_bancaria():
            print("❌ Cuenta bancaria inválida")
            self._cambiar_estado(EstadoPago.FALLIDO)
            return False
        
        if not self.__validar_codigo_verificacion():
            print("❌ Código de verificación incorrecto")
            self._cambiar_estado(EstadoPago.FALLIDO)
            return False
        
        # Simulación de procesamiento bancario (más lento)
        print("⏳ Confirmando transferencia con el banco...")
        print("✅ Transferencia bancaria procesada exitosamente")
        self._cambiar_estado(EstadoPago.EXITOSO)
        return True
    
    def validar_fondos(self) -> bool:
        """
        POLIMORFISMO: Validación mediante consulta bancaria
        """
        print("🔍 Verificando fondos en cuenta bancaria...")
        
        # Simulación de consulta a sistema bancario
        fondos_disponibles = self.get_monto() <= 10000  # Límite simulado
        
        if not fondos_disponibles:
            print("❌ Fondos insuficientes en cuenta bancaria")
            return False
        
        print("✅ Fondos validados en cuenta bancaria")
        return True
    
    def obtener_detalles_metodo(self) -> Dict:
        """
        POLIMORFISMO: Detalles específicos de transferencia
        """
        return {
            'tipo_metodo': 'Transferencia Bancaria',
            'banco_origen': self.__banco_origen,
            'cuenta_enmascarada': f"****{self.__numero_cuenta[-4:]}",
            'comision_porcentaje': '1%'
        }
    
    # ENCAPSULAMIENTO: Métodos privados bancarios
    def __validar_cuenta_bancaria(self) -> bool:
        """Valida formato de cuenta bancaria"""
        return len(self.__numero_cuenta) >= 10
    
    def __validar_codigo_verificacion(self) -> bool:
        """Valida código de verificación"""
        return len(self.__codigo_verificacion) == 6

# =============================================
# HERENCIA: PagoBilleteraDigital hereda de MetodoPago
# =============================================
class PagoBilleteraDigital(MetodoPago):
    """HERENCIA: PagoBilleteraDigital ES UN tipo de MetodoPago mediante billetera digital"""
    
    def __init__(self, monto: float, proveedor: ProveedorBilletera, email_cuenta: str, saldo_disponible: float):
        super().__init__(monto)
        
        self.proveedor = proveedor
        self.__email_cuenta = email_cuenta
        self.__saldo_disponible = saldo_disponible
        
        # Comisión específica para billetera digital
        self._comision_procesamiento = monto * 0.02  # 2%
    
    # =============================================
    # POLIMORFISMO: Implementación para Billetera Digital
    # =============================================
    def procesar_pago(self) -> bool:
        """
        POLIMORFISMO: Procesamiento mediante API de billetera digital
        """
        print(f"📱 Procesando pago con {self.proveedor.value}...")
        
        if not self.validar_fondos():
            self._cambiar_estado(EstadoPago.FALLIDO)
            return False
        
        self._cambiar_estado(EstadoPago.PROCESANDO)
        
        # Simulación de API de billetera digital
        if not self.__validar_cuenta_activa():
            print("❌ Cuenta de billetera no activa")
            self._cambiar_estado(EstadoPago.FALLIDO)
            return False
        
        if not self.__validar_limites():
            print("❌ Límite de transacción excedido")
            self._cambiar_estado(EstadoPago.FALLIDO)
            return False
        
        # Simulación de procesamiento rápido vía API
        print("⚡ Procesando mediante API...")
        print(f"✅ Pago con {self.proveedor.value} procesado exitosamente")
        self._cambiar_estado(EstadoPago.EXITOSO)
        return True
    
    def validar_fondos(self) -> bool:
        """
        POLIMORFISMO: Validación directa contra saldo disponible
        """
        print(f"🔍 Verificando saldo en {self.proveedor.value}...")
        
        total_pago = self.get_monto() + self._comision_procesamiento
        
        if total_pago > self.__saldo_disponible:
            print(f"❌ Saldo insuficiente en {self.proveedor.value}")
            return False
        
        print(f"✅ Saldo validado en {self.proveedor.value}")
        return True
    
    def obtener_detalles_metodo(self) -> Dict:
        """
        POLIMORFISMO: Detalles específicos de billetera digital
        """
        return {
            'tipo_metodo': 'Billetera Digital',
            'proveedor': self.proveedor.value,
            'email_cuenta': self.__email_cuenta,
            'saldo_disponible': self.__saldo_disponible,
            'comision_porcentaje': '2%'
        }
    
    # ENCAPSULAMIENTO: Métodos privados de billetera
    def __validar_cuenta_activa(self) -> bool:
        """Valida que la cuenta de billetera esté activa"""
        return "@" in self.__email_cuenta
    
    def __validar_limites(self) -> bool:
        """Valida límites de transacción"""
        return self.get_monto() <= 2000  # Límite simulado

# =============================================
# HERENCIA: PagoContraEntrega hereda de MetodoPago
# =============================================
class PagoContraEntrega(MetodoPago):
    """HERENCIA: PagoContraEntrega ES UN tipo de MetodoPago con pago al recibir"""
    
    def __init__(self, monto: float, requiere_cambio: bool = False, monto_entregado: float = 0):
        super().__init__(monto)
        
        self.requiere_cambio = requiere_cambio
        self.__monto_entregado = monto_entregado
        
        # Sin comisión para pago contra entrega
        self._comision_procesamiento = 0.0  # 0%
    
    # =============================================
    # POLIMORFISMO: Implementación para Contra Entrega
    # =============================================
    def procesar_pago(self) -> bool:
        """
        POLIMORFISMO: Procesamiento manual al momento de la entrega
        """
        print("📦 Procesando pago contra entrega...")
        
        if not self.validar_fondos():
            self._cambiar_estado(EstadoPago.FALLIDO)
            return False
        
        self._cambiar_estado(EstadoPago.PROCESANDO)
        
        # Simulación de proceso manual
        if self.requiere_cambio:
            cambio = self.__monto_entregado - self.get_monto()
            if cambio < 0:
                print("❌ Monto entregado insuficiente")
                self._cambiar_estado(EstadoPago.FALLIDO)
                return False
            print(f"💰 Cambio a devolver: ${cambio:.2f}")
        
        # Simulación de confirmación manual
        print("✅ Pago contra entrega registrado exitosamente")
        self._cambiar_estado(EstadoPago.EXITOSO)
        return True
    
    def validar_fondos(self) -> bool:
        """
        POLIMORFISMO: Validación simple para pago en efectivo
        """
        print("🔍 Validando pago contra entrega...")
        
        if self.requiere_cambio and self.__monto_entregado < self.get_monto():
            print("❌ Monto entregado insuficiente para pago")
            return False
        
        print("✅ Pago contra entrega validado")
        return True
    
    def obtener_detalles_metodo(self) -> Dict:
        """
        POLIMORFISMO: Detalles específicos de pago contra entrega
        """
        detalles = {
            'tipo_metodo': 'Pago Contra Entrega',
            'requiere_cambio': self.requiere_cambio,
            'comision_porcentaje': '0%'
        }
        
        if self.requiere_cambio:
            detalles['monto_entregado'] = self.__monto_entregado
            detalles['cambio'] = self.__monto_entregado - self.get_monto()
        
        return detalles

# =============================================
# DEMOSTRACIÓN DEL POLIMORFISMO Y SISTEMA
# =============================================
def demostrar_polimorfismo_pagos():
    """
    Esta función demuestra el POLIMORFISMO en acción:
    Diferentes métodos de pago responden al mismo método de manera única
    """
    print("🚀 DEMOSTRACIÓN DE POLIMORFISMO - SISTEMA DE PAGOS")
    print("=" * 60)
    
    # Crear diferentes métodos de pago
    metodos_pago = [
        PagoTarjeta(150.50, "4111111111111111", "123", "12/25", TipoTarjeta.VISA),
        PagoTransferencia(299.99, "Bancolombia", "12345678901", "123456"),
        PagoBilleteraDigital(75.25, ProveedorBilletera.MERCADOPAGO, "usuario@email.com", 500.0),
        PagoContraEntrega(89.99, True, 100.0)
    ]
    
    # POLIMORFISMO: Mismo método, comportamientos diferentes
    for metodo in metodos_pago:
        print(f"\n💳 {metodo.__class__.__name__}:")
        print("-" * 40)
        
        # POLIMORFISMO: obtener_detalles_metodo() retorna información diferente
        detalles = metodo.obtener_detalles_metodo()
        print(f"📋 Método: {detalles['tipo_metodo']}")
        print(f"💵 Comisión: {detalles['comision_porcentaje']}")
        
        # POLIMORFISMO: validar_fondos() realiza validaciones diferentes
        fondos_validos = metodo.validar_fondos()
        print(f"💰 Fondos válidos: {fondos_validos}")
        
        # POLIMORFISMO: procesar_pago() ejecuta procesos diferentes
        if fondos_validos:
            resultado = metodo.procesar_pago()
            print(f"✅ Procesamiento exitoso: {resultado}")
        
        # Comprobante común pero con datos específicos
        comprobante = metodo.generar_comprobante()
        print(f"🧾 ID Transacción: {comprobante['id_transaccion']}")

def simular_transacciones_completas():
    """
    Simula transacciones completas con cada método de pago
    """
    print("\n\n" + "="*60)
    print("💳 SIMULACIÓN COMPLETA DE TRANSACCIONES")
    print("="*60)
    
    # Simular múltiples transacciones
    transacciones = [
        {
            'metodo': PagoTarjeta(450.75, "5555555555554444", "456", "06/26", TipoTarjeta.MASTERCARD),
            'descripcion': "Compra de electrónicos"
        },
        {
            'metodo': PagoTransferencia(1200.00, "Davivienda", "98765432109", "654321"),
            'descripcion': "Compra mayorista"
        },
        {
            'metodo': PagoBilleteraDigital(65.50, ProveedorBilletera.DAVIPLATA, "user@davi.com", 200.0),
            'descripcion': "Compra rápida"
        },
        {
            'metodo': PagoContraEntrega(35.25, False),
            'descripcion': "Compra local"
        }
    ]
    
    reporte_comisiones = []
    
    for i, transaccion in enumerate(transacciones, 1):
        print(f"\n{'='*50}")
        print(f"🔄 TRANSACCIÓN {i}: {transaccion['descripcion']}")
        print(f"{'='*50}")
        
        metodo = transaccion['metodo']
        
        # Procesar transacción
        resultado = metodo.procesar_pago()
        
        # Generar comprobante
        comprobante = metodo.generar_comprobante()
        
        # Mostrar resultados
        print(f"📊 Estado: {comprobante['estado']}")
        print(f"💵 Monto: ${comprobante['monto']:.2f}")
        print(f"💰 Comisión: ${comprobante['comision']:.2f}")
        print(f"🧮 Total: ${comprobante['total_con_comision']:.2f}")
        
        # Agregar al reporte de comisiones
        reporte_comisiones.append({
            'metodo': metodo.__class__.__name__,
            'comision': comprobante['comision'],
            'porcentaje': metodo.obtener_detalles_metodo()['comision_porcentaje'],
            'estado': comprobante['estado']
        })
    
    # Generar reporte de comisiones
    print("\n\n" + "="*60)
    print("📊 REPORTE DE COMISIONES POR MÉTODO DE PAGO")
    print("="*60)
    
    total_comisiones = 0
    for reporte in reporte_comisiones:
        print(f"🔹 {reporte['metodo']}: {reporte['porcentaje']} = ${reporte['comision']:.2f} - {reporte['estado']}")
        total_comisiones += reporte['comision']
    
    print(f"\n💰 TOTAL COMISIONES: ${total_comisiones:.2f}")

def validar_seguridad_datos():
    """
    Demuestra las medidas de seguridad y encapsulamiento
    """
    print("\n\n" + "="*60)
    print("🔒 VALIDACIÓN DE SEGURIDAD DE DATOS SENSIBLES")
    print("="*60)
    
    # Crear pago con tarjeta para demostrar seguridad
    pago_tarjeta = PagoTarjeta(100.0, "4111111111111111", "123", "12/25", TipoTarjeta.VISA)
    
    # Intentar acceder a datos privados (no debería ser posible directamente)
    print("🔐 Datos encriptados y protegidos:")
    
    # Solo podemos acceder mediante métodos públicos
    detalles = pago_tarjeta.obtener_detalles_metodo()
    print(f"💳 Tarjeta: {detalles['tarjeta_enmascarada']}")
    print(f"📅 Expiración: {detalles['fecha_expiracion']}")
    
    # Comprobante seguro
    comprobante = pago_tarjeta.generar_comprobante()
    print(f"🆔 ID Transacción Seguro: {comprobante['id_transaccion']}")
    
    print("\n✅ Todos los datos sensibles están encriptados y protegidos")

# =============================================
# EJECUCIÓN PRINCIPAL
# =============================================
if __name__ == "__main__":
    # Demostración del polimorfismo
    demostrar_polimorfismo_pagos()
    
    # Simulación completa de transacciones
    simular_transacciones_completas()
    
    # Validación de seguridad
    validar_seguridad_datos()
    
    # Resumen final
    print("\n\n" + "="*60)
    print("✅ SISTEMA DE PAGOS IMPLEMENTADO EXITOSAMENTE")
    print("="*60)
    print("🔹 ABSTRACCIÓN: Clase base MetodoPago con métodos abstractos")
    print("🔹 HERENCIA: 4 tipos específicos de métodos de pago")
    print("🔹 ENCAPSULAMIENTO: Datos sensibles protegidos y encriptados")
    print("🔹 POLIMORFISMO: Mismos métodos, comportamientos diferentes")
    print("🔹 SEGURIDAD: Validaciones y encriptación implementadas")
    print("🔹 REPORTES: Comisiones y transacciones rastreables")