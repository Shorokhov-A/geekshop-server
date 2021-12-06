from django.core.management.base import BaseCommand
from products.models import Product
from django.db import connection
from django.db.models import Q
from products.views import db_profile_by_type


class Command(BaseCommand):
    def handle(self, *args, **options):
        test_products = Product.objects.filter(
            Q(category__name='Одежда') |
            Q(category__name='Аксессуары')
        )
        print(len(test_products))
        # print(test_products)
        db_profile_by_type('learn db', '', connection.queries)