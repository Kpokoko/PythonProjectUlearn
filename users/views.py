from django.shortcuts import render
from .forms import RegisterForm, LoginForm
from .models import User


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            surname = form.cleaned_data['surname']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            if User.objects.filter(email=email).exists():
                return render(request, 'register.html', {'form': form, 'answer': 'Вы уже зарегистрированы.'})
            hashed_password = User.hash_password(password)
            user = User(name=name, surname=surname, email=email, password=hashed_password)
            user.save()

            return render(request, 'register.html', {'form': RegisterForm(), 'answer': 'Регистрация успешна.'})
        return render(request, 'register.html', {'form': form, 'answer': 'Ошибка при заполнении капчи.'})

    form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def authorise(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.filter(email=email)
            if user.exists():
                if user.first().verify_password(password):
                    return render(request, 'index.html')
            return render(request, 'authorise.html', {'form': form, 'answer': 'Неверный логин или пароль.'})
        return render(request, 'authorise.html', {'form': form, 'answer': 'Ошибка при заполнении капчи.'})
    if request.method == 'GET':
        return render(request, 'authorise.html', {'form': LoginForm()})
