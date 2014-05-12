from django.shortcuts import render, render_to_response
# from django.template import RequestContext, loader, Context, Template
# from django.http import HttpResponse
from catalogue.models import Movie, Category
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
            d = {'search_param': search_param}
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
            d = {'search_param': search_param}
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
            d = {'search_param': search_param}
            return render_to_response('not_found.html', d)
    else:
        category_list = Category.objects.all()
    current_page = request.GET.get('page')
    categorires = _make_page(category_list, current_page, ITEMS_PER_PAGE)
    d = {'categories': categorires}
    return render_to_response('list_categories.html', d)
