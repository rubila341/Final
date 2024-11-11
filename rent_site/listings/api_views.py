from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from .models import City, Listing, Booking, Review, Rating, Chat, Message, UserActivity, Discount
from .serializers import CitySerializer, ListingSerializer, BookingSerializer, ReviewSerializer, RatingSerializer, ChatSerializer, MessageSerializer, UserActivitySerializer, DiscountSerializer
from django.shortcuts import get_object_or_404

# ViewSet для модели City
class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [IsAuthenticated]  # Только аутентифицированные пользователи

# ViewSet для модели Listing
class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [IsAuthenticated]

    # Пользовательский метод для активации объявления
    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def activate(self, request, pk=None):
        listing = self.get_object()
        listing.activate()
        return Response({'status': 'Listing activated'}, status=status.HTTP_200_OK)

    # Пользовательский метод для деактивации объявления
    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def deactivate(self, request, pk=None):
        listing = self.get_object()
        listing.deactivate()
        return Response({'status': 'Listing deactivated'}, status=status.HTTP_200_OK)

# ViewSet для модели Booking
class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

# ViewSet для модели Review
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

# ViewSet для модели Rating
class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

# ViewSet для модели Chat
class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]

# ViewSet для модели Message
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

# ViewSet для модели UserActivity
class UserActivityViewSet(viewsets.ModelViewSet):
    queryset = UserActivity.objects.all()
    serializer_class = UserActivitySerializer
    permission_classes = [IsAuthenticated]

# ViewSet для модели Discount
class DiscountViewSet(viewsets.ModelViewSet):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer
    permission_classes = [IsAdminUser]  # Только админы могут управлять скидками
