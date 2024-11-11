from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

# Модель для городов, включающая основную информацию и координаты
class City(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Уникальное название города
    country = models.CharField(max_length=100, default='Unknown')  # Страна
    latitude = models.FloatField(null=True, blank=True)  # Широта
    longitude = models.FloatField(null=True, blank=True)  # Долгота

    def __str__(self):
        return f"{self.name}, {self.country}"

    def get_full_address(self):
        return f"{self.name}, {self.country}"  # Возвращаем полный адрес города

    class Meta:
        ordering = ['name']  # Сортировка по имени города


# Модель для объявления
class Listing(models.Model):
    # Тип недвижимости с вариантами выбора
    PROPERTY_TYPE_CHOICES = [
        ('apartment', 'Apartment'),
        ('house', 'House'),
        ('studio', 'Studio'),
        ('villa', 'Villa'),
        ('cottage', 'Cottage'),
    ]

    title = models.CharField(max_length=200)  # Заголовок объявления
    description = models.TextField()  # Описание
    location = models.ForeignKey(City, on_delete=models.CASCADE)  # Связь с городом
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Цена
    rooms = models.PositiveIntegerField()  # Количество комнат
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPE_CHOICES)  # Тип недвижимости
    is_active = models.BooleanField(default=True)  # Активность объявления
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания
    updated_at = models.DateTimeField(auto_now=True)  # Дата последнего обновления
    owner = models.ForeignKey(User, on_delete=models.CASCADE)  # Владелец объявления
    image = models.ImageField(upload_to='listing_images/', blank=True, null=True)  # Изображение
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)  # Средний рейтинг
    review_count = models.PositiveIntegerField(default=0)  # Количество отзывов
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Скидочная цена

    def __str__(self):
        return f"{self.title} - {self.location.name}"

    # Деактивировать объявление
    def deactivate(self):
        self.is_active = False
        self.save()

    # Активировать объявление
    def activate(self):
        self.is_active = True
        self.save()

    # Обновить средний рейтинг объявления
    def update_rating(self):
        ratings = self.ratings.all()
        if ratings.exists():
            total_ratings = sum(rating.rating for rating in ratings)
            self.rating = total_ratings / ratings.count()
            self.review_count = ratings.count()
        else:
            self.rating = 0.0
            self.review_count = 0
        self.save()

    # Применить скидку, если активна
    def apply_discount(self):
        discount = Discount.objects.filter(listing=self, is_active=True).first()
        if discount:
            self.discounted_price = self.price - discount.amount
        else:
            self.discounted_price = self.price
        self.save()

    class Meta:
        ordering = ['-created_at']  # Сортировка по дате создания (новые - первыми)


# Модель скидок, привязанных к объявлениям
class Discount(models.Model):
    listing = models.ForeignKey('Listing', on_delete=models.CASCADE)  # Связь с объявлением
    applicable_to = models.CharField(max_length=255, default='All users')  # Для каких пользователей
    duration = models.DurationField(default=timedelta(days=30))  # Продолжительность скидки
    is_active = models.BooleanField(default=True)  # Активность скидки
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # Сумма скидки
    start_date = models.DateField(default=timezone.now)  # Дата начала
    end_date = models.DateField(null=True, blank=True)  # Дата окончания

    def __str__(self):
        return f"Discount for {self.listing}"

    # Сохраняем скидку и применяем её к объявлению
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.listing.apply_discount()

    # Метод для получения автоматической скидки в зависимости от бронирований пользователя
    @classmethod
    def get_automatic_discount(cls, user):
        completed_bookings = Booking.objects.filter(user=user, status='approved').count()
        if completed_bookings >= 15:
            return 10.0
        elif completed_bookings >= 5:
            return 5.0
        elif completed_bookings >= 1:
            return 1.0
        return 0.0

    class Meta:
        ordering = ['-listing']


# Модель отзывов
class Review(models.Model):
    listing = models.ForeignKey(Listing, related_name='reviews', on_delete=models.CASCADE)  # Связь с объявлением
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Автор отзыва
    rating = models.IntegerField(default=1)  # Рейтинг
    comment = models.TextField()  # Комментарий
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания
    updated_at = models.DateTimeField(auto_now=True)  # Дата последнего обновления

    def __str__(self):
        return f"Review by {self.user} on {self.listing} - {self.rating} stars"


# Модель бронирования
class Booking(models.Model):
    listing = models.ForeignKey(Listing, related_name='bookings', on_delete=models.CASCADE)  # Объявление
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Пользователь, сделавший бронирование
    start_date = models.DateField()  # Дата начала аренды
    end_date = models.DateField()  # Дата окончания аренды
    status = models.CharField(max_length=20,
                              choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')],
                              default='pending')  # Статус бронирования
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания
    booking_number = models.CharField(max_length=50, unique=True, null=True, blank=True)  # Уникальный номер бронирования

    def __str__(self):
        return f'{self.user} booked {self.listing} from {self.start_date} to {self.end_date}'

    # Применение автоматической скидки при бронировании
    def apply_automatic_discount(self):
        discount_percentage = Discount.get_automatic_discount(self.user)
        if discount_percentage > 0:
            self.listing.apply_discount(discount_percentage)

    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(fields=['user', 'listing', 'start_date', 'end_date'], name='unique_booking')
        ]


# Модель рейтинга
class Rating(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='ratings')  # Объявление
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Автор рейтинга
    rating = models.PositiveIntegerField(default=1)  # Оценка
    comment = models.TextField(blank=True, null=True)  # Комментарий
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания
    updated_at = models.DateTimeField(auto_now=True)  # Дата последнего обновления

    def __str__(self):
        return f'{self.user} rated {self.listing} with {self.rating}'

    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(fields=['listing', 'user'], name='unique_rating')
        ]


# Модель для чата между пользователями
class Chat(models.Model):
    participants = models.ManyToManyField(User)  # Участники чата
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания
    name = models.CharField(max_length=255, blank=True)  # Имя чата

    def __str__(self):
        return self.name or ', '.join(user.username for user in self.participants.all())

    def get_participants(self):
        return ', '.join(user.username for user in self.participants.all())  # Список участников чата

    class Meta:
        ordering = ['-created_at']


# Модель сообщений
class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages', null=True, blank=True)  # Чат
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')  # Отправитель
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages', null=True,
                                 blank=True)  # Получатель
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='messages', null=True, blank=True)  # Объявление
    content = models.TextField()  # Текст сообщения
    file = models.FileField(upload_to='messages/', blank=True, null=True)  # Вложение
    sent_at = models.DateTimeField(auto_now_add=True)  # Дата отправки
    is_read = models.BooleanField(default=False)  # Прочитано ли сообщение

    def __str__(self):
        return f"From {self.sender} to {self.receiver or 'Chat'} on {self.sent_at}"

    def get_sender_name(self):
        return self.sender.username

    def get_receiver_name(self):
        return self.receiver.username if self.receiver else 'Chat'

    class Meta:
        ordering = ['-sent_at']


# Модель активности пользователя
class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Пользователь
    action = models.CharField(max_length=255)  # Действие
    timestamp = models.DateTimeField(auto_now_add=True)  # Время действия
    activity_type = models.CharField(max_length=100, null=True)  # Тип активности
    details = models.TextField(blank=True, null=True)  # Дополнительные сведения

    def __str__(self):
        return f"{self.user} - {self.action} at {self.timestamp}"

    class Meta:
        ordering = ['-timestamp']
