import csv
from django.core.management.base import BaseCommand, CommandError
from formulario.models import Municipio

class Command(BaseCommand):
    help = 'Read a base of Brazilian municipalities'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            help='Place the path for the file with data from municipalities.',
        )
        parser.add_argument(
            '--prevent_duplicates',
            type=bool,
            help='Validate if database it is empty before execution. Prevent duplicates',
        )

    def handle(self, *args, **options):
        if options['file']:
            total_cities_in_database = Municipio.objects.count()
            execute_dataimport = (not bool(options['prevent_duplicates'])) or total_cities_in_database == 0

            if execute_dataimport:
                with open(options['file'], 'r') as f:
                    cities = csv.DictReader(f)
                    cities_list = []

                    for city in cities:
                        kwargs = {
                            'ibge': int(city['IBGE']),
                            'ibge7': int(city['IBGE7']),
                            'uf': city['UF'],
                            'municipio': city['Município'],
                            'regiao': city['Região'],
                            'populacao_2020': None if city['População 2020'] == '' else city['População 2020'],
                            'capital': city['Capital'] == 'Capital',
                        }
                        cities_list.append(Municipio(**kwargs))

                    Municipio.objects.bulk_create(cities_list)
                total_cities_read = Municipio.objects.count()
                self.stdout.write(self.style.SUCCESS(f'Successfully read data with {total_cities_read} cities'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Skipped read because database already have data with {total_cities_in_database} cities'))
        else:
            raise CommandError('Enter the file path: python manage.py read_data --file data.csv')
