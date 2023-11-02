# myapp/management/commands/backup_db.py
from django.core.management.base import BaseCommand
import os
import datetime
import shutil
import zipfile  # Importa el módulo zipfile para manejar archivos comprimidos

class Command(BaseCommand):
    help = 'Realiza un respaldo de la base de datos o carga una base de datos desde un respaldo'

    def add_arguments(self, parser):
        # Agrega un argumento llamado 'cargar' que indica si se debe cargar una base de datos
        parser.add_argument(
            '--cargar',
            action='store_true',
            dest='cargar',
            help='Cargar una base de datos desde un respaldo',
        )

    def handle(self, *args, **options):
        if options['cargar']:
            # Si se proporciona la opción --cargar, cargar una base de datos desde un respaldo
            self.cargar_bd()
        else:
            # Si no se proporciona la opción --cargar, realizar un respaldo
            self.respaldar_bd()

    def respaldar_bd(self):
        # El código para realizar un respaldo (como se hacía antes)

    def cargar_bd(self):
        # Directorio donde se almacenan los respaldos
        backup_dir = 'backups/'

        # Lista los archivos de respaldo en el directorio
        backups = [f for f in os.listdir(backup_dir) if f.startswith('backup_')]

        if not backups:
            self.stdout.write(self.style.ERROR('No se encontraron respaldos disponibles.'))
            return

        # Pregunta al usuario cuál respaldo cargar
        self.stdout.write('Respaldos disponibles:')
        for i, backup in enumerate(backups, 1):
            self.stdout.write(f'{i}. {backup}')
        seleccion = input('Seleccione el número del respaldo que desea cargar: ')

        try:
            seleccion = int(seleccion)
            if 1 <= seleccion <= len(backups):
                selected_backup = backups[seleccion - 1]
                self.cargar_respaldo(selected_backup)
            else:
                self.stdout.write(self.style.ERROR('Selección no válida.'))
        except ValueError:
            self.stdout.write(self.style.ERROR('Entrada no válida. Ingrese un número.'))

    def cargar_respaldo(self, selected_backup):
        # Ubicación del archivo de respaldo seleccionado
        backup_file = os.path.join('backups', selected_backup)

        # Ubicación de la base de datos actual
        db_file = 'db.sqlite3'

        # Realiza la carga de la base de datos desde el respaldo
        try:
            shutil.copy(backup_file, db_file)
            self.stdout.write(self.style.SUCCESS(f'Base de datos cargada desde: {selected_backup}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error al cargar la base de datos: {str(e)}'))
