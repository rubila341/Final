from django.contrib import admin
from .models import Listing, Booking, City, Rating, Review, Chat, Message, UserActivity, Discount

# Регистрация модели Listing в админ-панели с пользовательским классом админки
@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    # Указываем, какие поля будут отображаться в списке объектов
    list_display = (
        'title', 'location', 'price', 'rooms', 'property_type',
        'is_active', 'created_at', 'updated_at', 'owner', 'rating', 'review_count'
    )
    # Указываем, какие поля можно кликнуть для перехода к редактированию
    list_display_links = ('title', 'location')
    # Добавляем фильтры для упрощения поиска
    list_filter = (
        'property_type', 'location', 'is_active', 'created_at', 'updated_at'
    )
    # Указываем поля для поиска
    search_fields = ('title', 'description', 'location__name', 'owner__username')
    # Указываем порядок сортировки по дате создания
    ordering = ('-created_at',)
    # Указываем поля, которые будут доступны только для чтения
    readonly_fields = ('created_at', 'updated_at')
    # Определяем, как будут организованы поля в форме редактирования
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'location', 'price', 'rooms',
                       'property_type', 'is_active', 'owner', 'image'),
            'description': 'General information about the listing. All fields are mandatory.'
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
            'description': 'The dates when the listing was created and last updated.'
        }),
        ('Rating', {
            'fields': ('rating', 'review_count'),
            'classes': ('collapse',),
            'description': 'The average rating and the total number of reviews for this listing.'
        }),
    )

    # Метод для настройки текстов подсказок для полей формы
    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, **kwargs)
        help_texts = {
            'title': 'The title of the listing.',
            'description': 'A description of the listing.',
            'location': 'The location of the property.',
            'price': 'The price of the property.',
            'rooms': 'The number of rooms.',
            'property_type': 'The type of property.',
            'is_active': 'Whether the listing is active.',
            'owner': 'The owner of the property.',
            'image': 'An image of the property.',
            'rating': 'The average rating of the property.',
            'review_count': 'The number of reviews.'
        }
        if db_field.name in help_texts:
            formfield.help_text = help_texts[db_field.name]
        return formfield
# Регистрация модели Booking в админ-панели
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    # Указываем поля для отображения в списке
    list_display = (
        'user', 'listing', 'start_date', 'end_date', 'status', 'created_at',
        'booking_number'
    )
    list_display_links = ('user', 'listing')# Поля для кликабельных ссылок
    list_filter = ('start_date', 'end_date', 'user', 'status')# Фильтры
    search_fields = ('user__username', 'listing__title')# Поля для поиска
    ordering = ('-created_at',)# Сортировка по дате создания
    readonly_fields = ('created_at',)# Поля только для чтения
    # Действия для изменения статуса бронирования
    actions = ['approve_bookings', 'reject_bookings']

    def approve_bookings(self, request, queryset):
        queryset.update(status='Approved')

    approve_bookings.short_description = 'Approve selected bookings'

    def reject_bookings(self, request, queryset):
        queryset.update(status='Rejected')

    reject_bookings.short_description = 'Reject selected bookings'
    # Определяем структуру формы редактирования
    fieldsets = (
        (None, {
            'fields': ('user', 'listing', 'start_date', 'end_date', 'status', 'booking_number'),
            'description': 'Booking details, including the user, listing, and status.'
        }),
        ('Booking Date', {
            'fields': ('created_at',),
            'classes': ('collapse',),
            'description': 'The date when the booking was created.'
        }),
    )

    # Настройка текстов подсказок для полей
    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, **kwargs)
        help_texts = {
            'user': 'The user who made the booking.',
            'listing': 'The property being booked.',
            'start_date': 'The start date of the booking.',
            'end_date': 'The end date of the booking.',
            'status': 'The status of the booking.',
            'booking_number': 'The booking number.',
            'created_at': 'The date when the booking was created.'
        }
        if db_field.name in help_texts:
            formfield.help_text = help_texts[db_field.name]
        return formfield

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')
    list_display_links = ('name',)
    search_fields = ('name', 'country')
    ordering = ('name',)
    fieldsets = (
        (None, {
            'fields': ('name', 'country'),
            'description': 'City name and country.'
        }),
    )

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, **kwargs)
        help_texts = {
            'name': 'The name of the city.',
            'country': 'The country where the city is located.'
        }
        if db_field.name in help_texts:
            formfield.help_text = help_texts[db_field.name]
        return formfield

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('listing', 'user', 'rating', 'created_at', 'updated_at')
    list_display_links = ('listing', 'user')
    list_filter = ('listing', 'user', 'rating', 'created_at')
    search_fields = ('listing__title', 'user__username', 'rating')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('listing', 'user', 'rating', 'comment'),
            'description': 'The rating and optional comment from the user.'
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
            'description': 'Timestamps for when the rating was created and updated.'
        }),
    )

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, **kwargs)
        help_texts = {
            'listing': 'The property being rated.',
            'user': 'The user who gave the rating.',
            'rating': 'The rating given by the user.',
            'comment': 'Optional comment from the user.',
            'created_at': 'The date when the rating was created.',
            'updated_at': 'The date when the rating was last updated.'
        }
        if db_field.name in help_texts:
            formfield.help_text = help_texts[db_field.name]
        return formfield

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('listing', 'user', 'rating', 'created_at', 'updated_at')
    list_display_links = ('listing', 'user')
    list_filter = ('listing', 'user', 'rating', 'created_at')
    search_fields = ('listing__title', 'user__username', 'comment')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('listing', 'user', 'rating', 'comment'),
            'description': 'The review details, including the user rating and comment.'
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
            'description': 'Timestamps for when the review was created and updated.'
        }),
    )

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, **kwargs)
        help_texts = {
            'listing': 'The property being reviewed.',
            'user': 'The user who left the review.',
            'rating': 'The rating given in the review.',
            'comment': 'The comment provided in the review.',
            'created_at': 'The date when the review was created.',
            'updated_at': 'The date when the review was last updated.'
        }
        if db_field.name in help_texts:
            formfield.help_text = help_texts[db_field.name]
        return formfield

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    list_display_links = ('name',)
    search_fields = ('name', 'participants__username')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    filter_horizontal = ('participants',)
    fieldsets = (
        (None, {
            'fields': ('name', 'participants'),
            'description': 'Chat name and the list of participants.'
        }),
        ('Dates', {
            'fields': ('created_at',),
            'classes': ('collapse',),
            'description': 'Timestamp for when the chat was created.'
        }),
    )

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, **kwargs)
        help_texts = {
            'name': 'The name of the chat.',
            'participants': 'The participants in the chat.',
            'created_at': 'The date when the chat was created.'
        }
        if db_field.name in help_texts:
            formfield.help_text = help_texts[db_field.name]
        return formfield

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        'sender', 'receiver', 'chat', 'content', 'sent_at', 'is_read'
    )
    list_display_links = ('sender', 'receiver')
    list_filter = ('sender', 'receiver', 'chat', 'is_read', 'sent_at')
    search_fields = ('sender__username', 'receiver__username', 'content')
    ordering = ('-sent_at',)
    readonly_fields = ('sent_at',)
    fieldsets = (
        (None, {
            'fields': ('sender', 'receiver', 'chat', 'listing', 'content', 'file', 'is_read'),
            'description': 'Message details, including sender, receiver, content, and file attachment.'
        }),
        ('Dates', {
            'fields': ('sent_at',),
            'classes': ('collapse',),
            'description': 'Timestamp for when the message was sent.'
        }),
    )

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, **kwargs)
        help_texts = {
            'sender': 'The sender of the message.',
            'receiver': 'The receiver of the message.',
            'chat': 'The chat in which the message was sent.',
            'listing': 'The property related to the message.',
            'content': 'The content of the message.',
            'file': 'Attached file (if any).',
            'is_read': 'Whether the message has been read.',
            'sent_at': 'The date and time the message was sent.'
        }
        if db_field.name in help_texts:
            formfield.help_text = help_texts[db_field.name]
        return formfield
