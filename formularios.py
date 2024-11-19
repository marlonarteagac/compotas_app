from flask_wtf import FlaskForm
from wtforms import FloatField, IntegerField, SelectField, SelectMultipleField, StringField, DecimalField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class ProductoForm(FlaskForm):
    marca = StringField('Marca', validators=[DataRequired()])
    precio = DecimalField('Precio', validators=[
                          DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Crear Producto')


class VentaForm(FlaskForm):
    # Combobox para seleccionar el producto (marca)
    producto = SelectField('Producto', coerce=str,
                           choices=[], validators=[DataRequired()])
    cantidad = IntegerField('Cantidad', validators=[DataRequired()])
    submit = SubmitField('Realizar Venta')


class FacturaForm(FlaskForm):
    detalles = SelectMultipleField(
        'Detalles de Factura', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Agregar a la Factura')
