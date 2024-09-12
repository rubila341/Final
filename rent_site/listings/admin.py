from django.contrib import admin
from .models import Listing, Booking, City, Rating, Review, Chat, Message, UserActivity, Discount

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'location', 'price', 'rooms', 'property_type',
        'is_active', 'created_at', 'updated_at', 'owner', 'rating', 'review_count'
    )
    list_display_links = ('title', 'location')
    list_filter = (
        'property_type', 'location', 'is_active', 'created_at', 'updated_at'
    )
    search_fields = ('title', 'description', 'location__name', 'owner__username')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'location', 'price', 'rooms',
                       'property_type', 'is_active', 'owner', 'image')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
        ('Rating', {
            'fields': ('rating', 'review_count'),
            'classes': ('collapse',),
        }),
    )

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

    def approve_bookings(self, request, queryset):
        queryset.update(status='Approved')

    approve_bookings.short_description = 'Approve selected bookings'

    def reject_bookings(self, request, queryset):
        queryset.update(status='Rejected')

    reject_bookings.short_description = 'Reject selected bookings'

    # Remove is_active_booking from list_display and list_filter
    def is_active_booking(self, obj):
        return obj.status == 'Approved'

    is_active_booking.boolean = True

    fieldsets = (
        (None, {
            'fields': ('user', 'listing', 'start_date', 'end_date', 'status', 'booking_number')
        }),
        ('Booking Date', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'country'
    )
    list_display_links = ('name',)
    search_fields = ('name', 'country')
    ordering = ('name',)
    fieldsets = (
        (None, {
            'fields': ('name', 'country')
        }),
    )

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = (
        'listing', 'user', 'rating', 'created_at', 'updated_at'
    )
    list_display_links = ('listing', 'user')
    list_filter = ('listing', 'user', 'rating', 'created_at')
    search_fields = ('listing__title', 'user__username', 'rating')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('listing', 'user', 'rating', 'comment')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'listing', 'user', 'rating', 'created_at', 'updated_at'
    )
    list_display_links = ('listing', 'user')
    list_filter = ('listing', 'user', 'rating', 'created_at')
    search_fields = ('listing__title', 'user__username', 'comment')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('listing', 'user', 'rating', 'comment')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'created_at'
    )
    list_display_links = ('name',)
    search_fields = ('name', 'participants__username')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    filter_horizontal = ('participants',)
    fieldsets = (
        (None, {
            'fields': ('name', 'participants')
        }),
        ('Dates', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )

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
            'fields': ('sender', 'receiver', 'chat', 'listing', 'content', 'file', 'is_read')
        }),
        ('Dates', {
            'fields': ('sent_at',),
            'classes': ('collapse',),
        }),
    )

@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'action', 'timestamp'
    )
    list_display_links = ('user',)
    list_filter = ('user', 'action', 'timestamp')
    search_fields = ('user__username', 'action')
    ordering = ('-timestamp',)
    readonly_fields = ('timestamp',)
    fieldsets = (
        (None, {
            'fields': ('user', 'action', 'details')
        }),
        ('Timestamp', {
            'fields': ('timestamp',),
            'classes': ('collapse',),
        }),
    )

@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = (
        'listing', 'discount_percentage', 'start_date', 'end_date', 'is_active'
    )
    list_display_links = ('listing',)
    list_filter = ('listing', 'is_active', 'start_date', 'end_date')
    search_fields = ('listing__title',)
    ordering = ('-start_date',)
    fieldsets = (
        (None, {
            'fields': ('listing', 'discount_percentage', 'start_date', 'end_date', 'is_active')
        }),
    )
