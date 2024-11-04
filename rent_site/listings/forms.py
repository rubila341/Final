from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from datetime import date

from .models import Listing, City, Rating, Message, Review, Booking

# Форма для регистрации нового пользователя
class UserRegisterForm(UserCreationForm):
    # Поле для ввода адреса электронной почты
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email address'})
    )

    class Meta:
        model = User# Модель, с которой связана форма
        fields = ['username', 'email', 'password1', 'password2']# Поля, которые будут отображаться в форме
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
        }
        help_texts = {
            'username': 'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
            'password1': 'Your password must contain at least 8 characters.',
            'password2': 'Enter the same password as above, for verification.',
        }

    # Валидация поля имени пользователя
    def clean_username(self):
        username = self.cleaned_data.get('username')
        # Проверяем, существует ли уже пользователь с таким именем
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    # Валидация поля электронной почты
    def clean_email(self):
        # Проверяем, существует ли уже пользователь с таким адресом электронной почты
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email

# Форма для добавления нового объявления
class ListingForm(forms.ModelForm):
    # Поле выбора города из существующих
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
        labels = {
            'title': 'Title',
            'description': 'Description',
            'location': 'Location',
            'price': 'Price',
            'rooms': 'Number of rooms',
            'property_type': 'Property Type',
            'image': 'Image',
        }
        help_texts = {
            'title': 'Enter the title of the listing.',
            'description': 'Provide a detailed description of the listing.',
            'location': 'Select the location of the property.',
            'price': 'Enter the price of the property.',
            'rooms': 'Indicate the number of rooms in the property.',
            'property_type': 'Select the type of property.',
            'image': 'Upload an image of the property.',
        }

    # Валидация поля цены
    def clean_price(self):
        price = self.cleaned_data.get('price')
        # Проверяем, чтобы цена была больше нуля
        if price <= 0:
            raise forms.ValidationError("Price must be greater than zero.")
        return price

    # Валидация поля количества комнат
    def clean_rooms(self):
        # Проверяем, чтобы количество комнат было больше нуля
        rooms = self.cleaned_data.get('rooms')
        if rooms <= 0:
            raise forms.ValidationError("Number of rooms must be greater than zero.")
        return rooms

# Форма для выставления оценок
class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating', 'comment']# Поля, которые будут отображаться в форме
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, f'{i} Star') for i in range(1, 6)]),  # 1-5 stars
            'comment': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Leave a comment', 'rows': 4}),
        }
        labels = {
            'rating': 'Rate this listing',
            'comment': 'Comment (optional)',
        }
        help_texts = {
            'rating': 'Select a rating from 1 to 5 stars.',
            'comment': 'Provide additional feedback if you wish.',
        }

    # Валидация поля оценки
    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        # Проверяем, чтобы оценка была в диапазоне от 1 до 5
        if not (1 <= rating <= 5):
            raise forms.ValidationError("Rating must be between 1 and 5.")
        return rating

# Форма для отправки сообщений
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter your message here...', 'rows': 4}),
        }
        labels = {
            'content': 'Message',
        }
        help_texts = {
            'content': 'Write your message to the listing owner here.',
        }

    # Валидация поля содержимого сообщения
    def clean_content(self):
        content = self.cleaned_data.get('content')
        # Проверяем, чтобы содержание сообщения не было пустым
        if not content.strip():
            raise forms.ValidationError("Message content cannot be empty.")
        return content

# Форма для написания отзывов
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, f'{i} Star') for i in range(1, 6)]),  # 1-5 stars
            'comment': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Leave a comment', 'rows': 4}),
        }
        labels = {
            'rating': 'Rate this review',
            'comment': 'Comment (optional)',
        }
        help_texts = {
            'rating': 'Select a rating from 1 to 5 stars.',
            'comment': 'Provide additional feedback if you wish.',
        }

    # Валидация поля оценки
    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        # Проверяем, чтобы оценка была в диапазоне от 1 до 5
        if not (1 <= rating <= 5):
            raise forms.ValidationError("Rating must be between 1 and 5.")
        return rating

# Форма для бронирования
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
        labels = {
            'start_date': 'Start Date',
            'end_date': 'End Date',
        }
        help_texts = {
            'start_date': 'Select the start date for the booking.',
            'end_date': 'Select the end date for the booking.',
        }

    # Валидация поля даты начала
    def clean_start_date(self):
        start_date = self.cleaned_data.get('start_date')
        # Проверяем, чтобы дата начала не была в прошлом
        if start_date and start_date < date.today():
            raise forms.ValidationError("Start date cannot be in the past.")
        return start_date

    # Валидация поля даты окончания
    def clean_end_date(self):
        end_date = self.cleaned_data.get('end_date')
        start_date = self.cleaned_data.get('start_date')
        # Проверяем, чтобы дата окончания была после даты начала
        if end_date and start_date and end_date <= start_date:
            raise forms.ValidationError("End date must be after start date.")
        return end_date
