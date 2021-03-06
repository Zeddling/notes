from notes import models
from django import forms

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, label="Category name", required=True)

    class Meta:
        model = models.Category
        fields = ('name',)


class NotesForm(forms.ModelForm):
    class Meta:
        model = models.Note
        fields = ('title', 'description')
        field_order = ["title", "description"]

