from django.shortcuts import render, get_object_or_404, redirect
from django.forms import modelformset_factory
from django.http import HttpResponse
from django.contrib import messages

from main.models import Category, Recipe, Image
from main.forms import RecipeForm, ImageForm


def index(request):
    return render(request, 'index.html')


def category_detail(request, slug):
    category = Category.objects.get(slug=slug)
    recipes = Recipe.objects.filter(category_id=slug)
    return render(request, 'category_detail.html', locals())


def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    image = recipe.images.first()
    images = recipe.images.exclude(id=recipe.id)
    return render(request, 'recipe-detail.html', locals())


def add_recipe(request):
    ImageFormSet = modelformset_factory(Image, form=ImageForm, max_num=5)
    if request.method == 'POST':
        recipe_form = RecipeForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES, queryset=Image.objects.none())
        if recipe_form.is_valid() and formset.is_valid():
            recipe = recipe_form.save()

            for form in formset.cleaned_data:
                image = form.get('image')
                Image.objects.create(image=image, recipe=recipe)
            return redirect(recipe.get_absolute_url())
    else:
        recipe_form = RecipeForm()
        formset = ImageFormSet(queryset=Image.objects.none())
    return render(request, 'add-recipe.html', locals())


def update_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.user == recipe.user:
        ImageFormSet = modelformset_factory(Image, form=ImageForm, max_num=5)
        recipe_form = RecipeForm(request.POST or None, instance=recipe)
        formset = ImageFormSet(request.POST or None, request.FILES or None, queryset=Image.objects.filter(recipe=recipe))
        if recipe_form.is_valid() and formset.is_valid():
            recipe = recipe_form.save()

            images = formset.save(commit=False)
            for image in images:
                image.recipe = recipe
                image.save()
            return redirect(recipe.get_absolute_url())
        return render(request, 'update-recipe.html', locals())
    else:
        return HttpResponse('<h1>Forbidden</h1>')


def delete_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.method == 'POST':
        recipe.delete()
        messages.add_message(request, messages.SUCCESS, 'Successfully deleted!')
        return redirect('index')
    return render(request, 'delete-recipe.html', locals())