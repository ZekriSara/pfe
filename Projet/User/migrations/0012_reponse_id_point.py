# Generated by Django 4.0.3 on 2022-05-18 10:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0011_remove_reponse_id_point'),
    ]

    operations = [
        migrations.AddField(
            model_name='reponse',
            name='id_point',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='User.point', verbose_name='Points'),
        ),
    ]
