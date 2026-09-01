from django import forms
from django.contrib.auth.models import User

from .models import (
    UserProfile,
    Store,
    Product,
    Review
)


# ====================
# REGISTRATION FORM
# ====================

class RegistrationForm(forms.ModelForm):

    """Collect and validate buyer or vendor registration details."""
    ROLE_CHOICES = (
        ('BUYER', 'Buyer'),
        ('VENDOR', 'Vendor'),
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter password'
            }
        )
    )

    password_confirm = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Confirm password'
            }
        )
    )

    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }
        )
    )

    class Meta:

        """Represent the meta used by the application."""
        model = User

        fields = [
            'username',
            'email'
        ]

        widgets = {

            'username': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter username'
                }
            ),

            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter email address'
                }
            ),
        }

    def clean(self):

        """Validate the registration passwords and return the cleaned form data."""
        cleaned_data = super().clean()

        password = cleaned_data.get('password')

        password_confirm = cleaned_data.get(
            'password_confirm'
        )

        if password and password_confirm:

            if password != password_confirm:

                raise forms.ValidationError(
                    'The passwords do not match.'
                )

        return cleaned_data

    def save(self, commit=True):

        """Create a Django user with a securely hashed password and its role profile."""
        user = super().save(commit=False)

        user.set_password(
            self.cleaned_data['password']
        )

        if commit:

            user.save()

            UserProfile.objects.create(
                user=user,
                role=self.cleaned_data['role']
            )

        return user


# ==================
# STORE FORM
# ==================

class StoreForm(forms.ModelForm):

    """Collect the name and description of a vendor store."""
    class Meta:

        """Represent the meta used by the application."""
        model = Store

        fields = [
            'name',
            'description'
        ]

        widgets = {

            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter store name'
                }
            ),

            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter store description',
                    'rows': 5
                }
            ),
        }


# ================
# PRODUCT FORM
# ================

class ProductForm(forms.ModelForm):

    """Collect the details required to create a product."""
    class Meta:

        """Represent the meta used by the application."""
        model = Product

        fields = [
            'name',
            'description',
            'price',
            'stock',
            'image'
        ]

        widgets = {

            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter product name'
                }
            ),

            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter product description',
                    'rows': 5
                }
            ),

            'price': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'step': '0.01',
                    'min': '0'
                }
            ),

            'stock': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': '0'
                }
            ),

            'image': forms.ClearableFileInput(
                attrs={
                    'class': 'form-control'
                }
            ),
        }


# ==============
# REVIEW FORM
# ==============

class ReviewForm(forms.ModelForm):

    """Collect a buyer rating and comment for a product review."""
    class Meta:

        """Represent the meta used by the application."""
        model = Review

        fields = [
            'rating',
            'comment'
        ]

        widgets = {

            'rating': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': 1,
                    'max': 5
                }
            ),

            'comment': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4
                }
            ),
        }
