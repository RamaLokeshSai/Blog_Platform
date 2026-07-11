from django.db import migrations
from django.utils.text import slugify

def create_default_categories(apps, schema_editor):
    Category = apps.get_model('blog', 'Category')
    default_categories = [
        {'name': 'Technology', 'description': 'Software, coding, gadgets, and tech innovations.'},
        {'name': 'Design', 'description': 'UI/UX design, graphics, illustration, and art.'},
        {'name': 'Writing', 'description': 'Tips, stories, poetry, and creative writing ideas.'},
        {'name': 'Lifestyle', 'description': 'Health, thoughts, daily routines, and hobbies.'},
    ]
    for cat_data in default_categories:
        # In migrations, the custom Category.save() is not executed,
        # so we must supply the slug manually to avoid unique constraint collisions.
        Category.objects.get_or_create(
            name=cat_data['name'],
            defaults={
                'slug': slugify(cat_data['name']),
                'description': cat_data['description']
            }
        )

def remove_default_categories(apps, schema_editor):
    Category = apps.get_model('blog', 'Category')
    Category.objects.filter(name__in=['Technology', 'Design', 'Writing', 'Lifestyle']).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_default_categories, reverse_code=remove_default_categories),
    ]
