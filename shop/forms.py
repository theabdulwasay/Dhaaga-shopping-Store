from django import forms
from django.core.validators import RegexValidator, EmailValidator
from .models import Order, ContactMessage


class CheckoutForm(forms.ModelForm):
    phone_regex = RegexValidator(
        regex=r'^\+?92?\d{10,15}$',
        message="Phone number must be in format: +92XXXXXXXXXX or 03XXXXXXXXXX"
    )
    
    phone = forms.CharField(
        validators=[phone_regex],
        widget=forms.TextInput(attrs={'placeholder': '+92XXXXXXXXXX'})
    )
    
    class Meta:
        model = Order
        fields = ["full_name", "phone", "address", "city"]
        widgets = {
            "full_name": forms.TextInput(attrs={'placeholder': 'Full Name'}),
            "address": forms.Textarea(attrs={"rows": 3, 'placeholder': 'Complete delivery address'}),
            "city": forms.TextInput(attrs={'placeholder': 'City'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = True
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "message"]
        widgets = {
            "name": forms.TextInput(attrs={'placeholder': 'Your Name'}),
            "email": forms.EmailInput(attrs={'placeholder': 'your@email.com'}),
            "message": forms.Textarea(attrs={"rows": 4, 'placeholder': 'How can we help you?'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = True
            self.fields[field].widget.attrs.update({'class': 'form-control'})
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        validator = EmailValidator()
        try:
            validator(email)
        except:
            raise forms.ValidationError('Please enter a valid email address.')
        return email
