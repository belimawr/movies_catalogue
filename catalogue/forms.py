from django.forms import ModelForm
from catalogue.models import Movie, Category


class MovieForm(ModelForm):
    class Meta:
        model = Movie


class CategoryForm(ModelForm):
    class Meta:
        model = Category
