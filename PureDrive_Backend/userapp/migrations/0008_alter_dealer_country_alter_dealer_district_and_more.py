# Generated by Django 4.2.3 on 2023-07-30 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0007_alter_dealer_brand'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dealer',
            name='country',
            field=models.CharField(choices=[('india', 'India')], default='india', max_length=20),
        ),
        migrations.AlterField(
            model_name='dealer',
            name='district',
            field=models.CharField(choices=[('ernakulam', 'Ernakulam'), ('kannur', 'Kannur'), ('kollam', 'Kollam'), ('kozhikode', 'Kozhikode'), ('palakkad', 'Palakkad'), ('thiruvananthapuram', 'Thiruvananthapuram'), ('wayanad', 'Wayanad'), ('alappuzha', 'Alappuzha'), ('idukki', 'Idukki'), ('kasaragod', 'Kasaragod'), ('kottayam', 'Kottayam'), ('malappuram', 'Malappuram'), ('pathanamthitta', 'Pathanamthitta'), ('thrissur', 'Thrissur')], max_length=20),
        ),
        migrations.AlterField(
            model_name='dealer',
            name='state',
            field=models.CharField(choices=[('kerala', 'Kerala'), ('state2', 'State 2')], max_length=20),
        ),
    ]