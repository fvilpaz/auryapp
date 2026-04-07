from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.db.models import Case, When, Value, IntegerField
from datetime import timedelta
from .models import Empleado, Turno

def cuadrante(request):
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

    lunes = hoy - timedelta(days=hoy.weekday())
    domingo = lunes + timedelta(days=6)
    dias = [lunes + timedelta(days=i) for i in range(7)]
    semana_anterior = (lunes - timedelta(days=7)).strftime('%Y-%m-%d')
    semana_siguiente = (lunes + timedelta(days=7)).strftime('%Y-%m-%d')

    empleados = Empleado.objects.filter(activo=True).annotate(
        rol_orden=Case(
            When(rol='maitre', then=Value(0)),
            When(rol='segundo_maitre', then=Value(1)),
            When(rol='jefe_sector', then=Value(2)),
            When(rol='camarero', then=Value(3)),
            When(rol='ayudante_camarero', then=Value(4)),
            default=Value(99),
            output_field=IntegerField(),
        )
    ).order_by('rol_orden', 'nombre')
    turnos = Turno.objects.filter(
        fecha__gte=lunes,
        fecha__lte=domingo
    ).select_related('empleado')

    turno_map = {}
    for turno in turnos:
        turno_map[(turno.empleado.id, turno.fecha)] = turno

    rows = []
    for empleado in empleados:
        cells = []
        horas_total = 0
        for dia in dias:
            turno = turno_map.get((empleado.id, dia))
            if turno and turno.estado == 'trabajo':
                horas_total += turno.horas
            cells.append({'dia': dia, 'turno': turno})
        rows.append({'empleado': empleado, 'cells': cells, 'horas_total': horas_total})

    ids_con_turno = {t.empleado.id for t in turnos}
    empleados_disponibles = [e for e in empleados if e.id not in ids_con_turno]

    context = {
        'dias': dias,
        'rows': rows,
        'lunes': lunes,
        'domingo': domingo,
        'semana_anterior': semana_anterior,
        'semana_siguiente': semana_siguiente,
        'estados': Turno.ESTADO_CHOICES,
        'empleados_disponibles': empleados_disponibles,
    }
    return render(request, 'personal/cuadrante.html', context)

def lista_empleados(request):
    empleados = Empleado.objects.filter(activo=True).annotate(
        rol_orden=Case(
            When(rol='maitre', then=Value(0)),
            When(rol='segundo_maitre', then=Value(1)),
            When(rol='jefe_sector', then=Value(2)),
            When(rol='camarero', then=Value(3)),
            When(rol='ayudante_camarero', then=Value(4)),
            default=Value(99),
            output_field=IntegerField(),
        )
    ).order_by('rol_orden', 'nombre')
    context = {
        'empleados': empleados,
    }
    return render(request, 'personal/lista_empleados.html', context)

def nuevo_empleado(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        apellidos = request.POST.get('apellidos', '').strip()
        rol = request.POST.get('rol', '')
        telefono = request.POST.get('telefono', '').strip()
        email = request.POST.get('email', '').strip()
        fecha_nacimiento = request.POST.get('fecha_nacimiento') or None
        if nombre and rol:
            Empleado.objects.create(
                nombre=nombre,
                apellidos=apellidos,
                rol=rol,
                telefono=telefono,
                email=email,
                fecha_nacimiento=fecha_nacimiento,
            )
            return redirect('lista_empleados')
    return render(request, 'personal/nuevo_empleado.html', {
        'roles': Empleado.ROL_CHOICES,
    })

def editar_empleado(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    if request.method == 'POST':
        empleado.nombre = request.POST.get('nombre', '').strip()
        empleado.apellidos = request.POST.get('apellidos', '').strip()
        empleado.rol = request.POST.get('rol', '')
        empleado.telefono = request.POST.get('telefono', '').strip()
        empleado.email = request.POST.get('email', '').strip()
        empleado.fecha_nacimiento = request.POST.get('fecha_nacimiento') or None
        if empleado.nombre and empleado.rol:
            empleado.save()
            return redirect('lista_empleados')
    return render(request, 'personal/editar_empleado.html', {
        'empleado': empleado,
        'roles': Empleado.ROL_CHOICES,
    })

def guardar_turno(request):
    from django.http import JsonResponse
    if request.method == 'POST':
        empleado_id = request.POST.get('empleado_id')
        fecha = request.POST.get('fecha')
        estado = request.POST.get('estado')
        hora_inicio = request.POST.get('hora_inicio') or None
        hora_fin = request.POST.get('hora_fin') or None
        horas = request.POST.get('horas', 0) or 0

        empleado = get_object_or_404(Empleado, pk=empleado_id)
        turno, _ = Turno.objects.update_or_create(
            empleado=empleado,
            fecha=fecha,
            defaults={
                'estado': estado,
                'hora_inicio': hora_inicio,
                'hora_fin': hora_fin,
                'horas': horas,
            }
        )
        return JsonResponse({
            'ok': True,
            'turno_id': turno.pk,
            'estado': turno.estado,
            'hora_inicio': turno.hora_inicio.strftime('%H:%M') if turno.hora_inicio else '',
            'hora_fin': turno.hora_fin.strftime('%H:%M') if turno.hora_fin else '',
        })
    return JsonResponse({'ok': False}, status=405)
