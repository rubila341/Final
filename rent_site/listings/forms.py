from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from datetime import date

from .models import Listing, City, Rating, Message, Review, Booking, Discount

# Форма регистрации пользователя, наследующая от встроенной UserCreationForm
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email address'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
        }

    # Проверка уникальности имени пользователя
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    # Проверка уникальности адреса электронной почты
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email


# Форма добавления объявления, связанная с моделью Listing
class ListingForm(forms.ModelForm):
    location = forms.ModelChoiceField(
        queryset=City.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Select a city",
    )

    class Meta:
        model = Listing
        fields = ['title', 'description', 'location', 'price', 'rooms', 'property_type', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Listing title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describe the listing', 'rows': 4}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price'}),
            'rooms': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Number of rooms'}),
            'property_type': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

    # Проверка, что цена больше нуля
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise forms.ValidationError("Price must be greater than zero.")
        return price

    # Проверка, что количество комнат больше нуля
    def clean_rooms(self):
        rooms = self.cleaned_data.get('rooms')
        if rooms <= 0:
            raise forms.ValidationError("Number of rooms must be greater than zero.")
        return rooms


# Форма для оценки (рейтинг и комментарий) объявления
class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, f'{i} Star') for i in range(1, 6)]),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Leave a comment', 'rows': 4}),
        }

    # Проверка, что рейтинг в пределах 1-5
    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if not (1 <= rating <= 5):
            raise forms.ValidationError("Rating must be between 1 and 5.")
        return rating


# Форма для отправки сообщений между пользователями
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter your message here...', 'rows': 4}),
        }

    # Проверка, что сообщение не пустое
    def clean_content(self):
        content = self.cleaned_data.get('content')
        if not content.strip():
            raise forms.ValidationError("Message content cannot be empty.")
        return content


# Форма для добавления отзыва к объявлению
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, f'{i} Star') for i in range(1, 6)]),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Leave a comment', 'rows': 4}),
        }

    # Проверка, что рейтинг находится в пределах от 1 до 5
    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if not (1 <= rating <= 5):
            raise forms.ValidationError("Rating must be between 1 and 5.")
        return rating


# Форма для бронирования с автоматическим расчетом скидки, если применимо
class BookingForm(forms.ModelForm):
    discount_percentage = forms.DecimalField(
        max_digits=5,
        decimal_places=2,
        required=False,
        widget=forms.HiddenInput()
    )
    discounted_price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'})
    )

    class Meta:
        model = Booking
        fields = ['start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        # Дополнительные аргументы для получения пользователя и объявления
        user = kwargs.pop('user', None)
        listing = kwargs.pop('listing', None)
        super().__init__(*args, **kwargs)

        # Установка значений скидки и конечной цены, если указаны пользователь и объявление
        if user and listing:
            discount_percentage = Discount.get_automatic_discount(user)
            self.fields['discount_percentage'].initial = discount_percentage
            self.fields['discounted_price'].initial = listing.price - (listing.price * discount_percentage / 100)

    # Проверка, что дата начала не в прошлом
    def clean_start_date(self):
        start_date = self.cleaned_data.get('start_date')
        if start_date and start_date < date.today():
            raise forms.ValidationError("Start date cannot be in the past.")
        return start_date

    # Проверка, что дата окончания позже даты начала
    def clean_end_date(self):
        end_date = self.cleaned_data.get('end_date')
        start_date = self.cleaned_data.get('start_date')
        if end_date and start_date and end_date <= start_date:
            raise forms.ValidationError("End date must be after start date.")
        return end_date


# Форма для создания и редактирования скидок
class DiscountForm(forms.ModelForm):
    class Meta:
        model = Discount
        fields = ['listing', 'applicable_to', 'amount', 'start_date', 'end_date', 'duration', 'is_active']
        widgets = {
            'listing': forms.Select(attrs={'class': 'form-control'}),
            'applicable_to': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Applicable to'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Discount amount'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'duration': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Duration (in days)'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    # Проверка, что дата окончания позже даты начала
    def clean_end_date(self):
        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')
        if end_date and start_date and end_date < start_date:
            raise forms.ValidationError("End date must be after start date.")
        return end_date
