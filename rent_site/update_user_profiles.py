# update_user_profiles.py
import os
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rent_site.settings')
django.setup()

from django.contrib.auth.models import User
from listings.models import UserProfile  # Замените 'listings' на имя вашего приложения

# Список пользователей для обновления
usernames = ['rubila34', 'rubila341', 'admin', 'romark', 'romarkill', 'romarkadd']

# Получаем всех пользователей
users = User.objects.filter(username__in=usernames)

# Обновляем или создаем UserProfile для каждого пользователя
for user in users:
    profile, created = UserProfile.objects.get_or_create(user=user)
    profile.role = 'landlord'
    profile.save()
    if created:
        print(f"UserProfile created and role set to 'landlord' for user: {user.username}")
    else:
        print(f"UserProfile updated to 'landlord' for user: {user.username}")

print("User profiles updated.")
