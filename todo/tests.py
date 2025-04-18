from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from .forms import TodoForm
from .models import TodoItem


class TodoModelTest(TestCase):
    """
    Unit tests for the TodoItem model.
    """

    def setUp(self):
        """Create a test user."""
        self.user = User.objects.create_user(username='testuser',
                                             password='12345')

    def test_create_todo_item(self):
        """
        Test creating a TodoItem and ensure fields are saved correctly.
        """
        todo = TodoItem.objects.create(
            user=self.user,
            title='Test Task',
            description='This is a test task.',
            status='Pending',
            deadline=date.today()
        )
        self.assertEqual(str(todo.title), 'Test Task')
        self.assertEqual(todo.status, 'Pending')


class TodoFormTest(TestCase):
    """
    Unit tests for the TodoForm.
    """

    def test_valid_form(self):
        """
        Ensure that a form with valid data passes validation.
        """
        form_data = {
            'title': 'Test Task',
            'description': 'Some description',
            'status': 'In Progress',
            'deadline': '2025-04-18',
        }
        form = TodoForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        """
        Ensure that an empty form fails validation.
        """
        form = TodoForm(data={})
        self.assertFalse(form.is_valid())


class TodoViewTest(TestCase):
    """
    Integration tests for views and user interaction.
    """

    def setUp(self):
        """Create a test user and one TodoItem."""
        self.client = Client()
        self.user = User.objects.create_user(username='testuser',
                                             password='12345')
        self.todo = TodoItem.objects.create(
            user=self.user,
            title='Sample Task',
            status='Pending'
        )

    def test_signup_view(self):
        """
        Test the user signup view creates a new user and redirects.
        """
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'password1': 'complexpass123',
            'password2': 'complexpass123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login_required_redirect(self):
        """
        Ensure unauthenticated access to todo_list redirects to login.
        """
        response = self.client.get(reverse('todo_list'))
        self.assertEqual(response.status_code, 302)

    def test_todo_list_authenticated(self):
        """
        Ensure authenticated user can access the to_do list.
        """
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('todo_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sample Task')

    def test_add_todo(self):
        """
        Test adding a new to_do item through the form.
        """
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('add_todo'), {
            'title': 'New Task',
            'description': '',
            'status': 'Pending',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(TodoItem.objects.filter(title='New Task').exists())

    def test_edit_todo(self):
        """
        Test editing an existing to_do item updates its fields.
        """
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('edit_todo', args=[self.todo.pk]),
                                    {
                                        'title': 'Updated Title',
                                        'status': 'Done',
                                    })
        self.assertEqual(response.status_code, 302)
        self.todo.refresh_from_db()
        self.assertEqual(self.todo.title, 'Updated Title')
        self.assertEqual(self.todo.status, 'Done')

    def test_delete_todo(self):
        """
        Test deleting item from the database.
        """
        self.client.login(username='testuser', password='12345')
        response = self.client.post(
            reverse('delete_todo', args=[self.todo.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(TodoItem.objects.filter(pk=self.todo.pk).exists())
