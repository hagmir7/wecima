# myapp/management/commands/create_example.py
from django.core.management.base import BaseCommand
from scraping.models import Settings

class Command(BaseCommand):
    help = 'Create a configuration record in the database'

    def handle(self, *args, **options):
        # Your logic to create an example record
        Settings.objects.create(
            name='FreeWsad Blog',
            title = "The Best website for eduction",
            description =  "Download Free pdf books Without Guigou",
            tags = "Free books, pdf books, new books, Download free books",
            cover_title =  "The Best website for eduction",
            cover_description= "Download Free pdf books Without Guigou"

        )
        self.stdout.write(self.style.SUCCESS('Configuration created successfully'))


