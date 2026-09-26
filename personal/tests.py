from decimal import Decimal
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Empleado, HoraExtra


def _empleado():
    return Empleado.objects.create(nombre='Test', apellidos='Empleado', rol='camarero')


class HorasExtraTests(TestCase):

    def setUp(self):
        self.staff = User.objects.create_user('staff', password='x', is_staff=True)
        self.client = Client()
        self.client.force_login(self.staff)
        self.empleado = _empleado()

    def _url_añadir(self):
        return reverse('añadir_hora_extra', args=[self.empleado.pk])

    def _añadir(self, inicio, fin, motivo='Boda', fecha='2026-09-10', client=None):
        return (client or self.client).post(self._url_añadir(), {
            'fecha': fecha, 'hora_inicio': inicio, 'hora_fin': fin, 'motivo': motivo,
        })

    def _detalle(self):
        return self.client.get(reverse('detalle_empleado', args=[self.empleado.pk]))

    def test_añade_y_redondea_a_media_hora(self):
        resp = self._añadir('09:00', '11:20')
        self.assertRedirects(resp, reverse('detalle_empleado', args=[self.empleado.pk]),
                             fetch_redirect_response=False)
        hora = HoraExtra.objects.get(empleado=self.empleado)
        self.assertEqual(hora.horas, Decimal('2.5'))
        self.assertFalse(hora.pagadas)

    def test_hora_exacta(self):
        self._añadir('18:00', '19:00')
        self.assertEqual(HoraExtra.objects.get(empleado=self.empleado).horas, Decimal('1.0'))

    def test_minimo_media_hora(self):
        self._añadir('10:00', '10:05')
        self.assertEqual(HoraExtra.objects.get(empleado=self.empleado).horas, Decimal('0.5'))

    def test_fin_antes_de_inicio_no_crea(self):
        self._añadir('12:00', '10:00')
        self.assertFalse(HoraExtra.objects.exists())

    def test_sin_motivo_no_crea(self):
        self._añadir('12:00', '13:00', motivo='   ')
        self.assertFalse(HoraExtra.objects.exists())

    def test_usuario_no_staff_no_puede_añadir(self):
        normal = User.objects.create_user('normal', password='x', is_staff=False)
        c = Client()
        c.force_login(normal)
        resp = self._añadir('09:00', '10:00', client=c)
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(resp['Location'].startswith('/login/'))
        self.assertFalse(HoraExtra.objects.exists())

    def test_ficha_agrupa_por_mes_y_suma_pendiente(self):
        self._añadir('09:00', '11:20', motivo='Boda', fecha='2026-09-10')
        self._añadir('18:00', '19:00', motivo='Cena', fecha='2026-08-05')
        resp = self._detalle()
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Boda')
        self.assertContains(resp, 'Cena')
        self.assertEqual(resp.context['total_pendiente'], Decimal('3.5'))
        meses = resp.context['meses_horas']
        self.assertEqual([(m['año'], m['mes']) for m in meses], [(2026, 9), (2026, 8)])

    def test_lista_empleados_muestra_pendiente(self):
        self._añadir('09:00', '11:20', fecha='2026-09-10')
        self._añadir('18:00', '19:00', fecha='2026-08-05')
        resp = self.client.get(reverse('lista_empleados'))
        self.assertEqual(resp.status_code, 200)
        emp = next(e for e in resp.context['empleados'] if e.pk == self.empleado.pk)
        self.assertEqual(emp.horas_pendientes, Decimal('3.5'))
        self.assertRegex(resp.content.decode(), r'3[.,]5')

    def test_liquidar_solo_marca_ese_mes(self):
        self._añadir('09:00', '11:20', fecha='2026-09-10')
        self._añadir('18:00', '19:00', fecha='2026-08-05')
        self.client.post(reverse('liquidar_mes_horas', args=[self.empleado.pk]),
                         {'año': '2026', 'mes': '9'})
        sep = HoraExtra.objects.get(fecha__month=9)
        ago = HoraExtra.objects.get(fecha__month=8)
        self.assertTrue(sep.pagadas)
        self.assertFalse(ago.pagadas)
        self.assertEqual(self._detalle().context['total_pendiente'], Decimal('1.0'))

    def test_eliminar_solo_con_post(self):
        self._añadir('09:00', '10:00')
        hora = HoraExtra.objects.get()
        url = reverse('eliminar_hora_extra', args=[hora.pk])
        self.client.get(url)
        self.assertTrue(HoraExtra.objects.filter(pk=hora.pk).exists())
        self.client.post(url)
        self.assertFalse(HoraExtra.objects.filter(pk=hora.pk).exists())
