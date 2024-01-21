from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
# from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from .models import RoomModel, CustomUser


class RoomForm(forms.ModelForm):
    
    class Meta:
        model = RoomModel
        fields = '__all__'

class CustomUserCreationForm(forms.ModelForm):

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = CustomUser
        fields = ["name","email","username"]

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class updateUserProfileForm(forms.ModelForm):
    # bio = forms.Textarea()
    class Meta:
        model = CustomUser
        # fields = '__all__'
        fields = ["name","email","username", "bio"]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': ('form-control')
            })