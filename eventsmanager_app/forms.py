from django import forms
from django.forms import widgets
from s3direct.widgets import S3DirectWidget
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib import messages
from .models import *

class UserRegistrationForm(UserCreationForm):
    MONTH_ABBREVIATIONS = [
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'June',
        'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec'
    ]

    MONTH_CHOICES = list(enumerate(MONTH_ABBREVIATIONS, 1))
    YEAR_CHOICES = [(i, i) for i in range(2015, 2036)]

    email = forms.CharField(label='Email Address', widget=forms.EmailInput, help_text='Your email will be the username')

    creditcardnumber = forms.CharField(label="Credit Card Number")

    cvv = forms.CharField(max_length=5, label="Security Code (CVV)")

    expiry_month = forms.ChoiceField(choices=MONTH_CHOICES, label="Month")

    expiry_year = forms.ChoiceField(choices=YEAR_CHOICES, label="Year")

    stripe_id = forms.CharField(widget=forms.HiddenInput)

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)

    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model=User
        fields = ['email','password1','password2','stripe_id']
        exclude = ['username']


    def clean_password2(self):
        password1= self.cleaned_data.get('password1')
        password2= self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            message = 'Passwords do not match'
            raise ValidationError(message)
        return password2

    def save(self,commit=True):
        instance = super(UserRegistrationForm,self).save(commit=False)
        instance.username = instance.email
        if commit:
            instance.save()
        return instance

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("User Already Exist!!")
        else:
            return email

class UserLoginForm(forms.Form):
    email=forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class EventCreation(forms.ModelForm):
    class Meta:
        model = Webcast
        fields = '__all__'
        widgets = {
            'webcast_date' : widgets.DateInput(attrs={'id' : 'dateInput'}),
            'webcast_time' : widgets.TimeInput(attrs={'id' : 'timepicker'}),
            'webcast_img' : widgets.FileInput(attrs={'id': 'imageform'})
        }
        exclude = ('speaker_id', 'webcast_asset_ID', 'agenda_foreign',)