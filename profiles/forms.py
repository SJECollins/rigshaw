from django import forms
from allauth.account.forms import SignupForm

from .models import UserProfile

class CustomSignupForm(SignupForm):
    name = forms.CharField(max_length=100, label='Full Name')
    phone = forms.CharField(max_length=15, label='Phone Number')
    picture = forms.ImageField(label='Profile Picture', required=False)
    
    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        try:
            UserProfile.objects.create(
                user=user,
                name=self.cleaned_data['name'],
                phone=self.cleaned_data['phone'],
                picture=self.cleaned_data['picture']
            )            
        except: 
            user.delete()
            raise "Error creating user account"

        return user
    

class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name', 'phone', 'picture']
        labels = {
            'name': 'Full Name',
            'phone': 'Phone Number',
            'picture': 'Profile Picture'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }
        
        