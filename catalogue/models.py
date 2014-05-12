from django.db import models


class Category(models.Model):
    '''
    Movies category
    '''

    name = models.CharField(u'Category name', max_length=100)
    description = models.TextField(u'Category description')

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
    picture = models.ImageField(upload_to='pictures')

    def __unicode__(self):
        return "Movie: %s, %s" % (self.name, self.category)

    class Meta:
        ordering = ('name', )
        verbose_name_plural = "Movies"
