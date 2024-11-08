
# 1. La creación de una clase, de un objeto, de un método y el concepto de herencia y polimorfismo

#DEFINIMOS LA CLASE Y SUS METODOS
class Compotas():
    def __init__(self, nombre, precio):
        self.nombre = nombre
        self.precio = precio
#CREAMOS EL METODO DE LA CLASE COMPOTAS
    def calcular_descuento(self):
        #logica para calcular el descuento
        print(f"la compota es: {self.nombre} y su precio es: {self.precio}")

#SOLICITO INFORMACION AL USUARIO PARA CREAR COMPOTA

name_compota = input("Ingrese el nombre de la compota")
price_compota = int(input("Ingrese el valor de la compota"))

#HAGO INSTANCIA DE CLASE COMPOTA PARA CREAR UNA CON LOS DATOS INGRESADOR POR EL USER
compota1 = Compotas(name_compota, price_compota)

#IMPRIMO EL METODO QUE TIENE LA CLASE COMPOTAS
print(compota1.calcular_descuento())