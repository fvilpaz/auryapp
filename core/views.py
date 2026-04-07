from django.shortcuts import render
from django.utils import timezone
from .models import Espacio, Evento
from personal.models import Empleado, Turno
from tareas.models import TareaPlantilla

def dashboard(request):
    hoy = timezone.now().date()
    espacios = Espacio.objects.filter(activo=True)
    eventos_proximos = Evento.objects.filter(fecha__gte=hoy).order_by('fecha')[:5]
    total_eventos_mes = Evento.objects.filter(
        fecha__year=hoy.year,
        fecha__month=hoy.month
    ).count()
    total_personal = Empleado.objects.filter(activo=True).count()
    turnos_hoy = Turno.objects.filter(
        fecha=hoy,
        estado='trabajo'
    ).select_related('empleado')
    tareas_apertura = TareaPlantilla.objects.filter(
        momento='apertura',
        activa=True
    ).select_related('espacio')

    context = {
        'espacios': espacios,
        'total_espacios': espacios.count(),
        'eventos_proximos': eventos_proximos,
        'total_eventos_mes': total_eventos_mes,
        'total_personal': total_personal,
        'turnos_hoy': turnos_hoy,
        'tareas_apertura': tareas_apertura,
        'hoy': hoy,
    }
    return render(request, 'core/dashboard.html', context)

def lista_eventos(request):
    eventos = Evento.objects.all().order_by('fecha')
    context = {
        'eventos': eventos,
    }
    return render(request, 'core/eventos.html', context)