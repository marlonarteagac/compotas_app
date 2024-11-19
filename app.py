from flask import Flask, render_template, redirect, url_for, flash
from modelo import Factura, Producto, TipoTercero, Venta, VentaConDescuento
from formularios import FacturaForm, ProductoForm, TipoTerceroForm, VentaForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mi_secreto'

#modulo para vel inicio

@app.route('/')
def index():
    productos = Producto.obtener_todos()
    return render_template('index.html', productos=productos)


#modulo para mostrar los el producto creados
@app.route('/crear', methods=['GET', 'POST'])
def crear_producto():
    form = ProductoForm()
    if form.validate_on_submit():
        # Crear un producto estándar o con descuento según algún criterio
        producto = Producto(form.marca.data, form.precio.data)
        producto.guardar()
        flash('Producto creado con éxito', 'success')
        return redirect(url_for('crear_producto'))
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
        if form.producto.data.lower() == "rostington":
            venta = VentaConDescuento(form.producto.data, form.cantidad.data)
        elif form.producto.data.lower() == "premiere":
            venta = VentaConDescuento(form.producto.data, form.cantidad.data)
        else:
            venta = Venta(form.producto.data, form.cantidad.data)

        venta.guardar()
        flash(f'Venta realizada con éxito: {venta.marca_p}, Cantidad: {venta.cantidad},Valor Bruto: {venta.v_bruto}, Descuento: {venta.v_descuento} Valor Neto: {venta.v_neto},', 'success')
        return redirect(url_for('vender_producto'))

    return render_template('vender_producto.html', form=form)

@app.route('/ventas', methods=['GET', 'POST'])
def nueva_factura():
    factura = Factura()
    detalles_disponibles = factura.obtener_detalles_disponibles()
    # Preparar las opciones para el campo de selección
    opciones = [(detalle[0], f"{detalle[1]} - Cantidad: {detalle[2]}, Valor: {detalle[3]}") for detalle in detalles_disponibles]

    form = FacturaForm()
    form.detalles.choices = opciones  # Pasar opciones al formulario

    if form.validate_on_submit():
        detalles_seleccionados = form.detalles.data
        nueva_factura = Factura(id_df=detalles_seleccionados)
        nueva_factura.guardar()
        return redirect(url_for('listar_facturas'))

    return render_template('ventas.html', form=form)

#mostrar las facturas
@app.route('/facturas')
def listar_facturas():
    factura = Factura()
    facturas = factura.obtener_facturas()
    total = Factura.calcular_total(facturas)
    return render_template('facturas.html', facturas=facturas, total=total)


@app.route('/crear-tipo-tercero', methods=['GET', 'POST'])
def crear_tipo_tercero():
    tipos_terceros = TipoTercero.obtener_todos()
    form = TipoTerceroForm()
    if form.validate_on_submit():
        tipo = TipoTercero(tipo=form.tipo.data)
        tipo.guardar()
        flash('Tipo de Tercero creado con éxito', 'success')
        return redirect(url_for('crear_tipo_tercero'))
    return render_template('crear_tipo_tercero.html', form=form, tipos_terceros=tipos_terceros)











if __name__ == '__main__':
    app.run(debug=True)

