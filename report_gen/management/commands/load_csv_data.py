from django.core.management.base import BaseCommand
import csv
from report_gen.models import StoreStatus, StoreBusinessHours, StoreTimezone


class Command(BaseCommand):
    help = 'Load data from CSVs into the database'

    def add_arguments(self, parser):
        parser.add_argument('--stores', type=str, help="Path to the stores CSV")
        parser.add_argument('--hours', type=str, help="Path to the business hours CSV")
        parser.add_argument('--timezones', type=str, help="Path to the timezones CSV")

    def handle(self, *args, **options):
        # Load data from stores.csv
        with open(options['stores'], 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                StoreStatus.objects.create(
                    store_id=row['store_id'],
                    status=row['status']
                )

        # Load data from hours.csv
        with open(options['hours'], 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                StoreBusinessHours.objects.create(
                    store_id=row['store_id'],
                    dayOfWeek=row['dayOfWeek'],
                    start_time_local=row['start_time_local'],
                    end_time_local=row['end_time_local']
                )

        # Load data from timezones.csv
        with open(options['timezones'], 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                StoreTimezone.objects.create(
                    store_id=row['store_id'],
                    timezone_str=row['timezone_str']
                )

        self.stdout.write(self.style.SUCCESS('Successfully loaded data from CSVs'))
