# Generated by Django 4.1.5 on 2023-10-06 02:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_alter_userprofile_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_image',
            field=models.ImageField(default='images/default.jpg', upload_to='images/'),
        ),
    ]