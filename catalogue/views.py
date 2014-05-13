from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm


from catalogue.models import Movie, Category
from catalogue.forms import MovieForm, CategoryForm, UserForm


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
            return render(request, 'not_found.html', d)
    else:
        movies_list = Movie.objects.all()
    page = request.GET.get('page')
    movies = _make_page(movies_list, page, ITEMS_PER_PAGE)
    d = {'movies': movies}
    return render(request, 'list_movies.html', d)


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
            return render(request, 'not_found.html', d)
        page = request.GET.get('page')
        movies = _make_page(movies_list, page, ITEMS_PER_PAGE)
        d = {'movies': movies}
        return render(request, 'list_movies.html', d)
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
            return render(request, 'not_found.html', d)
    else:
        category_list = Category.objects.all()
    current_page = request.GET.get('page')
    categorires = _make_page(category_list, current_page, ITEMS_PER_PAGE)
    d = {'categories': categorires}
    return render(request, 'list_categories.html', d)


def movie_details(request, pk=None):
    movie = Movie.objects.filter(pk=pk)
    if len(movie) != 0:
        d = {'movie': movie[0]}
        return render(request, 'movie_details.html', d)
    else:
        d = {'error': 'Movie not found'}
        return render(request, 'not_found.html', d)


def category_details(request, pk=None):
    category = Category.objects.filter(pk=pk)
    if len(category) != 0:
        d = {'category': category[0]}
        return render(request, 'category_details.html', d)
    else:
        d = {'error': 'Category not found'}
        return render(request, 'not_found.html', d)


@login_required
def category_edit_form(request, pk):
    try:
        inst = Category.objects.get(id=pk)
    except Category.DoesNotExist:
        inst = Category()
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=inst)
        if form.is_valid():
            new_category = form.save()
            return HttpResponseRedirect(new_category.get_absolute_url())
        else:
            d = {'form': form,
                 'action_link': reverse('edit_category', args=[pk])}
            c = RequestContext(request, d)
            return render_to_response('forms.html', c)

    form = CategoryForm(instance=inst)
    d = {'form': form,
         'action_link': reverse('edit_category', args=[pk])}
    c = RequestContext(request, d)
    return render_to_response('forms.html', c)









@login_required
def movie_edit_form(request, pk=None):
    try:
        inst = Movie.objects.get(id=pk)
    except Movie.DoesNotExist:
        inst = Movie()
    if request.method == 'POST':
        form = MovieForm(request.POST, instance=inst)
        if form.is_valid():
            new_movie = form.save()
            return HttpResponseRedirect(new_movie.get_absolute_url())
        else:
            d = {'form': form,
                 'action_link': reverse('edit_movie', args=[pk])}
            c = RequestContext(request, d)
            return render_to_response('forms.html', c)

    form = MovieForm(instance=inst)
    d = {'form': form,
         'action_link': reverse('add_movie')}
    c = RequestContext(request, d)
    return render_to_response('forms.html', c)


@login_required
def delete_movie(request, pk):
    try:
        inst = Movie.objects.get(id=pk)
    except Movie.DoesNotExist:
        d = {'title': 'Movie not found',
             'error': 'This movie is not in our databases.'}
        return render(request, 'not_found.html', d)
    inst.delete()
    d = {'title': inst.name + ' deleted',
         'error': inst.name + ' deleted'}
    return render(request, 'not_found.html', d)


def add_user(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)
            return HttpResponseRedirect('/')
    else:
        form = UserForm()

    return render(request, 'forms.html', {'form': form})


def log_in(request):
    if request.method == 'GET':
        form = AuthenticationForm()
        return render(request, 'forms.html', {'form': form})
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            # Redirect to a success page.
            return HttpResponseRedirect(reverse('index'))
    else:
        return HttpResponseRedirect(reverse('login'))


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
