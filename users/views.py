from django.contrib.auth.hashers import verify_password
from django.shortcuts import render

from users.models import User


def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(email=email).exists():
            return render(request, 'register.html', {'answer': 'Вы уже были зарегистрированы!'})

        hashed_password = User.hash_password(password)
        user = User(name=name, surname=surname, email=email, password=hashed_password)
        user.save()
        return render(request, 'register.html', {'answer': 'Регистрация успешна'})

    return render(request, 'register.html')


def authorise(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.filter(email=email)
        if user.exists():
            print(user.first().verify_password(password))
            if user.first().verify_password(password):
                return render(request, 'index.html')
        return render(request, 'authorise.html', {'answer': 'Неверный логин или пароль'})
    if request.method == 'GET':
        return render(request, 'authorise.html')
