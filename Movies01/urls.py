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
                           'catalogue.views.movies_listing',
                           name='movies'),

                       url(r'^movies/(?P<search_param>\w+)',
                           'catalogue.views.movies_search_by_name',
                           name='search_movie'),

                       url(r'^categories/$',
                           'catalogue.views.categories_listing',
                           name='categories'),
                       )
