from django.conf.urls import patterns, include, url

from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static

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
                       url(r'^movies/details/(?P<pk>\d+)$',
                           'catalogue.views.movie_details',
                           name='movie_details'),
                       url(r'^movies/delete/(?P<pk>\d+)$',
                           'catalogue.views.delete_movie',
                           name='delete_movie'),

                       url(r'^categories/$',
                           'catalogue.views.categories_search_by_name',
                           name='categories'),
                       url(r'^categories/(?P<search_param>\w+)$',
                           'catalogue.views.categories_search_by_name',
                           name='categories'),
                       url(r'^category/details/(?P<pk>\d+)$',
                           'catalogue.views.category_details',
                           name='category_details'),

                       url(r'^add/movie/$',
                           'catalogue.views.movie_edit_form',
                           {},
                           'add_movie'),
                       url(r'^add/category/$',
                           'catalogue.views.category_edit_form',
                           {},
                           'add_category'),

                       url(r'^edit/category/(?P<pk>\d+)$',
                           'catalogue.views.category_edit_form',
                           name='edit_category'),
                       url(r'^edit/movie/(?P<pk>\d+)$',
                           'catalogue.views.movie_edit_form',
                           name='edit_movie'),

                       url(r'^user/add/$',
                           'catalogue.views.add_user',
                           {},
                           'adduser'),

                       url(r'^user/login/$',
                           'catalogue.views.log_in',
                           name='login'),

                       url(r'^user/logout/$',
                           'catalogue.views.logout_view',
                           name='logout')

                       )

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
