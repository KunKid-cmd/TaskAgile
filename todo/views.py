import json

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from .forms import TodoForm
from .models import TodoItem


class CustomLoginView(LoginView):
    """
    Handles user login using Django's built-in LoginView.
    """
    template_name = 'todo/login.html'


class CustomLogoutView(LogoutView):
    """
    Handles user logout using Django's built-in LogoutView.
    """
    next_page = 'login'


def signup_view(request):
    """
    Handles user registration.
    If the request is POST and form is valid, creates a new user
    """
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
    """
    Displays the list of todos for the logged-in user.
    Provides forms to add a new to_do and edit existing ones
    """
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
    """
    Handles the creation of a new to_do item.
    If the submitted form is valid, saves the to_do associated that user.
    """
    if request.method == 'POST':
        form = TodoForm(request.POST, request.FILES)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()
    return redirect('todo_list')


@login_required
def edit_todo(request, pk):
    """
    Handles editing of an existing to_do item.
    Only allows edits to todos owned by the current user.
    """
    todo = get_object_or_404(TodoItem, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TodoForm(request.POST, request.FILES, instance=todo)
        if form.is_valid():
            form.save()
    return redirect('todo_list')


@login_required
def delete_todo(request, pk):
    """
    Deletes a to_do item by its primary key.
    """
    todo = get_object_or_404(TodoItem, pk=pk, user=request.user)
    todo.delete()
    return redirect('todo_list')


@csrf_exempt
@login_required
def update_status(request):
    """
    Updates the status of a to_do item via a POST request.
    Expects a JSON payload with 'id' and 'status' fields.
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        todo_id = data.get('id')
        new_status = data.get('status')

        todo = get_object_or_404(TodoItem, id=todo_id, user=request.user)
        todo.status = new_status
        todo.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)
