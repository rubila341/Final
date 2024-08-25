# listings/admin.py

from django.contrib import admin
from .models import Listing, Booking, City

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'location', 'price', 'rooms', 'property_type',
        'is_active', 'created_at', 'updated_at', 'owner'
    )
    list_display_links = ('title', 'location')  # Сделать некоторые поля кликабельными
    list_filter = (
        'property_type', 'location', 'is_active', 'created_at', 'updated_at'
    )
    search_fields = ('title', 'description', 'location__name', 'owner__username')
    ordering = ('-created_at',)  # Сортировка по дате создания (новые сначала)

    readonly_fields = ('created_at', 'updated_at')  # Поля, которые не следует изменять
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'location', 'price', 'rooms',
                       'property_type', 'is_active', 'owner', 'image')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),  # Скрыть эти поля по умолчанию
        }),
    )

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'listing', 'booking_date', 'start_date', 'end_date'
    )
    list_display_links = ('user', 'listing')  # Сделать некоторые поля кликабельными
    list_filter = ('start_date', 'end_date', 'user')
    search_fields = ('user__username', 'listing__title')
    ordering = ('-booking_date',)  # Сортировка по дате бронирования (новые сначала)

    readonly_fields = ('booking_date',)  # Поле, которое не следует изменять
    fieldsets = (
        (None, {
            'fields': ('user', 'listing', 'start_date', 'end_date')
        }),
        ('Booking Date', {
            'fields': ('booking_date',),
            'classes': ('collapse',),  # Скрыть это поле по умолчанию
        }),
    )

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'country'
    )
    list_display_links = ('name',)  # Сделать поле кликабельным
    search_fields = ('name', 'country')
    ordering = ('name',)  # Сортировка по названию города (по алфавиту)

    fieldsets = (
        (None, {
            'fields': ('name', 'country')
        }),
    )
