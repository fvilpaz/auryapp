import sys
sys.path.insert(0, '/home/nando/code/github/auryapp')
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'beachclub.settings')
django.setup()

from core.models import Espacio, Evento
from datetime import date

# Espacios
espacios = {
    'atlantis':  Espacio.objects.get_or_create(nombre='Atlantis')[0],
    'cabaña':    Espacio.objects.get_or_create(nombre='La Cabaña')[0],
    'le_mirage': Espacio.objects.get_or_create(nombre='Le Mirage')[0],
    'vip':       Espacio.objects.get_or_create(nombre='Zona Vip')[0],
    'terraza':   Espacio.objects.get_or_create(nombre='Terraza')[0],
}

# Eventos 2026
eventos = [
    {'cliente': '',            'tipo': 'otro',       'fecha': date(2026, 4, 10), 'espacios': ['cabaña'],                    'concepto': 'comida',    'personas': 7,   'notas': 'Prueba de menú'},
    {'cliente': '',            'tipo': 'otro',       'fecha': date(2026, 4, 17), 'espacios': ['cabaña'],                    'concepto': 'comida',    'personas': 0,   'notas': 'Prueba de menú'},
    {'cliente': '',            'tipo': 'otro',       'fecha': date(2026, 4, 24), 'espacios': ['cabaña'],                    'concepto': 'comida',    'personas': 0,   'notas': 'Prueba de menú'},
    {'cliente': 'Olaya&Luis',  'tipo': 'boda',       'fecha': date(2026, 4, 25), 'espacios': ['vip', 'terraza'],            'concepto': 'cena',      'personas': 100, 'notas': 'Ceremonia/Cena/Barra'},
    {'cliente': 'Colegio Maravillas', 'tipo': 'graduacion', 'fecha': date(2026, 5, 15), 'espacios': ['terraza'],           'concepto': 'cena',      'personas': 150, 'notas': 'Cena/Barra'},
    {'cliente': 'Arian',       'tipo': 'comunion',   'fecha': date(2026, 5, 23), 'espacios': ['vip'],                      'concepto': 'almuerzo',  'personas': 80,  'notas': 'Almuerzo/Barra'},
    {'cliente': 'Colegio El Coto', 'tipo': 'graduacion', 'fecha': date(2026, 5, 23), 'espacios': ['terraza'],              'concepto': 'cena',      'personas': 140, 'notas': 'Cena/Barra'},
    {'cliente': 'Lorenzo&Remi','tipo': 'boda',       'fecha': date(2026, 5, 30), 'espacios': ['vip'],                      'concepto': 'almuerzo',  'personas': 60,  'notas': 'Ceremonia/Almuerzo'},
    {'cliente': 'IES Arroyo de la Miel', 'tipo': 'graduacion', 'fecha': date(2026, 6, 5), 'espacios': ['terraza'],         'concepto': 'cena',      'personas': 100, 'notas': 'Cena/Barra'},
    {'cliente': 'Veronika&Andre', 'tipo': 'boda',    'fecha': date(2026, 6, 6), 'espacios': ['vip', 'terraza'],            'concepto': 'cena',      'personas': 150, 'notas': 'Ceremonia/Cena/Barra'},
    {'cliente': 'Albaytar',    'tipo': 'graduacion', 'fecha': date(2026, 6, 19), 'espacios': ['terraza'],                  'concepto': 'cena',      'personas': 190, 'notas': 'Cena/Barra'},
    {'cliente': 'IES Benalmadena', 'tipo': 'graduacion', 'fecha': date(2026, 6, 20), 'espacios': ['terraza'],              'concepto': 'cena',      'personas': 150, 'notas': 'Cena/Barra'},
    {'cliente': 'Nerea&Adrian','tipo': 'boda',       'fecha': date(2026, 9, 5),  'espacios': ['vip', 'terraza', 'cabaña'], 'concepto': 'cena',      'personas': 170, 'notas': 'Ceremonia/Cena/Barra'},
]

for e in eventos:
    evento, created = Evento.objects.get_or_create(
        cliente=e['cliente'],
        fecha=e['fecha'],
        defaults={
            'tipo': e['tipo'],
            'concepto': e['concepto'],
            'personas': e['personas'],
            'notas': e['notas'],
        }
    )
    for key in e['espacios']:
        evento.espacios.add(espacios[key])

    print(f"{'Creado' if created else 'Ya existe'}: {evento}")

print("\nDatos cargados correctamente.")
