from django.contrib.auth.forms import forms
from .models import *
from django_summernote.widgets import SummernoteWidget


class FormCreatePage(forms.ModelForm):
    body = forms.CharField(
        widget=SummernoteWidget(attrs={"data-user-id": 123456, "data-device": "iphone"})
    )

    class Meta:
        model = Page
        fields = ("title", "body")


class CreateContact(forms.ModelForm):
    class Meta:
        model = Contact
        fields = "__all__"


class PostForm(forms.ModelForm):
    body = forms.CharField(
        widget=SummernoteWidget(attrs={"data-user-id": 123456, "data-device": "iphone"})
    )

    class Meta:
        model = Post
        fields = ("title", "category", "description", "image", "tags", "body")
        widgets = {
            "category": forms.SelectMultiple(attrs={"class": "form-control mb-2"}),
        }


class LinkForm(forms.ModelForm):
    class Meta:
        model = Link
        fields = ("name", "url", "footer", "header", "new_tab")
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "url": forms.TextInput(attrs={"class": "form-control"}),
            "footer": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "header": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "new_tab": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    name = models.CharField(max_length=100)
    title = models.CharField(max_length=150)
    description = models.TextField()
    tags = models.CharField(max_length=200)
    logo = models.ImageField(upload_to="Logos", null=True, blank=True)


class SiteInfoForm(forms.ModelForm):
    class Meta:
        model = Settings
        fields = (
            "name",
            "title",
            "description",
            "tags",
            "logo",
            "theme_color",
            "favicon",
        )
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control mb-2"}),
            "title": forms.TextInput(attrs={"class": "form-control mb-2"}),
            "description": forms.Textarea(
                attrs={"class": "form-control mb-2", "rows": 2}
            ),
            "tags": forms.TextInput(attrs={"class": "form-control mb-3"}),
            "theme_color": forms.TextInput(attrs={"class": "form-control mb-2"}),
            "logo": forms.ClearableFileInput(attrs={"class": "form-control mb-3"}),
            "favicon": forms.ClearableFileInput(attrs={"class": "form-control mb-3"}),
        }

    cover = models.ImageField(upload_to="Covers", null=True, blank=True)
    cover_title = models.CharField(max_length=100)
    cover_description = models.TextField(max_length=150)


class CoverForm(forms.ModelForm):
    class Meta:
        model = Settings
        fields = ("cover", "cover_title", "cover_description")
        widgets = {
            "cover": forms.ClearableFileInput(attrs={"class": "form-control mb-2"}),
            "cover_title": forms.TextInput(attrs={"class": "form-control mb-2"}),
            "cover_description": forms.Textarea(
                attrs={"class": "form-control mb-2", "rows": 2}
            ),
        }


class AdvancedForm(forms.ModelForm):
    class Meta:
        model = Settings
        fields = ("head", "script", "ads")
        widgets = {
            "head": forms.Textarea(attrs={"class": "form-control mb-2", "rows": 4}),
            "script": forms.Textarea(attrs={"class": "form-control mb-4", "rows": 4}),
            "ads": forms.TextInput(attrs={"class": "form-control my-2"}),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "image"]
