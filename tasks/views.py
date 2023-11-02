from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaksForm, UsuarioForm, ProductoForm, ClienteForm , OrdenForm, ventaForm, CompraForm,TicketForm, IncidentesLaboralesForm, OpionionForm, HerramientaForm, ProveedorForm, ServicioForm, MantenimientoForm
from .models import Task, Usuario, Producto, Cliente, Orden, Venta,  Compra, Ticket, IncidenteLaboral, Opionion, Herramienta, Proveedor, Servicio, Mantenimiento, User
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from django.shortcuts import render
import os

from django.shortcuts import render
from django.http import HttpResponse
from .forms import RestoreForm  # Asumiendo que tienes un formulario para cargar el archivo de respaldo

from django.shortcuts import render
from django.http import HttpResponse
from .forms import RestoreForm  # Asegúrate de importar el formulario

from django.utils import timezone
from datetime import timedelta

 
 
def nosotros(request):
    return render(request, 'nosotros.html')

def home(request):
    cutoff_date = timezone.now() - timedelta(minutes=1)

    #total = Usuario.objects.filter(date_joined__gte=cutoff_date).count()
    #total = Usuario.objects.filter(tipo='Administrador').count()
    usr = Usuario.objects.latest('date_joined')
    newproduct = Producto.objects.filter(visto=False).count()
    newventa = Venta.objects.filter(visto=False).count()
    

    print(newproduct)
    print(newventa)
    
    #print(usr)
    return render(request, 'home.html',{
        #'total':total,
        'usr':usr,
        'newproduct':newproduct,
        'newventa':newventa
        
    })






def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })

    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                '''user = User.objects.create_user(username=request.POST['username'],
                                                password=request.POST['password1'])'''
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'], email=request.POST['email'])

                user.save()
                login(request, user)
                return redirect('tasks')
            except:
                return render(request, 'signup.html', {
                    "error": 'EL USUARIO YA EXISTE',
                    'form': UserCreationForm
                })
        return render(request, 'signup.html', {
            "error": 'LAS CONTRASEÑAS NO COINCIDEN',
            'form': UserCreationForm
        })

        

def signout(request):
    logout(request)
    return redirect(home)

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:

        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'EL USUARIO O CONTRASEÑA SON INCORRECTOS'
            })
        else:
            login(request, user)
            return redirect('home')

# Productos
@login_required
def productos(request):
    newventa = Venta.objects.filter(visto=False).count()
    newproduct = Producto.objects.filter(visto=False).count()
    print(newproduct)
    if request.user.is_superuser:
        productos = Producto.objects.all().order_by('nombre')
        
    else:
        
        #productos = Producto.objects.filter(user=request.user).order_by('nombre')
        productos = Producto.objects.all().order_by('nombre')

    return render(request, 'productos.html', {
        'productos': productos,
        'newproduct':newproduct,
        'newventa':newventa
    })

@login_required
def delete_productos(request,producto_id):
    if request.user.is_superuser:
        producto = get_object_or_404(Producto,pk=producto_id)
        producto.delete()
        return redirect('productos')
    else:
        producto = get_object_or_404(Producto, pk=producto_id, user=request.user)
        if request.method == 'POST':
            producto.delete()
            return redirect('productos')

@login_required
def producto_detail(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)

    # Verificar si el usuario es un superusuario
    if request.user.is_superuser:
        form = ProductoForm(instance=producto)
    else:
        # Si el usuario no es un superusuario, verificar si es el propietario del producto
        if producto.user != request.user:
            # Si el usuario no es el propietario, no tiene permiso para acceder a la vista
            return HttpResponseForbidden("No tienes permiso para acceder a esta página.")

        form = ProductoForm(instance=producto)

    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('productos')

    return render(request, 'producto_detail.html', {
        'producto': producto,
        'form': form
    })

@login_required
def create_productos(request):
    provedores = Proveedor.objects.all()
    if request.method == 'GET':
        return render(request, 'create_productos.html', {
            'form': ProductoForm,
            'provedores':provedores
        })
    else:
        try:
            form = ProductoForm(request.POST)
            new_product = form.save(commit=False)
            new_product.user = request.user
            new_product.save()
            return redirect('productos')
        except ValueError:
            return render(request, 'create_productos.html', {
                'form': ProductoForm,
                'error': 'Porfavor ingresar datos validos'
            })

# CHECAR ESTA FUNCION - que no esta leyendo objects.all()

@login_required
def ordenes(request):
    if request.user.is_superuser:
        # EDITAR PARA QUE SE VEAN SOLO LOS NOMBRES
        ordenes = Orden.objects.all().order_by('tipoOrden')
    else:
        
        ordenes = Orden.objects.filter(user=request.user).order_by('tipoOrden')

    return render(request,'ordenes.html',{
        'ordenes':ordenes,
    })

@login_required
def delete_ordenes(request,orden_id):
    if request.user.is_superuser:
        orden = get_object_or_404(Orden,pk=orden_id)
        orden.delete()
        return redirect('ordenes')
    else:
        orden = get_object_or_404(Orden,pk=orden_id,user=request.user)
        if request.method == 'POST':
            orden.delete()
            return redirect('ordenes')

@login_required
def orden_detail(request, orden_id):
    orden = get_object_or_404(Orden, pk = orden_id)

    if request.user.is_superuser:
        form = OrdenForm(instance=orden)
    else:
        if orden.user != request.user:
            return HttpResponseForbidden("No tienes permiso de acceder a esta pagina")
        
        form = OrdenForm(instance=orden)
    if request.method =='POST':
        form = OrdenForm(request.POST, instance=orden)
        if form.is_valid():
            form.save()
            return redirect('ordenes')
    
    return render ( request, 'orden_detail.html',{
        'orden': orden,
        'form':form
    })


@login_required
def create_orden(request):
    
    clientes = Cliente.objects.all()
    users = User.objects.all()
    provedores = Proveedor.objects.all()
    productos = Producto.objects.all()
    servicios = Servicio.objects.all()
    
    if request.method == 'GET':
        return render (request,'Create_ordenes.html',{
            'form':OrdenForm,
            'clientes':clientes,
            'users':users,
            'provedores':provedores,
            'productos':productos,
            'servicios':servicios

        })
    else:
        try:
            form = OrdenForm(request.POST)
            new_orden = form.save(commit=False)
            new_orden.user = request.user
            new_orden.save()
            return redirect('ordenes')
        except ValueError:
            return render(request,'create_ordenes.html',{
                'form':OrdenForm,
                'error':'Porfavor ingresa datos validos'
            })
# USER

@login_required
def users(request):
    usr = User.objects.all()
    if request.user.is_superuser:
        #users = Usuario.objects.all().order_by('usuario')
        usr = User.objects.all()
    else:


        #users = Usuario.objects.filter(user=request.user).order_by('nombre')
        usr = User.objects.all()

    return render(request, 'users.html', {
        #'users': users,
        'usr': usr
        
    })

@login_required
def delete_user(request,user_id):
    if request.user.is_superuser:
        user = get_object_or_404(Usuario, pk=user_id)
        user.delete()
        return redirect('users')
    else:
        user = get_object_or_404(Usuario, pk=user_id,user=request.user)
        if request.method == 'POST':
            user.delete()
            return redirect('users')

@login_required
def user_detail(request, user_id):
    user = get_object_or_404(Usuario, pk=user_id)
    print(user)
    if request.user.is_superuser:
        
        form = UsuarioForm(instance=user)

    else:

        if user.user != request.user:

            return HttpResponseForbidden("No tienes permiso para acceder a esta pagina")
        
        form = UsuarioForm(instance=user)
        
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('users')
        
    return render(request,'user_detail.html',{
        'user':user,
        'form':form
    })
  
@login_required
def create_user(request):
    
    if request.method == 'GET':
        return render(request, 'create_user.html', {
            'form': UsuarioForm
        })
    else:
        try:
            form = UsuarioForm(request.POST)
            new_user = form.save(commit=False)
            new_user.user = request.user
            new_user.save()
            return redirect('users')
        except ValueError:
            return render(request, 'create_user.html', {
                'form': UsuarioForm,
                'error': 'Porfavor ingresar datos validos'
            })



#CLIENTES

# Esta funcion sirve para ver todos los clientes si eres super usuario
@login_required
def clientes(request):
    if request.user.is_superuser:
        clientes = Cliente.objects.all().order_by('nombre')
    else:

        clientes = Cliente.objects.filter(user=request.user).order_by('nombre')
    
    return render(request, 'clientes.html', {
        'clientes': clientes,
    })


@login_required
def cliente_detail(request, cliente_id):
    cliente = get_object_or_404(Cliente, pk=cliente_id)
    
    if request.user.is_superuser:
        form = ClienteForm(instance=cliente)
        
    else:
        if cliente.user != request.user:
            return HttpResponseForbidden("No tienes permiso para acceder a esta página.")

        form = ClienteForm(instance=cliente)

    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)  # Pasar instance=cliente para actualizar el cliente existente
        if form.is_valid():
            form.save()
            return redirect('clientes')

    return render(request, 'cliente_detail.html', {
        'cliente': cliente,
        'form': form
    })


@login_required
def delete_clientes(request,cliente_id):
    if request.user.is_superuser:
        cliente = get_object_or_404(Cliente,pk=cliente_id)
        cliente.delete()
        return redirect('clientes')
    else:

        cliente = get_object_or_404(Cliente,pk=cliente_id,user=request.user)
        if request.method == 'POST':
            cliente.delete()
            return redirect('clientes')

@login_required
def create_cliente(request):
    if request.method == 'GET':
        return render(request, 'create_cliente.html', {
            'form': ClienteForm
        })
    else:
        try:
            form = ClienteForm(request.POST)
            new_cliente = form.save(commit=False)
            new_cliente.user = request.user
            new_cliente.save()
            return redirect('clientes')
        except ValueError:
            return render(request, 'create_cliente.html', {
                'form': ClienteForm,
                'error': 'Porfavor ingresar datos validos'
            })




#TAREAS
@login_required
def tasks(request):
        
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull =True)
    return render(request, 'tasks.html', {
        'tasks': tasks,

    })


@login_required
def create_task(request):
    users = Usuario.objects.all()  # Consulta la tabla de usuarios y obtén todos los usuarios
    if request.method == 'GET':
        form = TaksForm()  # Crea una instancia del formulario
        return render(request, 'create_task.html', {'form': form, 'users': users})
    elif request.method == 'POST':
        form = TaksForm(request.POST)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        else:
            return render(request, 'create_task.html', {'form': TaksForm(), 'error': 'Por favor ingresa datos válidos', 'users': users})
    else:
        return HttpResponse("Método no permitido")

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')

@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull =False).order_by('-datecompleted')
    return render(request, 'tasks.html', {
        'tasks': tasks,})
#Esta funcion es unica. 
@login_required    
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')



@login_required
def task_detail(request, task_id):
    
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaksForm(instance=task)

        return render(request, 'task_detail.html', {
            'task': task,
            'form': form
            })
    else:
        try:
                
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaksForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {
            'task': task,
            'form': form
            })

# VENTAS
@login_required
def ventas(request):
    newventa = Venta.objects.filter(visto=False).count()
    if request.user.is_superuser:
        # ARREGLAR LA ORDENACION
        ventas = Venta.objects.all()       

    else:    

        ventas = Venta.objects.filter(user=request.user).order_by('FechaVenta')
    return render(request, 'ventas.html', {
        'ventas': ventas,
        'newventa':newventa

    })



@login_required
def delete_ventas(request,venta_id):
    if request.user.is_superuser:
        venta = get_object_or_404(Venta,pk=venta_id)
        venta.delete()
        return redirect('ventas')
    else:
        venta = get_object_or_404(Venta, pk=venta_id, user=request.user)
        if request.method == 'POST':
            venta.delete()
            # checar funcionamiento de venta o ventas en la linea 260
            return redirect('ventas')

@login_required
def venta_detail(request, venta_id):
    venta = get_object_or_404(Venta, pk=venta_id)

    # Verificar si el usuario es un superusuario
    if request.user.is_superuser:
        form = ventaForm(instance=venta)
    else:
        # Si el usuario no es un superusuario, verificar si es el propietario del producto
        if venta.user != request.user:
            # Si el usuario no es el propietario, no tiene permiso para acceder a la vista
            return HttpResponseForbidden("No tienes permiso para acceder a esta página.")

        form = ventaForm(instance=venta)

    if request.method == 'POST':
        form = ventaForm(request.POST, instance=venta)
        if form.is_valid():
            form.save()
            return redirect('ventas')

    return render(request, 'venta_detail.html', {
        'venta': venta,
        'form': form
    })

@login_required
def create_ventas(request):
    clientes = Cliente.objects.all()
    users = User.objects.all()
    ordenes = Orden.objects.all()
    productos = Producto.objects.all()
    servicios = Servicio.objects.all()
    

    if request.method == 'GET':
        return render(request,  'create_ventas.html', {
            'form': ventaForm,
            'clientes':clientes,
            'users':users,
            'ordenes':ordenes,
            'productos':productos,
            'servicios':servicios,

        })
    else:
        try:
            form = ventaForm(request.POST)
            new_venta = form.save(commit=False)
            new_venta.user = request.user
            new_venta.save()
            return redirect('ventas')
        except ValueError:
            return render(request, 'create_ventas.html', {
                'form': ventaForm,
                'error': 'Porfavor ingresar datos validos'
            })
'''
@login_required
def detalleventas(request):
    if request.user.is_superuser:
        detalleventas = DetalleVenta.objects.all()
    else:

        detalleventas = DetalleVenta.objects.filter(user=request.user).order_by('cantidad')

    return render(request, 'detalleventas.html', {
        'detalleventas': detalleventas,
    })

@login_required
def delete_detalleventa(request,DetalleVenta_id):
    if request.user.is_superuser:
        detalleventa = get_object_or_404(DetalleVenta, pk=DetalleVenta_id)
        detalleventa.delete()
        return redirect('detalleventas')
    else:
        detalleventa = get_object_or_404(DetalleVenta, pk=DetalleVenta_id,user=request.user)
        if request.method == 'POST':
            detalleventa.delete()
            return redirect('detalleventas')

@login_required
def detalleventa_detail(request, DetalleVenta_id):
    detalleventa = get_object_or_404(DetalleVenta, pk=DetalleVenta_id)

    if request.user.is_superuser:
        
        form = DetalleVentaForm(instance=detalleventa)

    else:

        if detalleventa.user != request.user:

            return HttpResponseForbidden("No tienes permiso para acceder a esta pagina")
        
        form = DetalleVentaForm(instance=detalleventa)
        
    if request.method == 'POST':
        form = DetalleVentaForm(request.POST, instance=detalleventa)
        if form.is_valid():
            form.save()
            return redirect('detalleventas')
        
    return render(request,'detalleventa_detail.html',{
        'detalleventa':detalleventa,
        'form':form
    })



@login_required
def create_detalleventa(request):
    if request.method == 'GET':
        return render (request,'create_detalleventa.html',{
            'form':DetalleVentaForm
        })
    else:
        try:
            form = DetalleVentaForm(request.POST)
            new_detalleventa = form.save(commit=False)
            new_detalleventa.user = request.user
            new_detalleventa.save()
            return redirect('detalleventas')
        except ValueError:
            return render(request,'create_detalleventa.html',{
                'form':DetalleVentaForm,
                'error':'Porfavor ingresa datos validos'
            })

            '''
            
@login_required
def compras(request):
    if request.user.is_superuser:
        compras = Compra.objects.all()
        print(request.user)
    else:
        compras = Compra.objects.filter(user=request.user)

    return render(request,'compras.html',{
        'compras':compras,
    })

@login_required
def delete_compras(request,compra_id):
    if request.user.is_superuser:
        compra = get_object_or_404(Compra,pk=compra_id)
        compra.delete()
        return redirect('compras')
    else:
        compra = get_object_or_404(Compra,pk=compra_id,user=request.user)

        if request.method == 'POST':
            compra.delete()
            return redirect('compra')
        
@login_required
def compra_detail(request,compra_id):
    compra = get_object_or_404(Compra,pk=compra_id)

    if request.user.is_superuser:
        form = CompraForm(instance=compra)
    else:
        if compra.user != request.user:
            return HttpResponseForbidden(" No tienes permiso para acceder a esta pagina.")
        form = CompraForm(instance=compra)

    if request.method =='POST':
        form = CompraForm(request.POST, instance=compra)
        if form.is_valid():
            form.save()
            return redirect('compras')
    return render(request,'compra_detail.html',{
        'compra':compra,
        'form':form
    })

@login_required
def create_compras(request):
    ordenes =Orden.objects.all()
    provedores = Proveedor.objects.all()
    users = User.objects.all()
    productos = Producto.objects.all()

    if request.method == 'GET':
        return render(request,  'create_compras.html', {
            'form': CompraForm,
            'ordenes':ordenes,
            'provedores':provedores,
            'users':users,
            'productos':productos
        })
    else:
        try:
            form = CompraForm(request.POST)
            new_compra = form.save(commit=False)
            new_compra.user = request.user
            new_compra.save()
            return redirect('compras')
        except ValueError:
            return render(request, 'create_compras.html', {
                'form': CompraForm,
                'error': 'Porfavor ingresar datos validos'
            })

@login_required
def tickets(request):
    if request.user.is_superuser:
        tickets = Ticket.objects.all()
    else:
        tickets = Ticket.objects.all()

    return render(request, 'tickets.html', {
        'tickets': tickets,
    })


@login_required
def delete_ticket(request,ticket_id):
    if request.user.is_superuser:
        ticket = get_object_or_404(Ticket, pk=ticket_id)
        ticket.delete()
        return redirect('tickets')
    else:
        ticket = get_object_or_404(Ticket, pk=ticket_id,user=request.user)
        if request.method == 'POST':
            ticket.delete()
            return redirect('tickets')

@login_required
def ticket_detail(request,ticket_id):
    ticket = get_object_or_404(Ticket, pk = ticket_id)

    if request.user.is_superuser:
        form = TicketForm(instance=ticket)
    else:
        if ticket.user != request.user:
            return HttpResponseForbidden("No tienes permiso de acceder a esta pagina")
        
        form = TicketForm(instance=ticket)
    if request.method =='POST':
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('tickets')
    
    return render ( request, 'ticket_detail.html',{
        'ticket': ticket,
        'form':form
    })

@login_required
def create_ticket(request):
    users = Usuario.objects.all()  # Consulta la tabla de usuarios y obtén todos los usuarios
    clientes = Cliente.objects.all()
    if request.method == 'GET':
        return render (request,'create_ticket.html',{
            'form':TicketForm,
            'users':users,
            'clientes':clientes
        })
    else:
        try:
            form = TicketForm(request.POST)
            new_ticket = form.save(commit=False)
            new_ticket.user = request.user
            new_ticket.save()
            return redirect('tickets')
        except ValueError:
            return render(request,'create_ticket.html',{
                'form':TicketForm,
                'error':'Porfavor ingresa datos validos'
            })
    
@login_required
def incidenteslaborales(request):
    if request.user.is_superuser:
        incidenteslaborales = IncidenteLaboral.objects.all()
        print(request.user)
    else:
        incidenteslaborales = IncidenteLaboral.objects.filter(user=request.user)

    return render(request,'incidenteslaborales.html',{
        'incidenteslaborales':incidenteslaborales,
    })

@login_required
def delete_incidenteslaborales(request,incidenteslaborales_id):
    if request.user.is_superuser:
        IncidenteLaborales = get_object_or_404(IncidenteLaboral,pk=incidenteslaborales_id)
        IncidenteLaborales.delete()
        return redirect('incidenteslaborales')
    else:
        IncidenteLaborales = get_object_or_404(IncidenteLaboral,pk=incidenteslaborales_id,user=request.user)

        if request.method == 'POST':
            IncidenteLaborales.delete()
            return redirect('incidenteslaborales')

@login_required
def incidentelaboral_detail(request,incidenteslaborales_id):
    incidentelaboral = get_object_or_404(IncidenteLaboral,pk=incidenteslaborales_id)

    if request.user.is_superuser:
        form = IncidentesLaboralesForm(instance=incidentelaboral)
    else:
        if incidentelaboral.user != request.user:
            return HttpResponseForbidden(" No tienes permiso para acceder a esta pagina.")
        form = IncidentesLaboralesForm(instance=incidentelaboral)

    if request.method =='POST':
        form = IncidentesLaboralesForm(request.POST, instance=incidentelaboral)
        if form.is_valid():
            form.save()
            return redirect('incidenteslaborales')
    return render(request,'incidentelaboral_detail.html',{
        'incidentelaboral':incidentelaboral,
        'form':form
    })

@login_required
def create_incidenteslaborales(request):
    if request.method == 'GET':
        return render(request,  'create_incidenteslaborales.html', {
            'form': IncidentesLaboralesForm
        })
    else:
        try:
            form = IncidentesLaboralesForm(request.POST)
            new_incidentelaboral = form.save(commit=False)
            new_incidentelaboral.user = request.user
            new_incidentelaboral.save()
            return redirect('incidenteslaborales')
        except ValueError:
            return render(request, 'create_incidenteslaborales.html', {
                'form': IncidentesLaboralesForm,
                'error': 'Porfavor ingresar datos validos'
            })


@login_required
def opiniones(request):
    if request.user.is_superuser:
        opiniones = Opionion.objects.all()
    else:
        # checar como va a ser el filtro 
        opiniones = Opionion.objects.filter(user=request.user)
    
    return render(request, 'opiniones.html', {
        'opiniones': opiniones,
    })

@login_required
def opinion_detail(request, opinion_id):
    opinion = get_object_or_404(Opionion, pk=opinion_id)

    if request.user.is_superuser:
        form = OpionionForm(instance=opinion)
    else:
        if opinion.user != request.user:
            return HttpResponseForbidden("No tienes permiso para acceder a esta página.")

        form = OpionionForm(instance=opinion)

    if request.method == 'POST':
        form = OpionionForm(request.POST, instance=opinion)  # Pasar instance=cliente para actualizar el cliente existente
        if form.is_valid():
            form.save()
            return redirect('opiniones')

    return render(request, 'opinion_detail.html', {
        'opinion': opinion,
        'form': form
    })

@login_required
def delete_opiniones(request,opinion_id):
    if request.user.is_superuser:
        opinion = get_object_or_404(Opionion,pk=opinion_id)
        opinion.delete()
        return redirect('opiniones')
    else:

        opinion = get_object_or_404(Opionion,pk=opinion_id,user=request.user)
        if request.method == 'POST':
            opinion.delete()
            return redirect('opiniones')

@login_required
def create_opinion(request):
    if request.method == 'GET':
        return render(request, 'create_opinion.html', {
            'form': OpionionForm
        })
    else:
        try:
            form = OpionionForm(request.POST)
            new_opinion = form.save(commit=False)
            new_opinion.user = request.user
            new_opinion.save()
            return redirect('opiniones')
        except ValueError:
            return render(request, 'create_opinion.html', {
                'form': OpionionForm,
                'error': 'Porfavor ingresar datos validos'
            })

@login_required
def herramientas(request):
    
    if request.user.is_superuser:
        herramientas = Herramienta.objects.all().order_by('marca')
        
    else:

        #herramientas = Herramienta.objects.filter(user=request.user).order_by('marca')
        herramientas = Herramienta.objects.all()
    
    return render(request, 'herramientas.html', {
        'herramientas': herramientas,

    })

@login_required
def herramienta_detail(request, herramienta_id):
    herramienta = get_object_or_404(Herramienta, pk=herramienta_id)

    if request.user.is_superuser:
        form = HerramientaForm(instance=herramienta)
    else:
        if herramienta.user != request.user:
            return HttpResponseForbidden("No tienes permiso para acceder a esta página.")

        form = HerramientaForm(instance=herramienta)

    if request.method == 'POST':
        form = HerramientaForm(request.POST, instance=herramienta)  # Pasar instance=cliente para actualizar el cliente existente
        if form.is_valid():
            form.save()
            return redirect('herramientas')

    return render(request, 'herramienta_detail.html', {
        'herramienta': herramienta,
        'form': form
    })

@login_required
def delete_herramientas(request,herramienta_id):
    if request.user.is_superuser:
        Herramientas = get_object_or_404(Herramienta,pk=herramienta_id)
        Herramientas.delete()
        return redirect('herramientas')
    else:

        Herramientas = get_object_or_404(Herramienta,pk=herramienta_id,user=request.user)
        if request.method == 'POST':
            Herramientas.delete()
            return redirect('herramientas')

@login_required
def create_herramienta(request):
    if request.method == 'GET':
        return render(request, 'create_herramienta.html', {
            'form': HerramientaForm
        })
    else:
        try:
            form = HerramientaForm(request.POST)
            new_herramienta = form.save(commit=False)
            new_herramienta.user = request.user
            new_herramienta.save()
            return redirect('herramientas')
        except ValueError:
            return render(request, 'create_herramienta.html', {
                'form': HerramientaForm,
                'error': 'Porfavor ingresar datos validos'
            })

# PROVEEDORES
@login_required
def proveedores(request):
    if request.user.is_superuser:
        proveedores = Proveedor.objects.all()        
    else:

        proveedores = Proveedor.objects.all()
    
    return render(request, 'proveedores.html', {
        'proveedores': proveedores,
    })

@login_required
def proveedor_detail(request, proveedor_id):
    proveedor = get_object_or_404(Proveedor, pk=proveedor_id)

    if request.user.is_superuser:
        form = ProveedorForm(instance=proveedor)
    else:
        if proveedor.user != request.user:
            return HttpResponseForbidden("No tienes permiso para acceder a esta página.")

        form = ProveedorForm(instance=proveedor)

    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=proveedor)  # Pasar instance=cliente para actualizar el cliente existente
        if form.is_valid():
            form.save()
            return redirect('proveedores')

    return render(request, 'proveedores_detail.html', {
        'proveedor': proveedor,
        'form': form
    })

@login_required
def delete_proveedores(request,proveedor_id):
    if request.user.is_superuser:
        proveedor = get_object_or_404(Proveedor,pk=proveedor_id)
        proveedor.delete()
        return redirect('proveedores')
    else:

        proveedor = get_object_or_404(Proveedor,pk=proveedor_id,user=request.user)
        if request.method == 'POST':
            proveedor.delete()
            return redirect('proveedores')

@login_required
def create_proveedor(request):
    if request.method == 'GET':
        return render(request, 'create_proveedor.html', {
            'form': ProveedorForm
        })
    else:
        try:
            form = ProveedorForm(request.POST)
            new_proveedor = form.save(commit=False)
            new_proveedor.user = request.user
            new_proveedor.save()
            
            return redirect('proveedores')
        
        except ValueError:
            return render(request, 'create_proveedor.html', {
                'form': ProveedorForm,
                'error': 'Porfavor ingresar datos validos'
            })

@login_required
def servicio (request):
    if request.user.is_superuser:
        servicio = Servicio.objects.all()
        
    else:

        #servicio = Servicio.objects.filter(user=request.user).order_by('nombre')
        servicio = Servicio.objects.all()
    
    return render(request, 'servicio.html', {
        'servicio': servicio,
    })

@login_required
def create_servicio(request):
    if request.method == 'GET':
        return render(request, 'create_servicio.html', {
            'form': ServicioForm,
        })
    else:
        try:
            form = ServicioForm(request.POST)
            new_servicio = form.save(commit=False)
            new_servicio.user = request.user
            new_servicio.save()
            return redirect('servicio')
        except ValueError:
            return render(request, 'create_servicio.html', {
                'form': ServicioForm,
                'error': 'Porfavor ingresar datos validos'
            })

@login_required
def delete_servicio(request,servicio_id):
    if request.user.is_superuser:
        servicio = get_object_or_404(Servicio,pk=servicio_id)
        servicio.delete()
        return redirect('servicio')
    else:

        servicios = get_object_or_404(Servicios,pk=servicio_id,user=request.user)
        if request.method == 'POST':
            servicios.delete()
            return redirect('servicios')

@login_required
def servicio_detail(request, servicio_id):
    servicio = get_object_or_404(Servicio, pk=servicio_id)

    if request.user.is_superuser:
        form = ServicioForm(instance=servicio)
    else:
        if servicio.user != request.user:
            return HttpResponseForbidden("No tienes permiso para acceder a esta página.")

        form = ServicioForm(instance=servicio)

    if request.method == 'POST':
        form = ServicioForm(request.POST, instance=servicio)  # Pasar instance=cliente para actualizar el cliente existente
        if form.is_valid():
            form.save()
            return redirect('servicio')

    return render(request, 'servicios_detail.html', {
        'servicio': servicio,
        'form': form
    })
@login_required
def mantenimiento(request):
    
    if request.user.is_superuser:
        mantenimientos = Mantenimiento.objects.all()
    else:
        mantenimientos = Mantenimiento.objects.filter(user=request.user).order_by('responsable')
    
    return render(request, 'mantenimiento.html', {
        'mantenimientos': mantenimientos,
    })




@login_required
def create_mantenimiento(request):
    herramientas = Herramienta.objects.all()
    users = User.objects.all()
    if request.method == 'GET':
        return render(request, 'create_mantenimiento.html', {
            'form': MantenimientoForm,
            'herramientas':herramientas,
            'users':users
        })
    else:
        try:
            form = MantenimientoForm(request.POST)
            new_mantenimiento = form.save(commit=False)
            new_mantenimiento.user = request.user
            new_mantenimiento.save()
            return redirect('mantenimiento')
        except ValueError:
            return render(request, 'create_mantenimiento.html', {
                'form': MantenimientoForm,
                'error': 'Porfavor ingresar datos validos'
            })

@login_required
def delete_mantenimiento(request,mantenimiento_id):
    if request.user.is_superuser:
        mantenimiento = get_object_or_404(Mantenimiento,pk=mantenimiento_id)
        mantenimiento.delete()
        return redirect('mantenimiento')
    else:

        mantenimiento = get_object_or_404(Mantenimiento,pk=mantenimiento_id,user=request.user)
        if request.method == 'POST':
            servicios.delete()
            return redirect('mantenimiento')
    
@login_required
def mantenimiento_detail(request, mantenimiento_id):
    mantenimiento = get_object_or_404(Mantenimiento, pk=mantenimiento_id)

    if request.user.is_superuser:
        form = MantenimientoForm(instance=mantenimiento)
    else:
        if mantenimiento.user != request.user:
            return HttpResponseForbidden("No tienes permiso para acceder a esta página.")

        form = MantenimientoForm(instance=mantenimiento)

    if request.method == 'POST':
        form = MantenimientoForm(request.POST, instance=mantenimiento)  # Pasar instance=cliente para actualizar el cliente existente
        if form.is_valid():
            form.save()
            return redirect('mantenimiento')

    return render(request, 'mantenimiento_detail.html', {
        'mantenimiento': mantenimiento,
        'form': form
    })



def backup_database(request):
    # Ejecuta el comando de respaldo
    result = os.system('python manage.py backup_db')
    if result == 0:
        message = 'Respaldo exitoso.'
    else:
        message = 'Error al realizar el respaldo.'

    return render(request, 'respaldo.html', {'message': message})




import shutil
import io

from django.http import JsonResponse


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .forms import RestoreForm
# ...

def restore_database(request):
    if request.method == 'POST':
        form = RestoreForm(request.POST, request.FILES)
        if form.is_valid():
            backup_file = request.FILES['backup_file']
            backup_data = backup_file.read()  # Lee los datos del archivo

            # Guarda los datos del respaldo en el archivo de la base de datos
            with open('db.sqlite3', 'wb') as db_file:
                db_file.write(backup_data)

            #return render(request, 'home.html')
            #return HttpResponse("La base de datos se restauro correctamente")
            return JsonResponse({'message': 'La base de datos se restauró correctamente.'})

    else:
        form = RestoreForm()

    return render(request, 'restore.html', {'form': form})



from django.contrib.auth.views import PasswordResetView

def password_reset_view(request):
    return PasswordResetView.as_view()(request)




