from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


class City(models.Model):
    name = models.CharField(max_length=100, unique=True)
    country = models.CharField(max_length=100, default='Unknown')
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.name}, {self.country}"

    def get_full_address(self):
        return f"{self.name}, {self.country}"

    class Meta:
        ordering = ['name']


class Listing(models.Model):
    PROPERTY_TYPE_CHOICES = [
        ('apartment', 'Apartment'),
        ('house', 'House'),
        ('studio', 'Studio'),
        ('villa', 'Villa'),
        ('cottage', 'Cottage'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.ForeignKey(City, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rooms = models.PositiveIntegerField()
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPE_CHOICES)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='listing_images/', blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    review_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.title} - {self.location.name}"

    def deactivate(self):
        self.is_active = False
        self.save()

    def activate(self):
        self.is_active = True
        self.save()

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

    class Meta:
        ordering = ['-created_at']


class Discount(models.Model):
    listing = models.ForeignKey('Listing', on_delete=models.CASCADE)
    applicable_to = models.CharField(max_length=255, default='All users')
    duration = models.DurationField(default=timedelta(days=30))  # Длительность действия скидки
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Discount for {self.listing}"

    @classmethod
    def get_automatic_discount(cls, user):
        completed_bookings = Booking.objects.filter(user=user, status='approved').count()

        if completed_bookings >= 10:
            return 10.0
        elif completed_bookings >= 5:
            return 5.0
        elif completed_bookings >= 1:
            return 1.0
        return 0.0

    def is_valid(self, booking_date):
        # Скидка действительна, если она активна и срок действия не истек
        return self.is_active and (booking_date <= (self.duration.total_seconds() + self.created_at.timestamp()))

    class Meta:
        ordering = ['-listing']


class Review(models.Model):
    listing = models.ForeignKey(Listing, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=1)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review by {self.user} on {self.listing} - {self.rating} stars"


class Booking(models.Model):
    listing = models.ForeignKey(Listing, related_name='bookings', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20,
                              choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')],
                              default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    booking_number = models.CharField(max_length=50, unique=True, null=True, blank=True)

    def __str__(self):
        return f'{self.user} booked {self.listing} from {self.start_date} to {self.end_date}'

    def apply_automatic_discount(self):
        discount_percentage = Discount.get_automatic_discount(self.user)
        if discount_percentage > 0:
            Discount.objects.create(
                listing=self.listing,
                discount_percentage=discount_percentage,
                start_date=self.start_date,
                end_date=self.end_date,
                is_active=True
            )

    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(fields=['user', 'listing', 'start_date', 'end_date'], name='unique_booking')
        ]


class Rating(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=1)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user} rated {self.listing} with {self.rating}'

    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(fields=['listing', 'user'], name='unique_rating')
        ]


class Chat(models.Model):
    participants = models.ManyToManyField(User)
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name or ', '.join(user.username for user in self.participants.all())

    def get_participants(self):
        return ', '.join(user.username for user in self.participants.all())

    class Meta:
        ordering = ['-created_at']


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages', null=True, blank=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages', null=True,
                                 blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='messages', null=True, blank=True)
    content = models.TextField()
    file = models.FileField(upload_to='messages/', blank=True, null=True)
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"From {self.sender} to {self.receiver or 'Chat'} on {self.sent_at}"

    def get_sender_name(self):
        return self.sender.username

    def get_receiver_name(self):
        return self.receiver.username if self.receiver else 'Chat'

    class Meta:
        ordering = ['-sent_at']


class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    activity_type = models.CharField(max_length=100, null=True)
    details = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.user} - {self.action} at {self.timestamp}"

    class Meta:
        ordering = ['-timestamp']
