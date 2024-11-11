from django.contrib import admin
from .models import Listing, Booking, City, Rating, Review, Chat, Message, UserActivity, Discount

# Админка для управления скидками
@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('listing', 'applicable_to', 'amount', 'start_date', 'end_date', 'duration', 'is_active')
    list_display_links = ('listing',)
    list_filter = ('is_active', 'start_date')
    search_fields = ('listing__title',)
    ordering = ('-listing',)

    # Поля и описание формы для скидки
    fieldsets = (
        (None, {
            'fields': ('listing', 'applicable_to', 'amount', 'start_date', 'end_date', 'duration', 'is_active'),
            'description': 'Details of the discount, including object, applicability, discount amount, start and end dates.',
        }),
    )

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, **kwargs)
        help_texts = {
            'listing': 'Object to which the discount applies.',
            'applicable_to': 'Category of users for whom the discount applies.',
            'amount': 'Discount amount applicable to the listing.',
            'duration': 'Duration of the discount during which it will be active.',
            'start_date': 'Discount start date.',
            'end_date': 'Discount end date.',
            'is_active': 'Whether this discount is active for users.'
        }
        if db_field.name in help_texts:
            formfield.help_text = help_texts[db_field.name]
        return formfield

# Админка для управления объявлениями
@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'location', 'price', 'discounted_price', 'rooms', 'property_type',
        'is_active', 'created_at', 'updated_at', 'owner', 'rating', 'review_count'
    )
    list_display_links = ('title', 'location')
    list_filter = ('property_type', 'location', 'is_active', 'created_at', 'updated_at')
    search_fields = ('title', 'description', 'location__name', 'owner__username')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at', 'discounted_price')

    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'location', 'price', 'discounted_price', 'rooms',
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

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, **kwargs)
        help_texts = {
            'title': 'The title of the listing.',
            'description': 'A description of the listing.',
            'location': 'The location of the property.',
            'price': 'The price of the property.',
            'discounted_price': 'The discounted price of the property if applicable.',
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

# Админка для бронирований
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'listing', 'start_date', 'end_date', 'status', 'created_at',
        'booking_number'
    )
    list_display_links = ('user', 'listing')
    list_filter = ('start_date', 'end_date', 'user', 'status')
    search_fields = ('user__username', 'listing__title')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

    actions = ['approve_bookings', 'reject_bookings']

    # Действия для одобрения и отклонения бронирований
    def approve_bookings(self, request, queryset):
        queryset.update(status='Approved')
    approve_bookings.short_description = 'Approve selected bookings'

    def reject_bookings(self, request, queryset):
        queryset.update(status='Rejected')
    reject_bookings.short_description = 'Reject selected bookings'

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

# Админка для управления городами
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

# Админка для выставления оценок
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

# Админка для управления отзывами
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

# Админка для управления чатами
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
            'participants': 'The users participating in the chat.',
            'created_at': 'The date when the chat was created.'
        }
        if db_field.name in help_texts:
            formfield.help_text = help_texts[db_field.name]
        return formfield

# Админка для сообщений
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('chat', 'sender', 'created_at')
    list_display_links = ('chat', 'sender')
    list_filter = ('chat', 'sender', 'created_at')
    search_fields = ('chat__name', 'sender__username', 'content')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

    fieldsets = (
        (None, {
            'fields': ('chat', 'sender', 'content'),
            'description': 'Message details, including the chat, sender, and content.'
        }),
        ('Date', {
            'fields': ('created_at',),
            'classes': ('collapse',),
            'description': 'Timestamp for when the message was created.'
        }),
    )

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, **kwargs)
        help_texts = {
            'chat': 'The chat where the message was sent.',
            'sender': 'The user who sent the message.',
            'content': 'The content of the message.',
            'created_at': 'The date when the message was sent.'
        }
        if db_field.name in help_texts:
            formfield.help_text = help_texts[db_field.name]
        return formfield

# Админка для действий пользователя
@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'activity_type', 'timestamp')
    list_display_links = ('user',)
    search_fields = ('user__username', 'activity_type')
    ordering = ('-timestamp',)
    readonly_fields = ('timestamp',)

    fieldsets = (
        (None, {
            'fields': ('user', 'activity_type', 'timestamp'),
            'description': 'Activity details, including the user and activity type.'
        }),
    )

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, **kwargs)
        help_texts = {
            'user': 'The user who performed the activity.',
            'activity_type': 'The type of activity performed by the user.',
            'timestamp': 'The time when the activity was recorded.'
        }
        if db_field.name in help_texts:
            formfield.help_text = help_texts[db_field.name]
        return formfield
