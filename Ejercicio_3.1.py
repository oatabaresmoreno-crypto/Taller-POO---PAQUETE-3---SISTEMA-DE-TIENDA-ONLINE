"""
EJERCICIO 3.1: CATALOGO DE PRODUCTOS
----------------------------------------------------------------------------------------------------------------------
CONTEXTO:
Una tienda online vende productos fisicos, digitales, servicios y suscripciones.
Cada categoria tiene caracteristicas de envio, entrega y almacenamiento diferentes.

REQUERIMIENTOS:
1. Crear clase abstracta "Producto" (ABSTRACCION):
   - Atributos privados: nombre, codigo_SKU, precio, stock, categoria
   - Atributo protegido: _descuento_actual
   - Metodo abstracto: calcular_costo_envio()
   - Metodo abstracto: tiempo_entrega()
   - Metodo concreto: aplicar_descuento(porcentaje)

2. Clases derivadas (HERENCIA):
   - ProductoFisico: peso_kg, dimensiones, almacen_ubicacion
   - ProductoDigital: tamaño_archivo_mb, formato, url_descarga, licencia
   - Servicio: duracion_horas, profesional_asignado, fecha_prestacion
   - Suscripcion: periodo (mensual, anual), auto_renovable, beneficios

3. ENCAPSULAMIENTO:
   - Precio con validacion y control de cambios
   - Metodo privado __calcular_impuestos()
   - Stock privado con alertas

4. POLIMORFISMO:
   - calcular_costo_envio(): Fisico (segun peso), Digital (0),
     Servicio (desplazamiento), Suscripcion (0)
   - tiempo_entrega() varia drasticamente

ENTREGABLES:
- Todas las clases implementadas
- Catalogo con 3 productos de cada tipo
- Calcular costos totales incluyendo envio
- Aplicar descuentos de forma polimórfica

"""

from abc import ABC, abstractmethod
from typing import List, Dict

# 1. Abstraccion 
class Producto(ABC):
    def __init__(self, nombre, codigo_SKU, precio, stock, categoria):
        self.__nombre = nombre
        self.__codigo_SKU = codigo_SKU
        self.__precio = precio
        self.__stock = stock
        self.__categoria = categoria
        self._descuento_actual = 0.0
        self.__historial_precios = [precio]

    #metodos abstractos
    @abstractmethod
    def calcular_costo_envio(self):
        pass
    
    @abstractmethod
    def tiempo_entrega(self):
        pass

    #metodo concreto
    def aplicar_descuento(self, porcentaje):
        if porcentaje < 0 or porcentaje > 100:
            raise ValueError ("El descuento debe estar entre 0 y 100")
        self._descuento_actual = porcentaje
        print(f"Descuento del {porcentaje}% aplicado a {self.nombre}")
    
    def calcular_precio_final(self):
        return self.precio + self.calcular_costo_envio() + self.__calcular_impuestos()

    def mostrar_info(self):
        return f"""
{self.nombre} ({self.codigo_SKU})
Precio: ${self.precio} (Stock: {self.stock})
Categoria: {self.categoria}
Envio: ${self.calcular_costo_envio()} - {self.tiempo_entrega()}
Precio final: ${self.calcular_precio_final()}
"""

    #3. Encapsulamiento
    @property
    def nombre(self):
        return self.__nombre
    
    @property
    def codigo_SKU(self):
        return self.__codigo_SKU
    
    @property
    def precio(self):
        precio_con_descuento = self.__precio * (1 - self._descuento_actual / 100)
        return round(precio_con_descuento, 2)
    
    @precio.setter
    def precio(self, nuevo_precio):
        if nuevo_precio < 0:
            raise ValueError("El precio no puede ser negativo")
        self.__precio = nuevo_precio
        self.__historial_precios.append(nuevo_precio)
        print(f"Precio actualizado para {self.__nombre}: ${nuevo_precio}")
    
    @property
    def stock(self):
        return self.__stock
    
    @stock.setter
    def stock(self, nuevo_stock):
        if nuevo_stock < 0:
            raise ValueError("El stock no puede ser negativo")
        if nuevo_stock < 5 and self.__stock >= 5:
            print(f"ALERTA: Stock bajo para {self.__nombre} - Solo {nuevo_stock} unidades")
        self.__stock = nuevo_stock
    
    @property
    def categoria(self):
        return self.__categoria
    
    def __calcular_impuestos(self):
        return self.precio * 0.19

# 2. Herencia

class producto_fisico(Producto):
    def __init__(self, nombre, codigo_SKU, precio, stock, peso_kg, dimensiones, almacen_ubicacion):
        super().__init__(nombre, codigo_SKU, precio, stock, "Fisico")
        self.peso_kg = peso_kg
        self.dimensiones = dimensiones
        self.almacen_ubicacion = almacen_ubicacion
    
    #4. Polimorfismo - implementacion especifica
    def calcular_costo_envio(self):
        costo_base = 5.0
        costo_por_kg = 2.0
        return costo_base + (self.peso_kg * costo_por_kg)
    
    def tiempo_entrega(self):
        if "Bogota" in self.almacen_ubicacion:
            return "1-2 dias habiles"
        elif "Medellin" in self.almacen_ubicacion:
            return "2-3 dias habiles"
        else:
            return "3-5 dias habiles"

class producto_digital(Producto):
    def __init__(self, nombre, codigo_SKU, precio, stock, tamaño_archivo_mb, formato, url_descarga, licencia):
        super().__init__(nombre, codigo_SKU, precio, stock, "Digital")
        self.tamaño_archivo_mb = tamaño_archivo_mb
        self.formato = formato
        self.url_descarga = url_descarga
        self.licencia = licencia
    
    #4. Polimorfismo - implementacion especifica
    def calcular_costo_envio(self):
        return 0.0
    
    def tiempo_entrega(self):
        return "Inmediato - Descarga instantanea"
    
class servicio(Producto):
    def __init__(self, nombre, codigo_SKU, precio, stock, duracion_horas, profesional_asignado, fecha_prestacion):
        super().__init__(nombre, codigo_SKU, precio, stock, "Servicio")
        self.duracion_horas = duracion_horas
        self.profesional_asignado = profesional_asignado
        self.fecha_prestacion = fecha_prestacion
    
    #4. Polimorfismo - implementacion especifica
    def calcular_costo_envio(self):
        return 20.0 + (self.duracion_horas * 5.0)
    
    def tiempo_entrega(self):
        return f"Asignado para {self.fecha_prestacion}"

class suscripcion(Producto):
    def __init__(self, nombre, codigo_SKU, precio, stock, periodo, auto_renovable, beneficios ):
        super().__init__(nombre, codigo_SKU, precio, stock, "Suscripcion")
        self.periodo = periodo
        self.auto_renovable = auto_renovable
        self.beneficios = beneficios
    
    #4. Polimorfismo - implementacion especifica
    def calcular_costo_envio(self):
        return 0.0
    
    def tiempo_entrega(self):
        return "Inmediato - Activacion al instante"
    

#Catalogo y ejecucion

class Catalogo:
    def __init__(self):
        self.productos = []
    
    def agregar_producto(self, producto):
        self.productos.append(producto)
    
    def mostrar_catalogo(self):
        print("CATALOGO DE PRODUCTOS")
        print("=" * 60)
        for producto in self.productos:
            print(producto.mostrar_info())
            print("-" * 40)
    
    def calcular_costos_totales(self):
        print("RESUMEN DE COSTOS TOTALES")
        print("-" * 40)
        total_sin_envio = 0
        total_envios = 0
        total_final = 0

        for producto in self.productos:
            precio_base = producto.precio
            costo_envio = producto.calcular_costo_envio()
            precio_final = producto.calcular_precio_final()

            total_sin_envio += precio_base
            total_envios += costo_envio
            total_final += precio_final

            print(f"{producto.nombre}: Base ${precio_base} + Envio ${costo_envio} = Total ${precio_final}")
        
def main():
    #Crear catalogo
    catalogo = Catalogo()

    #Productos fisicos
    catalogo.agregar_producto(
        producto_fisico("Laptop Gaming", "LAP-GAM-001", 1500.00, 10, 2.5, "40x30x5 cm", "Almacen Bogota")
    )

    catalogo.agregar_producto(
        producto_fisico("Mouse inalambrico", "MOU-WIR-002", 45.00, 25, 0.3, "12x8x4 cm", "Almacen Medellin")
    )

    catalogo.agregar_producto(
        producto_fisico("Monitos 24\"", "MON-24-003", 320.00, 8, 4.2, "55x35x15 cm", "Almacen Cali")
    )

    #Productos digitales
    catalogo.agregar_producto(
        producto_digital("Curso Python Pro", "CUR-PYT-101", 89.00, 100, 4500, "MP4", "https://descarga.com/curso-python", "Vitalicia")
    )
    catalogo.agregar_producto(
        producto_digital("E-book Machine Learning", "EBOOK-ML-102", 29.00, 200, 25, "PDF", "https://descarga.com/ebook-ml", "Permanente")
    )
    catalogo.agregar_producto(
        producto_digital("Pack Iconos Premium", "ICO-PRE-103", 15.00, 150, 180, "SVG", "https://descarga.com/iconos", "Comercial")
    )

    #Servicios
    catalogo.agregar_producto(
        servicio("Consultoria SEO", "SER-SEO-201", 200.00, 5, 3.0, "Ana Garcia", "2026-01-16")
    )
    catalogo.agregar_producto(
        servicio("Desarrollo Web", "SER-DEV-202", 500.00, 3, 8.0, "Carlos Lopez", "2026-01-20")
    )
    catalogo.agregar_producto(
        servicio("Mantenimiento IT", "SER-IT-203", 150.00, 8, 2.0, "Maria Rodriguez", "2026-02-01")
    )

    #Suscripciones
    catalogo.agregar_producto(
        suscripcion("Netflix Premium", "SUB-STR-301", 15.99, 1000, "mensual", True, ["4 pantallas", "Ultra HD", "Descargas"])
    )
    catalogo.agregar_producto(
        suscripcion("Spotify Family", "SUB-MUS-302", 24.99, 500, "mensual", True, ["6 cuentas", "sin anuncios", "Descargas"])
    )
    catalogo.agregar_producto(
        suscripcion("Adobe Creative Cloud", "SUB-DES-303", 52.99, 200, "mensual", True, ["Todas las apps", "Cloud Storage", "Updates"])
    )

    #Mostrar catalogo completo
    catalogo.mostrar_catalogo()

    #Aplicar descuentos de forma poliformica
    print("\n APLICANDO DESCUENTOS POLIMORFICOS")
    print("=" * 40)

    catalogo.productos[0].aplicar_descuento(10) # Laptop 10% off
    catalogo.productos[3].aplicar_descuento(20) # Curso python 20% off
    catalogo.productos[6].aplicar_descuento(15) # Consultoria SEO 15% off
    catalogo.productos[9].aplicar_descuento(5)  # Netflix 5% off

    #Calcular costos totaltes
    print("\n" + "=" * 50)
    catalogo.calcular_costos_totales()

    #Demostrar encapsulamiento
    print("\n DEMOSTRAR ENCAPSULAMIENTO")
    print("=" * 40)

    try:
        catalogo.productos[0].precio = -100
    except ValueError as e:
        print(f"Error al cambiar de precio: {e}")
        
    print("\n CAMBIOS DE STOCK:")
    catalogo.productos[1].stock = 3

if __name__ == "__main__":
    main()