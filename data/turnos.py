import sys
sys.path.insert(0, '/home/nando/code/github/auryapp')
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'beachclub.settings')
django.setup()

from personal.models import Empleado, Turno
from datetime import date, time

# Empleados
aury    = Empleado.objects.get(nombre='Aury')
edu     = Empleado.objects.get(nombre='Edu')
antonio = Empleado.objects.get(nombre='Antonio')
inma    = Empleado.objects.get(nombre='Inma')
laura   = Empleado.objects.get(nombre='Laura')

def turno(empleado, fecha, estado='trabajo', h_ini=None, h_fin=None, horas=0):
    Turno.objects.get_or_create(
        empleado=empleado,
        fecha=fecha,
        defaults={
            'estado': estado,
            'hora_inicio': h_ini,
            'hora_fin': h_fin,
            'horas': horas,
        }
    )

T = time  # alias corto

# ── Semana 6-12 abril ──────────────────────────────────────────
turno(aury,    date(2026,4,6),  'libre')
turno(aury,    date(2026,4,7),  'trabajo', T(10,0), T(18,0), 8)
turno(aury,    date(2026,4,8),  'trabajo', T(10,0), T(18,0), 8)
turno(aury,    date(2026,4,9),  'trabajo', T(10,0), T(18,0), 8)
turno(aury,    date(2026,4,10), 'trabajo', T(12,0), T(1,0),  12)
turno(aury,    date(2026,4,11), 'trabajo', T(12,0), T(18,0), 6)
turno(aury,    date(2026,4,12), 'libre')

turno(edu,     date(2026,4,6),  'trabajo', T(10,0), T(18,0), 8)
turno(edu,     date(2026,4,7),  'trabajo', T(10,0), T(18,0), 8)
turno(edu,     date(2026,4,8),  'libre')
turno(edu,     date(2026,4,9),  'libre')
turno(edu,     date(2026,4,10), 'trabajo', T(10,0), T(18,0), 8)
turno(edu,     date(2026,4,11), 'trabajo', T(10,0), T(18,0), 8)
turno(edu,     date(2026,4,12), 'trabajo', T(10,0), T(18,0), 8)

turno(antonio, date(2026,4,6),  'libre')
turno(antonio, date(2026,4,7),  'libre')
turno(antonio, date(2026,4,8),  'trabajo', T(10,0), T(18,0), 8)
turno(antonio, date(2026,4,9),  'trabajo', T(10,0), T(18,0), 8)
turno(antonio, date(2026,4,10), 'trabajo', T(10,0), T(18,0), 8)
turno(antonio, date(2026,4,11), 'trabajo', T(10,0), T(18,0), 8)
turno(antonio, date(2026,4,12), 'trabajo', T(10,0), T(18,0), 8)

turno(inma,    date(2026,4,6),  'libre')
turno(inma,    date(2026,4,7),  'libre')
turno(inma,    date(2026,4,8),  'trabajo', T(10,0), T(16,0), 6)
turno(inma,    date(2026,4,9),  'trabajo', T(10,0), T(16,0), 6)
turno(inma,    date(2026,4,10), 'trabajo', T(10,0), T(16,0), 6)
turno(inma,    date(2026,4,11), 'trabajo', T(10,0), T(16,0), 6)
turno(inma,    date(2026,4,12), 'trabajo', T(10,0), T(16,0), 6)

turno(laura,   date(2026,4,6),  'trabajo', T(10,0), T(18,0), 8)
turno(laura,   date(2026,4,7),  'trabajo', T(10,0), T(18,0), 8)
turno(laura,   date(2026,4,8),  'trabajo', T(10,0), T(18,0), 8)
turno(laura,   date(2026,4,9),  'trabajo', T(10,0), T(18,0), 8)
turno(laura,   date(2026,4,10), 'trabajo', T(17,0), T(1,0),  8)
turno(laura,   date(2026,4,11), 'libre')
turno(laura,   date(2026,4,12), 'libre')

# ── Semana 13-19 abril ─────────────────────────────────────────
turno(aury,    date(2026,4,13), 'libre')
turno(aury,    date(2026,4,14), 'trabajo', T(10,0), T(18,0), 8)
turno(aury,    date(2026,4,15), 'trabajo', T(10,0), T(18,0), 8)
turno(aury,    date(2026,4,16), 'trabajo', T(10,0), T(18,0), 8)
turno(aury,    date(2026,4,17), 'trabajo', T(10,0), T(18,0), 8)
turno(aury,    date(2026,4,18), 'trabajo', T(10,0), T(18,0), 8)
turno(aury,    date(2026,4,19), 'libre')

turno(edu,     date(2026,4,13), 'trabajo', T(10,0), T(18,0), 8)
turno(edu,     date(2026,4,14), 'trabajo', T(10,0), T(18,0), 8)
turno(edu,     date(2026,4,15), 'trabajo', T(10,0), T(18,0), 8)
turno(edu,     date(2026,4,16), 'trabajo', T(10,0), T(18,0), 8)
turno(edu,     date(2026,4,17), 'trabajo', T(10,0), T(18,0), 8)
turno(edu,     date(2026,4,18), 'libre')
turno(edu,     date(2026,4,19), 'libre')

turno(antonio, date(2026,4,13), 'trabajo', T(10,0), T(18,0), 8)
turno(antonio, date(2026,4,14), 'trabajo', T(10,0), T(18,0), 8)
turno(antonio, date(2026,4,15), 'libre')
turno(antonio, date(2026,4,16), 'libre')
turno(antonio, date(2026,4,17), 'trabajo', T(10,0), T(18,0), 8)
turno(antonio, date(2026,4,18), 'trabajo', T(10,0), T(18,0), 8)
turno(antonio, date(2026,4,19), 'trabajo', T(10,0), T(18,0), 8)

turno(inma,    date(2026,4,13), 'trabajo', T(10,0), T(16,0), 6)
turno(inma,    date(2026,4,14), 'trabajo', T(10,0), T(16,0), 6)
turno(inma,    date(2026,4,15), 'libre')
turno(inma,    date(2026,4,16), 'libre')
turno(inma,    date(2026,4,17), 'trabajo', T(10,0), T(16,0), 6)
turno(inma,    date(2026,4,18), 'trabajo', T(10,0), T(16,0), 6)
turno(inma,    date(2026,4,19), 'trabajo', T(10,0), T(16,0), 6)

turno(laura,   date(2026,4,13), 'trabajo', T(10,0), T(18,0), 8)
turno(laura,   date(2026,4,14), 'trabajo', T(10,0), T(18,0), 8)
turno(laura,   date(2026,4,15), 'trabajo', T(10,0), T(18,0), 8)
turno(laura,   date(2026,4,16), 'trabajo', T(10,0), T(18,0), 8)
turno(laura,   date(2026,4,17), 'libre')
turno(laura,   date(2026,4,18), 'libre')
turno(laura,   date(2026,4,19), 'trabajo', T(10,0), T(18,0), 8)

# ── Semana 20-26 abril ─────────────────────────────────────────
turno(aury,    date(2026,4,20), 'libre')
turno(aury,    date(2026,4,21), 'trabajo', T(10,0), T(18,0), 8)
turno(aury,    date(2026,4,22), 'trabajo', T(10,0), T(18,0), 8)
turno(aury,    date(2026,4,23), 'trabajo', T(10,0), T(18,0), 8)
turno(aury,    date(2026,4,24), 'trabajo', T(10,0), T(18,0), 8)
turno(aury,    date(2026,4,25), 'trabajo', T(10,0), T(18,0), 8)  # EVENTO
turno(aury,    date(2026,4,26), 'libre')

turno(edu,     date(2026,4,20), 'libre')
turno(edu,     date(2026,4,21), 'libre')
turno(edu,     date(2026,4,22), 'trabajo', T(10,0), T(18,0), 8)
turno(edu,     date(2026,4,23), 'trabajo', T(10,0), T(18,0), 8)
turno(edu,     date(2026,4,24), 'trabajo', T(10,0), T(18,0), 8)
turno(edu,     date(2026,4,25), 'trabajo', T(10,0), T(18,0), 8)  # EVENTO
turno(edu,     date(2026,4,26), 'trabajo', T(10,0), T(18,0), 8)

turno(antonio, date(2026,4,20), 'trabajo', T(10,0), T(18,0), 8)
turno(antonio, date(2026,4,21), 'libre')
turno(antonio, date(2026,4,22), 'trabajo', T(10,0), T(18,0), 8)
turno(antonio, date(2026,4,23), 'trabajo', T(10,0), T(18,0), 8)
turno(antonio, date(2026,4,24), 'trabajo', T(10,0), T(18,0), 8)
turno(antonio, date(2026,4,25), 'trabajo', T(10,0), T(18,0), 8)  # EVENTO
turno(antonio, date(2026,4,26), 'libre')

turno(inma,    date(2026,4,20), 'trabajo', T(10,0), T(16,0), 6)
turno(inma,    date(2026,4,21), 'trabajo', T(10,0), T(16,0), 6)
turno(inma,    date(2026,4,22), 'libre')
turno(inma,    date(2026,4,23), 'libre')
turno(inma,    date(2026,4,24), 'trabajo', T(10,0), T(16,0), 6)
turno(inma,    date(2026,4,25), 'trabajo', T(10,0), T(16,0), 6)
turno(inma,    date(2026,4,26), 'trabajo', T(10,0), T(16,0), 6)

turno(laura,   date(2026,4,20), 'trabajo', T(10,0), T(18,0), 8)
turno(laura,   date(2026,4,21), 'trabajo', T(10,0), T(18,0), 8)
turno(laura,   date(2026,4,22), 'trabajo', T(10,0), T(18,0), 8)
turno(laura,   date(2026,4,23), 'trabajo', T(10,0), T(18,0), 8)
turno(laura,   date(2026,4,24), 'libre')
turno(laura,   date(2026,4,25), 'trabajo', T(10,0), T(18,0), 8)  # EVENTO
turno(laura,   date(2026,4,26), 'libre')

# ── Semana 27-30 abril ─────────────────────────────────────────
turno(aury,    date(2026,4,27), 'trabajo', T(10,0), T(18,0), 8)
turno(aury,    date(2026,4,28), 'libre')
turno(aury,    date(2026,4,29), 'trabajo', T(10,0), T(18,0), 8)
turno(aury,    date(2026,4,30), 'trabajo', T(10,0), T(18,0), 8)

turno(edu,     date(2026,4,27), 'libre')  
turno(edu,     date(2026,4,28), 'libre')
turno(edu,     date(2026,4,29), 'trabajo', T(10,0), T(18,0), 8)
turno(edu,     date(2026,4,30), 'trabajo', T(10,0), T(18,0), 8)

turno(antonio, date(2026,4,27), 'libre')
turno(antonio, date(2026,4,28), 'trabajo', T(10,0), T(18,0), 8)
turno(antonio, date(2026,4,29), 'trabajo', T(10,0), T(18,0), 8)
turno(antonio, date(2026,4,30), 'trabajo', T(10,0), T(18,0), 8)

turno(inma,    date(2026,4,27), 'trabajo', T(10,0), T(16,0), 6)
turno(inma,    date(2026,4,28), 'trabajo', T(10,0), T(16,0), 6)
turno(inma,    date(2026,4,29), 'trabajo', T(10,0), T(16,0), 6)
turno(inma,    date(2026,4,30), 'trabajo', T(10,0), T(16,0), 6)

turno(laura,   date(2026,4,27), 'libre')
turno(laura,   date(2026,4,28), 'libre')
turno(laura,   date(2026,4,29), 'trabajo', T(10,0), T(18,0), 8)
turno(laura,   date(2026,4,30), 'trabajo', T(10,0), T(18,0), 8)

print("Turnos de abril cargados correctamente.")