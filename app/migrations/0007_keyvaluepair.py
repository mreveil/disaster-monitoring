# Generated by Django 3.2.6 on 2021-08-16 02:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_report_embed_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='KeyValuePair',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=15)),
                ('value', models.CharField(max_length=50)),
            ],
        ),
    ]