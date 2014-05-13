from django.db import models
from django.core.urlresolvers import reverse


class Category(models.Model):
    '''
    Movies category
    '''

    name = models.CharField(u'Category name', max_length=100)
    description = models.TextField(u'Category description')

    def get_absolute_url(self):
        return reverse('catalogue.views.category_details',
                       kwargs={'pk': self.id})

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name', )
        verbose_name_plural = "Categories"


class Movie(models.Model):

    '''
    Class to store all movies information
    '''

    name = models.CharField(u'Name', max_length=100)
    description = models.TextField(u'Movie description')
    category = models.ManyToManyField(Category)
    year_released = models.IntegerField(u'Year')
    picture = models.ImageField(upload_to='pictures', blank=True, null=True)

    @property
    def image_url(self):
        if self.picture and hasattr(self.picture, 'url'):
            return self.picture.url

    def get_absolute_url(self):
        return reverse('catalogue.views.movie_details', kwargs={'pk': self.id})

    def __unicode__(self):
        return "Movie: %s, %s" % (self.name, self.category)

    class Meta:
        ordering = ('name', )
        verbose_name_plural = "Movies"
