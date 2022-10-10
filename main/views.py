from functools import wraps

from django.core.handlers.exception import response_for_exception
from django.shortcuts import render, redirect, Http404
from django.http import HttpResponse
from datetime import datetime
from main.models import Film, Review, Category
from .forms import FilmCreateForm, UserCreateForm, LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.db.models import Q


# Create your views here.


def index_html(request):
    return render(request, 'index.html')


def index(request):
    date = datetime.now().strftime('%H:%M:%S')
    hour = "<html><body><b>Время в Кыргыстане:</b> %s</body></html>" % date
    return HttpResponse(hour)


PAGE_SIZE = 8


def film_views(request):
    page = int(request.GET.get('Страница', 1))
    queryset = Film.objects.all()
    all_films = Film.objects.all()
    lists = all_films[PAGE_SIZE * (page - 1):PAGE_SIZE * page]
    if all_films.count() % PAGE_SIZE == 0:
        buttons = all_films.count() // PAGE_SIZE
    else:
        buttons = all_films.count() // PAGE_SIZE + 1
    context = {
        'film_list': lists,
        'films_list': queryset,
        'next': page+1,
        'disabled_next': 'disabled' if page >= buttons else '',
        'category': Category.objects.all(),
        'buttons': [i for i in range(1, buttons + 1)]
    }
    return render(request, 'film.html', context=context)


def film_item_view(request, id):
    try:
        details = Film.objects.get(id=id)
    except Film.DoesNotExist:
        raise Http404('News not found')
    if request.method == 'GET':
        contexts = {
            'film_detail': details,
            'reviews': Review.objects.filter(film_id=id)
        }
        return render(request, 'detail.html', context=contexts)
    else:
        id1 = (request.POST.get('review'))
        text = (request.POST.get('text'))
        assert isinstance(id, object)
        Review.objects.create(
            film_id=id,
            id=id1,
            text=text

        )
        return redirect(f'/films{id}/')


def category_films(request, id):
    context = {
        'film_list': Film.objects.filter(category_id=id)
    }
    return render(request, 'film.html', context=context)


@login_required(login_url='/login/')
def film_create_view(request):
    if request.method == 'GET':
        context = {
            'form': FilmCreateForm()
        }
        return render(request, 'add_film.html', context=context)
    else:
        form = FilmCreateForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/films/')
        return render(request, 'add_film.html', context={
            'form': form
        })


def register_user_view(request):
    context = {
        'form': UserCreateForm()
    }
    if request.method == 'POST':
        form = UserCreateForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            User.objects.create_user(username=username, email=email,
                                     password=password,
                                     is_active=True)
            return redirect('/login/')
        else:
            context = {
                'form': form
            }
    return render(request, 'register.html', context=context)


def login_user_view(request):
    context = {
        'form': LoginForm()
    }
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('/films')
            return redirect('login')
    return render(request, 'login.html', context=context)


def logout_user_view(request):
    logout(request)
    return redirect('/films/')


def search_view(request):
    search = request.GET.get('search_word', '')
    queryset = Film.objects.filter(Q(title__icontains=search) | Q(text__icontains=search))
    lists = Film.objects.all()
    context = {
        'title': 'Результаты..' if queryset else 'Фильм не найден',
        'film_list': lists,
        'films_list': queryset
    }
    return render(request, 'search.html', context=context)
