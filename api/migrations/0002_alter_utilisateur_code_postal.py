# Generated by Django 5.1.6 on 2025-03-26 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='utilisateur',
            name='code_postal',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
