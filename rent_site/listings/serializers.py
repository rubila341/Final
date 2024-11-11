from rest_framework import serializers
from django.contrib.auth.models import User
from .models import City, Listing, Discount, Review, Booking, Rating, Chat, Message, UserActivity


# Сериализатор для модели City
class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name', 'country', 'latitude', 'longitude', 'get_full_address']


# Сериализатор для модели Listing
class ListingSerializer(serializers.ModelSerializer):
    location = CitySerializer()  # Вложенный сериализатор для отображения города
    owner = serializers.StringRelatedField()  # Имя пользователя как строка

    class Meta:
        model = Listing
        fields = [
            'id', 'title', 'description', 'location', 'price', 'rooms', 'property_type',
            'is_active', 'created_at', 'updated_at', 'owner', 'image', 'rating', 'review_count',
            'discounted_price'
        ]


# Сериализатор для модели Discount
class DiscountSerializer(serializers.ModelSerializer):
    listing = ListingSerializer()  # Вложенный сериализатор для отображения объявления

    class Meta:
        model = Discount
        fields = [
            'id', 'listing', 'applicable_to', 'duration', 'is_active', 'amount', 'start_date', 'end_date'
        ]


# Сериализатор для модели Review
class ReviewSerializer(serializers.ModelSerializer):
    listing = serializers.StringRelatedField()  # Отображение названия объявления
    user = serializers.StringRelatedField()  # Имя пользователя как строка

    class Meta:
        model = Review
        fields = [
            'id', 'listing', 'user', 'rating', 'comment', 'created_at', 'updated_at'
        ]


# Сериализатор для модели Booking
class BookingSerializer(serializers.ModelSerializer):
    listing = serializers.StringRelatedField()  # Отображение названия объявления
    user = serializers.StringRelatedField()  # Имя пользователя как строка

    class Meta:
        model = Booking
        fields = [
            'id', 'listing', 'user', 'start_date', 'end_date', 'status', 'created_at', 'booking_number'
        ]


# Сериализатор для модели Rating
class RatingSerializer(serializers.ModelSerializer):
    listing = serializers.StringRelatedField()  # Отображение названия объявления
    user = serializers.StringRelatedField()  # Имя пользователя как строка

    class Meta:
        model = Rating
        fields = [
            'id', 'listing', 'user', 'rating', 'comment', 'created_at', 'updated_at'
        ]


# Сериализатор для модели Chat
class ChatSerializer(serializers.ModelSerializer):
    participants = serializers.StringRelatedField(many=True)  # Отображение имен участников

    class Meta:
        model = Chat
        fields = [
            'id', 'participants', 'created_at', 'name'
        ]


# Сериализатор для модели Message
class MessageSerializer(serializers.ModelSerializer):
    chat = serializers.StringRelatedField()  # Отображение названия чата
    sender = serializers.StringRelatedField()  # Имя отправителя
    receiver = serializers.StringRelatedField()  # Имя получателя

    class Meta:
        model = Message
        fields = [
            'id', 'chat', 'sender', 'receiver', 'created_at', 'listing', 'content', 'file', 'sent_at', 'is_read'
        ]


# Сериализатор для модели UserActivity
class UserActivitySerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # Имя пользователя

    class Meta:
        model = UserActivity
        fields = [
            'id', 'user', 'action', 'timestamp', 'activity_type', 'details'
        ]
