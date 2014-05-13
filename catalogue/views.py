from django.shortcuts import render, render_to_response
from django.template import RequestContext, loader, Context, Template
from django.http import HttpResponse, HttpResponseRedirect
from catalogue.models import Movie, Category
from catalogue.forms import MovieForm, CategoryForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


ITEMS_PER_PAGE = 15


def _make_page(full_data, page, items_per_page):
    paginator = Paginator(full_data, items_per_page)
    try:
        chopped_list = paginator.page(page)
    except (PageNotAnInteger):
        # If the page is not an integer, deliver the first page
        chopped_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver the last one
        chopped_list = paginator.page(paginator.num_pages)
    return chopped_list


def index(request):
    movies = Movie.objects.all()
    d = {'title': 'My First website in Django',
         'movies': movies
         }
    return render(request, 'default.html', d)


def movies_search_by_name(request, search_param=None):
    if search_param is not None:
        movies_list = Movie.objects.filter(name__icontains=search_param)
        if(len(movies_list) == 0):
            msg = 'There is no movie that contains <B>"'
            msg += search_param
            msg += '"</B> in its name.'
            error = {'title': 'Movie not found :(',
                     'message': msg
                     }
            d = {'error': error}
            return render_to_response('not_found.html', d)
    else:
        movies_list = Movie.objects.all()
    page = request.GET.get('page')
    movies = _make_page(movies_list, page, ITEMS_PER_PAGE)
    d = {'movies': movies}
    return render_to_response('list_movies.html', d)


def movies_search_by_category(request, search_param=None):
    if search_param is not None:
        movies_list = Movie.objects.filter(
            category__name__icontains=search_param)
        if(len(movies_list) == 0):
            msg = 'There is no movie that its category contains <B>"'
            msg += search_param
            msg += '"</B> in its name.'
            error = {'title': 'Movie not found :(',
                     'message': msg
                     }
            d = {'error': error}
            return render_to_response('not_found.html', d)
        page = request.GET.get('page')
        movies = _make_page(movies_list, page, ITEMS_PER_PAGE)
        d = {'movies': movies}
        return render_to_response('list_movies.html', d)
    else:
        return movies_search_by_name(request)


def categories_search_by_name(request, search_param=None):
    if search_param is not None:
        category_list = Category.objects.filter(name__icontains=search_param)
        if(len(category_list) == 0):
            msg = 'There is no category containing <B>"'
            msg += search_param
            msg += '"</B> in its name.'
            error = {'title': 'Category not found :(',
                     'message': msg
                     }
            d = {'error': error}
            return render_to_response('not_found.html', d)
    else:
        category_list = Category.objects.all()
    current_page = request.GET.get('page')
    categorires = _make_page(category_list, current_page, ITEMS_PER_PAGE)
    d = {'categories': categorires}
    return render_to_response('list_categories.html', d)


def movie_details(request, pk=None):
    movie = Movie.objects.filter(pk=pk)
    if len(movie) != 0:
        d = {'movie': movie[0]}
        return render_to_response('movie_details.html', d)
    else:
        d = {'error': 'Movie not found'}
        return render_to_response('not_found.html', d)


def movie_form(request):
    if request.method == 'GET':
        # mform = MovieForm(request.POST or None)
        mf = MovieForm()
        d = {'form': mf}
        c = RequestContext(request, d)
        return render_to_response('forms.html', c)
    elif request.method == 'POST':
        form = MovieForm(request.POST or None)
        if form.is_valid():
            new_movie = form.save()
            return HttpResponseRedirect(new_movie.get_absolute_url())
        else:
            d = {'form': form}
            c = RequestContext(request, d)
            return render_to_response('forms.html', c)
