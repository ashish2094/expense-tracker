# Generated by Django 3.0.7 on 2021-03-21 17:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0002_auto_20210321_1537'),
    ]

    operations = [
        migrations.RenameField(
            model_name='expense',
            old_name='categery',
            new_name='category',
        ),
    ]