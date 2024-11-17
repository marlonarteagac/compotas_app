import sqlite3

class Database:
    def __init__(self, db_path='dbp'):
        self.connection = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def commit(self):
        self.connection.commit()

    def close(self):
        self.connection.close()

class Producto(Database):
    def __init__(self, marca_p, precio_p):
        super().__init__()
        self.marca_p = marca_p
        self.precio_p = float(precio_p)

    def guardar(self):
        self.cursor.execute(
            "INSERT INTO productos (marca_p, precio_p) VALUES (?, ?)",
            (self.marca_p, self.precio_p)
        )
        self.commit()

#cargar todo a la pantalla de inicio
    @classmethod
    def obtener_todos(cls):
        # Conectar a la base de datos
        conexion = sqlite3.connect('dbp')
        cursor = conexion.cursor()
        
        # Ejecutar la consulta para obtener todos los productos
        cursor.execute("SELECT marca_p, precio_p FROM productos")
        productos = cursor.fetchall()
        
        # Cerrar la conexión a la base de datos
        conexion.close()
        
        # Convertir cada fila en una instancia de Producto
        lista_productos = [cls(marca_p, precio_p) for marca_p, precio_p in productos]
        return lista_productos

# Polimorfismo: una clase hija que hereda de Producto
class ProductoDescuento(Producto):
    def __init__(self, marca, precio, descuento):
        super().__init__(marca, precio)
        self.descuento = descuento

    def precio_final(self):
        return self.precio * (1 - self.descuento)
    
    
#modelo detalle de venta
class DetalleVenta(Database):
    def __init__(self, marca_p, cantidad):
        super().__init__()
        self.marca_p = marca_p
        self.cantidad = cantidad

    def guardar(self):
        self.cursor.execute(
            "INSERT INTO detalles_f (marca_p, cantidad) VALUES (?, ?)",
            (self.marca_p, self.cantidad)
        )
        self.commit()
        
        
#modelo para detalle de venta
class Venta(Database):
    def __init__(self, marca_p, cantidad):
        super().__init__()
        self.marca_p = marca_p
        self.cantidad = cantidad
        
        # Obtener el precio del producto seleccionado
        self.precio = self.obtener_precio_producto(marca_p)
        self.v_bruto = self.calcular_valor_bruto()
        self.v_neto = self.calcular_valor_neto()
        self.v_descuento = self.calcular_descuento()
        

    def obtener_precio_producto(self, marca_p):
        # Consulta el precio del producto por su marca
        self.cursor.execute("SELECT precio_p FROM productos WHERE marca_p = ?", (marca_p,))
        resultado = self.cursor.fetchone()
        return resultado[0] if resultado else 0

    def calcular_valor_bruto(self):
        # Valor bruto = precio * cantidad
        return self.precio * self.cantidad
    def calcular_descuento(self):
        # Valor bruto = precio * cantidad
        return self.v_bruto - self.v_neto  

    def calcular_valor_neto(self):
        # El valor neto puede ser el mismo que el bruto, o con un descuento, por ejemplo.
        # Si no hay descuento, el valor neto será igual al bruto.
        return self.v_bruto  # O puedes aplicar un cálculo adicional aquí si lo deseas

    def guardar(self):
        # Inserta el detalle de la venta en la tabla detalles_f
        self.cursor.execute(
            "INSERT INTO detalles_f (marca_p, cantidad, v_bruto, v_neto) VALUES (?, ?, ?, ?)",
            (self.marca_p, self.cantidad, self.v_bruto, self.v_neto)
        )
        self.commit()

#clase que hereda de Venta
class VentaConDescuento(Venta):
    def calcular_valor_neto(self):
        # Aplicar descuento basado en la marca y la cantidad
        if self.marca_p.lower() == "emma":
            if self.cantidad < 100:
                descuento = 0.20  # 20% de descuento
            elif 100 <= self.cantidad <= 200:
                descuento = 0.30  # 30% de descuento
            else:
                descuento = 0.40  # 40% de descuento
        else:
            # Si no es "Emma", no se aplica descuento
            descuento = 0

        # Valor neto con el descuento aplicado
        return self.v_bruto * (1 - descuento)
