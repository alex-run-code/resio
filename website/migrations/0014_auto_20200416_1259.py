# Generated by Django 3.0.3 on 2020-04-16 09:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0013_auto_20200416_1258'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.City'),
        ),
    ]
