from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
import uuid

# Create your models here.
class Category(models.Model):
    user = models.ForeignKey(to=User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self) -> str:
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)


class Note(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(to=Category, null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=128, unique=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.id)
