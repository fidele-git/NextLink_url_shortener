from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'block w-full px-4 py-3 rounded-xl border border-slate-200 bg-slate-50 text-slate-900 focus:border-primary focus:ring-4 focus:ring-primary/5 transition-all outline-none font-medium',
                'placeholder': 'First Name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'block w-full px-4 py-3 rounded-xl border border-slate-200 bg-slate-50 text-slate-900 focus:border-primary focus:ring-4 focus:ring-primary/5 transition-all outline-none font-medium',
                'placeholder': 'Last Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'block w-full px-4 py-3 rounded-xl border border-slate-200 bg-slate-50 text-slate-900 focus:border-primary focus:ring-4 focus:ring-primary/5 transition-all outline-none font-medium',
                'placeholder': 'Email Address'
            }),
        }
