from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView
from django.contrib import messages
from .forms import CustomUserCreationForm


def home(request):
    return render(request, 'home.html')


def register(request):
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно зарегистрировались! Теперь вы можете войти в систему.')
            return redirect('login')

    return render(request, 'register.html', {'form': form, 'submitted': request.method == 'POST'})


class CustomLoginView(LoginView):
    template_name = 'login.html'

