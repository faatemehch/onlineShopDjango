# Generated by Django 3.1.5 on 2021-03-02 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eshop_products', '0009_product_sub_categories'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='visit_count',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='تعداد یازدید'),
        ),
    ]