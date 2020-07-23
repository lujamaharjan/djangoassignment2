from django import forms
from .models import User, Blog


class SignupForm(forms.Form):
    first_name = forms.CharField(label='First Name', max_length=100,
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Last Name', max_length=100,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Password", max_length=126,
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(label="Confirm Password", max_length=126,
                                       widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError("This Email is already taken!")
        return self.cleaned_data['email']

    def clean(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError("Your Passwords do not match!")


class LoginForm(forms.Form):
    email = forms.EmailField(label='Email',
                             widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Password", max_length=126,
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    # def clean(self):
    #     password = self.cleaned_data['password']
    #     email = self.cleaned_data['email']
    #     user = User.objects.filter(email=email).first()
    #     if user:
    #         if user.password != User.set
    #             raise forms.ValidationError("Your credentials are not matched!")
    #     else:
    #         raise forms.ValidationError("Account with entered email is not Found!")


class ProfileUpdate(forms.ModelForm):
    first_name = forms.CharField(label='First Name', max_length=100,
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Last Name', max_length=100,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Password", max_length=126,
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    profile_pic = forms.ImageField(label="Profile_pic")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'password', 'profile_pic']


class BlogForm(forms.ModelForm):
    title = forms.CharField(label='Title', max_length=100,
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    body = forms.TimeField(label="Body",
                           widget=forms.Textarea(attrs={'class': 'form-control'}))
    featured_image = forms.ImageField(label="Featured Image")

    class Meta:
        model = Blog
        fields = '__all__'


class CreateBlogForm(forms.ModelForm):
    featured_image = forms.ImageField(label="Featured Image")

    class Meta:
        model = Blog
        exclude = "__all__"
