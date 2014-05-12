from django.contrib import admin
from catalogue.models import Movie, Category
# Register your models here.


class MovieAdmin(admin.ModelAdmin):
    list_display = ['name',
                    #'picture',
                    'description',
                    'year_released']

    list_filter = ['category', 'year_released']


admin.site.register(Movie, MovieAdmin)
admin.site.register(Category)
