# Generated by Django 4.2.1 on 2023-05-05 23:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation_app', '0003_alter_user_employee_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.IntegerField(default=1),
        ),
    ]
