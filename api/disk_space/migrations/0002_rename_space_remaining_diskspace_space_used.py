# Generated by Django 3.2.3 on 2021-09-05 00:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('disk_space', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='diskspace',
            old_name='space_remaining',
            new_name='space_used',
        ),
    ]
