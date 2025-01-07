from django import forms
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox


class RegisterForm(forms.Form):
    name = forms.CharField(max_length=50, label='Имя')
    surname = forms.CharField(max_length=50, label='Фамилия')
    email = forms.EmailField(label='Почта')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

class LoginForm(forms.Form):
    email = forms.EmailField(label='Почта')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)