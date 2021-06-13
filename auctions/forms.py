from django.forms import ModelForm
from django import forms

from .models import AdListing, Comment, Bid


class AdListingForm(ModelForm):
    class Meta:
        model = AdListing
        fields = ['title', 'description', 'start_bid', 'category', 'photo']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'description': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'start_bid': forms.TextInput(attrs={
                'class': 'form-control',
            }),
        }


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter comment...',
            })
        }


class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['price']
