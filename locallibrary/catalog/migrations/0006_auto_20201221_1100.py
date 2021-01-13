# Generated by Django 3.1.4 on 2020-12-21 05:30

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_auto_20201221_1047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookinstance',
            name='id',
            field=models.UUIDField(default=uuid.UUID('122c9e90-24df-4bbd-84f2-16503a25799f'), editable=False, help_text='Unique ID of this book', primary_key=True, serialize=False),
        ),
    ]