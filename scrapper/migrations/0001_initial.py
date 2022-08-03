# Generated by Django 4.0.7 on 2022-08-03 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.TextField(default='')),
                ('title', models.TextField(default='')),
                ('subtitle', models.TextField(default='')),
                ('shared_by', models.TextField(default='')),
                ('content_image', models.TextField(default='')),
                ('content_link', models.TextField(default='')),
                ('content_summary', models.TextField(default='')),
                ('last_update', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
