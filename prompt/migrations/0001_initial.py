# Generated by Django 5.1.6 on 2025-03-05 21:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PromptCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True)),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'verbose_name_plural': 'Prompt categories',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='WritingPrompt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('difficulty', models.CharField(choices=[('easy', 'Easy (5-10 minutes)'), ('medium', 'Medium (15-20 minutes)'), ('deep', 'Deep (30+ minutes)')], default='medium', max_length=15)),
                ('prompt_type', models.CharField(choices=[('journal', 'Journal Entry'), ('memoir', 'Memoir/Memory'), ('both', 'Both')], default='both', max_length=15)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prompts', to='prompt.promptcategory')),
                ('tags', models.ManyToManyField(blank=True, related_name='prompts', to='prompt.tag')),
            ],
        ),
    ]
