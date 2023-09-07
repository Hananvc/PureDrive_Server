# Generated by Django 4.2.3 on 2023-07-31 04:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vehicleapp', '0001_initial'),
        ('userapp', '0010_dealer_is_dealer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dealer',
            name='email',
        ),
        migrations.RemoveField(
            model_name='dealer',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='dealer',
            name='is_dealer',
        ),
        migrations.RemoveField(
            model_name='dealer',
            name='is_staff',
        ),
        migrations.RemoveField(
            model_name='dealer',
            name='is_superuser',
        ),
        migrations.RemoveField(
            model_name='dealer',
            name='last_login',
        ),
        migrations.RemoveField(
            model_name='dealer',
            name='password',
        ),
        migrations.RemoveField(
            model_name='dealer',
            name='username',
        ),
        migrations.AddField(
            model_name='dealer',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user',
            name='is_dealer',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='dealer',
            name='address',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='dealer',
            name='brand',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='vehicleapp.brand'),
        ),
        migrations.AlterField(
            model_name='dealer',
            name='country',
            field=models.CharField(choices=[('india', 'India')], default='india', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='dealer',
            name='district',
            field=models.CharField(choices=[('ernakulam', 'Ernakulam'), ('kannur', 'Kannur'), ('kollam', 'Kollam'), ('kozhikode', 'Kozhikode'), ('palakkad', 'Palakkad'), ('thiruvananthapuram', 'Thiruvananthapuram'), ('wayanad', 'Wayanad'), ('alappuzha', 'Alappuzha'), ('idukki', 'Idukki'), ('kasaragod', 'Kasaragod'), ('kottayam', 'Kottayam'), ('malappuram', 'Malappuram'), ('pathanamthitta', 'Pathanamthitta'), ('thrissur', 'Thrissur')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='dealer',
            name='field_experience',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='dealer',
            name='is_verified',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name='dealer',
            name='num_staff',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='dealer',
            name='pin_code',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='dealer',
            name='sales_contact_no',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='dealer',
            name='service_contact_no',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='dealer',
            name='state',
            field=models.CharField(choices=[('kerala', 'Kerala')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='dealer',
            name='website',
            field=models.CharField(max_length=150, null=True),
        ),
    ]