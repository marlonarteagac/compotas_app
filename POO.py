# CREAMOS LA CLASE COMPOTAS


# ESTA ES LA CLASE PADRE
class Producto():
    def __init__(self, name, price):
        self.name = name
        self.price = price
# CREAMOS EL METODO DE LA CLASE COMPOTAS
    def calcular_descuento(self):
        print('soy el descuento')


# SOLICITO INFORMACION AL USUARIO PARA CREAR COMPOTA
name_compota = input('ingrese el nombre de la compota:\n')
price_compota = int(input('ingrese el valor de la compota:\n'))

# CREAMOS LAS SUBCLASE O CLASE HIJA QUE HERADA DE LA PRINCIPAL O PADRE
class Compota(Producto):
    def __init__(self,name,price):
        super().__init__(name, price)
        
    def calcular_descuento(self, cantidad):
        
print(f'soy la compota: {name_compota} y mi precio es {price_compota}')


compota1 = Compota(name_compota, price_compota)
compota1.calcular_descuento()

