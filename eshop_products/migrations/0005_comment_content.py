# Generated by Django 3.1.5 on 2021-01-17 15:45

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eshop_products', '0004_auto_20210117_1530'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='content',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]