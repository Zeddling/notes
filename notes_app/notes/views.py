from django.http.response import HttpResponseNotFound, HttpResponseRedirect
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

def add_notes(request, category_name_slug):
    context_dict = {}
    context_dict['categories'] = models.Category.objects.all()
    category = models.Category.objects.get(slug=category_name_slug)
    if category != None:
        if request.method == 'POST':
            form = forms.NotesForm(request.POST)
            if form.is_valid():
                note = form.save(commit=False)
                note.category = category
                note.save()
                return redirect(reverse('note', args=[category_name_slug]))
        else:
            form = forms.NotesForm()
        context_dict["form"] = form
        return render(
            request,
            'notes/add_notes.html',
            context_dict
        )
    
    else:
        return HttpResponseNotFound("Page not found")
    

def index(request):
    context_dict = {}
    context_dict['categories'] = models.Category.objects.all()
    return render(request, 'notes/index.html', context_dict)

def show_category(request, category_name_slug):
    category = models.Category.objects.get(slug=category_name_slug)
    context_dict = {}
    context_dict['category'] = category
    context_dict['categories'] = models.Category.objects.all()
    context_dict['notes'] = models.Note.objects.filter(category=category)
    return render(request, 'notes/category.html', context_dict)

def show_note(request, category_name_slug, id):
    cat = models.Category.objects.get(slug=category_name_slug)
    context_dict = {}
    context_dict['category'] = cat
    context_dict['categories'] = models.Category.objects.all()
    context_dict['note'] = models.Note.objects.get(id=id)
    return render(request, 'notes/note.html', context_dict)
