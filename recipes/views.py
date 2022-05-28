from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_list_or_404, get_object_or_404, render

from .models import Recipe


def home(request):

    recipes = Recipe.objects.filter(is_published=True).order_by('-id')
    paginator = Paginator(recipes, 9)  # Mostra 25 contatos por página
    page = request.GET.get('page')
    recipes = paginator.get_page(page)
    return render(request, 'recipes/home.html', {'recipes': recipes})


def category(request, category_id):

    recipes = get_list_or_404(
        Recipe.objects.filter(category__id=category_id, is_published=True).order_by('-id'))

    paginator = Paginator(recipes, 9)  # Mostra 25 contatos por página
    page = request.GET.get('page')
    recipes = paginator.get_page(page)

    return render(request, 'recipes/category.html', context={
        'recipes': recipes,
        'title': f'{recipes[0].category.name}',
    })


def recipe(request, id):
    recipe = get_object_or_404(Recipe, pk=id, is_published=True)

    return render(request, 'recipes/recipe-view.html', context={
        'recipe': recipe,
        'is_detail_page': True})


def search(request):
    search_term = request.GET.get('q', '').strip()
    if not search_term:
        raise Http404()

    recipes = Recipe.objects.filter(
        Q(
            Q(title__icontains=search_term) |
            Q(description__icontains=search_term)
        ),
        is_published=True).order_by('-id')

    paginator = Paginator(recipes, 9)  # Mostra 25 contatos por página
    page = request.GET.get('page')
    recipes = paginator.get_page(page)

    return render(request, 'recipes/search.html', context={
        'recipes': recipes,
        'title': f'Search: {search_term}',
        'search_term': search_term,
    })
