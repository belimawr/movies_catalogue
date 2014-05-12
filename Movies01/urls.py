from django.conf.urls import patterns, include, url

from django.contrib import admin

# from Movies import views

admin.autodiscover()

# Examples:
# url(r'^$', 'Movies01.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),
urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),

                       url(r'^$', 'catalogue.views.index', name='index'),

                       url(r'^movies/$',
                           'catalogue.views.movies_search_by_name',
                           name='movies'),

                       url(r'^movies/category/(?P<search_param>\w+)$',
                           'catalogue.views.movies_search_by_category',
                           name='movies_category'),

                       url(r'^movies/(?P<search_param>\w+)$',
                           'catalogue.views.movies_search_by_name',
                           name='movies'),

                       url(r'^categories/$',
                           'catalogue.views.categories_search_by_name',
                           name='categories'),

                       url(r'^categories/(?P<search_param>\w+)$',
                           'catalogue.views.categories_search_by_name',
                           name='categories'),
                       )
