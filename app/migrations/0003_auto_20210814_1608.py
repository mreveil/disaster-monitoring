# Generated by Django 3.2.6 on 2021-08-14 20:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20210814_1552'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('affiliation', models.CharField(max_length=50)),
                ('profile_link', models.CharField(max_length=50)),
                ('affiliation_link', models.CharField(max_length=50)),
            ],
        ),
        migrations.RemoveField(
            model_name='report',
            name='author_affiliation',
        ),
        migrations.RemoveField(
            model_name='report',
            name='author_link',
        ),
        migrations.RemoveField(
            model_name='report',
            name='author_name',
        ),
        migrations.AddField(
            model_name='report',
            name='title',
            field=models.CharField(default='None', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='report',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.author'),
        ),
    ]
