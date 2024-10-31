from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import DesignRequestForm
from .models import DesignRequest
from django.contrib.auth.decorators import user_passes_test
from .forms import CategoryForm
from .models import Category


@login_required
def create_design_request(request):
    if request.method == 'POST':
        form = DesignRequestForm(request.POST, request.FILES)
        if form.is_valid():
            design_request = form.save(commit=False)
            design_request.user = request.user
            design_request.save()
            messages.success(request, 'Заявка успешно создана!')
            return redirect('view_requests')
    else:
        form = DesignRequestForm()
    return render(request, 'create_request.html', {'form': form})

@login_required
def view_requests(request):
    if request.user.is_superuser:
        requests = DesignRequest.objects.all().order_by('-created_at')
    else:
        requests = DesignRequest.objects.filter(user=request.user).order_by('-created_at')
    status_filter = request.GET.get('status')
    if status_filter:
        requests = requests.filter(status=status_filter)
    return render(request, 'view_requests.html', {
        'requests': requests,
        'status_choices': DesignRequest.STATUS_CHOICES
    })


@login_required
def delete_request(request, pk):
    design_request = get_object_or_404(DesignRequest, pk=pk, status='Новая')
    if request.method == 'POST':
        design_request.delete()
        messages.success(request, 'Заявка успешно удалена.')
        return redirect('view_requests')
    return render(request, 'confirm_delete_request.html', {'design_request': design_request})

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

@login_required
def profile(request):
    return render(request, 'profile.html')