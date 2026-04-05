import sys
sys.path.insert(0, '/home/nando/code/github/auryapp')
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'beachclub.settings')
django.setup()

from personal.models import Empleado

empleados = [
    {'nombre': 'Aury',     'apellidos': '', 'rol': 'maitre',       'telefono': '', 'email': ''},
    {'nombre': 'Edu',      'apellidos': '', 'rol': 'jefe_sector',  'telefono': '', 'email': ''},
    {'nombre': 'Antonio',  'apellidos': '', 'rol': 'camarero',     'telefono': '', 'email': ''},
    {'nombre': 'Eva',      'apellidos': '', 'rol': 'camarero',     'telefono': '', 'email': ''},
    {'nombre': 'Inma',     'apellidos': '', 'rol': 'camarero',     'telefono': '', 'email': ''},
    {'nombre': 'Laura',    'apellidos': '', 'rol': 'camarero',     'telefono': '', 'email': ''},
    {'nombre': 'Vane',     'apellidos': '', 'rol': 'camarero',     'telefono': '', 'email': ''},
    {'nombre': 'Arlen',    'apellidos': '', 'rol': 'camarero',     'telefono': '', 'email': ''},
    {'nombre': 'Sergio',   'apellidos': '', 'rol': 'camarero',     'telefono': '', 'email': ''},
]

for e in empleados:
    empleado, created = Empleado.objects.get_or_create(
        nombre=e['nombre'],
        defaults={
            'apellidos': e['apellidos'],
            'rol': e['rol'],
            'telefono': e['telefono'],
            'email': e['email'],
        }
    )
    print(f"{'Creado' if created else 'Ya existe'}: {empleado}")

print("\nEmpleados cargados correctamente.")
