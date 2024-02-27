from django.forms import ModelForm
from .models import Task, Usuario, Producto, Cliente,Orden,Venta,Compra,Ticket,IncidenteLaboral, Opionion,Herramienta,Proveedor , Servicio ,Mantenimiento

class TaksForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description','important','estadotarea','NotasTarea','Comentarios',]
        labels ={
            'title': 'Nombre de la tarea',
            'description' : 'Descripcion',
            'important': 'Es importante',
            'estadotarea':'Estado de la tarea',
            'NotasTarea':'Notas de tarea'
        }

class UsuarioForm(ModelForm):
    class Meta:
        model = Usuario
        fields = ['usuario','tipo','nombre','apellido','correo','telefono',]
        

class ProductoForm(ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre','descripcion','categoria','precioComun','precioMayoreo','canStock','tamaño','material','tiempodeProduccion','estado','visto','idProveedor',]
        #fields = ['nombre','descripcion','categoria','precioComun','precioMayoreo','canStock','tamaño','material','tiempodeProduccion',]
        labels = {
            'precioComun':'Precio Comun',
            'precioMayoreo':'Precio mayoreo',
            'canStock':'Cantidad en stock',
            'fechaingreso':'Fecha de Ingreso',
            'tiempodeProduccion':'Tiempo de produccion',
            'idProveedor':'Proveedor'
        }
        
class ClienteForm(ModelForm):
    class Meta:
        model = Cliente
        #Checar el campo fechanacimiento que quite. 
        fields = ['nombre','paterno','materno','tipocliente','fechanacimiento','correo','celular','referencias','direccion',]
        labels = { 
            'fechanacimiento':'Fecha de nacimiento',
            'tipocliente':'Tipo de cliente'
            }

class OrdenForm(ModelForm):
    class Meta:
        model = Orden
        fields = ['tipoOrden','descripcion','totalOrden','idCliente','idEmpleado','idProveedor',
        'idProducto','idServicio','cantidadProductos','precioUnitarioProducto',
        'subtotalProductos','cantidadServicios','precioUnitarioServicios','subtotalServicio',]
                  
        labels = {
            'tipoOrden':'Tipo de orden',
            'descripcion':'Descripcion',
            'totalOrden':'Total orden',
            'idCliente':'Cliente',
            'idEmpleado':'Empleado',
            'idProveedor':'Proveedor',            
            'idProducto':'Producto',
            'idServicio':'Servicio',
            'cantidadProductos':'Cantidad de producto',
            'precioUnitarioProducto':'Precio por producto',
            'subtotalProductos':'Subtotal productos',
            'cantidadServicios':'Cantidad de servicios',
            'precioUnitarioServicios':'Precio por servicio',
            'subtotalServicio':'subtotal servicios'

        }


class ventaForm(ModelForm):
    class Meta:
        model = Venta

        #fields = ['descripcion','idOrden','totalVenta','idCliente','idEmpleado','estado']
        #fields = ['descripcion','totalVenta','idCliente','idEmpleado','estado','producto','cantidad','servicio','cantidadservicio']
        fields = ['producto','cantidad','servicio','cantidadservicio','descripcion','estado','idCliente','visto']
        labels = {
            'descripcion':'Descripcion',
            'idOrden':'Orden',
            'totalVenta':'Total venta',
            'idCliente':'Cliente',
            'idEmpleado':'Empleado'
        }
        
'''
class DetalleVentaForm(ModelForm):
    class Meta:
        model = DetalleVenta

        #fields = ['idVenta','idProducto','cantidad','precioUnitario','totalDetalle']
        fields = ['cantidad','precioUnitario','totalDetalle']
        labels = {
            'idVenta':'Venta',
            'idProducto':'Producto',
            'cantidad':'Cantidad',
            'preciounitario':'Precio',
            'totalDetalle':'Total'
        }
'''

class CompraForm(ModelForm):
    class Meta:
        model = Compra

        #fields = ['totalCompra','idOrden','idProveedor','idEmpleado','idProducto','idProducto']
        fields = ['idProveedor','idProducto','cantidad',]
        labels = {
            'totalCompra':'Total',
            'idOrden':'Orden',
            'idProveedor':'Proveedor',
            'idEmpleado':'Empleado',
            'idProducto':'Producto'
        }

class TicketForm(ModelForm):
    class Meta:
        model = Ticket

        fields = ['fechaCreacion','asunto','descripcion','idCliente','idEmpleado','estadoTicket']
        labels = {
            'fechaCreacion':'Fecha',
            'asunto':'Asunto',
            'descripcion':'Descripcion',
            'idCliente':'Cliente',
            'idEmpleado':'Empleado',
            'estadoTicket':'Estado de ticket'
        }

class IncidentesLaboralesForm(ModelForm):
    class Meta:
        model = IncidenteLaboral

        fields = ['horaIncidente','descripcion','tipoIncidente','accionesCorrectivas','comentarios']
        #fields = ['horaIncidente','descripcion','reportadopor','tipoIncidente','accionesCorrectivas','comentarios']
        labels = {
            'horaIncidente':'Hora del incidente',
            'HoraIncidente':'Hora de incidente',
            'descripcion':'Descripción',
            'reportadopor':'Reportado Por',
            'tipoIncidente':'Tipo incidente',
            'accionesCorrectivas':'Acciones correctivas',
            'comentarios':'Comentarios'
        }


class OpionionForm(ModelForm):
    class Meta:
        model = Opionion

        fields = ['Correo','tipo','descripcion','calificacion']
        labels = {
            'Correo':'Correo',
            'FechaRegistro':'Fecha de registro',
            'tipo':'Tipo',
            'descripcion':'Descripcion',
            'calificacion':'Calificacion'
        }

class HerramientaForm(ModelForm):
    class Meta:
        model = Herramienta

        fields = ['nombreHerramienta','tipo','marca','fechaAdquisicion','idProveedor','estadoHerramienta','valor','notas']
        labels = {
            'nombreHerramienta':'Nombre herramienta',
            'marca':'Marca',
            'fechaAdquisicion':'Fecha adquisicion',
            'proveedor':'Proveedor',
            'estadoHerramienta':'Estado de la herramienta',
            'valor':'Valor',
            'notas':'Notas',
            'idProveedor':'Proveedor'
        }

class ProveedorForm(ModelForm):
    class Meta:
        model = Proveedor

        #fields = ['nombre','correo','telefono','estadodelprovedor','productos',]
        fields = ['nombre','correo','telefono','estadodelprovedor',]
        labels = {
            'nombre':'Nombre',
            'correo':'Correo',
            'telefono':'Telefono',
            'estadodelprovedor':'Estado del proveedor'
        }

class ServicioForm(ModelForm):
    class Meta:

        model = Servicio
    
        fields = ['nombre','descripcion', 'precio','tiempoestimado','categoria','notas','estadoServicio']
        labels = {
            'nombre':'Nombre',
            'descripcion':'Descripcion',
            'precio':'Precio',
            
            'tiempoestimado':'Tiempo estimado',
            'categoria':'Categoria',
            'notas':'Notas',
            'estadoServicio':'Estado servicio'
        }
        

class MantenimientoForm(ModelForm):
    class Meta:
        model = Mantenimiento

        fields = ['idHerramienta','fechaMantenimineto','tipoMantenimiento','detalles','costo','responsable',]
        labels = {
            'idHerramienta':'Herramientas',
            'fechaMantenimineto':'Fecha de mantenimiento',
            'tipoMantenimiento':'Tipo mantenimiento',
            'detalles':'Detalles',
            'costo':'Costo',
            'responsable':'Responsable'
        }


from django import forms

class RestoreForm(forms.Form):
    backup_file = forms.FileField(label='Archivo de Respaldo')
