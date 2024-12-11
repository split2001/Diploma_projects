from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User
# from django.contrib.auth.models import User


# создаем свою форму, чтобы добавить email и age в существующую форму UserCreationForm
class UserRegister(UserCreationForm):
    email = forms.EmailField(label='Введите email:', required=True)
    # age = forms.IntegerField(max_value=100, label='Введите возраст:', required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class RecipeForm(forms.Form):
    title = forms.CharField(max_length=100,  label='Описание',)
    description = forms.CharField(widget=forms.Textarea, label='Описание', required=False)
    ingredients = forms.CharField(widget=forms.Textarea, label='Ингридиенты', required=False)
    instructions = forms.CharField(widget=forms.Textarea, label='Инструкция по приготовлению', required=False)
    image = forms.ImageField(label='Загрузить изображение')



# class Login(AuthenticationForm):
#     username = forms.CharField(max_length=10, label='Введите логин:', required=True, widget=forms.TextInput)
#     password1 = forms.CharField(min_length=8, label='Введите пароль:', required=True, widget=forms.PasswordInput)