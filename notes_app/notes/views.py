from django.http.response import HttpResponseRedirect
from django.urls.base import reverse
from . import forms, models
from django.shortcuts import redirect, render

# Create your views here.
def add_category(request):
    if request.method == 'POST':
        form = forms.CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            return redirect('category', category_name_slug=category.slug)
    else:
        form = forms.CategoryForm()
    return render(
        request,
        'notes/add_category.html',
        {
            'form': form
        }
    )
        
def index(request):
    context_dict = {}
    context_dict['categories'] = models.Category.objects.order_by("name")
    return render(request, 'notes/index.html', context_dict)

def show_category(request, category_name_slug):
    context_dict = {}
    
    try:
        category = models.Category.objects.get(slug=category_name_slug)
        context_dict['category'] = category
    except:
        context_dict['category'] = None
    
    return render(request, 'notes/category.html', context_dict)
