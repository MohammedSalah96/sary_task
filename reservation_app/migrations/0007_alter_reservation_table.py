# Generated by Django 4.2.1 on 2023-05-06 16:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reservation_app', '0006_reservation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='table',
            field=models.ForeignKey(db_column='table_id', on_delete=django.db.models.deletion.PROTECT, related_name='table', to='reservation_app.table'),
        ),
    ]