# Generated by Django 3.0.3 on 2020-03-13 19:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0005_auto_20200227_1741'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hospital',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('website', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('about', models.CharField(max_length=2550)),
            ],
        ),
        migrations.CreateModel(
            name='Paperwork',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Specialty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.AlterField(
            model_name='candidate',
            name='location',
            field=models.CharField(choices=[('Alba Iulia', 'Alba Iulia'), ('Cluj-Napoca', 'Cluj-Napoca'), ('Bucharest', 'Bucharest'), ('Mara Mures', 'Mara Mures'), ('Timisoara', 'Timisoara')], max_length=255),
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chief_name', models.CharField(max_length=255)),
                ('chief_surname', models.CharField(max_length=255)),
                ('residanatms_url', models.CharField(max_length=255)),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.Hospital')),
                ('specialty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.Specialty')),
            ],
        ),
        migrations.CreateModel(
            name='Paperwork_Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paperwork', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.Paperwork')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.Service')),
            ],
        ),
    ]
