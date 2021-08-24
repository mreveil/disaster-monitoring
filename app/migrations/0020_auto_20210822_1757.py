# Generated by Django 3.2.6 on 2021-08-22 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_auto_20210822_1737'),
    ]

    operations = [
        migrations.AlterField(
            model_name='relief',
            name='item_subtype',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='relief',
            name='item_type',
            field=models.CharField(choices=[('Money', 'Money'), ('Food', 'Food'), ('Necessities', 'Necessities'), ('Personnel', 'Skilled Personnel'), ('Water', 'Water'), ('Construction Materials', 'Construction Materials'), ('Temporary Shelter', 'Temporary Shelter'), ('Medical care', 'Medical Care'), ('Mental Care', 'Mental Care'), ('Other', 'Other')], max_length=50),
        ),
        migrations.AlterField(
            model_name='relief',
            name='status',
            field=models.CharField(choices=[('Promised', 'Promised'), ('Delivered', 'Delivered')], max_length=50),
        ),
    ]