# Generated by Django 2.0.6 on 2019-01-17 17:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product_app', '0009_auto_20190117_2119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='product_app.Post'),
        ),
    ]