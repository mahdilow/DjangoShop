from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=255, required=True)
    
    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']  # Removed phone_number

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hide the username field as we'll set it automatically
        if 'username' in self.fields:
            self.fields['username'].widget = forms.HiddenInput()
            self.fields['username'].required = False

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        
        if email:
            # Extract username from email (part before @)
            username = email.split('@')[0]
            
            # Check if username already exists
            counter = 1
            temp_username = username
            while User.objects.filter(username=temp_username).exists():
                temp_username = f"{username}{counter}"
                counter += 1
            
            username = temp_username
            cleaned_data['username'] = username
            
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['username']
        if commit:
            user.save()
        return user