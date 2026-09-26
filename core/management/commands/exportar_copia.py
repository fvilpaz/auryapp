from pathlib import Path
from django.core.management.base import BaseCommand
from core.backup import construir_copia, copia_a_json, nombre_fichero


class Command(BaseCommand):
    help = 'Guarda una copia de seguridad completa (JSON) de la BD a la que apunte DATABASE_URL.'

    def add_arguments(self, parser):
        parser.add_argument('--carpeta', default='.', help='Carpeta de destino (por defecto, la actual)')

    def handle(self, *args, **opts):
        carpeta = Path(opts['carpeta'])
        carpeta.mkdir(parents=True, exist_ok=True)
        copia = construir_copia()
        destino = carpeta / nombre_fichero()
        if destino.exists():
            # Varias copias el mismo día: no pisar la anterior
            n = 2
            while (carpeta / f'{destino.stem}-{n}.json').exists():
                n += 1
            destino = carpeta / f'{destino.stem}-{n}.json'
        destino.write_text(copia_a_json(copia), encoding='utf-8')
        total = sum(copia['conteo'].values())
        self.stdout.write(f'Copia guardada en {destino} ({total} registros, {len(copia["usuarios"])} usuarios)')
        for etiqueta, n in copia['conteo'].items():
            self.stdout.write(f'  {etiqueta}: {n}')
