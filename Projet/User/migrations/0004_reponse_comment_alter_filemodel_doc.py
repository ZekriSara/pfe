# Generated by Django 4.0.3 on 2022-05-16 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0003_filemodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='reponse',
            name='comment',
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='filemodel',
            name='doc',
            field=models.FileField(upload_to='CSVs'),
        ),
    ]
