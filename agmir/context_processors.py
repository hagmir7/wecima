from django.contrib.auth.models import User
from scraping.models import Contact, Link, Settings
from django.conf import settings as setting


def context_data(request):
    messages = Contact.objects.filter(readed=None)
    links = Link.objects.all()
    footer = Link.objects.filter(footer=True) 
    header = Link.objects.filter(header=True)
    settings = Settings.objects.last() 

    return {
        'contacts': messages,
        'footer' : footer,
        'header' : header,
        'settings' : settings,
        'links' : links,
        'cpanel' : setting.CPANEL
        }
    