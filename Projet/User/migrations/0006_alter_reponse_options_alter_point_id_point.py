# Generated by Django 4.0.3 on 2022-05-18 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0005_alter_chapitre_options_alter_norme_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reponse',
            options={'verbose_name': 'Reponse'},
        ),
        migrations.AlterField(
            model_name='point',
            name='id_point',
            field=models.TextField(primary_key=True, serialize=False),
        ),
    ]