from django import forms
from app1.models import Food,FoodCart
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from captcha.fields import CaptchaField

User=get_user_model()

class FoodForm(forms.ModelForm):

    class Meta:
        model = Food
        fields = "__all__"

class CartForm(forms.ModelForm):
    class  Meta:
        model = FoodCart
        fields = ['quantity']

class SignUpForm(UserCreationForm):
    email =forms.EmailField(required=True)
    captcha = CaptchaField()

    class Meta:
        model =User
        fields = ['username','email','password1','password2'] 



