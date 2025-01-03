# Generated by Django 5.1.3 on 2024-12-31 20:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventorymgmt', '0008_remove_stock_export_to_csv_alter_stock_catagory'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='export_to_csv',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='stock',
            name='catagory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventorymgmt.catagory'),
        ),
    ]
