from django.template.defaultfilters import title
from notes import forms, models
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django_webtest import WebTest

# Create your tests here.
class CategoryModelTests(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="test", password="12345678")
        self.user.save()
        self.client.login(username="test", password="12345678")
    
    def tearDown(self) -> None:
        self.client.login()
        self.user.delete()

    def test__str__(self):
        category = models.Category(name="Test Case", user=self.user)
        self.assertEqual(str(category), category.name)

    def test_on_save_slug_set(self):
        category = models.Category.objects.create(name="Test Case", user=self.user)
        self.assertEqual(category.slug, "test-case")

    def test_verbose_name_plural(self):
        self.assertEqual(
            str(models.Category._meta.verbose_name_plural),
            "Categories"
        )


class CategoryFormTests(WebTest):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="test", password="12345678")
        self.user.save()
        self.client.login(username="test", password="12345678")
    
    def tearDown(self) -> None:
        self.client.logout()
        self.user.delete()

    def test_redirect_on_valid(self):
        form = self.app.get(reverse('add_category'), user='test').form
        form['name'] = 'Test Case'
        response = form.submit().follow()
        self.assertEqual(response.status_code, 200)


class CategoryPageTests(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="test", password="12345678")
        self.user.save()
        self.client.login(username="test", password="12345678")

        self.category = models.Category.objects.create(name="Test Case", user=self.user)
    
    def tearDown(self) -> None:
        self.client.login()
        self.category.delete()
        self.user.delete()
    
    def test_category_template_used(self):
        res = self.client.get(reverse('category', args=["test-case"]))
        self.assertTemplateUsed(res, "notes/category.html")
    
    def test_category_rendered(self):
        res = self.client.get(reverse('category', args=["test-case"]))
        self.assertIn(b'Test Case', res.content)


class NotesModeTests(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="test", password="12345678")
        self.user.save()
        self.category = models.Category.objects.create(name="Test Category")
        self.category.save()
    
    def tearDown(self) -> None:
        self.client.login()
        self.user.delete()
        self.category.delete()
    
    def test_str(self):
        note = models.Note(title="Test Note", category=self.category)
        self.assertTrue(str(note), str(note.id))


class NotesFormTests(WebTest):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="test", password="12345678")
        self.user.save()
        self.client.login(username="test", password="12345678")
        self.category = models.Category.objects.create(name="Test Category")
        self.category.save()
    
    def tearDown(self) -> None:
        self.client.login()
        self.user.delete()
    
    


class NotesPageTests(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="test", password="12345678")
        self.user.save()
        self.client.login(username="test", password="12345678")
        self.category = models.Category.objects.create(name="Test Category")
        self.category.save()
        self.note = models.Note.objects.create(
            title="Test Note",
            description="Hello world"
        )
        self.note.save()
    
    def tearDown(self) -> None:
        self.client.login()
        self.user.delete()

    def test_add_notes_form_template_used(self):
        res = self.client.get(reverse('add_note', args=[self.category.slug]))
        self.assertTemplateUsed(res, "notes/add_notes.html")
    
    def test_notes_page_template_used(self):
        res = self.client.get(reverse('note', args=[self.category.slug, self.note.id]))
        self.assertTemplateUsed(res, "notes/note.html")
    
    def test_note_displayed(self):
       res = self.client.get(reverse('note', args=[self.category.slug, self.note.id]))
       self.assertIn(b'Test Note', res.content)

class IndexPageTests(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="test", password="12345678")
        self.user.save()
        self.client.login(username="test", password="12345678")

        self.category = models.Category.objects.create(name="Test Case", user=self.user)
    
    def tearDown(self) -> None:
        self.client.login()
        self.category.delete()
        self.user.delete()

    def test_index_template_used(self):
        res = self.client.get(reverse('index'))
        self.assertTemplateUsed(res, "notes/index.html")
    
    def test_categories_displayed(self):
        res = self.client.get(reverse('index'))
        self.assertIn(b'Test Case', res.content)
