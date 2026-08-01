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
