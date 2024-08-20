# -*- encoding: utf-8 -*-
"""
Copyright (c) 2024 - Ahmed Salim
"""

from django import forms
from apps.authentication.models import Dweet, Message, Profile


class ProfileImageForm(forms.ModelForm):
    image = forms.ImageField(label=(''),required=False, error_messages = {'invalid':("Image files only")}, widget=forms.FileInput)
    class Meta:
        model = Profile
        fields = ['image']

class DweetForm(forms.ModelForm):
    body = forms.CharField(
        required=True,
        widget=forms.widgets.Textarea(
            attrs={
                "placeholder": "Post something...",
                "class": "textarea is-primary is-medium",
            }
        ),
        label="",
    )
    class Meta:
        model = Dweet
        exclude = ("user",)

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['receiver', 'subject', 'body']
        widgets = {
            'receiver': forms.Select(attrs={'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
        }
