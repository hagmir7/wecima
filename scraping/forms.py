from django.contrib.auth.forms import forms
from . models import *
from django_summernote.widgets import SummernoteWidget




class FormCreatePage(forms.ModelForm):
    body = forms.CharField(widget=SummernoteWidget(attrs={'data-user-id': 123456, 'data-device': 'iphone'}))
    class Meta:
        model = Page
        fields = ('title', 'body')



class CreateContact(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('__all__')