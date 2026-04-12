from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Espacio, Evento, ArticuloPedido, Nota, EventoDocumento, EventoRango, EventoCamarero
from personal.models import Empleado, Turno, SolicitudAusencia
from tareas.models import TareaPlantilla, TareaDelDia
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
    ).select_related('empleado', 'espacio')

    resumen_espacios = []
    for espacio in espacios:
        asignados = turnos_hoy.filter(espacio=espacio).select_related('empleado')
        total_tareas = TareaPlantilla.objects.filter(espacio=espacio, activa=True).count()
        completadas = TareaDelDia.objects.filter(
            plantilla__espacio=espacio, fecha=hoy, completada=True
        ).count()
        porcentaje = int(completadas / total_tareas * 100) if total_tareas > 0 else 0
        resumen_espacios.append({
            'espacio': espacio,
            'asignados': asignados,
            'total_tareas': total_tareas,
            'completadas': completadas,
            'porcentaje': porcentaje,
        })

    # Próximos 7 días
    en_7_dias = hoy + timezone.timedelta(days=7)
    eventos_esta_semana = Evento.objects.filter(fecha__gte=hoy, fecha__lte=en_7_dias).count()

    # Vacaciones próximas (todas, no rechazadas)
    vacaciones_proximas = SolicitudAusencia.objects.filter(
        tipo='vacaciones',
        fecha_fin__gte=hoy,
    ).exclude(estado='rechazada').select_related('empleado').order_by('fecha_inicio')

    # Días sueltos próximos (todos, no rechazados)
    dias_sueltos_proximos = SolicitudAusencia.objects.filter(
        tipo__in=['libre', 'inamovible', 'libre_vacaciones', 'finde_largo'],
        fecha_fin__gte=hoy,
    ).exclude(estado='rechazada').select_related('empleado').order_by('fecha_inicio')

    # Cumpleaños próximos (comparando mes y día)
    cumpleanos_proximos = []
    for empleado in Empleado.objects.filter(activo=True, fecha_nacimiento__isnull=False):
        cumple = empleado.fecha_nacimiento.replace(year=hoy.year)
        if cumple < hoy:
            cumple = cumple.replace(year=hoy.year + 1)
        if hoy <= cumple <= en_7_dias:
            cumpleanos_proximos.append({'empleado': empleado, 'fecha': cumple})
    cumpleanos_proximos.sort(key=lambda x: x['fecha'])

    # Contratos que vencen en el año en curso
    contratos_proximos = Empleado.objects.filter(
        activo=True,
        fecha_vencimiento__isnull=False,
        fecha_vencimiento__year=hoy.year,
    ).order_by('fecha_vencimiento')

    solicitudes_pendientes = SolicitudAusencia.objects.filter(estado='pendiente').count()
    solicitudes_vacaciones = SolicitudAusencia.objects.filter(
        tipo='vacaciones', fecha_fin__gte=hoy
    ).exclude(estado='rechazada').count()
    solicitudes_dias = SolicitudAusencia.objects.filter(
        tipo__in=['libre', 'inamovible', 'libre_vacaciones', 'finde_largo'], fecha_fin__gte=hoy
    ).exclude(estado='rechazada').count()

    context = {
        'resumen_espacios': resumen_espacios,
        'total_espacios': espacios.count(),
        'eventos_proximos': eventos_proximos,
        'total_eventos_mes': total_eventos_mes,
        'total_personal': total_personal,
        'turnos_activos_hoy': turnos_hoy.count(),
        'eventos_esta_semana': eventos_esta_semana,
        'total_notas': Nota.objects.count(),
        'vacaciones_proximas': vacaciones_proximas,
        'dias_sueltos_proximos': dias_sueltos_proximos,
        'cumpleanos_proximos': cumpleanos_proximos,
        'contratos_proximos': contratos_proximos,
        'solicitudes_pendientes': solicitudes_pendientes,
        'solicitudes_vacaciones': solicitudes_vacaciones,
        'solicitudes_dias': solicitudes_dias,
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

def nuevo_evento(request):
    espacios = Espacio.objects.filter(activo=True)
    if request.method == 'POST':
        evento = Evento.objects.create(
            cliente=request.POST.get('cliente', '').strip(),
            tipo=request.POST.get('tipo', ''),
            fecha=request.POST.get('fecha'),
            concepto=request.POST.get('concepto', ''),
            personas=request.POST.get('personas', 0),
            notas=request.POST.get('notas', '').strip(),
        )
        evento.espacios.set(request.POST.getlist('espacios'))
        return redirect('lista_eventos')
    return render(request, 'core/form_evento.html', {
        'espacios': espacios,
        'tipos': Evento.TIPO_CHOICES,
        'conceptos': Evento.CONCEPTO_CHOICES,
        'evento': None,
        'fecha_inicial': request.GET.get('fecha', ''),
    })

def editar_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    espacios = Espacio.objects.filter(activo=True)
    if request.method == 'POST':
        evento.cliente = request.POST.get('cliente', '').strip()
        evento.tipo = request.POST.get('tipo', '')
        evento.fecha = request.POST.get('fecha')
        evento.concepto = request.POST.get('concepto', '')
        evento.personas = request.POST.get('personas', 0)
        evento.notas = request.POST.get('notas', '').strip()
        evento.save()
        evento.espacios.set(request.POST.getlist('espacios'))
        return redirect('lista_eventos')
    return render(request, 'core/form_evento.html', {
        'espacios': espacios,
        'tipos': Evento.TIPO_CHOICES,
        'conceptos': Evento.CONCEPTO_CHOICES,
        'evento': evento,
        'fecha_inicial': '',
    })

def eliminar_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    if request.method == 'POST':
        evento.delete()
    return redirect('lista_eventos')

def detalle_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    documentos = evento.documentos.all()
    rangos = evento.rangos.all()
    return render(request, 'core/detalle_evento.html', {
        'evento': evento,
        'documentos': documentos,
        'rangos': rangos,
        'plano_json': evento.plano_json or '',
    })

def nuevo_rango(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        if nombre:
            EventoRango.objects.create(evento=evento, nombre=nombre, orden=evento.rangos.count())
    return redirect('detalle_evento', pk=pk)

def eliminar_rango(request, rango_pk):
    rango = get_object_or_404(EventoRango, pk=rango_pk)
    evento_pk = rango.evento.pk
    if request.method == 'POST':
        rango.delete()
    return redirect('detalle_evento', pk=evento_pk)

def nuevo_camarero(request, rango_pk):
    rango = get_object_or_404(EventoRango, pk=rango_pk)
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        funcion = request.POST.get('funcion', '').strip()
        if nombre:
            EventoCamarero.objects.create(rango=rango, nombre=nombre, funcion=funcion)
    return redirect('detalle_evento', pk=rango.evento.pk)

def editar_camarero(request, camarero_pk):
    camarero = get_object_or_404(EventoCamarero, pk=camarero_pk)
    evento_pk = camarero.rango.evento.pk
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        funcion = request.POST.get('funcion', '').strip()
        if nombre:
            camarero.nombre = nombre
            camarero.funcion = funcion
            camarero.save()
    return redirect('detalle_evento', pk=evento_pk)

def eliminar_camarero(request, camarero_pk):
    camarero = get_object_or_404(EventoCamarero, pk=camarero_pk)
    evento_pk = camarero.rango.evento.pk
    if request.method == 'POST':
        camarero.delete()
    return redirect('detalle_evento', pk=evento_pk)

def resumen_mesas(request, pk):
    import json as _json, re as _re
    evento = get_object_or_404(Evento, pk=pk)
    TIPOS_DISPONIBLES = [
        ('mesa-redonda', 'Mesas redondas'),
        ('mesa-rect',    'Mesas rectangulares'),
        ('coctel',       'Mesas cóctel'),
    ]
    # Por defecto solo mesas (no cóctel); el usuario puede activar con ?tipos=
    tipos_activos = request.GET.getlist('tipos') or ['mesa-redonda', 'mesa-rect']
    mesas = []
    if evento.plano_json:
        try:
            data = _json.loads(evento.plano_json)
            for o in data.get('objects', []):
                if o.get('_tipo') in tipos_activos and o.get('_etiqueta'):
                    info = o.get('_info') or {}
                    rango_raw = info.get('rango', '')
                    rango = _re.sub(r'\s*\([^)]*\)$', '', rango_raw).strip()
                    mesas.append({
                        'etiqueta': o.get('_etiqueta', ''),
                        'tipo':     o.get('_tipo', ''),
                        'rango': rango,
                        'pax': info.get('pax', ''),
                        'carne': info.get('carne', ''),
                        'pescado': info.get('pescado', ''),
                        'veg': info.get('veg', ''),
                        'infantil': info.get('infantil', ''),
                        'celiaco': info.get('celiaco', ''),
                        'alergico': info.get('alergico', ''),
                        'notas': info.get('notas', ''),
                    })
            mesas.sort(key=lambda m: (m['rango'] or 'zzz', m['etiqueta']))
        except Exception:
            pass
    rangos = evento.rangos.prefetch_related('camareros').all()
    return render(request, 'core/resumen_mesas.html', {
        'evento': evento,
        'mesas': mesas,
        'rangos': rangos,
        'tipos_disponibles': TIPOS_DISPONIBLES,
        'tipos_activos': tipos_activos,
    })

def guardar_plano(request, pk):
    import json as _json
    evento = get_object_or_404(Evento, pk=pk)
    if request.method == 'POST':
        try:
            data = _json.loads(request.body)
            evento.plano_json = _json.dumps(data.get('plano', {}))
            evento.save(update_fields=['plano_json'])
            return JsonResponse({'ok': True})
        except Exception as e:
            return JsonResponse({'ok': False, 'error': str(e)}, status=400)
    return JsonResponse({'ok': False}, status=405)

def subir_documento(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    if request.method == 'POST' and request.FILES.get('archivo'):
        archivo = request.FILES['archivo']
        nombre = request.POST.get('nombre', '').strip() or archivo.name
        EventoDocumento.objects.create(evento=evento, archivo=archivo, nombre=nombre)
    return redirect('detalle_evento', pk=pk)

def eliminar_documento(request, doc_pk):
    doc = get_object_or_404(EventoDocumento, pk=doc_pk)
    evento_pk = doc.evento.pk
    if request.method == 'POST':
        doc.archivo.delete(save=False)
        doc.delete()
    return redirect('detalle_evento', pk=evento_pk)

def calendario(request):
    return render(request, 'core/calendario.html')

def agenda(request):
    if request.method == 'POST':
        texto = request.POST.get('texto', '').strip()
        if texto:
            Nota.objects.create(texto=texto)
        return redirect('agenda')
    notas = Nota.objects.all()
    return render(request, 'core/agenda.html', {'notas': notas})

def eliminar_nota(request, pk):
    nota = get_object_or_404(Nota, pk=pk)
    if request.method == 'POST':
        nota.delete()
    return redirect('agenda')

def lista_espacios(request):
    espacios = Espacio.objects.filter(activo=True)
    return render(request, 'core/lista_espacios.html', {'espacios': espacios})

def detalle_espacio(request, pk):
    espacio = get_object_or_404(Espacio, pk=pk)
    hoy = timezone.now().date()

    # Permitir ver/asignar otro día via ?fecha=
    fecha_param = request.GET.get('fecha')
    try:
        from datetime import date
        año, mes, dia = fecha_param.split('-')
        fecha = date(int(año), int(mes), int(dia))
    except:
        fecha = hoy

    empleados_disponibles = Turno.objects.filter(
        fecha=fecha,
        estado='trabajo',
        espacio__isnull=True
    ).select_related('empleado')

    turno_asignado = Turno.objects.filter(
        fecha=fecha,
        estado='trabajo',
        espacio=espacio
    ).select_related('empleado')

    # Generar TareaDelDia solo para hoy
    if fecha == hoy:
        plantillas = TareaPlantilla.objects.filter(espacio=espacio, activa=True)
        for plantilla in plantillas:
            TareaDelDia.objects.get_or_create(plantilla=plantilla, fecha=hoy)

    tareas_hoy = TareaDelDia.objects.filter(
        plantilla__espacio=espacio,
        fecha=fecha
    ).select_related('plantilla').order_by('plantilla__momento', 'plantilla__orden')

    otros_espacios = Espacio.objects.filter(activo=True).exclude(pk=espacio.pk)

    context = {
        'espacio': espacio,
        'empleados_disponibles': empleados_disponibles,
        'turno_asignado': turno_asignado,
        'tareas_hoy': tareas_hoy,
        'fecha': fecha,
        'hoy': hoy,
        'es_hoy': fecha == hoy,
        'otros_espacios': otros_espacios,
    }
    return render(request, 'core/detalle_espacio.html', context)

def desasignar_empleado(request, pk, turno_id):
    if request.method == 'POST':
        turno = get_object_or_404(Turno, pk=turno_id)
        turno.espacio = None
        turno.save()
    fecha = request.GET.get('fecha', '')
    url = redirect('detalle_espacio', pk=pk).url
    if fecha:
        url += f'?fecha={fecha}'
    return redirect(url)

def mover_empleado(request, pk, turno_id):
    if request.method == 'POST':
        turno = get_object_or_404(Turno, pk=turno_id)
        nuevo_espacio_id = request.POST.get('espacio_id')
        if nuevo_espacio_id:
            turno.espacio = get_object_or_404(Espacio, pk=nuevo_espacio_id)
            turno.save()
    fecha = request.GET.get('fecha', '')
    url = redirect('detalle_espacio', pk=pk).url
    if fecha:
        url += f'?fecha={fecha}'
    return redirect(url)

def toggle_tarea(request, pk):
    if request.method == 'POST':
        tarea = get_object_or_404(TareaDelDia, pk=pk)
        tarea.completada = not tarea.completada
        tarea.save()
        return JsonResponse({'completada': tarea.completada})
    return JsonResponse({'error': 'método no permitido'}, status=405)

def asignar_empleado(request, pk):
    if request.method == 'POST':
        espacio = get_object_or_404(Espacio, pk=pk)
        turno_id = request.POST.get('turno_id')
        if turno_id:
            turno = get_object_or_404(Turno, pk=turno_id)
            turno.espacio = espacio
            turno.save()
    fecha = request.GET.get('fecha', '')
    url = redirect('detalle_espacio', pk=pk).url
    if fecha:
        url += f'?fecha={fecha}'
    return redirect(url)

def pedidos_espacio(request, pk):
    espacio = get_object_or_404(Espacio, pk=pk)
    articulos = ArticuloPedido.objects.filter(espacio=espacio)
    return render(request, 'core/pedidos_espacio.html', {
        'espacio': espacio,
        'articulos': articulos,
    })

def nuevo_articulo(request, pk):
    espacio = get_object_or_404(Espacio, pk=pk)
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        if nombre:
            ArticuloPedido.objects.create(espacio=espacio, nombre=nombre, cantidad=0)
        return redirect('pedidos_espacio', pk=pk)
    return render(request, 'core/nuevo_articulo.html', {'espacio': espacio})

def editar_articulo(request, pk):
    articulo = get_object_or_404(ArticuloPedido, pk=pk)
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        if nombre:
            articulo.nombre = nombre
            articulo.save()
        return redirect('pedidos_espacio', pk=articulo.espacio.pk)
    return render(request, 'core/editar_articulo.html', {'articulo': articulo})

def eliminar_articulo(request, pk):
    articulo = get_object_or_404(ArticuloPedido, pk=pk)
    espacio_pk = articulo.espacio.pk
    if request.method == 'POST':
        articulo.delete()
    return redirect('pedidos_espacio', pk=espacio_pk)

def actualizar_cantidad(request, pk):
    if request.method == 'POST':
        articulo = get_object_or_404(ArticuloPedido, pk=pk)
        accion = request.POST.get('accion')
        if accion == 'subir':
            articulo.cantidad += 1
        elif accion == 'bajar' and articulo.cantidad > 0:
            articulo.cantidad -= 1
        elif accion == 'set':
            try:
                articulo.cantidad = max(0, int(request.POST.get('valor', 0)))
            except ValueError:
                pass
        articulo.save()
        return JsonResponse({'cantidad': articulo.cantidad})
    return JsonResponse({'error': 'método no permitido'}, status=405)
