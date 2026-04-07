from django.shortcuts import render
from django.utils import timezone
from .models import Espacio, Evento
from personal.models import Empleado, Turno
from tareas.models import TareaPlantilla
from django.http import JsonResponse

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

def eventos_json(request):
    eventos = Evento.objects.all()
    data = []
    colores = {
        'boda': '#1a6fc4',
        'graduacion': '#1d9e75',
        'comunion': '#e8a020',
        'gala': '#c0392b',
        'preboda': '#8e44ad',
        'otro': '#6b7280',
    }
    for evento in eventos:
        data.append({
            'title': evento.cliente if evento.cliente else evento.get_tipo_display(),
            'start': evento.fecha.isoformat(),
            'color': colores.get(evento.tipo, '#6b7280'),
            'url': f'/eventos/',
        })
    return JsonResponse(data, safe=False)

def calendario(request):
    return render(request, 'core/calendario.html')
