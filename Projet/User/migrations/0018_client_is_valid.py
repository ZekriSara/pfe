# Generated by Django 4.0.3 on 2022-05-27 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0017_loi_client_date_fin_client_num_fisc_admin'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='is_valid',
            field=models.BooleanField(default=False),
        ),
    ]