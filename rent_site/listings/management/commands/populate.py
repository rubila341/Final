import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from listings.models import Listing

class Command(BaseCommand):
    help = 'Populate the database with random listings'

    def handle(self, *args, **kwargs):
        locations = ['Berlin', 'Munich', 'Hamburg', 'Cologne', 'Frankfurt']
        property_types = ['apartment', 'house', 'studio', 'villa', 'cottage']

        # Получаем существующего пользователя
        try:
            owner = User.objects.get(username='rubila34')
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('User rubila34 does not exist. Please create the user first.'))
            return

        for _ in range(10):
            title = f"Property {random.randint(1, 1000)}"
            description = "A cozy place in a great location. Perfect for you!"
            location = random.choice(locations)
            price = random.randint(100000, 1000000)
            rooms = random.randint(1, 5)
            property_type = random.choice(property_types)

            Listing.objects.create(
                title=title,
                description=description,
                location=location,
                price=price,
                rooms=rooms,
                property_type=property_type,
                owner=owner  # Указываем владельца
            )

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with listings'))
