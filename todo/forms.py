from django import forms

from .models import TodoItem


class TodoForm(forms.ModelForm):
    """
    Form for creating and editing TodoItem instances.
    Includes fields for title, description, status, image, and deadline.
    """

    class Meta:
        model = TodoItem
        fields = ['title', 'description', 'status', 'image', 'deadline']
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'}),
        }
