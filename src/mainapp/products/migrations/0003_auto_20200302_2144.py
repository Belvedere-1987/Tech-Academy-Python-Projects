# Generated by Django 2.1.5 on 2020-03-03 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20200229_1516'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='type',
            field=models.CharField(choices=[('appetizers', 'appetizers'), ('treats', 'treats'), ('drinks', 'drinks'), ('entrees', 'entrees')], max_length=60),
        ),
    ]
