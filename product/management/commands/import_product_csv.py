import csv
from pathlib import Path
from django.core.management.base import BaseCommand
from product.models import Product
from django.conf import settings

class Command(BaseCommand):
    help = 'Import products from a CSV file'

    def handle(self, *args, **kwargs):
        csv_file_path = Path(settings.MEDIA_ROOT) / 'products_info' / 'products.csv'
        
        if not csv_file_path:
            self.stdout.write(self.style.ERROR('CSV file not found'))
            return
        
        products = []
        with open(csv_file_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                product = Product(
                    name=row['name'],
                    year=int(row['year']),
                    price=float(row['price']),
                    km_driven=int(row['km_driven']),
                    image_url=row['image_url'],
                    dealer=row['dealer']
                )
                products.append(product)
        
        Product.objects.bulk_create(products)
        self.stdout.write(self.style.SUCCESS(f'Successfully added {len(products)} products.'))