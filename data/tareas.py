import sys
sys.path.insert(0, '/home/nando/code/github/auryapp')
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'beachclub.settings')
django.setup()

from core.models import Espacio
from tareas.models import TareaPlantilla

atlantis  = Espacio.objects.get(nombre='Atlantis')
le_mirage = Espacio.objects.get(nombre='Le Mirage')
cabana    = Espacio.objects.get(nombre='La Cabaña')

tareas = [
    # Atlantis apertura
    {'nombre': 'Limpieza terraza',          'espacio': atlantis,  'momento': 'apertura', 'orden': 1},
    {'nombre': 'Puesta en marcha máquinas', 'espacio': atlantis,  'momento': 'apertura', 'orden': 2},
    {'nombre': 'Cortar fruta',              'espacio': atlantis,  'momento': 'apertura', 'orden': 3},
    {'nombre': 'Poner hielo',               'espacio': atlantis,  'momento': 'apertura', 'orden': 4},
    {'nombre': 'Colocar pedido',            'espacio': atlantis,  'momento': 'apertura', 'orden': 5},
    {'nombre': 'Reposición de mercancía',   'espacio': atlantis,  'momento': 'apertura', 'orden': 6},
    {'nombre': 'Limpieza neveras',          'espacio': atlantis,  'momento': 'apertura', 'orden': 7},
    # Atlantis cierre
    {'nombre': 'Limpieza y reposición máquinas', 'espacio': atlantis, 'momento': 'cierre', 'orden': 1},
    {'nombre': 'Limpieza de terraza',            'espacio': atlantis, 'momento': 'cierre', 'orden': 2},
    {'nombre': 'Limpieza del bar',               'espacio': atlantis, 'momento': 'cierre', 'orden': 3},
    {'nombre': 'Reposición barriles, hielo y menaje', 'espacio': atlantis, 'momento': 'cierre', 'orden': 4},
    # Le Mirage apertura
    {'nombre': 'Limpieza terraza',          'espacio': le_mirage, 'momento': 'apertura', 'orden': 1},
    {'nombre': 'Puesta en marcha máquinas', 'espacio': le_mirage, 'momento': 'apertura', 'orden': 2},
    {'nombre': 'Cortar fruta',              'espacio': le_mirage, 'momento': 'apertura', 'orden': 3},
    {'nombre': 'Poner hielo',               'espacio': le_mirage, 'momento': 'apertura', 'orden': 4},
    {'nombre': 'Colocar pedido',            'espacio': le_mirage, 'momento': 'apertura', 'orden': 5},
    {'nombre': 'Reposición de mercancía',   'espacio': le_mirage, 'momento': 'apertura', 'orden': 6},
    {'nombre': 'Limpieza neveras',          'espacio': le_mirage, 'momento': 'apertura', 'orden': 7},
    # Le Mirage cierre
    {'nombre': 'Limpieza y reposición máquinas',      'espacio': le_mirage, 'momento': 'cierre', 'orden': 1},
    {'nombre': 'Limpieza de terraza',                 'espacio': le_mirage, 'momento': 'cierre', 'orden': 2},
    {'nombre': 'Limpieza del bar',                    'espacio': le_mirage, 'momento': 'cierre', 'orden': 3},
    {'nombre': 'Reposición barriles, hielo y menaje', 'espacio': le_mirage, 'momento': 'cierre', 'orden': 4},
    # La Cabaña apertura
    {'nombre': 'Carros preparados',           'espacio': cabana, 'momento': 'apertura', 'orden': 1},
    {'nombre': 'Subir cubos de basura',       'espacio': cabana, 'momento': 'apertura', 'orden': 2},
    {'nombre': 'Preparar terraza excursiones','espacio': cabana, 'momento': 'apertura', 'orden': 3},
    # La Cabaña cierre
    {'nombre': 'Reposición de buffet',                    'espacio': cabana, 'momento': 'cierre', 'orden': 1},
    {'nombre': 'Limpieza y reposición de carros',         'espacio': cabana, 'momento': 'cierre', 'orden': 2},
    {'nombre': 'Mantener cubos y tronas limpios',         'espacio': cabana, 'momento': 'cierre', 'orden': 3},
    {'nombre': 'Mesas, sillas y manteles bien colocados', 'espacio': cabana, 'momento': 'cierre', 'orden': 4},
]

for t in tareas:
    obj, created = TareaPlantilla.objects.get_or_create(
        nombre=t['nombre'],
        espacio=t['espacio'],
        momento=t['momento'],
        defaults={'orden': t['orden']}
    )
    print(f"{'Creada' if created else 'Ya existe'}: {obj}")

print("\nTareas plantilla cargadas correctamente.")