from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Основные пути
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('add_listing/', views.add_listing, name='add_listing'),
    path('search/', views.search_listings, name='search_listings'),
    path('city/<str:city>/', views.city_listings, name='city_listings'),
    path('all_listings/', views.all_listings, name='all_listings'),  # Путь для просмотра всех объявлений
    path('bookings/', views.bookings, name='bookings'),
    path('profile/', views.profile, name='profile'),
    path('change_password/', views.change_password, name='change_password'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('listing/<int:id>/', views.listing_detail, name='listing_detail'),
    path('contact/', views.contact, name='contact'),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
    path('rate_listing/<int:id>/', views.rate_listing, name='rate_listing'),

    # Путь для чатов
    path('chat/', views.chat_list, name='chat_list'),

    # Путь для чата между пользователями
    path('chat/<int:recipient_id>/', views.chat_view, name='chat_view'),

    # Путь для отправки сообщений
    path('send_message/<int:recipient_id>/', views.send_message, name='send_message'),

    # Путь для редактирования объявления
    path('edit_listing/<int:id>/', views.edit_listing, name='edit_listing'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
