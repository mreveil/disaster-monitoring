# Generated by Django 3.2.6 on 2021-08-19 19:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_auto_20210818_2354'),
    ]

    operations = [
        migrations.AddField(
            model_name='keyvaluepair',
            name='change',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='mediacoverage',
            name='description',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AddField(
            model_name='mediacoverage',
            name='image',
            field=models.ImageField(default=None, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='mediacoverage',
            name='title',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.CreateModel(
            name='KeyEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pub_time', models.DateTimeField()),
                ('pub_link', models.CharField(max_length=250)),
                ('title', models.CharField(max_length=100, null=True)),
                ('embed_code', models.CharField(max_length=1000)),
                ('description', models.CharField(blank=True, max_length=250, null=True)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.author')),
            ],
        ),
    ]
