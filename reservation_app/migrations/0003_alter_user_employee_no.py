# Generated by Django 4.2.1 on 2023-05-05 23:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation_app', '0002_alter_user_employee_no_alter_user_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='employee_no',
            field=models.CharField(max_length=4, unique=True),
        ),
    ]
