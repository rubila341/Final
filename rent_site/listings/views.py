from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.core.paginator import Paginator
from django.http import HttpResponseNotAllowed, JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from datetime import datetime

from .forms import UserRegisterForm, ListingForm, RatingForm, MessageForm, ReviewForm, BookingForm
from .models import Listing, Booking, Rating, City, User, Message, Chat, Review
from django.shortcuts import render

def home(request):
    # Пример списка номеров изображений
    image_numbers = list(range(1, 12))  # Список от 1 до 11
    return render(request, 'home.html', {'image_numbers': image_numbers})

# Политика конфиденциальности
def privacy_policy(request):
    return render(request, 'listings/privacy_policy.html')

# Домашняя страница
def home(request):
    cities = City.objects.values('name').distinct()
    return render(request, 'listings/index.html', {'cities': cities})

# Регистрация пользователя
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = UserRegisterForm()
    return render(request, 'listings/register.html', {'form': form})

# Авторизация пользователя
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'listings/login.html', {'form': form})

# Добавление нового объявления
@login_required
def add_listing(request):
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.owner = request.user
            listing.save()
            return redirect('home')
    else:
        form = ListingForm()
    return render(request, 'listings/add_listing.html', {'form': form})

# Редактирование объявления
@login_required
def edit_listing(request, id):
    listing = get_object_or_404(Listing, id=id, owner=request.user)

    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES, instance=listing)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ListingForm(instance=listing)

    return render(request, 'listings/edit_listing.html', {'form': form, 'listing': listing})

# Поиск объявлений
def search_listings(request):
    query = request.GET.get('q', '')
    listings = Listing.objects.filter(title__icontains=query) if query else Listing.objects.all()
    return render(request, 'listings/search_listings.html', {'listings': listings, 'query': query})

# Отображение объявлений в конкретном городе
def city_listings(request, city):
    city_object = get_object_or_404(City, name=city)
    listings = Listing.objects.filter(location=city_object)
    return render(request, 'listings/city_listings.html', {'listings': listings, 'city': city})

# Просмотр бронирований пользователя
@login_required
def bookings(request):
    user_bookings = Booking.objects.filter(user=request.user)
    return render(request, 'listings/bookings.html', {'bookings': user_bookings})

# Профиль пользователя с управлением объявлениями
@login_required
def profile(request):
    user_listings = Listing.objects.filter(owner=request.user)

    if request.method == 'POST':
        action = request.POST.get('action')
        listing_id = request.POST.get('listing_id')
        if action and listing_id:
            listing = get_object_or_404(Listing, id=listing_id, owner=request.user)
            if action == 'activate':
                listing.is_active = True
            elif action == 'deactivate':
                listing.is_active = False
            elif action == 'delete':
                listing.delete()
            else:
                return HttpResponseNotAllowed(['POST'])
            listing.save()
            return redirect('profile')

    return render(request, 'listings/profile.html', {'listings': user_listings})

# Смена пароля пользователя
@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('profile')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'listings/change_password.html', {'form': form})

# Выход из учетной записи
@login_required
def logout(request):
    if request.method == 'POST':
        auth_logout(request)
        return redirect('home')
    return HttpResponseNotAllowed(['POST'])

# Просмотр всех объявлений с пагинацией и сортировкой
def all_listings(request):
    page_number = request.GET.get('page', 1)
    items_per_page = int(request.GET.get('items_per_page', 5))
    sort_by = request.GET.get('sort_by', 'created_at')
    location = request.GET.get('location', '')
    min_price = request.GET.get('min_price', 0)
    max_price = request.GET.get('max_price', 10000)
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')

    valid_sort_fields = ['created_at', 'title', 'price', 'rating']
    if sort_by not in valid_sort_fields:
        sort_by = 'created_at'

    # Получаем все города для фильтрации
    cities = City.objects.all()

    # Фильтруем объявления по выбранному городу и ценовому диапазону
    listings = Listing.objects.filter(is_active=True)

    if location:
        city_object = get_object_or_404(City, id=location)
        listings = listings.filter(location=city_object)

    if min_price:
        listings = listings.filter(price__gte=min_price)

    if max_price:
        listings = listings.filter(price__lte=max_price)

    # Фильтрация по датам
    if start_date and end_date:
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            # Убедитесь, что в модели Listing есть поля для дат доступности
            # если таких полей нет, этот блок нужно удалить или заменить
            listings = listings.filter(created_at__gte=start_date, created_at__lte=end_date)
        except ValueError:
            pass

    listings = listings.order_by(sort_by)
    paginator = Paginator(listings, items_per_page)
    page = paginator.get_page(page_number)

    return render(request, 'listings/all_listings.html', {
        'page': page,
        'paginator': paginator,
        'sort_by': sort_by,
        'items_per_page': items_per_page,
        'cities': cities,
        'location': location,
        'min_price': min_price,
        'max_price': max_price,
        'start_date': start_date,
        'end_date': end_date
    })

# Детальный просмотр объявления
def listing_detail(request, id):
    listing = get_object_or_404(Listing, id=id)
    user_rating = None
    if request.user.is_authenticated:
        user_rating = Rating.objects.filter(listing=listing, user=request.user).first()

    rating_form = RatingForm()
    message_form = MessageForm()

    if request.method == 'POST':
        if 'rating_submit' in request.POST:
            rating_form = RatingForm(request.POST)
            if rating_form.is_valid():
                rating_value = rating_form.cleaned_data.get('rating')
                rating, created = Rating.objects.get_or_create(listing=listing, user=request.user)
                rating.rating = rating_value
                rating.save()
                listing.update_rating()  # Убедитесь, что этот метод существует
                return redirect('listing_detail', id=id)
        elif 'message_submit' in request.POST:
            message_form = MessageForm(request.POST, request.FILES)
            if message_form.is_valid():
                message = message_form.save(commit=False)
                message.sender = request.user
                message.receiver = listing.owner
                message.listing = listing
                message.save()
                return redirect('listing_detail', id=id)

    return render(request, 'listings/listing_detail.html', {
        'listing': listing,
        'rating_form': rating_form,
        'message_form': message_form,
        'user_rating': user_rating.rating if user_rating else None
    })

# Оценка объявления
@login_required
def rate_listing(request, id):
    listing = get_object_or_404(Listing, id=id)
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating_value = form.cleaned_data.get('rating')
            rating, created = Rating.objects.get_or_create(listing=listing, user=request.user)
            rating.rating = rating_value
            rating.save()
            listing.update_rating()  # Убедитесь, что этот метод существует
            return JsonResponse({'success': True, 'new_rating': listing.rating})
        return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)

# Представление для страницы контактов
def contact(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message_content = form.cleaned_data.get('content')
            send_mail(
                'Contact Form Message',
                message_content,
                settings.DEFAULT_FROM_EMAIL,
                [settings.CONTACT_EMAIL],
            )
            return redirect('home')
    else:
        form = MessageForm()
    return render(request, 'listings/contact.html', {'form': form})

# Функция для отправки сообщения
@login_required
def send_message(request, recipient_id):
    recipient = get_object_or_404(User, id=recipient_id)
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = recipient
            chat, created = Chat.objects.get_or_create(participants__in=[request.user, recipient])
            message.chat = chat
            message.save()
            return redirect('chat_view', recipient_id=recipient_id)
    else:
        form = MessageForm()
    return render(request, 'listings/send_message.html', {'form': form, 'recipient': recipient})

# Представление для списка чатов
@login_required
def chat_list(request):
    # Получаем список уникальных чатов для пользователя
    sent_chats = Message.objects.filter(sender=request.user).values('receiver').distinct()
    received_chats = Message.objects.filter(receiver=request.user).values('sender').distinct()

    # Объединяем оба списка и убираем дубликаты
    all_chats = list(sent_chats) + list(received_chats)
    unique_chats = set(chat['receiver'] if 'receiver' in chat else chat['sender'] for chat in all_chats)

    chat_objects = []
    for chat_id in unique_chats:
        recipient = get_object_or_404(User, id=chat_id)
        last_message = Message.objects.filter(
            (Q(sender=request.user) & Q(receiver=recipient)) |
            (Q(sender=recipient) & Q(receiver=request.user))
        ).latest('sent_at')
        chat_objects.append({
            'recipient': recipient,
            'last_message': last_message.content,
            'last_message_date': last_message.sent_at
        })

    return render(request, 'listings/chat_list.html', {'chats': chat_objects})

# Представление для чата
@login_required
def chat_view(request, recipient_id):
    recipient = get_object_or_404(User, id=recipient_id)
    chat, created = Chat.objects.get_or_create(participants__in=[request.user, recipient])

    messages = Message.objects.filter(chat=chat).order_by('sent_at')

    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = recipient
            message.chat = chat
            message.save()
            return redirect('chat_view', recipient_id=recipient_id)
    else:
        form = MessageForm()

    return render(request, 'listings/chat.html', {
        'recipient': recipient,
        'messages': messages,
        'form': form
    })

# Добавление отзыва
@login_required
def add_review(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.listing = listing
            review.user = request.user
            review.save()
            return redirect('listing_detail', id=listing_id)  # Исправлен идентификатор на listing_id
    else:
        form = ReviewForm()
    return render(request, 'listings/add_review.html', {'form': form})  # Исправлен путь шаблона

# Просмотр отзывов
@login_required
def view_reviews(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    reviews = listing.reviews.all()
    return render(request, 'listings/view_reviews.html', {'listing': listing, 'reviews': reviews})

# Бронирование
@login_required
def make_booking(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.listing = listing
            booking.user = request.user
            booking.status = 'pending'
            booking.save()
            return redirect('profile')
    else:
        form = BookingForm()
    return render(request, 'listings/make_booking.html', {'form': form, 'listing': listing})

# Управление бронированием
@login_required
def manage_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            booking.status = 'approved'
        elif action == 'reject':
            booking.status = 'rejected'
        booking.save()
        return redirect('profile')
    return render(request, 'listings/manage_booking.html', {'booking': booking})
