from django.contrib.auth.models import User
from django.contrib.auth import forms
from django.contrib import admin
from django.contrib.auth import admin as auth_admin

from django.contrib.auth.admin import UserAdmin
from .models import User


# Register your models here.
class CustomUserCreationForm(forms.UserCreationForm):
    class Meta(forms.UserCreationForm.Meta):
        model = User
        fields = forms.UserCreationForm.Meta.fields + ('email',)
    def __init__(self, *args, **kwargs): # Adiciona 
        super().__init__(*args, **kwargs)  
        for field_name, field in self.fields.items():   
            field.widget.attrs['class'] = 'form-control'
                        
admin.site.register(User, UserAdmin)