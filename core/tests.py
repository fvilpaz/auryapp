import json
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Evento, Espacio


def _evento():
    espacio = Espacio.objects.create(nombre='Terraza')
    evento = Evento.objects.create(
        cliente='Test Cliente',
        tipo='boda',
        fecha='2026-09-01',
        concepto='cena',
        personas=100,
    )
    evento.espacios.add(espacio)
    return evento


def _plano_con_info(etiqueta='Mesa 1', info=None):
    """Devuelve un plano_json con una mesa que ya tiene _info."""
    return json.dumps({
        'objects': [{
            '_tipo': 'mesa-redonda',
            '_etiqueta': etiqueta,
            '_info': info or {'pax': 8, 'carne': 4, 'pescado': 4, 'alergias': ''},
            'objects': [{'type': 'text', 'text': etiqueta}],
        }]
    })


class GuardarPlanoTests(TestCase):

    def setUp(self):
        self.staff = User.objects.create_user('staff', password='x', is_staff=True)
        self.client = Client()
        self.client.force_login(self.staff)
        self.evento = _evento()

    def _url(self, pk=None):
        return reverse('guardar_plano', args=[pk or self.evento.pk])

    def _post(self, plano, pk=None):
        return self.client.post(
            self._url(pk),
            data=json.dumps({'plano': plano}),
            content_type='application/json',
        )

    def test_guarda_plano_vacio(self):
        resp = self._post({'objects': []})
        self.assertEqual(resp.status_code, 200)
        self.assertJSONEqual(resp.content, {'ok': True})
        self.evento.refresh_from_db()
        self.assertEqual(json.loads(self.evento.plano_json), {'objects': []})

    def test_preserva_info_al_guardar_estructura(self):
        """guardar_plano NUNCA debe sobreescribir _info guardado en BD."""
        info_original = {'pax': 8, 'carne': 4, 'pescado': 4, 'alergias': 'nueces'}
        self.evento.plano_json = _plano_con_info('Mesa 1', info_original)
        self.evento.save()

        # Llega un canvas nuevo que viene sin _info (como lo envía Fabric.js tras editar estructura)
        plano_nuevo = {
            'objects': [{
                '_tipo': 'mesa-redonda',
                '_etiqueta': 'Mesa 1',
                'objects': [{'type': 'text', 'text': 'Mesa 1'}],
            }]
        }
        self._post(plano_nuevo)
        self.evento.refresh_from_db()
        plano_bd = json.loads(self.evento.plano_json)
        info_guardada = plano_bd['objects'][0].get('_info')
        self.assertEqual(info_guardada, info_original,
                         "guardar_plano destruyó _info — regresión crítica")

    def test_get_devuelve_405(self):
        resp = self.client.get(self._url())
        self.assertEqual(resp.status_code, 405)

    def test_sin_autenticacion_redirige(self):
        c = Client()
        resp = c.post(self._url(), data='{}', content_type='application/json')
        self.assertRedirects(resp, f'/login/?next={self._url()}',
                             fetch_redirect_response=False)

    def test_evento_inexistente_devuelve_404(self):
        resp = self._post({}, pk=99999)
        self.assertEqual(resp.status_code, 404)


class GuardarInfoMesaTests(TestCase):

    def setUp(self):
        self.staff = User.objects.create_user('staff', password='x', is_staff=True)
        self.client = Client()
        self.client.force_login(self.staff)
        self.evento = _evento()
        self.evento.plano_json = _plano_con_info('Mesa 1', {'pax': 6})
        self.evento.save()

    def _url(self, pk=None):
        return reverse('guardar_info_mesa', args=[pk or self.evento.pk])

    def _post(self, payload):
        return self.client.post(
            self._url(),
            data=json.dumps(payload),
            content_type='application/json',
        )

    def test_actualiza_info_de_mesa(self):
        info_nueva = {'pax': 10, 'carne': 5, 'pescado': 5, 'alergias': ''}
        resp = self._post({'etiqueta': 'Mesa 1', 'info': info_nueva})
        self.assertEqual(resp.status_code, 200)
        self.assertJSONEqual(resp.content, {'ok': True})
        self.evento.refresh_from_db()
        plano = json.loads(self.evento.plano_json)
        self.assertEqual(plano['objects'][0]['_info'], info_nueva)

    def test_renombra_mesa_y_conserva_info(self):
        info = {'pax': 6, 'carne': 3, 'pescado': 3, 'alergias': ''}
        self.evento.plano_json = _plano_con_info('Mesa 1', info)
        self.evento.save()

        resp = self._post({'etiqueta': 'Mesa 1', 'nuevo_nombre': 'Mesa VIP', 'info': info})
        self.assertEqual(resp.status_code, 200)
        self.evento.refresh_from_db()
        plano = json.loads(self.evento.plano_json)
        mesa = plano['objects'][0]
        self.assertEqual(mesa['_etiqueta'], 'Mesa VIP')
        self.assertEqual(mesa['objects'][0]['text'], 'Mesa VIP')
        self.assertEqual(mesa['_info'], info)

    def test_get_devuelve_405(self):
        resp = self.client.get(self._url())
        self.assertEqual(resp.status_code, 405)

    def test_sin_autenticacion_redirige(self):
        c = Client()
        resp = c.post(self._url(), data='{}', content_type='application/json')
        self.assertRedirects(resp, f'/login/?next={self._url()}',
                             fetch_redirect_response=False)


class RegistroTests(TestCase):
    """El registro ya no es público: solo staff crea cuentas."""

    DATOS = {
        'first_name': 'Nuevo', 'last_name': 'Usuario', 'username': 'nuevo',
        'email': 'nuevo@example.com', 'password1': 'Clave-segura-123', 'password2': 'Clave-segura-123',
    }

    def setUp(self):
        self.url = reverse('registro')

    def test_anonimo_no_puede_registrarse(self):
        resp = Client().post(self.url, self.DATOS)
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(resp['Location'].startswith('/login/'))
        self.assertFalse(User.objects.filter(username='nuevo').exists())

    def test_usuario_no_staff_no_puede_registrar(self):
        normal = User.objects.create_user('normal', password='x')
        c = Client()
        c.force_login(normal)
        resp = c.post(self.url, self.DATOS)
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(resp['Location'].startswith('/login/'))
        self.assertFalse(User.objects.filter(username='nuevo').exists())

    def test_staff_crea_cuenta_sin_perder_su_sesion(self):
        staff = User.objects.create_user('staff', password='x', is_staff=True)
        c = Client()
        c.force_login(staff)
        resp = c.post(self.url, self.DATOS)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'nuevo')
        nuevo = User.objects.get(username='nuevo')
        self.assertFalse(nuevo.is_staff)
        self.assertEqual(int(c.session['_auth_user_id']), staff.pk)

    def test_login_no_enlaza_al_registro(self):
        resp = Client().get('/login/')
        self.assertEqual(resp.status_code, 200)
        self.assertNotContains(resp, self.url)


class ExportarCopiaTests(TestCase):
    """La copia incluye todos los datos (planos con _info incluidos) y nunca contraseñas."""

    def setUp(self):
        self.url = reverse('exportar_copia')
        self.staff = User.objects.create_user('staff', password='x', is_staff=True)
        self.evento = _evento()
        self.evento.plano_json = _plano_con_info('Mesa 1', {'pax': 8, 'alergias': 'nueces'})
        self.evento.save()

    def _descargar(self):
        c = Client()
        c.force_login(self.staff)
        return c.get(self.url)

    def test_staff_descarga_json_con_cabecera(self):
        resp = self._descargar()
        self.assertEqual(resp.status_code, 200)
        self.assertIn('attachment; filename="auryapp-', resp['Content-Disposition'])
        data = json.loads(resp.content)
        self.assertEqual(data['schema'], 'auryapp')
        self.assertEqual(data['version'], 1)
        self.assertIn('0001_initial', data['migraciones']['core'])

    def test_incluye_plano_con_info_y_espacios(self):
        data = json.loads(self._descargar().content)
        eventos = data['datos']['core.Evento']
        self.assertEqual(len(eventos), 1)
        plano = json.loads(eventos[0]['fields']['plano_json'])
        self.assertEqual(plano['objects'][0]['_info']['alergias'], 'nueces')
        self.assertEqual(len(eventos[0]['fields']['espacios']), 1)
        self.assertEqual(data['conteo']['core.Espacio'], 1)

    def test_usuarios_sin_contrasena(self):
        resp = self._descargar()
        data = json.loads(resp.content)
        self.assertEqual([u['username'] for u in data['usuarios']], ['staff'])
        self.assertNotIn('password', data['usuarios'][0])
        self.assertNotIn(self.staff.password, resp.content.decode())

    def test_no_staff_no_puede_descargar(self):
        normal = User.objects.create_user('normal', password='x')
        c = Client()
        c.force_login(normal)
        resp = c.get(self.url)
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(resp['Location'].startswith('/login/'))

    def test_anonimo_no_puede_descargar(self):
        resp = Client().get(self.url)
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(resp['Location'].startswith('/login/'))

    def test_la_copia_incluye_todos_los_modelos_de_la_app(self):
        """Si se crea un modelo nuevo y no se añade a backup.MODELOS, sus datos no irían en la copia."""
        from django.apps import apps
        from .backup import MODELOS
        todos = {m for app in ('core', 'personal', 'tareas') for m in apps.get_app_config(app).get_models()}
        self.assertEqual(todos - set(MODELOS), set(), 'Modelos que faltan en core/backup.py MODELOS')


class IconosTests(TestCase):
    """El favicon debe verse también sin sesión (login) y /favicon.ico no puede ir al login."""

    def test_favicon_ico_publico(self):
        resp = Client().get('/favicon.ico')
        self.assertEqual(resp.status_code, 301)
        self.assertIn('img/icons/favicon', resp['Location'])
        self.assertFalse(resp['Location'].startswith('/login/'))

    def test_login_enlaza_iconos(self):
        resp = Client().get('/login/')
        self.assertContains(resp, 'img/icons/favicon-32')
        self.assertContains(resp, 'apple-touch-icon')

    def test_app_enlaza_iconos(self):
        staff = User.objects.create_user('staff', password='x', is_staff=True)
        c = Client()
        c.force_login(staff)
        resp = c.get(reverse('dashboard'))
        self.assertContains(resp, 'img/icons/favicon-32')


class PwaTests(TestCase):
    """Manifest y service worker: públicos, sin caché y con la versión del despliegue."""

    def test_manifest_publico_y_valido(self):
        from django.contrib.staticfiles import finders
        resp = Client().get('/manifest.webmanifest')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp['Content-Type'], 'application/manifest+json')
        data = json.loads(resp.content)
        self.assertEqual(data['start_url'], '/')
        self.assertEqual(data['display'], 'standalone')
        tamaños = {i['sizes'] for i in data['icons']}
        self.assertTrue({'192x192', '512x512'} <= tamaños)
        self.assertIn('maskable', {i['purpose'] for i in data['icons']})
        for icono in data['icons']:
            ruta = icono['src'].replace('/static/', '', 1)
            self.assertIsNotNone(finders.find(ruta), f'no existe {ruta}')

    def test_service_worker_publico_sin_cache_y_versionado(self):
        from django.contrib.staticfiles import finders
        from . import pwa
        resp = Client().get('/sw.js')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('javascript', resp['Content-Type'])
        self.assertIn('no-cache', resp['Cache-Control'])
        js = resp.content.decode()
        self.assertIn(f'const VERSION = "{pwa.VERSION}";', js)
        for ruta in pwa.PRECACHE:
            self.assertIsNotNone(finders.find(ruta), f'precache apunta a un fichero que no existe: {ruta}')
            self.assertIn(f'"/static/{ruta}"', js)

    def test_la_version_sale_de_k_revision(self):
        import importlib, os
        from . import pwa
        antes = os.environ.get('K_REVISION')
        try:
            os.environ['K_REVISION'] = 'auryapp-00042-abc'
            importlib.reload(pwa)
            self.assertEqual(pwa.VERSION, 'auryapp-00042-abc')
        finally:
            if antes is None:
                os.environ.pop('K_REVISION', None)
            else:
                os.environ['K_REVISION'] = antes
            importlib.reload(pwa)

    def test_paginas_enlazan_manifest_y_registran_sw(self):
        resp = Client().get('/login/')
        self.assertContains(resp, 'rel="manifest"')
        self.assertContains(resp, "register('/sw.js')")
        staff = User.objects.create_user('staff', password='x', is_staff=True)
        c = Client()
        c.force_login(staff)
        self.assertContains(c.get(reverse('dashboard')), 'rel="manifest"')
