from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from .models import Empleado, Turno

# Create your views here.
def cuadrante(request):
    # Semana actual o la que viene por parámetro
    semana_param = request.GET.get('semana')
    if semana_param:
        try:
            from datetime import date
            año, mes, dia = semana_param.split('-')
            hoy = date(int(año), int(mes), int(dia))
        except:
            hoy = timezone.now().date()
    else:
        hoy = timezone.now().date()

    # Calcular lunes y domingo de la semana
    lunes = hoy - timedelta(days=hoy.weekday())
    domingo = lunes + timedelta(days=6)
    dias = [lunes + timedelta(days=i) for i in range(7)]

    # Semana anterior y siguiente para navegación
    semana_anterior = (lunes - timedelta(days=7)).strftime('%Y-%m-%d')
    semana_siguiente = (lunes + timedelta(days=7)).strftime('%Y-%m-%d')

    # Empleados y sus turnos de la semana
    empleados = Empleado.objects.filter(activo=True)
    turnos = Turno.objects.filter(
        fecha__gte=lunes,
        fecha__lte=domingo
    ).select_related('empleado')

    # Organizar turnos por empleado y día
    turno_map = {}
    for turno in turnos:
        key = (turno.empleado.id, turno.fecha)
        turno_map[key] = turno

    context = {
        'dias': dias,
        'empleados': empleados,
        'turno_map': turno_map,
        'lunes': lunes,
        'domingo': domingo,
        'semana_anterior': semana_anterior,
        'semana_siguiente': semana_siguiente,
    }
    return render(request, 'personal/cuadrante.html', context)