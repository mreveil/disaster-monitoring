# Generated by Django 3.2.6 on 2021-08-15 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpage',
            name='intro',
            field=models.CharField(default='', max_length=250),
            preserve_default=False,
        ),
    ]
