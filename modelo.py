import sqlite3


class Database:
    def __init__(self, db_path='DB\dbp'):
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
            (self.marca_p, float(self.precio_p))
        )
        self.commit()

# cargar todo a la pantalla de inicio
    @classmethod
    def obtener_todos(cls):
        # Conectar a la base de datos
        conexion = sqlite3.connect('DB\dbp')
        cursor = conexion.cursor()

        # Ejecutar la consulta para obtener todos los produ ctos
        cursor.execute("SELECT marca_p, precio_p FROM productos")
        productos = cursor.fetchall()

        # Cerrar la conexión a la base de datos
        conexion.close()

        # Convertir cada fila en una instancia de Producto
        lista_productos = [cls(marca_p, precio_p)
                           for marca_p, precio_p in productos]
        return lista_productos

# Polimorfismo: una clase hija que hereda de Producto


class ProductoDescuento(Producto):
    def __init__(self, marca, precio, descuento):
        super().__init__(marca, precio)
        self.descuento = descuento

    def precio_final(self):
        return self.precio * (1 - self.descuento)


# modelo detalle de venta
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


# modelo para detalle de venta
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
        self.cursor.execute(
            "SELECT precio_p FROM productos WHERE marca_p = ?", (marca_p,))
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
            "INSERT INTO detalles_f (marca_p, cantidad, v_bruto, v_descuento, v_neto) VALUES (?, ?, ?, ?, ?)",
            (self.marca_p, self.cantidad, self.v_bruto, self.v_descuento, self.v_neto)
        )   
        self.commit()

# clase que hereda de Venta


class VentaConDescuento(Venta):
    def calcular_valor_neto(self):
        # Aplicar descuento basado en la marca y la cantidad
        # descuentos para rostington
        if self.marca_p.lower() == "rostington":
            if self.cantidad < 100:
                descuento = 0.20  # 20% de descuento
            elif 100 <= self.cantidad <= 200:
                descuento = 0.25  # 25% de descuento
            else:
                descuento = 0.45  # 45% de descuento
        # descuentos por rostington
        elif self.marca_p.lower() == "premiere":
            if self.cantidad < 100:
                descuento = 0.15  # 15% de descuento
            elif 100 <= self.cantidad <= 200:
                descuento = 0.35  # 30% de descuento
            else:
                descuento = 0.50  # 40% de descuento
        else:
            # Si no es rostington o premiere, no se aplica descuento
            descuento = 0

    # Valor neto con el descuento aplicado
        return self.v_bruto * (1 - descuento)

# facturacion


class Factura(Database):
    def __init__(self, id_df=None):
        super().__init__()
        self.id_df = id_df

    def guardar(self):
        # Insertar una nueva factura y obtener el ID generado
        self.cursor.execute("INSERT INTO facturas DEFAULT VALUES")
        factura_id = self.cursor.lastrowid
        # Asociar los detalles de factura seleccionados a esta factura
        for detalle_id in self.id_df:
            self.cursor.execute(
                "UPDATE facturas SET id_df = ? WHERE id_fc = ?",
                (detalle_id, factura_id)
            )
        self.commit()

    def obtener_facturas(self):
        # Obtener todas las facturas y sus detalles
        self.cursor.execute("""
                            SELECT 
                            f.id_fc AS factura_id,
                            f.id_df AS detalle_factura_id,
                            d.marca_p AS producto,
                            d.cantidad,
                            d.v_bruto AS valor_bruto,
							d.v_descuento as descuento,
                            d.v_neto AS valor_neto
							
                            FROM 
                            facturas f
                            JOIN 
                            detalles_f d ON f.id_df = d.id_df;
        """)
        facturas = self.cursor.fetchall()
        return facturas

    @staticmethod
    def calcular_total(facturas):
        # Calcular el total de todas las facturas
        # f[46] es el valor neto de cada detalle
        total = sum(f[6] for f in facturas)
        return total

    def obtener_detalles_disponibles(self):
        # Obtener detalles disponibles para asociar a una factura
        self.cursor.execute("""
            SELECT * from detalles_f
        """)
        detalles = self.cursor.fetchall()
        return detalles
