from flask import Flask, render_template, redirect, url_for, flash
from modelo import Producto, Venta, VentaConDescuento
from formularios import ProductoForm, VentaForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mi_secreto'

#modulo para vel inicio

@app.route('/')
def index():
    productos = Producto.obtener_todos()
    return render_template('index.html', productos=productos)


#modulo para crear el producto
@app.route('/crear', methods=['GET', 'POST'])
def crear_producto():
    form = ProductoForm()
    if form.validate_on_submit():
        # Crear un producto estándar o con descuento según algún criterio
        producto = Producto(form.marca.data, form.precio.data)
        producto.guardar()
        flash('Producto creado con éxito', 'success')
        return redirect(url_for('index'))
    return render_template('crear_producto.html', form=form)


#modulo para vender el producto
@app.route('/vender', methods=['GET', 'POST'])
def vender_producto():
    form = VentaForm()
    
    # Cargar los productos en el combobox
    productos = Producto.obtener_todos()
    form.producto.choices = [(producto.marca_p, producto.marca_p) for producto in productos]  # (marca, marca)

    if form.validate_on_submit():
        # Usar la clase correcta basada en la marca
        if form.producto.data.lower() == "emma":
            venta = VentaConDescuento(form.producto.data, form.cantidad.data)
        else:
            venta = Venta(form.producto.data, form.cantidad.data)

        venta.guardar()
        flash(f'Venta realizada con éxito: {venta.marca_p}, Cantidad: {venta.cantidad},Valor Bruto: {venta.v_bruto}, Descuento: {venta.v_descuento} Valor Neto: {venta.v_neto},', 'success')
        return redirect(url_for('index'))

    return render_template('vender_producto.html', form=form)

















if __name__ == '__main__':
    app.run(debug=True)

