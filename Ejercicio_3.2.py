"""
CONTEXTO:
La tienda maneja clientes regulares, clientes premium, clientes corporativos
y afiliados, cada uno con beneficios y descuentos diferentes.

REQUERIMIENTOS:
1. Crear clase abstracta "Cliente" (ABSTRACCION):
   - Atributos privados: nombre, email, telefono, fecha_registro
   - Atributo protegido: _historial_compras (lista)
   - Metodo abstracto: calcular_descuento()
   - Metodo abstracto: obtener_beneficios()
   - Metodo concreto: agregar_compra(compra)

2. Clases derivadas (HERENCIA):
   - ClienteRegular: puntos_acumulados, nivel (bronce, plata, oro)
   - ClientePremium: fecha_inicio_membresia, cuota_mensual, envio_gratis
   - ClienteCorporativo: empresa, RUC, limite_credito, descuento_volumen
   - Afiliado: codigo_afiliado, comision_porcentaje, referidos

3. ENCAPSULAMIENTO:
   - Datos personales privados
   - Metodo privado __calcular_puntos()
   - Historial protegido con acceso controlado

4. POLIMORFISMO:
   - calcular_descuento(): Regular (puntos), Premium (10% siempre),
     Corporativo (volumen), Afiliado (5% + comision)
   - Metodo generar_factura() formateado diferente

ENTREGABLES:
- Implementar todas las clases
- Crear 2 clientes de cada tipo
- Simular compras y calcular descuentos
- Reporte de beneficios por tipo de cliente

"""
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Dict

#Abstraccion

class Cliente(ABC):
    def __init__(self, nombre, email, telefono):
        #Encapsulamiento: atributos privados
        self.__nombre = nombre
        self.__email = email
        self.__telefono = telefono
        self.__fecha_registro = datetime.now()
        #Encapsulamiento: atributo protegido
        self._historial_compras = []

    #Encapsulamiento
    def get_nombre(self):
        return self.__nombre
    
    def get_email(self):
        return self.__email
        
    def get_fecha_registro(self):
        return self.__fecha_registro

    def agregar_compra(self, compra):
        self._historial_compras.append({
            **compra,
            "Fecha" : datetime.now()
        })
    
    def obtener_historial(self):
        return self._historial_compras.copy()
    
    #Abstraccion
    @abstractmethod
    def calcular_descuento(self, monto):
        pass

    @abstractmethod
    def obtener_beneficios(self):
        pass

    @abstractmethod
    def generar_factura(self, compra):
        pass
    
#Herencia

class ClienteRegular(Cliente):
    def __init__(self, nombre, email, telefono, nivel: str = "bronce"):
        super().__init__(nombre, email, telefono)
        self.puntos_acumulados = 0
        self.nivel = nivel #bronce, plata, oro
    
    #Encapsulamiento
    def __calcular_puntos(self, monto):
        multiplicadores = {"bronce": 1, "plata": 2, "oro": 3}
        return int(monto * 0.1) * multiplicadores.get(self.nivel, 1)
    
    def calcular_descuento(self, monto):
        #Polimorfismo
        descuento_nivel = {"bronce": 0.02, "plata": 0.05, "oro": 0.08}
        descuento_base = descuento_nivel.get(self.nivel, 0.02)
        descuento_puntos = min(self.puntos_acumulados * 0.001, 0.05)

        return monto * (descuento_base + descuento_puntos)
    
    def obtener_beneficios(self):
        #Polimorfismo
        beneficios = [
            "Acumulacion de puntos por compras"
            "Descuentos progresivos segun nivel"
            "Ofertas exclusivas por email"
        ]

        if self.nivel == "plata":
            beneficios.append("Atencion prioritaria")
        elif self.nivel == "oro":
            beneficios.extend(["Atencion prioritaria", "Acceso a eventos exclusivos"])
        
        return beneficios
    
    def generar_factura(self, compra):
        descuento = self.calcular_descuento(compra["monto"])
        self.puntos_acumulados += self.__calcular_puntos(compra["monto"])
        return f"""
        FACTURA CLIENTE REGULAR
        =======================
        Cliente: {self.get_nombre()}
        Nivel: {self.nivel}
        Puntos acumulados: {self.puntos_acumulados}
        Subtotal: ${compra["monto"]:.2f}
        Descunto: ${descuento:.2f}
        Total: ${compra["monto"] - descuento:.2f}
        ========================
        """
    
#Herencia
class ClientePremium(Cliente):
    def __init__(self, nombre, email, telefono, cuota_mensual):
        super().__init__(nombre, email, telefono)
        self.fecha_inicio_membresia = datetime.now()
        self.cuota_mensual = cuota_mensual
        self.envio_gratis = True
    
    #Polimorfismo
    def calcular_descuento(self, monto):
        #polimorfismo
        return monto * 0.10
    
    def obtener_beneficios(self):
        #polimorfismo
        return [
            "10 % de descuento en todas las compras",
            "Envio gratis ilimiado",
            "Acceso prioritario a nuevos productos",
            "Soporte VIP 24/7",
            "Devoluciones sin costo"
        ]
    
    def generar_factura(self, compra):
        descuento = self.calcular_descuento(compra["monto"])
        return f"""
        ⭐FACTURA CLIENTE PREMIUM⭐
        ============================
        Cliente: {self.get_nombre()}
        Membresia desde: {self.fecha_inicio_membresia.strftime("%d/%m/%Y")}
        Cuota mensual: ${self.cuota_mensual:.2f}
        -----------------------
        Subtotal: ${compra["monto"]:.2f}
        Descuento Premium (10%): ${descuento:.2f}
        Envio: Gratis
        Total: ${compra["monto"] - descuento:.2f}
        =============================
        Gracias por se Premium!🌟
        """

#Herencia
class ClienteCorporativo(Cliente):
    def __init__(self, nombre, email, telefono, empresa, ruc):
        super().__init__(nombre, email, telefono)
        self.empresa = empresa
        self.__ruc = ruc
        self.limite_credito = 10000.0
        self.descuento_volumen = 0.15
    
    #Encapsulamiento
    def get_ruc(self):
        return self.__ruc
    
    #Polimorfismo
    def calcular_descuento(self, monto):
        descuento_base = self.descuento_volumen

        if monto > 5000:
            descuento_base += 0.05
        elif monto > 2000:
            descuento_base += 0.02
        
        return monto * descuento_base

    def obtener_beneficios(self):
        #polimorfismo
        return[
            "Descuentos por volumen de compra"
            "Linea de credito corporativa"
            "Facturacion consolidada"
            "Account manager dedicado"
            "Pedidos prioritarios"
        ]
    
    def generar_factura(self, compra):
        descuento = self.calcular_descuento(compra["monto"])
        return f"""
        FACTURA CORPORATIVA
        ===================
        Empresa: {self.empresa}
        RUC: {self.get_ruc()}
        Contacto: {self.get_nombre()}
        -------------------
        Subtotal: ${compra["monto"]:,.2f}
        Descuento corporativo: ${descuento:,.2f}
        TOTAL: ${compra["monto"] - descuento:,.2f}
        ===================
        Limite de credito: ${self.limite_credito:,.2f}
        """
    
#Herencia
class Afiliado(Cliente):
    def __init__(self, nombre, email, telefono, codigo_afiliado):
        super().__init__(nombre, email, telefono)
        self.codigo_afiliado = codigo_afiliado
        self.comision_porcentaje = 0.05
        self.referidos = 0

    #polimorfismo
    def calcular_descuento(self, monto):
        descuento_base = monto * 0.05
        comision_adicional = monto * (min(self.referidos, 10) * 0.001)
        
        return descuento_base + comision_adicional

    def obtener_beneficios(self):
        #polimorfismo
        beneficios = [
            "5% de descuento en todas las compras",
            "Comision por referidos",
            "Codigo de afiliado personal"
        ]

        if self.referidos > 5:
            beneficios.append("Comision bonus por referidos frecuentes")
        
        return beneficios

    def generar_factura(self, compra):
        #polimorfismo
        descuento = self.calcular_descuento(compra["monto"])
        comision = compra["monto"] * self.comision_porcentaje

        return f"""
        FACTURA AFILIADO
        ====================
        Afiliado: {self.get_nombre()}
        Codigo: {self.codigo_afiliado}
        Referidos: {self.referidos}
        --------------------
        Subtotal: ${compra["monto"]:.2f}
        Descuento afiliado: ${descuento:.2f}
        Comision ganada: ${comision:.2f}
        Total a pagar: ${compra["monto"] - descuento:.2f}
        ====================
        Gracias por su compra.
        """
    
    
#demostrar polimorfismo
def demostrar_polimorfismo():
    print("DEMOSTRACION DE POLIMORFISMO")
    print("=" * 40)

    clientes = [
        ClienteRegular("Juan Pérez", "juan@email.com", "123456789", "oro"),
        ClientePremium("María García", "maria@email.com", "987654321", 29.99),
        ClienteCorporativo("Carlos Ruiz", "carlos@empresa.com", "555555555", "Tech Corp", "20123456789"),
        Afiliado("Ana López", "ana@email.com", "111111111", "AFL-001")
    ]
    
    compra_ejemplo = {"monto": 1000.0, "productos": ["Laptop", "Mouse"]}

    for cliente in clientes:
        print(f"\n {cliente.__class__.__name__}:")
        print("=" * 30)

        descuento = cliente.calcular_descuento(compra_ejemplo["monto"])
        print(f"Descuento aplicado: ${descuento:.2f}")

        beneficios = cliente.obtener_beneficios()
        print(f"Beneficios: {beneficios[0]}...")

        factura = cliente.generar_factura(compra_ejemplo)
        print("Factura generada con formato especifico")

#Ejemplo de uso
if __name__ == "__main__":
    demostrar_polimorfismo()

    print("\n\n" + "=" * 60)
    print("EJEMPLO PRACTICO COMPLETO")
    print("=" * 60)

    cliente_regular = ClienteRegular("Laura Martínez", "laura@email.com", "123123123", "plata")
    cliente_premium = ClientePremium("Roberto Silva", "roberto@email.com", "456456456", 49.99)
    
    compra_grande = {"monto": 2500.0, "productos": ["TV 55", "Soundbar", "Base TV"]}

    cliente_regular.agregar_compra(compra_grande)
    cliente_premium.agregar_compra(compra_grande)

    print("\n FACTURA CLIENTE REGULAR:")
    print(cliente_regular.generar_factura(compra_grande))
    
    print("\n FACTURA CLIENTE PREMIUM:")
    print(cliente_premium.generar_factura(compra_grande))