from django.db import models
from django.contrib.auth.models import User

class City(models.Model):
    name = models.CharField(max_length=100, unique=True)
    country = models.CharField(max_length=100, default='Unknown')
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
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

    def __str__(self):
        return f"{self.title} - {self.location.name}"

    def deactivate(self):
        self.is_active = False
        self.save()

    def activate(self):
        self.is_active = True
        self.save()

    def update_rating(self):
        """
        Updates the listing rating based on related ratings.
        """
        ratings = self.ratings.all()
        if ratings.exists():
            total_ratings = sum(rating.rating for rating in ratings)
            self.rating = total_ratings / ratings.count()
        else:
            self.rating = 0.0
        self.save()

    class Meta:
        ordering = ['-created_at']

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f'{self.user} booked {self.listing} from {self.start_date} to {self.end_date}'

    class Meta:
        ordering = ['-booking_date']
        constraints = [
            models.UniqueConstraint(fields=['user', 'listing', 'start_date', 'end_date'], name='unique_booking')
        ]

class Rating(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=1)  # Default rating value
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

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
    name = models.CharField(max_length=255, blank=True)  # Optional chat name

    def __str__(self):
        return self.name or ', '.join(user.username for user in self.participants.all())

    class Meta:
        ordering = ['-created_at']

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages', null=True, blank=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages', null=True, blank=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='messages', null=True, blank=True)
    content = models.TextField()
    file = models.FileField(upload_to='messages/', blank=True, null=True)
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)  # To track if the message has been read

    def __str__(self):
        return f"From {self.sender} to {self.receiver or 'Chat'} on {self.sent_at}"

    class Meta:
        ordering = ['-sent_at']
