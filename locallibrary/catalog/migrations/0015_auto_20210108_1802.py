# Generated by Django 3.1.4 on 2021-01-08 12:32

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0014_auto_20210105_1826'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookinstance',
            name='id',
            field=models.UUIDField(default=uuid.UUID('3658b1e2-2d6e-4384-a2a6-6350497c599e'), help_text='Unique ID of this book', primary_key=True, serialize=False),
        ),
    ]
