"""Copia de seguridad completa de AuryApp en un JSON.

Mismo formato que el export de Mi Cartera (Crypto_Portafolio): cabecera con
schema/version/fecha + todo el estado. Incluye los planos de mesas (Evento.plano_json,
con el _info de cada mesa). Los usuarios van SIN contraseña. Los documentos adjuntos
de eventos viven en Cloud Storage: aquí solo va su referencia.
"""
import json
from django.contrib.auth.models import User
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.db import connection
from django.db.migrations.recorder import MigrationRecorder
from django.utils import timezone

from core.models import Espacio, Evento, EventoRango, EventoCamarero, EventoDocumento, Nota, ArticuloPedido
from personal.models import Empleado, Turno, HoraExtra, SolicitudAusencia
from tareas.models import TareaPlantilla, TareaDelDia

SCHEMA = 'auryapp'
VERSION = 1

# Orden de dependencias: cada modelo va después de aquellos a los que apunta.
MODELOS = [
    Espacio, Evento, EventoRango, EventoCamarero, EventoDocumento, Nota, ArticuloPedido,
    Empleado, Turno, HoraExtra, SolicitudAusencia,
    TareaPlantilla, TareaDelDia,
]

CAMPOS_USUARIO = ['username', 'first_name', 'last_name', 'email',
                  'is_staff', 'is_superuser', 'is_active', 'date_joined']


def construir_copia():
    # Una tabla que aún no existe en esa BD (p. ej. producción antes de aplicar la
    # migración que la crea) se omite y se anota. Cualquier otro error se propaga:
    # mejor que la copia falle a que salga incompleta sin avisar.
    tablas = set(connection.introspection.table_names())
    datos, omitidos = {}, []
    for modelo in MODELOS:
        etiqueta = modelo._meta.label  # p. ej. 'core.Evento'
        if modelo._meta.db_table not in tablas:
            omitidos.append(etiqueta)
            continue
        datos[etiqueta] = serializers.serialize('python', modelo.objects.order_by('pk'))

    migraciones = {}
    for app in ('core', 'personal', 'tareas'):
        migraciones[app] = sorted(
            MigrationRecorder.Migration.objects.filter(app=app).values_list('name', flat=True)
        )

    return {
        'schema': SCHEMA,
        'version': VERSION,
        'exportedAt': timezone.now().isoformat(),
        'migraciones': migraciones,
        'usuarios': list(User.objects.order_by('pk').values(*CAMPOS_USUARIO)),
        'conteo': {etiqueta: len(filas) for etiqueta, filas in datos.items()},
        'omitidos': omitidos,
        'datos': datos,
    }


def copia_a_json(copia):
    return json.dumps(copia, cls=DjangoJSONEncoder, ensure_ascii=False, indent=2)


def nombre_fichero():
    return f"auryapp-{timezone.localdate().isoformat()}.json"
