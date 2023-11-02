from django.contrib import admin
from .models import Task
from .models import Usuario,Producto, Proveedor,Cliente,Orden,Venta,Compra,Ticket,IncidenteLaboral,Opionion,Herramienta,Servicio #,Mantenimiento
# Register your models here.

#####################################################
class TaskAdmin (admin.ModelAdmin):
    readonly_fields=("created",)

admin.site.register(Task,TaskAdmin)

#####################################################
class UsuarioAdmin(admin.ModelAdmin):
    readonly_fields=("tipo",)

admin.site.register(Usuario,UsuarioAdmin)


#####################################################
class UsuarioAdmin(admin.ModelAdmin):
    readonly_fields=("nombre",)

admin.site.register(Producto,UsuarioAdmin)



#####################################################
class UsuarioAdmin(admin.ModelAdmin):
    readonly_fields=("nombre",)

admin.site.register(Proveedor,UsuarioAdmin)



#####################################################
class UsuarioAdmin(admin.ModelAdmin):
    readonly_fields=("nombre",)

admin.site.register(Cliente,UsuarioAdmin)



#####################################################


#####################################################
class UsuarioAdmin(admin.ModelAdmin):
    readonly_fields=("tipoOrden",)

admin.site.register(Orden,UsuarioAdmin)


#####################################################
class UsuarioAdmin(admin.ModelAdmin):
    readonly_fields=("descripcion",)

admin.site.register(Venta,UsuarioAdmin)



#####################################################
class UsuarioAdmin(admin.ModelAdmin):
    readonly_fields=("fechaCompra",)

admin.site.register(Compra,UsuarioAdmin)



#####################################################
class UsuarioAdmin(admin.ModelAdmin):
    readonly_fields=("asunto",)

admin.site.register(Ticket,UsuarioAdmin)


#####################################################
class UsuarioAdmin(admin.ModelAdmin):
    readonly_fields=("descripcion",)

admin.site.register(IncidenteLaboral,UsuarioAdmin)




class UsuarioAdmin(admin.ModelAdmin):
    readonly_fields=("Correo",)

admin.site.register(Opionion,UsuarioAdmin)


class UsuarioAdmin(admin.ModelAdmin):
    readonly_fields=("nombreHerramienta",)

admin.site.register(Herramienta,UsuarioAdmin)


class UsuarioAdmin(admin.ModelAdmin):
    readonly_fields=("nombre",)

admin.site.register(Servicio,UsuarioAdmin)

