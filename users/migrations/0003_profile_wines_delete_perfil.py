# Generated by Django 5.1.6 on 2025-02-13 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_perfil_user_remove_perfil_vinos_profile'),
        ('wines', '0003_wine_delete_vino'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='wines',
            field=models.ManyToManyField(blank=True, to='wines.wine'),
        ),
        migrations.DeleteModel(
            name='Perfil',
        ),
    ]
