# Generated by Django 4.2.3 on 2023-07-30 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0009_alter_dealer_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='dealer',
            name='is_dealer',
            field=models.BooleanField(default=False),
        ),
    ]
