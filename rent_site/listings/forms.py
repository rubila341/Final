from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Listing, City, Rating, Message

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
        help_texts = {
            'username': 'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
            'password1': 'Your password must contain at least 8 characters.',
            'password2': 'Enter the same password as above, for verification.',
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email

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

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise forms.ValidationError("Price must be greater than zero.")
        return price

    def clean_rooms(self):
        rooms = self.cleaned_data.get('rooms')
        if rooms <= 0:
            raise forms.ValidationError("Number of rooms must be greater than zero.")
        return rooms

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating', 'comment']
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

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if not (1 <= rating <= 5):
            raise forms.ValidationError("Rating must be between 1 and 5.")
        return rating

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

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if not content.strip():
            raise forms.ValidationError("Message content cannot be empty.")
        return content
