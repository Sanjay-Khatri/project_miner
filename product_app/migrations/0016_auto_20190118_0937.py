# Generated by Django 2.0.6 on 2019-01-18 04:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product_app', '0015_auto_20190118_0935'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='post_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='product_app.Post'),
        ),
    ]