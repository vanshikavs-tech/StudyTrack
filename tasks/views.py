from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Task
from .forms import TaskForm


def login_view(request):
    """Handles user login using Django's built-in authentication."""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            next_url = request.POST.get('next') or request.GET.get('next') or 'dashboard'
            if not next_url or next_url == 'None':
                next_url = 'dashboard'
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    """Logs the user out and redirects to the login page."""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')


@login_required
def dashboard_view(request):
    """
    Renders the student dashboard with:
    - User's tasks only
    - Total task count
    - Completed task count
    """
    user_tasks = Task.objects.filter(user=request.user).order_by('-created_at')
    total_tasks = user_tasks.count()
    completed_tasks = user_tasks.filter(completed=True).count()

    context = {
        'username': request.user.username,
        'tasks': user_tasks,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
    }
    return render(request, 'dashboard.html', context)


@login_required
def add_task_view(request):
    """
    Handles creating a new task using ModelForm.
    Automatically assigns the task to the currently logged-in user.
    """
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, 'Task added successfully!')
            return redirect('dashboard')
    else:
        form = TaskForm()

    return render(request, 'add_task.html', {'form': form})


@login_required
def complete_task_view(request, id):
    """
    Marks a task as completed.
    Ensures the task strictly belongs to the logged-in user.
    """
    task = get_object_or_404(Task, id=id, user=request.user)
    task.completed = True
    task.save()
    messages.success(request, f'Task "{task.title}" marked as completed!')
    return redirect('dashboard')


@login_required
def delete_task_view(request, id):
    """
    Deletes a task via POST request.
    Ensures the task strictly belongs to the logged-in user.
    """
    task = get_object_or_404(Task, id=id, user=request.user)
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted successfully!')
    return redirect('dashboard')
