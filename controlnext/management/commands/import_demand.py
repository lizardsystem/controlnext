import csv

from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from controlnext import models

class Command(BaseCommand):
    help = '''Insert or update demands per grower
    from csv-file.'''
    
    option_list = BaseCommand.option_list + (
        make_option('--f',
                    default=None,
                    help='csv-filepath with demands.'),
    )                
        
    def handle(self, *args, **options):
        filepath = options.get('f', None)
        if filepath is None:
            self.stdout.write('Tell me where is the csv-file with demands.')
            return
        self.stdout.write('Start import.')
        with open(filepath, 'rb') as f:
            reader = csv.DictReader(f,skipinitialspace=True, delimiter=';')
            count = 0
            for row in reader:
                if row['grower_id'] in [None, '']:
                    continue
                if row['day_number'] in [None, '']:
                    continue
                if row['week_number'] in [None, '']:
                    continue
                self.insert_or_update_demand(row)
        self.stdout.write('Successfully passed.')

    def insert_or_update_demand(self, row):
        """."""
        demand = None
        try:
            demand = models.WaterDemand.objects.get(
                **{'owner__id': row['grower_id'],
                   'daynumber': row['day_number']}
            )
            demand.demand = row['evaporation']
            demand.weeknumber = row['week_number']
            demand.save()
            self.stdout.write('Update demand.')
        except Exception, ex:
            demand = models.WaterDemand(
                grower=models.Basin.objects.get(pk=row['grower_id']),
                daynumber=row['day_number'],
                demand=row['evaporation'],
                weeknumber=row['week_number'])
            demand.save()
            self.stdout.write('Add a new demand.')
