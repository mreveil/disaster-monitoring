# Generated by Django 3.2.6 on 2021-08-14 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('publication_time', models.DateTimeField()),
                ('author', models.CharField(max_length=10)),
                ('publication_link', models.FloatField()),
                ('event_time', models.FloatField()),
                ('longitude', models.FloatField()),
                ('latitude', models.FloatField()),
                ('bad_feedback', models.IntegerField()),
            ],
            options={
                'unique_together': {('publication_link',)},
            },
        ),
    ]
