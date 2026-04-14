from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from django.http import JsonResponse
from datetime import timedelta, date
from .models import Empleado, Turno, SolicitudAusencia
from django.contrib.auth.decorators import login_required, user_passes_test

staff_required = user_passes_test(lambda u: u.is_active and u.is_staff, login_url='/login/')


def _redirect_seguro(request, next_param, fallback_view, fallback_pk=None):
    """Redirige solo a URLs internas; nunca a dominios externos."""
    url = next_param or ''
    if url and url_has_allowed_host_and_scheme(url, allowed_hosts={request.get_host()}):
        return redirect(url)
    if fallback_pk is not None:
        return redirect(fallback_view, pk=fallback_pk)
    return redirect(fallback_view)

@login_required(login_url='/login/')
def cuadrante(request):
    semana_param = request.GET.get('semana')
    if semana_param:
        try:
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

    empleados = Empleado.objects.filter(activo=True).order_by('posicion', 'nombre')
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
        'todos_empleados': empleados,
    }
    return render(request, 'personal/cuadrante.html', context)

@login_required(login_url='/login/')
def lista_empleados(request):
    empleados = Empleado.objects.filter(activo=True).order_by('posicion', 'nombre')
    context = {
        'empleados': empleados,
    }
    return render(request, 'personal/lista_empleados.html', context)

@login_required(login_url='/login/')
def detalle_empleado(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    solicitudes = SolicitudAusencia.objects.filter(empleado=empleado).order_by('-fecha_inicio')
    todos_empleados = Empleado.objects.filter(activo=True).order_by('posicion', 'nombre')
    hoy = timezone.now().date()
    context = {
        'empleado': empleado,
        'solicitudes': solicitudes,
        'tipos_solicitud': SolicitudAusencia.TIPO_CHOICES,
        'todos_empleados': todos_empleados,
        'hoy': hoy,
        'en_30_dias': hoy + timedelta(days=30),
    }
    return render(request, 'personal/detalle_empleado.html', context)

@staff_required
def nuevo_empleado(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        apellidos = request.POST.get('apellidos', '').strip()
        rol = request.POST.get('rol', '')
        telefono = request.POST.get('telefono', '').strip()
        email = request.POST.get('email', '').strip()
        fecha_nacimiento = request.POST.get('fecha_nacimiento') or None
        tipo_contrato = request.POST.get('tipo_contrato', '')
        fecha_vencimiento = request.POST.get('fecha_vencimiento') or None
        if nombre and rol:
            Empleado.objects.create(
                nombre=nombre, apellidos=apellidos, rol=rol,
                telefono=telefono, email=email,
                fecha_nacimiento=fecha_nacimiento,
                tipo_contrato=tipo_contrato,
                fecha_vencimiento=fecha_vencimiento,
            )
            return redirect('lista_empleados')
    return render(request, 'personal/nuevo_empleado.html', {
        'roles': Empleado.ROL_CHOICES,
        'contratos': Empleado.CONTRATO_CHOICES,
    })

@staff_required
def editar_empleado(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    if request.method == 'POST':
        empleado.nombre = request.POST.get('nombre', '').strip()
        empleado.apellidos = request.POST.get('apellidos', '').strip()
        empleado.rol = request.POST.get('rol', '')
        empleado.telefono = request.POST.get('telefono', '').strip()
        empleado.email = request.POST.get('email', '').strip()
        empleado.fecha_nacimiento = request.POST.get('fecha_nacimiento') or None
        empleado.tipo_contrato = request.POST.get('tipo_contrato', '')
        empleado.fecha_vencimiento = request.POST.get('fecha_vencimiento') or None
        if empleado.nombre and empleado.rol:
            empleado.save()
            return redirect('lista_empleados')
    return render(request, 'personal/editar_empleado.html', {
        'empleado': empleado,
        'roles': Empleado.ROL_CHOICES,
        'contratos': Empleado.CONTRATO_CHOICES,
    })

@staff_required
def guardar_turno(request):
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

@staff_required
def guardar_posiciones(request):
    if request.method == 'POST':
        for key, val in request.POST.items():
            if key.startswith('posicion_'):
                emp_id = key.replace('posicion_', '')
                try:
                    Empleado.objects.filter(pk=int(emp_id)).update(posicion=int(val))
                except (ValueError, TypeError):
                    pass
        return JsonResponse({'ok': True})
    return JsonResponse({'ok': False}, status=405)

@staff_required
def nueva_solicitud(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    if request.method == 'POST':
        tipo = request.POST.get('tipo')
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')
        notas = request.POST.get('notas', '').strip()
        if tipo and fecha_inicio and fecha_fin:
            SolicitudAusencia.objects.create(
                empleado=empleado,
                tipo=tipo,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                notas=notas,
            )
    return redirect('detalle_empleado', pk=pk)

@staff_required
def aprobar_solicitud(request, pk):
    solicitud = get_object_or_404(SolicitudAusencia, pk=pk)
    if request.method == 'POST':
        solicitud.estado = 'aprobada'
        solicitud.save()
        dia_actual = solicitud.fecha_inicio
        while dia_actual <= solicitud.fecha_fin:
            Turno.objects.update_or_create(
                empleado=solicitud.empleado,
                fecha=dia_actual,
                defaults={'estado': solicitud.tipo}
            )
            dia_actual += timedelta(days=1)
        next_url = request.POST.get('next', '')
        return _redirect_seguro(request, next_url, 'detalle_empleado', solicitud.empleado.pk)
    return redirect('detalle_empleado', pk=solicitud.empleado.pk)

@staff_required
def rechazar_solicitud(request, pk):
    solicitud = get_object_or_404(SolicitudAusencia, pk=pk)
    if request.method == 'POST':
        solicitud.estado = 'rechazada'
        solicitud.save()
        next_url = request.POST.get('next', '')
        return _redirect_seguro(request, next_url, 'detalle_empleado', solicitud.empleado.pk)
    return redirect('detalle_empleado', pk=solicitud.empleado.pk)

@login_required(login_url='/login/')
def lista_solicitudes(request):
    solicitudes = SolicitudAusencia.objects.filter(estado='pendiente').select_related('empleado').order_by('fecha_inicio')
    context = {'solicitudes': solicitudes}
    return render(request, 'personal/lista_solicitudes.html', context)

@login_required(login_url='/login/')
def lista_vencimientos(request):
    hoy = timezone.now().date()
    empleados = Empleado.objects.filter(
        activo=True,
        fecha_vencimiento__isnull=False,
    ).order_by('fecha_vencimiento')
    datos = []
    for emp in empleados:
        dias = (emp.fecha_vencimiento - hoy).days
        abs_dias = abs(dias)
        meses = abs_dias // 30
        datos.append({'empleado': emp, 'dias': dias, 'abs_dias': abs_dias, 'meses': meses})
    context = {'datos': datos, 'hoy': hoy}
    return render(request, 'personal/lista_vencimientos.html', context)

@login_required(login_url='/login/')
def lista_vacaciones(request):
    hoy = timezone.now().date()
    solicitudes = SolicitudAusencia.objects.filter(
        tipo='vacaciones',
        fecha_fin__gte=hoy,
    ).exclude(estado='rechazada').select_related('empleado').order_by('fecha_inicio')
    empleados = Empleado.objects.filter(activo=True).order_by('posicion', 'nombre')
    tipos = [('vacaciones', 'Vacaciones')]
    context = {'solicitudes': solicitudes, 'titulo': 'Vacaciones', 'empleados': empleados, 'tipos': tipos}
    return render(request, 'personal/lista_ausencias.html', context)

@login_required(login_url='/login/')
def lista_dias_sueltos(request):
    hoy = timezone.now().date()
    solicitudes = SolicitudAusencia.objects.filter(
        tipo__in=['libre', 'inamovible', 'libre_vacaciones', 'finde_largo'],
        fecha_fin__gte=hoy,
    ).exclude(estado='rechazada').select_related('empleado').order_by('fecha_inicio')
    empleados = Empleado.objects.filter(activo=True).order_by('posicion', 'nombre')
    tipos = [t for t in SolicitudAusencia.TIPO_CHOICES if t[0] != 'vacaciones']
    context = {'solicitudes': solicitudes, 'titulo': 'Días sueltos', 'empleados': empleados, 'tipos': tipos}
    return render(request, 'personal/lista_ausencias.html', context)

@staff_required
def crear_solicitud(request):
    if request.method == 'POST':
        empleado_id = request.POST.get('empleado_id')
        tipo = request.POST.get('tipo')
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')
        notas = request.POST.get('notas', '').strip()
        if empleado_id and tipo and fecha_inicio and fecha_fin:
            empleado = get_object_or_404(Empleado, pk=empleado_id)
            SolicitudAusencia.objects.create(
                empleado=empleado,
                tipo=tipo,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                notas=notas,
            )
    return _redirect_seguro(request, request.POST.get('next', ''), 'lista_solicitudes')
