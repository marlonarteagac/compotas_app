import sqlite3
from dataclasses import dataclass, field

# Clase para gestionar la conexión con la base de datos
class Database:
    def __init__(self, db_path='dbp'):
        self.db_path = db_path

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
        self.cursor = self.connection.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.connection.commit()
        self.connection.close()

# Modelo Producto
@dataclass
class Producto:
    marca_p: str
    precio_p: float

    def guardar(self):
        with Database() as db:
            db.cursor.execute(
                "INSERT INTO productos (marca_p, precio_p) VALUES (?, ?)",
                (self.marca_p, self.precio_p))
            

#cargar todo a la pantalla de inicio
    @classmethod
    def obtener_todos(cls):
        with Database() as db:
            db.cursor.execute("SELECT marca_p, precio_p FROM productos")
            productos = db.cursor.fetchall()
            return [cls(marca_p, precio_p) for marca_p, precio_p in productos]

# Modelo Venta
@dataclass
class Venta:
    marca_p: str
    cantidad: int
    precio: float = field(init=False)
    v_bruto: float = field(init=False)
    v_neto: float = field(init=False)
    v_descuento: float = field(init=False)

    def __post_init__(self):
        self.precio = self.obtener_precio_producto()
        self.v_bruto = self.calcular_valor_bruto()
        self.v_descuento = self.calcular_descuento()
        self.v_neto = self.v_bruto - self.v_descuento

    def obtener_precio_producto(self):
        with Database() as db:
            db.cursor.execute("SELECT precio_p FROM productos WHERE marca_p = ?", (self.marca_p,))
            resultado = db.cursor.fetchone()
            return resultado[0] if resultado else 0

    def calcular_valor_bruto(self):
        return self.precio * self.cantidad

    def calcular_descuento(self):
        # Puedes personalizar esta función para aplicar descuentos específicos
        return 0

    def guardar(self):
        with Database() as db:
            db.cursor.execute(
                "INSERT INTO detalles_f (marca_p, cantidad, v_bruto, v_neto) VALUES (?, ?, ?, ?)",
                (self.marca_p, self.cantidad, self.v_bruto, self.v_neto)
            )

# Clase Venta con Descuento
class VentaConDescuento(Venta):
    def calcular_descuento(self):
        descuento = 0
        if self.marca_p.lower() == "emma":
            if self.cantidad < 100:
                descuento = 0.20  # 20% de descuento
            elif 100 <= self.cantidad <= 200:
                descuento = 0.30  # 30% de descuento
            else:
                descuento = 0.40  # 40% de descuento
        return self.v_bruto * descuento

