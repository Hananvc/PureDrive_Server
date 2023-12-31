# Generated by Django 4.2.3 on 2023-09-07 14:12

from django.db import migrations, models
import django.db.models.deletion
import vehicleapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicleapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1000)),
                ('description', models.TextField(null=True)),
                ('url', models.URLField(max_length=1000, null=True)),
                ('url_to_image', models.URLField(max_length=1000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='testride',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_reference', models.CharField(max_length=50)),
                ('brand', models.CharField(max_length=50)),
                ('model_name', models.CharField(max_length=50)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('dealer', models.CharField(max_length=50)),
                ('dealer_email', models.EmailField(max_length=254)),
                ('customer_name', models.CharField(max_length=50)),
                ('customer_email', models.CharField(max_length=50)),
                ('customer_phone', models.BigIntegerField()),
                ('booking_status', models.CharField(default='Pending', max_length=50, null=True)),
                ('review', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='vehicle',
            name='brochure',
            field=models.FileField(blank=True, null=True, upload_to='brochures/', validators=[vehicleapp.models.validate_brochure]),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='default_image',
            field=models.ImageField(blank=True, null=True, upload_to='default_images/', validators=[vehicleapp.models.validate_default_image]),
        ),
        migrations.AlterField(
            model_name='variant',
            name='color',
            field=models.CharField(choices=[('White', 'White'), ('Black', 'Black'), ('Green', 'Green'), ('Red', 'Red'), ('Yellow', 'Yellow'), ('Blue', 'Blue'), ('Brown', 'Brown'), ('Orange', 'Orange')], max_length=50),
        ),
        migrations.CreateModel(
            name='image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('images', models.ImageField(null=True, upload_to='vehicle_images')),
                ('Variant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='images', to='vehicleapp.variant')),
                ('Vehicle', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='vehicleapp.vehicle')),
            ],
        ),
    ]
