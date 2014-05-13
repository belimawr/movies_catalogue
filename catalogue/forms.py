from django.forms import ModelForm
from django.contrib.auth.models import User

from catalogue.models import Movie, Category


class MovieForm(ModelForm):
    class Meta:
        model = Movie


class CategoryForm(ModelForm):
    class Meta:
        model = Category


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password', 'email']

