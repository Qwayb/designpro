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
from .forms import UpdateStatusForm


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


@user_passes_test(lambda u: u.is_superuser)
@login_required
def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Категория успешно создана!')
            return redirect('home')
    else:
        form = CategoryForm()
    return render(request, 'create_category.html', {'form': form})



@user_passes_test(lambda u: u.is_superuser)
@login_required
def view_categories(request):
    categories = Category.objects.all()
    return render(request, 'view_categories.html', {'categories': categories})

@user_passes_test(lambda u: u.is_superuser)
@login_required
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Категория успешно удалена.')
        return redirect('view_categories')
    return render(request, 'confirm_delete_category.html', {'category': category})

@user_passes_test(lambda u: u.is_superuser)
@login_required
def update_request_status(request, pk):
    design_request = get_object_or_404(DesignRequest, pk=pk)
    if request.method == 'POST':
        form = UpdateStatusForm(request.POST, request.FILES, instance=design_request)
        if form.is_valid():
            form.save()
            messages.success(request, 'Статус заявки успешно обновлён.')
            return redirect('view_requests')
    else:
        form = UpdateStatusForm(instance=design_request)
    return render(request, 'update_request_status.html', {'form': form, 'design_request': design_request})

def home(request):
    recent_completed_requests = DesignRequest.objects.filter(status='Выполнено').order_by('-created_at')[:4]
    in_progress_count = DesignRequest.objects.filter(status='Принято в работу').count()
    return render(request, 'home.html', {
        'recent_completed_requests': recent_completed_requests,
        'in_progress_count': in_progress_count
    })


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