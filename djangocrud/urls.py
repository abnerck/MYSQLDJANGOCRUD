"""
URL configuration for djangocrud project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tasks import views

from django.urls import path
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home, name='home'),
    path('nosotros/',views.nosotros,name='nosotros'),
    path('signup/',views.signup,name='signup'),
    
    
    
    
    path('users/',views.users,name='users'),
    path('clientes/',views.clientes,name='clientes'),
    path('productos/',views.productos,name='productos'),
    path('ordenes/',views.ordenes,name='ordenes'),
    path('ventas/',views.ventas,name='ventas'),
    path('compras/',views.compras,name='compras'),
    path('tickets/',views.tickets,name='tickets'),
    path('opiniones/',views.opiniones,name='opiniones'),
    path('servicio/',views.servicio,name='servicio'),
    path('mantenimiento/',views.mantenimiento,name='mantenimiento'),
    path('proveedores/',views.proveedores,name='proveedores'),
    path('herramientas/',views.herramientas,name='herramientas'),
    #path('detalleventas/',views.detalleventas,name='detalleventas'),
    path('incidenteslaborales/',views.incidenteslaborales,name='incidenteslaborales'),
    path('logout/',views.signout,name='logout'),
    path('signin/',views.signin,name='signin'),
    
    # TAREAS 
    path('tasks/',views.tasks,name='tasks'),
    path('tasks/<int:task_id>/', views.task_detail,name='task_detail'),
    path('tasks/<int:task_id>/complete', views.complete_task, name='complete_task'),
    path('tasks/<int:task_id>/delete', views.delete_task, name='delete_task'),
    path('tasks_completed/', views.tasks_completed, name='tasks_completed'),
    
    path('tasks/create/', views.create_task,name='create_task'),

    # USUARIOS
    path('users/create/', views.create_user,name='create_user'),
    path('users/<int:user_id>/', views.user_detail,name='user_detail'),
    path('users/<int:user_id>/delete', views.delete_user, name='delete_users'),
    
    # PRODUCTOS 
    path('productos/create/', views.create_productos,name='create_productos'),
    path('productos/<int:producto_id>/', views.producto_detail,name='producto_detail'),
    path('productos/<int:producto_id>/delete', views.delete_productos, name='delete_productos'),

    #ORDENES
    path('ordenes/create/', views.create_orden,name='create_ordenes'),
    path('ordenes/<int:orden_id>/', views.orden_detail,name='orden_detail'),
    path('ordenes/<int:orden_id>/delete',views.delete_ordenes,name='delete_ordenes'),

    #ventas
    path('ventas/create/', views.create_ventas,name='create_ventas'),
    path('ventas/<int:venta_id>/', views.venta_detail,name='venta_detail'),
    path('ventas/<int:venta_id>/delete',views.delete_ventas,name='delete_ventas'),
    
    #cliente-cliente_detail,create_cliente
    #COMPRAS
    path('compras/create/', views.create_compras,name='create_compras'),
    path('compras/<int:compra_id>/', views.compra_detail,name='compra_detail'),
    path('compras/<int:compra_id>/delete',views.delete_compras,name='delete_compras'),
    
    
    #Detalle Ventas
    #path('detalleventas/create/', views.create_detalleventa,name='create_detalleventa'),
    #path('detalleventas/<int:DetalleVenta_id>/', views.detalleventa_detail,name='detalleventa_detail'),
    #path('detalleventas/<int:DetalleVenta_id>/delete',views.delete_detalleventa,name='delete_detalleventa'),
    
    
    # CLIENTES 

    path('clientes/create/', views.create_cliente,name='create_cliente'),
    path('clientes/<int:cliente_id>/', views.cliente_detail,name='cliente_detail'),
    path('clientes/<int:cliente_id>/delete', views.delete_clientes, name='delete_cliente'),

    # TICKETS
    path('tickets/create/', views.create_ticket,name='create_ticket'),
    path('tickets/<int:ticket_id>/', views.ticket_detail,name='ticket_detail'),
    path('tickets/<int:ticket_id>/delete', views.delete_ticket, name='delete_ticket'),

    #Incidentes laborales
    # No puedo ver los detalles de los incidentes... de ahi en fuera creeo que ya esta bien.

    path('incidenteslaborales/create/', views.create_incidenteslaborales,name='create_incidenteslaborales'),
    path('incidenteslaborales/<int:incidenteslaborales_id>/', views.incidentelaboral_detail,name='incidentelaboral_detail'),
    path('incidenteslaborales/<int:incidenteslaborales_id>/delete', views.delete_incidenteslaborales, name='delete_incidenteslaborales'),
    
    #OpinionesQuejas
    path('opiniones/create/', views.create_opinion,name='create_opinion'),
    path('opiniones/<int:opinion_id>/', views.opinion_detail,name='opinion_detail'),
    path('opiniones/<int:opinion_id>/delete', views.delete_opiniones, name='delete_opiniones'),

    # HERRAMIENTAS
    path('herramientas/create/', views.create_herramienta,name='create_herramienta'),
    path('herramientas/<int:herramienta_id>/', views.herramienta_detail,name='herramienta_detail'),
    path('herramientas/<int:herramienta_id>/delete', views.delete_herramientas, name='delete_herramientas'),

    #Proveedores

    path('proveedores/create/', views.create_proveedor,name='create_proveedor'),
    path('proveedores/<int:proveedor_id>/', views.proveedor_detail,name='proveedor_detail'),
    path('proveedores/<int:proveedor_id>/delete', views.delete_proveedores, name='delete_proveedores'),

    #Servicios
    path('servicio/create/', views.create_servicio,name='create_servicio'),
    path('servicio/<int:servicio_id>/', views.servicio_detail,name='servicio_detail'),
    path('servicio/<int:servicio_id>/delete', views.delete_servicio, name='delete_servicio'),

    # MANTENIMIENTO
    path('mantenimiento/create/', views.create_mantenimiento,name='create_mantenimiento'),
    path('mantenimiento/<int:mantenimiento_id>/', views.mantenimiento_detail,name='mantenimiento_detail'),
    path('mantenimiento/<int:mantenimiento_id>/delete', views.delete_mantenimiento, name='delete_mantenimiento'),

    path('respaldo/', views.backup_database, name='respaldo'),
    path('restore/', views.restore_database, name='restore'),

    path('reset_password/', views.password_reset_view, name='password_reset'),
    
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),

    # Vista para mostrar un mensaje de confirmación después de enviar el correo de restablecimiento
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),

    # Vista para restablecer la contraseña después de hacer clic en el enlace del correo
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    # Vista para mostrar un mensaje de confirmación después de restablecer la contraseña
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),




]
