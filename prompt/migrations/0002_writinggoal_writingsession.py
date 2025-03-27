# Generated by Django 5.1.6 on 2025-03-27 08:50

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prompt', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='WritingGoal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goal_type', models.CharField(choices=[('time', 'Minutes per session'), ('words', 'Words per session'), ('sessions', 'Number of sessions')], default='time', max_length=10)),
                ('target_value', models.PositiveIntegerField(help_text='Target value (minutes, words, or sessions)', validators=[django.core.validators.MinValueValidator(1)])),
                ('frequency', models.CharField(choices=[('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly')], default='daily', max_length=10)),
                ('start_date', models.DateField(default=django.utils.timezone.now)),
                ('end_date', models.DateField(blank=True, help_text='Leave blank for ongoing goals', null=True)),
                ('active', models.BooleanField(default=True)),
                ('notes', models.TextField(blank=True, help_text='Why did you set this goal? What are you working towards?')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='writing_goals', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='WritingSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('minutes_spent', models.PositiveIntegerField(help_text='How many minutes did you spend writing?', validators=[django.core.validators.MinValueValidator(1)])),
                ('word_count', models.PositiveIntegerField(default=0, help_text='Approximately how many words did you write? (Optional)')),
                ('mood', models.CharField(choices=[('very_negative', 'Very Difficult'), ('negative', 'Difficult'), ('neutral', 'Neutral'), ('positive', 'Enjoyable'), ('very_positive', 'Very Enjoyable')], default='neutral', help_text='How was your writing session?', max_length=15)),
                ('notes', models.TextField(blank=True, help_text='What did you write about? How did it go?')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('prompt_used', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='writing_sessions', to='prompt.writingprompt')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='writing_sessions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date', '-created_at'],
            },
        ),
    ]
