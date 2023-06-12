# Generated by Django 4.2 on 2023-06-11 02:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_book_contributors_book_publisher_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='cover',
            field=models.ImageField(blank=True, null=True, upload_to='book_covers/'),
        ),
        migrations.AddField(
            model_name='book',
            name='samples',
            field=models.FileField(blank=True, null=True, upload_to='book_samples/'),
        ),
    ]
