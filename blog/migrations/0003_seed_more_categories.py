from django.db import migrations
from django.utils.text import slugify

def seed_more_categories(apps, schema_editor):
    Category = apps.get_model('blog', 'Category')
    extra_categories = [
        {'name': 'Food', 'description': 'Recipes, reviews, culinary arts, and dining guides.'},
        {'name': 'Travel', 'description': 'Adventures, destinations, itineraries, and travel stories.'},
    ]
    for cat_data in extra_categories:
        Category.objects.get_or_create(
            name=cat_data['name'],
            defaults={
                'slug': slugify(cat_data['name']),
                'description': cat_data['description']
            }
        )

def remove_more_categories(apps, schema_editor):
    Category = apps.get_model('blog', 'Category')
    Category.objects.filter(name__in=['Food', 'Travel']).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_seed_categories'),
    ]

    operations = [
        migrations.RunPython(seed_more_categories, reverse_code=remove_more_categories),
    ]
