# Generated by Django 2.1.7 on 2019-03-20 01:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitterCloneApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='description',
            field=models.CharField(blank=True, max_length=124, null=True),
        ),
        migrations.AddField(
            model_name='notification',
            name='title',
            field=models.CharField(default='Filler Text', max_length=124),
        ),
    ]
