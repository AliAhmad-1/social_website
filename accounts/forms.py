from django import forms
from accounts.models import MyUser as User
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
class LoginForm(AuthenticationForm):
    # remember_me=forms.BooleanField(required=False,label='remember_me',widget=forms.CheckboxInput())
    username=forms.CharField(label='Username or Email',required=True)
    password=forms.CharField(widget=forms.PasswordInput())
    class Meta:
        fields=['username','password']



class RegisterForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','password1','password2']
        error_messages={'email':{'required':'This field is required .'}}        

    def clean_password2(self):
        password1=self.cleaned_data['password1']
        password2=self.cleaned_data['password2']
        if password1 != password2:
            raise forms.ValidationError('Passwords don\'t match.')
        return password2


    def clean_email(self):
        input_email=self.cleaned_data['email']
        qs = User.objects.exclude(id=self.instance.id).filter(email=input_email)
        if qs.exists():
            raise forms.ValidationError('%(value)s already in use.',params={'value':input_email})
        return input_email

        
class UpdateProfileUser(forms.ModelForm):
    image_profile=forms.ImageField()
    
    class Meta:
        model=User
        fields=['username','email','image_profile','cover_profile','bio']
        widgets={'bio':forms.Textarea(attrs={'rows':5})}
