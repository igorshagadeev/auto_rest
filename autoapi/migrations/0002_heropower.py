# Generated by Django 3.0.5 on 2020-04-27 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autoapi', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HeroPower',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hero', models.CharField(max_length=60)),
                ('power', models.CharField(max_length=60)),
                ('description', models.CharField(max_length=60)),
            ],
        ),
    ]
