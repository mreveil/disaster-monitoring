# Generated by Django 3.2.6 on 2021-08-28 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0026_usersubmission_publication_datetime'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usersubmission',
            name='publication_datetime',
        ),
        migrations.AddField(
            model_name='fundraiser',
            name='author',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='fundraiser',
            name='publication_date',
            field=models.DateField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='embed_code',
            field=models.CharField(max_length=1500),
        ),
    ]
