from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .forms import TodoForm
from .models import TodoItem


class CustomLoginView(LoginView):
    template_name = 'todo/login.html'


class CustomLogoutView(LogoutView):
    next_page = 'login'


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('todo_list')
    else:
        form = UserCreationForm()
    return render(request, 'todo/signup.html', {'form': form})


@login_required
def todo_list(request):
    todos = TodoItem.objects.filter(user=request.user).order_by('deadline',
                                                                '-created_at')
    add_form = TodoForm()
    edit_forms = [(todo.id, TodoForm(instance=todo)) for todo in todos]

    return render(request, 'todo/todo_list.html', {
        'todos': todos,
        'add_form': add_form,
        'edit_forms': edit_forms,
    })


@login_required
def add_todo(request):
    if request.method == 'POST':
        form = TodoForm(request.POST, request.FILES)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()
    return redirect('todo_list')


@login_required
def edit_todo(request, pk):
    todo = get_object_or_404(TodoItem, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TodoForm(request.POST, request.FILES, instance=todo)
        if form.is_valid():
            form.save()
    return redirect('todo_list')


@login_required
def delete_todo(request, pk):
    todo = get_object_or_404(TodoItem, pk=pk, user=request.user)
    todo.delete()
    return redirect('todo_list')


@csrf_exempt
@login_required
def update_status(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        todo_id = data.get('id')
        new_status = data.get('status')

        todo = get_object_or_404(TodoItem, id=todo_id, user=request.user)
        todo.status = new_status
        todo.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)
