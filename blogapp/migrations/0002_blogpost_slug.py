# Generated by Django 3.0.6 on 2020-06-04 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='slug',
            field=models.CharField(default=1, max_length=150),
            preserve_default=False,
        ),
    ]
